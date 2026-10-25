"""Frozen E3 arch8 MCS wrapper over caller-owned complete loss vectors only.

No source I/O, loss recovery, forecasting, alias decisions or result selection
occurs here. Exact loss classes stabilize the library call while all distinct
procedure labels remain present in the unfolded set and p-values.
"""
from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
import math
from numbers import Integral
import warnings

import arch
from arch.bootstrap import MCS
import numpy as np

from run_study import StudyStop
from run_v8_wp3 import DriverStop


RESOURCE_ERRORS = (StudyStop, DriverStop)


def _integer(value):
    return isinstance(value, Integral) and not isinstance(value, (bool, np.bool_))


def _indices(values, count):
    ids = list(values)
    if (any(not _integer(v) or not 0 <= int(v) < count for v in ids)
            or len(set(map(int, ids))) != len(ids)):
        raise ValueError('INVALID_LIBRARY_MEMBERSHIP_INDEX')
    return {int(v) for v in ids}


def compute_mcs(losses, identity, design, checkpoint=None):
    """Compute once, or return a visible analytic/input/numerical failure row."""
    row = dict(status='FAILED_INPUT', n=None, seed=None, block_size=None,
        method_ids=[], method_count=0, unique_loss_groups=[], unique_loss_class_count=0,
        included=[], excluded=[], pvalues={}, reason=None,
        diagnostics=dict(arch_version=str(arch.__version__), library_attempts=0))
    try:
        period, source = identity['period'], identity['normalized_source']
        h, w = identity['horizon'], identity['window']
        if (not isinstance(period, str) or not period or not isinstance(source, str) or not source
                or not _integer(h) or h < 1 or not _integer(w) or w < 1):
            raise ValueError('INVALID_COMPARISON_IDENTITY')
        serialized = json.dumps([period, source, int(h), int(w)], separators=(',', ':'), ensure_ascii=True)
        prefix = design['seed_prefix']
        reps = design['bootstrap_repetitions']
        if (design['package'] != 'arch==8.0.0' or arch.__version__ != '8.0.0'
                or design['size'] != .1 or design['statistic'] != 'R'
                or design['bootstrap'] != 'stationary' or prefix != 'v10-MCS-20261024|'
                or not _integer(reps) or reps < 1):
            raise ValueError('FROZEN_MCS_CONFIGURATION_MISMATCH')
        row['seed'] = int.from_bytes(hashlib.sha256((prefix+serialized).encode('utf-8')).digest()[:4], 'big')
        row['diagnostics'].update(size=.1, statistic='R', bootstrap='stationary', bootstrap_repetitions=int(reps))
        if not isinstance(losses, Mapping) or any(not isinstance(k, str) or not k for k in losses):
            raise ValueError('METHOD_LOSS_MAPPING_REQUIRED')
        methods = sorted(losses)
        row.update(method_ids=methods, method_count=len(methods))
        if not methods:
            row.update(status='UNAVAILABLE', n=0, reason='NO_COMPLETE_METHODS')
            return row
        columns = {}
        for method in methods:
            raw = np.asarray(losses[method])
            if raw.ndim != 1 or raw.dtype.kind not in 'iuf' or not len(raw):
                raise ValueError('INVALID_FULL_LOSS_VECTOR:'+method)
            vector = np.asarray(raw, dtype=float)
            if not np.isfinite(vector).all() or np.any(vector < 0):
                raise ValueError('NONFINITE_OR_NEGATIVE_LOSS:'+method)
            if row['n'] is None:
                row['n'] = int(len(vector))
            elif len(vector) != row['n']:
                raise ValueError('FULL_LOSS_LENGTH_MISMATCH:'+method)
            columns[method] = vector.copy()
        row['block_size'] = max(int(h), int(math.ceil(row['n']**(1/3))))
        groups = []
        for method in methods:
            equal = next((g for g in groups if np.array_equal(columns[method], columns[g['representative']])), None)
            if equal is None:
                groups.append(dict(representative=method, members=[method]))
            else:
                equal['members'].append(method)
        row.update(unique_loss_groups=groups, unique_loss_class_count=len(groups))
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        row['reason'] = str(exc)
        return row

    if checkpoint is not None:
        checkpoint(stage='mcs_input_validated', n=row['n'], method_count=len(methods))
    if len(groups) == 1:
        row.update(status='COMPLETE_SINGLE_METHOD' if len(methods) == 1 else 'COMPLETE_IDENTICAL_LOSSES',
            included=methods.copy(), excluded=[], pvalues={method: 1. for method in methods})
        row['diagnostics']['analytic_case'] = 'single complete procedure; no inferential discrimination' if len(methods) == 1 else 'exactly identical complete loss vectors'
        return row

    matrix = np.column_stack([columns[group['representative']] for group in groups])
    if checkpoint is not None:
        checkpoint(stage='mcs_before_library', n=row['n'], unique_loss_class_count=len(groups))
    row['diagnostics']['library_attempts'] = 1
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', RuntimeWarning)
            model = MCS(matrix, size=.1, method='R', bootstrap='stationary',
                reps=int(reps), block_size=row['block_size'], seed=row['seed'])
            model.compute()
            included = _indices(model.included, len(groups))
            excluded = _indices(model.excluded, len(groups))
            if not included or included & excluded or included | excluded != set(range(len(groups))):
                raise ValueError('INVALID_LIBRARY_MEMBERSHIP_PARTITION')
            table = model.pvalues
            index = list(table.index)
            if _indices(index, len(groups)) != set(range(len(groups))):
                raise ValueError('INCOMPLETE_LIBRARY_PVALUES')
            pvalues = {}
            for raw_index, value in zip(index, table['Pvalue']):
                p = float(value)
                if not math.isfinite(p) or not 0 <= p <= 1:
                    raise ValueError('NONFINITE_OR_OUT_OF_RANGE_LIBRARY_PVALUE')
                i = int(raw_index)
                if (i in included) != (p > .1) or (i in excluded) != (p <= .1):
                    raise ValueError('LIBRARY_MEMBERSHIP_PVALUE_MISMATCH')
                pvalues[i] = p
            unfolded = {method: pvalues[i] for i, group in enumerate(groups) for method in group['members']}
            row.update(status='COMPLETE',
                included=sorted(method for i, group in enumerate(groups) if i in included for method in group['members']),
                excluded=sorted(method for i, group in enumerate(groups) if i in excluded for method in group['members']),
                pvalues={method: unfolded[method] for method in methods})
    except RESOURCE_ERRORS:
        raise
    except Exception as exc:
        row.update(status='MCS_FAILED', reason=type(exc).__name__+': '+str(exc),
                   included=[], excluded=[], pvalues={})
        row['diagnostics'].update(error_type=type(exc).__name__, error_message=str(exc))
    if checkpoint is not None:
        checkpoint(stage='mcs_after_library', n=row['n'], status=row['status'])
    return row
