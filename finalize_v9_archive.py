"""Exact postrun serialization of saved receipts; never fits or forecasts.

The frozen runner's final reporting failed on a NumPy integer. Its partial
file, successful summaries, code and all unit bytes remain untouched.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def native_scalars(value):
    import numpy as np
    if isinstance(value,np.generic):return value.item()
    if isinstance(value,dict):return {k:native_scalars(v) for k,v in value.items()}
    if isinstance(value,list):return [native_scalars(v) for v in value]
    if isinstance(value,tuple):return [native_scalars(v) for v in value]
    return value


def digest(raw):return hashlib.sha256(raw).hexdigest()


def finalize(directory):
    from run_v9_nonstationarity import prediction_status,verify_seal
    directory=Path(directory);out=directory/'postrun'
    names=('manifest.json','diagnostics.json','summary.json','run-plan.json',
           'formal/completion.json','formal/units-manifest.json','predictions.json')
    source={name:(directory/name).read_bytes() for name in names}
    parsed={name:json.loads(raw) for name,raw in source.items() if name!='predictions.json'}
    manifest=parsed['manifest.json'];verify_seal(manifest)
    archive=directory/'formal/units.zip'
    if digest(archive.read_bytes())!=parsed['formal/units-manifest.json']['archive_sha256']:
        raise ValueError('FORMAL_ARCHIVE_SHA_MISMATCH')
    records=[];plan=parsed['run-plan.json'];R=plan['repetitions']
    with zipfile.ZipFile(archive) as z:
        for rep in range(R):
            for index in range(13):
                row=json.loads(z.read(f's{index:02}-r{rep:03}/result.json'))
                if row.get('rep')!=rep or row.get('source_index')!=index:
                    raise ValueError('UNIT_IDENTITY_MISMATCH')
                records.extend(row.get('records',[]))
    ids=[r['source_id'] for r in manifest['sources'][:13]]
    predictions=prediction_status(parsed['summary.json'],parsed['diagnostics.json'],ids)
    native=native_scalars(predictions)
    payloads={name:source[name] for name in ('manifest.json','diagnostics.json','summary.json')}
    payloads.update({'predictions.json':(json.dumps(native,indent=2,allow_nan=False)+'\n').encode(),
                    'formal/replicate-scores.json':(json.dumps(records,indent=2,allow_nan=False)+'\n').encode()})
    # Serialization and input checks finish before creating the exclusive output.
    out.mkdir(exist_ok=False)
    for name,raw in payloads.items():
        path=out/name;path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f:f.write(raw)
    provenance=dict(schema='v9-postrun-serialization-v1',study_rerun=False,
        scientific_code_changed=False,source_files_modified=False,
        cause='Frozen runner postrun JSON writer rejected numpy.int64 N1.holm_rejections; all forecast tasks had already ended and units.zip was complete.',
        transformation='NumPy scalar.item() only; no rounding, deletion, changed prediction threshold, partial median or replacement result.',
        source_sha256={name:digest(raw) for name,raw in source.items()},
        formal_archive_sha256=digest(archive.read_bytes()),
        source_error_file_preserved='predictions.json',
        output_sha256={name:digest(raw) for name,raw in payloads.items()},
        registered_repetitions=R,archived_comparison_records=len(records),
        original_formal_completion=parsed['formal/completion.json'])
    with (out/'provenance.json').open('x') as f:json.dump(provenance,f,indent=2,allow_nan=False);f.write('\n')
    for name,raw in source.items():
        if (directory/name).read_bytes()!=raw:raise ValueError('SOURCE_BYTES_CHANGED')
    print(json.dumps(native,indent=2))
    return provenance


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    finalize(parser.parse_args().directory)
