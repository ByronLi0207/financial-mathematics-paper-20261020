"""Read frozen E3 vectors for E4; no cost/headroom mean is calculated here."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path

import numpy as np


ALLOW_RECOVERY = {'QR4::QR4', 'Levy::Levy_L'}
IDENTITY = ('period', 'normalized_source', 'horizon', 'window')


class CostInputError(ValueError):
    """A full comparison lacks an unchanged, identified common floor."""


def _path(root, value):
    root=Path(root).resolve(); path=Path(value)
    if not path.is_absolute():path=root/path
    if path.is_symlink():raise CostInputError('SYMLINK_INPUT')
    path=path.resolve()
    if not path.is_relative_to(root) or not path.is_file():raise CostInputError('INPUT_OUTSIDE_NEW_ROOT_OR_MISSING')
    return path


def _read_npz(root, location, size, digest):
    path=_path(root,location);raw=path.read_bytes()
    if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=digest:raise CostInputError('INPUT_BYTES_OR_SHA_CHANGED')
    try:
        with np.load(io.BytesIO(raw),allow_pickle=False) as z:arrays={k:np.array(z[k],copy=True) for k in z.files}
    except (ValueError,TypeError,OSError,EOFError) as exc:
        raise CostInputError('INVALID_NUMERIC_NPZ') from exc
    if path.read_bytes()!=raw:raise CostInputError('INPUT_CHANGED_DURING_READ')
    return path,arrays


def _array_pin(array):
    return dict(shape=list(array.shape),dtype=array.dtype.str,sha256=hashlib.sha256(array.tobytes()).hexdigest())


def _vector(array,n,label,nonnegative=False):
    if (array.shape!=(n,) or array.dtype.kind not in 'iuf' or not np.isfinite(array).all()
            or nonnegative and np.any(array<0)):
        raise CostInputError('INVALID_FULL_VECTOR:'+label)
    return np.asarray(array,dtype=float)


def _row_identity(row,inventory):
    aliases=inventory.get('source_aliases',{})
    source=row.get('normalized_source') or aliases.get(row.get('source'),row.get('source'))
    return (row.get('period'),source,row.get('horizon'),row.get('window'))


def _recover(method,group,inventory,root,origins,target,floor):
    method_id=method['method_id']
    if method_id not in ALLOW_RECOVERY:raise CostInputError('UNDECLARED_MISSING_FLOOR:'+method_id)
    identity=tuple(group['identity'][k] for k in IDENTITY)
    rows=[row for row in inventory.get('methods',[]) if _row_identity(row,inventory)==identity
          and row.get('family','')+'::'+row.get('method','')==method_id
          and row.get('scope_classification','requested_core_saved_method')=='requested_core_saved_method']
    if len(rows)!=1:raise CostInputError('RECOVERY_SOURCE_IDENTITY_NOT_UNIQUE')
    row=rows[0]; recovery=row.get('floor_recovery')
    if row.get('floor_key') is not None or not isinstance(recovery,dict) or recovery.get('origin_axis_sha256_match') is not True:
        raise CostInputError('FLOOR_RECOVERY_NOT_REGISTERED')
    provenance=method.get('provenance',{})
    if (provenance.get('original_trace_path') not in (None,row['trace_path'])
            or not any(r.get('trace_path')==row['trace_path'] for r in provenance.get('source_rows',[]))):
        raise CostInputError('CANDIDATE_SOURCE_PROVENANCE_MISMATCH')
    source=recovery.get('trace_path'); key=recovery.get('key')
    if not isinstance(key,str) or not key.endswith('floor'):raise CostInputError('INVALID_RECOVERY_FLOOR_KEY')
    pins=[p for p in inventory.get('minimum_core_private_copy_manifest',[]) if p.get('path')==source]
    if len(pins)!=1:raise CostInputError('RECOVERY_COPY_PIN_NOT_UNIQUE')
    pin=pins[0]
    path,arrays=_read_npz(root,pin['proposed_scratch_relative'],pin['bytes'],pin['sha256'])
    prefix=key[:-len('floor')];origin_key=prefix+'origins';target_key=prefix+'peak'
    if not {origin_key,target_key,key}<=set(arrays):raise CostInputError('RECOVERY_PREFIX_KEYS_MISSING')
    old_origins=arrays[origin_key]
    if old_origins.dtype.kind not in 'iu' or not np.array_equal(old_origins,origins):raise CostInputError('RECOVERY_ENTIRE_ORIGIN_AXIS_MISMATCH')
    old_target=_vector(arrays[target_key],len(origins),'recovery target')
    old_floor=_vector(arrays[key],len(origins),'recovery floor',True)
    if not np.array_equal(old_target,target):raise CostInputError('RECOVERY_ENTIRE_TARGET_MISMATCH')
    if not np.array_equal(old_floor,floor):raise CostInputError('RECOVERY_FLOOR_DIFFERS_FROM_CANONICAL_F')
    return dict(method_id=method_id,reference_id='F',identity=dict(group['identity']),
        candidate_original_trace=row['trace_path'],reference_original_trace=source,
        reference_copy_path=str(path.relative_to(Path(root).resolve())),bytes=int(pin['bytes']),sha256=str(pin['sha256']),
        origin_key=origin_key,target_key=target_key,source_floor_key=key,
        canonical_floor_key=next(m['floor_key'] for m in group['methods'] if m['method_id']=='F'),
        canonical_floor_sha256=group['arrays'][next(m['floor_key'] for m in group['methods'] if m['method_id']=='F')]['sha256'],
        entire_origins='EXACT_MATCH',entire_target='EXACT_MATCH',entire_floor='EXACT_MATCH')


def _load_cost_group(group,inventory,root):
    if group.get('status')!='READY':raise CostInputError('GROUP_NOT_READY')
    _,arrays=_read_npz(root,group['private_path'],group['bytes'],group['sha256'])
    if set(arrays)!=set(group['arrays']):raise CostInputError('E3_ARRAY_INVENTORY_CHANGED')
    for key,array in arrays.items():
        if (array.dtype.kind not in 'iuf' or not np.isfinite(array).all()
                or _array_pin(array)!=group['arrays'][key]):raise CostInputError('E3_ARRAY_PIN_CHANGED:'+key)
    n=group['n'];methods=group['methods'];k=len(methods)
    if not isinstance(n,int) or isinstance(n,bool) or n<=0 or not k:raise CostInputError('INVALID_GROUP_DIMENSIONS')
    required={'origins','peak','capacities_matrix','loss_matrix'}
    if not required<=set(arrays):raise CostInputError('REQUIRED_E3_ARRAY_MISSING')
    origins=arrays['origins']
    if (origins.dtype.kind not in 'iu' or origins.shape!=(n,)
            or not np.array_equal(origins,np.arange(group['first_origin'],group['last_origin']+1))):
        raise CostInputError('E3_FULL_ORIGIN_GRID_MISMATCH')
    target=_vector(arrays['peak'],n,'target',True)
    if (arrays['capacities_matrix'].shape!=(n,k) or arrays['loss_matrix'].shape!=(n,k)
            or np.any(arrays['loss_matrix']<0)):raise CostInputError('E3_METHOD_MATRIX_SHAPE_OR_LOSS')
    ids=[m['method_id'] for m in methods]
    if len(set(ids))!=k or ids.count('F')!=1:raise CostInputError('UNIQUE_CANONICAL_F_REQUIRED')
    reference=next(m for m in methods if m['method_id']=='F')
    if reference.get('method_class')!='matched_historical' or reference.get('floor_key') is None:
        raise CostInputError('CANONICAL_F_PROVIDED_FLOOR_REQUIRED')
    floor_key=reference['floor_key']
    if floor_key not in arrays:raise CostInputError('CANONICAL_F_FLOOR_ARRAY_ABSENT')
    floor=_vector(arrays[floor_key],n,'canonical floor',True)
    if np.any(target<floor):raise CostInputError('TARGET_BELOW_CURRENT_FLOOR')
    capacities={};recoveries=[]
    for j,method in enumerate(methods):
        if method.get('column_index')!=j:raise CostInputError('METHOD_COLUMN_BINDING_MISMATCH')
        capacity=_vector(arrays['capacities_matrix'][:,j],n,'capacity',True)
        key=method.get('floor_key')
        if key is not None:
            if key not in arrays or not np.array_equal(_vector(arrays[key],n,'provided floor',True),floor):
                raise CostInputError('PROVIDED_FLOOR_DIFFERS_FROM_CANONICAL_F')
        else:recoveries.append(_recover(method,group,inventory,root,origins,target,floor))
        if np.any(capacity<floor):raise CostInputError('CAPACITY_BELOW_CURRENT_FLOOR')
        value=np.array(capacity,copy=True);value.setflags(write=False);capacities[method['method_id']]=value
    result=dict(origins=np.array(origins,copy=True),target=np.array(target,copy=True),
                floor=np.array(floor,copy=True),capacities=capacities,recovery_receipts=recoveries)
    for key in ('origins','target','floor'):result[key].setflags(write=False)
    return result


def load_cost_group(group,inventory,root):
    """Return a complete read-only group or raise one whole-group input error.

    Only NEW-root private files are opened. Old paths identify E0 provenance,
    never I/O targets. No mean, reserve, breach, excess or cost is computed.
    """
    try:
        return _load_cost_group(group,inventory,root)
    except CostInputError:
        raise
    except (KeyError,TypeError,ValueError,OSError,OverflowError) as exc:
        raise CostInputError('INVALID_COST_INPUT_METADATA:'+str(exc)) from exc
