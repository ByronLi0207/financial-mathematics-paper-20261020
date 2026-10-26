"""Aggregate-only WP2 publication, with an immutable 56-slot ranking family.

Import and aggregate_wp2 perform no file I/O. Only main installs disk loaders,
checks the frozen receipts, and exclusively creates the two new public reports.
Injected loaders permit synthetic tests without opening financial archives.
"""
from __future__ import annotations

import math
import numpy as np

import v6_inference as inf

METHODS = ('ACI_F', 'ACI_QR', 'SAV')
CONTROLS = ('frozen_F', 'QR')
TAU = .95
_DIAGNOSTICS = {'gamma', 'initial_calibration_count', 'alpha_min', 'alpha_max',
    'calibration_min', 'calibration_max', 'rank_min', 'rank_max', 'clip_count',
    'issue_count', 'clipped_issue_count', 'clipped_issue_fraction',
    'matured_wrapped_feedback_consumed', 'cumulative_matured_wrapped_feedback'}
_RESOURCES = {'started_utc', 'ended_utc', 'elapsed_seconds', 'peak_rss_bytes',
    'maximum_observed_os_threads', 'thread_snapshot_count', 'requested_numerical_threads',
    'internal_wall_seconds', 'hard_wall_seconds', 'internal_rss_bytes', 'hard_rss_bytes'}


class DataIdentityError(ValueError):
    """Admission discrepancy: stop the affected WP and create no public result."""
    def __init__(self, code, cell=None):
        self.code, self.cell = str(code), cell
        super().__init__(self.code + (': ' + cell if cell else ''))


class _MethodUnavailable(ValueError):
    """Declared procedure NA (or missing receipt in diagnostic-only aggregation)."""


def _scalars(value, allowed):
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError('INVALID_PUBLIC_METADATA')
    result = {}
    for key in sorted(allowed & set(value)):
        item = value[key]
        if item is not None and (not isinstance(item, (str, int, float, bool))
                or isinstance(item, float) and not math.isfinite(item)):
            raise ValueError('NONFINITE_OR_NONSCALAR_PUBLIC_METADATA')
        result[key] = item
    return result


def _ident(source, horizon, window, method):
    return f'{source}-h{horizon}-w{window}-{method}'


def _slot(source, horizon, window, left, right):
    return f'{source}:H{horizon}:W{window}:{left}-minus-{right}'


def _cells(spec):
    result = [(s, h, w) for s, c in spec['sources'].items()
              for h in spec['horizons'] for w in c['windows']]
    if len(result) != 8 or len(set(result)) != 8:
        raise ValueError('exactly eight original WP2 cells required')
    return result


def _fingerprint(value):
    return (isinstance(value, str) and len(value) == 64
            and all(c in '0123456789abcdef' for c in value))


def _proof(value):
    if not isinstance(value, dict) or any(not _fingerprint(value.get(k))
            for k in ('sha256', 'receipt_sha256')):
        raise ValueError('TRACE_RECEIPT_FINGERPRINT_MISSING')
    if any(type(value.get(k)) is not int or value[k] < 1 for k in ('bytes', 'receipt_bytes')):
        raise ValueError('TRACE_RECEIPT_BYTES_MISSING')
    return {k: value[k] for k in ('sha256', 'bytes', 'receipt_sha256', 'receipt_bytes')}


def _public_metrics(metrics):
    # The inference module's origins field is already aggregate metadata. Rename
    # it here to make the absence of public per-origin vectors explicit.
    import copy
    result = copy.deepcopy(metrics)
    if result.get('coverage'):
        grid = result['coverage']['fixed_grid']
        grid['grid_design'] = grid.pop('origins')
    return result


def _trace(bundle, expected, *, horizon, new):
    proof = _proof(bundle.get('provenance'))
    data = bundle['trace']
    ids = np.asarray(data['origins'])
    if ids.dtype.kind not in 'iu' or not np.array_equal(ids, expected):
        raise ValueError('ORIGIN_IDENTITY')
    capacity = np.asarray(data['capacities' if new else 'capacity'], dtype=float)
    peak, floor = (np.asarray(data[k], dtype=float) for k in ('peak', 'floor'))
    if any(v.shape != expected.shape or not np.isfinite(v).all()
           for v in (capacity, peak, floor)):
        raise ValueError('NONFINITE_OR_MISALIGNED_TRACE')
    if np.any(floor < 0) or np.any(capacity < floor) or np.any(peak < floor):
        raise ValueError('INVALID_FLOOR_GEOMETRY')
    metrics = inf.summarize_scores(peak, capacity, tau=TAU, origins=ids, horizon=horizon)
    if metrics['status'] != 'OK':
        raise ValueError('SCORE_REFERENCE_FAILURE')
    return dict(origins=ids, capacity=capacity, peak=peak, floor=floor,
                losses=inf.pinball_losses(peak, capacity, tau=TAU), metrics=metrics,
                proof=proof, archived_original_aggregate=data.get('original_aggregate'))


def _base_row(source, horizon, window, method):
    return dict(source=source, horizon=horizon, window=window, method=method,
                phase='evaluation', tau=TAU, update='original_refit_grid',
                analysis_status='post-result / exploratory', status='NA', reason=None)


def _failure(row, error):
    row['status'] = 'NA'
    row['reason'] = str(error) if isinstance(error, ValueError) else type(error).__name__
    return row


def _pair(left, right):
    return dict(mean_loss_difference=left['mean_loss'] - right['mean_loss'],
                coverage_distance_difference=left['coverage_distance'] - right['coverage_distance'],
                full_rate_difference=left['full_rate'] - right['full_rate'],
                full_hits_difference=left['full_hits'] - right['full_hits'])


def aggregate_wp2(spec, design_freeze, receipts, *, load_new, load_original, provenance):
    """Return (public summary, 56-row comparisons) using explicit loader evidence.

    receipts maps cell-method IDs to {receipt, sha256, bytes} envelopes. A loader
    returns {trace, provenance}; provenance contains the ACTUALLY VERIFIED file
    sha256/bytes and its public receipt sha256/bytes. The disk implementation in
    main computes these from bytes, checks private hashes before np.load, and
    uses worker.original_trace for original manifest/aggregate admission.

    No source units are pooled. Declared NA/missing methods remain rows; their
    ranking slots retain raw_p=None and bookkeeping_p=1. Input identity errors
    raise DataIdentityError and stop publication. DM normal-reference p
    is adjusted under the fixed original convention; raw HLN p is also retained.
    """
    cells = _cells(spec)
    slots = [_slot(s, h, w, m, c) for s, h, w in cells for m in METHODS for c in CONTROLS]
    slots += [_slot(s, h, w, 'ACI_QR', 'ACI_F') for s, h, w in cells]
    if (design_freeze.get('family_sizes', {}).get('WP2') != 56
            or design_freeze.get('wp2_contrast_slots') != slots):
        raise ValueError('frozen 56-slot inventory identity required')
    expected_ids = {_ident(s, h, w, m) for s, h, w in cells for m in METHODS}
    if set(receipts) - expected_ids:
        raise ValueError('undeclared evaluation receipt')
    for key in ('executable_freeze_sha256', 'selection_freeze_sha256',
                'design_freeze_sha256', 'spec_sha256'):
        if not _fingerprint(provenance.get(key)):
            raise ValueError('missing frozen provenance ' + key)
    admitted = {}
    rows, controls, pairs = [], [], []
    for source, horizon, window in cells:
        cfg = spec['sources'][source]
        expected = np.arange(cfg['evaluation_origin_first'], cfg['evaluation_origin_last'] + 1,
                             dtype=np.int64)
        if not len(expected):
            raise ValueError('nonempty original evaluation segment required')
        local_controls = {}
        for method in CONTROLS:
            row = _base_row(source, horizon, window, method)
            try:
                trace = _trace(load_original(source, horizon, window, method), expected,
                               horizon=horizon, new=False)
                if local_controls:
                    anchor = next(iter(local_controls.values()))
                    if not all(np.array_equal(trace[k], anchor[k]) for k in ('peak', 'floor')):
                        raise ValueError('CONTROL_TARGET_FLOOR_IDENTITY')
                local_controls[method] = trace
                admitted[_ident(source, horizon, window, method)] = trace
                row.update(status='COMPLETE', scores=_public_metrics(trace['metrics']),
                           input_fingerprints=trace['proof'],
                           archived_original_aggregate=_scalars(trace['archived_original_aggregate'],
                               set(trace['archived_original_aggregate'] or {})))
            except Exception as error:
                raise DataIdentityError(str(error), _ident(source, horizon, window, method)) from error
            controls.append(row)
        for method in METHODS:
            ident = _ident(source, horizon, window, method)
            row = _base_row(source, horizon, window, method)
            try:
                envelope = receipts.get(ident)
                if envelope is None:
                    raise _MethodUnavailable('MISSING_EVALUATION_RECEIPT')
                receipt = envelope['receipt']
                if not _fingerprint(envelope.get('sha256')) or type(envelope.get('bytes')) is not int or envelope['bytes'] < 1:
                    raise ValueError('EVALUATION_RECEIPT_FINGERPRINT_MISSING')
                row['evaluation_receipt_sha256'] = envelope['sha256']
                row['evaluation_receipt_bytes'] = envelope['bytes']
                if any(receipt.get(k) != value for k, value in
                       (('source', source), ('horizon', horizon), ('window', window),
                        ('method', method), ('phase', 'evaluation'))):
                    raise ValueError('EVALUATION_RECEIPT_IDENTITY')
                if receipt.get('executable_freeze_sha256') != provenance['executable_freeze_sha256']:
                    raise ValueError('EXECUTABLE_FREEZE_IDENTITY')
                if receipt.get('status') not in ('COMPLETE', 'NA'):
                    raise ValueError('INVALID_EVALUATION_STATUS')
                if receipt['status'] == 'NA':
                    raise _MethodUnavailable(receipt.get('reason') or 'EVALUATION_NA')
                validation = provenance.get('validation', {}).get(ident, {})
                if validation.get('status') != 'COMPLETE' or not _fingerprint(validation.get('receipt_sha256')):
                    raise ValueError('VALIDATION_INELIGIBLE')
                if method.startswith('ACI_'):
                    if (receipt.get('selection_freeze_sha256') != provenance['selection_freeze_sha256']
                            or receipt.get('validation_prefix_identical') is not True):
                        raise ValueError('SELECTION_FREEZE_IDENTITY')
                    if (receipt.get('selected_gamma') not in (.001, .005, .01, .05)
                            or receipt.get('selected_gamma') != validation.get('selected_gamma')):
                        raise ValueError('SELECTED_GAMMA_IDENTITY')
                if len(local_controls) != 2:
                    raise ValueError('CONTROL_ADMISSION_FAILURE')
                bundle = load_new(source, horizon, window, method, receipt)
                proof = _proof(bundle.get('provenance'))
                expected_private = receipt.get('private_artifact', {})
                if (proof['sha256'] != expected_private.get('sha256')
                        or proof['bytes'] != expected_private.get('bytes')
                        or proof['receipt_sha256'] != envelope['sha256']
                        or proof['receipt_bytes'] != envelope['bytes']):
                    raise ValueError('PRIVATE_ARTIFACT_IDENTITY')
                trace = _trace(bundle, expected, horizon=horizon, new=True)
                anchor = local_controls['frozen_F']
                if not all(np.array_equal(trace[k], anchor[k]) for k in ('peak', 'floor')):
                    raise ValueError('TARGET_FLOOR_IDENTITY')
                if trace['metrics'] != receipt.get('scores'):
                    raise ValueError('RECEIPT_SCORE_IDENTITY')
                admitted[ident] = trace
                row.update(status='COMPLETE', scores=_public_metrics(trace['metrics']),
                           input_fingerprints=trace['proof'],
                           resources=_scalars(receipt.get('resources'), _RESOURCES),
                           selected_gamma=receipt.get('selected_gamma'))
                if method.startswith('ACI_'):
                    base_method = 'QR' if method == 'ACI_QR' else 'frozen_F'
                    change = _pair(trace['metrics'], local_controls[base_method]['metrics'])
                    if 'unwrapped_scores' in receipt and receipt['unwrapped_scores'] != local_controls[base_method]['metrics']:
                        raise ValueError('UNWRAPPED_RECEIPT_SCORE_IDENTITY')
                    row.update(unwrapped_method=base_method,
                               wrapped_minus_base_mean_loss=change['mean_loss_difference'],
                               wrapped_minus_base_coverage_distance=change['coverage_distance_difference'],
                               wrapped_minus_base_full_rate=change['full_rate_difference'],
                               wrapped_minus_base_full_hits=change['full_hits_difference'],
                               diagnostics=_scalars(receipt.get('diagnostics'), _DIAGNOSTICS))
                else:
                    refits = receipt.get('refits', [])
                    row['refit_count'] = receipt.get('refit_count')
                    row['analytic_refit_count'] = sum(r.get('status') == 'ANALYTIC_CONSTANT' for r in refits)
                    row['converged_refit_count'] = sum(r.get('status') == 'CONVERGED' for r in refits)
            except _MethodUnavailable as error:
                _failure(row, error)
            except Exception as error:
                raise DataIdentityError(str(error), ident) from error
            rows.append(row)
        pair = dict(source=source, horizon=horizon, window=window, tau=TAU,
                    direction='QR_minus_F', status='NA', reason='WRAPPED_PAIR_UNAVAILABLE')
        if len(local_controls) == 2:
            unwrapped = _pair(local_controls['QR']['metrics'], local_controls['frozen_F']['metrics'])
            pair.update(unwrapped_qr_minus_f_mean_loss=unwrapped['mean_loss_difference'],
                        unwrapped_qr_minus_f_coverage_distance=unwrapped['coverage_distance_difference'],
                        unwrapped_qr_minus_f_full_hits=unwrapped['full_hits_difference'])
        left, right = (admitted.get(_ident(source, horizon, window, m)) for m in ('ACI_QR', 'ACI_F'))
        if left is not None and right is not None:
            wrapped = _pair(left['metrics'], right['metrics'])
            pair.update(status='COMPLETE', reason=None,
                        wrapped_qr_minus_f_mean_loss=wrapped['mean_loss_difference'],
                        wrapped_qr_minus_f_coverage_distance=wrapped['coverage_distance_difference'],
                        wrapped_qr_minus_f_full_hits=wrapped['full_hits_difference'])
        pairs.append(pair)
    comparisons = []
    for slot_id in slots:
        source, h, w, contrast = slot_id.split(':')
        horizon, window = int(h[1:]), int(w[1:])
        left_method, right_method = contrast.split('-minus-')
        row = dict(slot_id=slot_id, contrast_id=slot_id, source=source, horizon=horizon,
                   window=window, left_method=left_method, right_method=right_method,
                   tau=TAU, update='original_refit_grid', direction='new_minus_control',
                   status='NA_CELL', raw_p=None, dm_p=None, hln_p=None,
                   mean_difference=None)
        left, right = (admitted.get(_ident(source, horizon, window, m)) for m in (left_method, right_method))
        if left is not None and right is not None:
            diagnostic = inf.compare_losses(left['losses'], right['losses'], horizon=horizon)
            row.update(diagnostic)
            row['raw_p'] = diagnostic.get('dm_p') if diagnostic.get('status') == 'OK' else None
        comparisons.append(row)
    holm = inf.fixed_slot_holm(slots, {r['slot_id']: r['raw_p'] for r in comparisons})
    for row, adjusted in zip(comparisons, holm['slots']):
        row.update(bookkeeping_p=adjusted['bookkeeping_p'], holm_p=adjusted['holm_p'],
                   holm_component_status=adjusted['status'])
    public_provenance = {key: provenance[key] for key in
                         ('executable_freeze_sha256', 'selection_freeze_sha256',
                          'design_freeze_sha256', 'spec_sha256')}
    code = provenance.get('code_fingerprints', {})
    if not isinstance(code, dict) or any(not _fingerprint(v) for v in code.values()):
        raise DataIdentityError('INVALID_CODE_FINGERPRINTS')
    if code:
        public_provenance['code_fingerprints'] = dict(code)
    common = dict(analysis_status='post-result / exploratory', tau=TAU,
                  provenance=public_provenance,
                  interpretation='Working-reference diagnostics; inspected evaluation archive, dependent training and overlap, no imported coverage guarantee or selection-adjusted confirmation.')
    summary = dict(**common, status=('INCOMPLETE_EVALUATION_INVENTORY' if set(receipts) != expected_ids
                   else 'COMPLETE_WITH_NA' if any(r['status'] != 'COMPLETE' for r in rows + controls) else 'COMPLETE'),
                   method_row_count=24, control_row_count=16, method_rows=rows,
                   control_rows=controls, aci_pairs=pairs,
                   complete_method_count=sum(r['status'] == 'COMPLETE' for r in rows),
                   na_method_count=sum(r['status'] != 'COMPLETE' for r in rows))
    ranking = dict(**common, family='WP2', family_n=56, rows=comparisons,
                   raw_na_count=holm['raw_na_count'], raw_p_definition='normal-reference DM dm_p',
                   hln_p_definition='Student-reference HLN; unadjusted diagnostic',
                   holm_note='All 56 frozen slots retained; raw NA maps to bookkeeping 1 only. Adjustments do not validate failed reference distributions or cover all historical analysis selection.')
    return summary, ranking


def main(argv=None):
    """Root-owned serial entry point. Financial/archive I/O exists only here."""
    import argparse
    import hashlib
    import json
    from pathlib import Path
    import v6_worker as worker

    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    root = Path(__file__).resolve().parent
    public = root / 'results/revision-20261023/v6'
    private = root / '.scratch/revision-v6/wp2'
    outputs = (public / 'wp2-summary.json', public / 'wp2-comparisons.json')
    if any(p.exists() for p in outputs):
        raise FileExistsError('WP2_PUBLIC_REPORT_ALREADY_EXISTS')

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def envelope(path):
        data = path.read_bytes()
        return dict(receipt=json.loads(data), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))

    def read(path):
        return envelope(path)['receipt']

    execution_hash = worker.check_execution_freeze()
    spec_path = root / worker.SPEC
    design_path = root / 'protocol/revision-v6/design-freeze.json'
    selection_path = public / 'wp2-selection-freeze.json'
    spec, design, selection = read(spec_path), read(design_path), read(selection_path)
    if sha(spec_path) != design['original_spec_sha256']:
        raise ValueError('ORIGINAL_SPEC_CHANGED')
    if sha(root / worker.SELECTION) != design['original_selection_sha256']:
        raise ValueError('ORIGINAL_SELECTION_CHANGED')
    for path, fingerprint in design['documents'].items():
        if sha(root / path) != fingerprint:
            raise ValueError('FROZEN_DESIGN_DOCUMENT_CHANGED')
    if selection.get('status') != 'FROZEN_BEFORE_WP2_EVALUATION' or selection.get('cell_count') != 24:
        raise ValueError('WP2_SELECTION_FREEZE_IDENTITY')
    receipts, validation, envelopes = {}, {}, {}
    for source, horizon, window in _cells(spec):
        for method in METHODS:
            ident = _ident(source, horizon, window, method)
            frozen = selection['cells'][ident]
            path = public / 'wp2' / f'validation-{ident}.json'
            val_envelope = envelope(path)
            if val_envelope['sha256'] != frozen['receipt_sha256']:
                raise DataIdentityError('VALIDATION_RECEIPT_CHANGED', ident)
            val = val_envelope['receipt']
            if val['status'] != frozen['status']:
                raise DataIdentityError('VALIDATION_STATUS_CHANGED', ident)
            if method.startswith('ACI_') and val.get('selection', {}).get('gamma') != frozen.get('selected_gamma'):
                raise DataIdentityError('FROZEN_VALIDATION_GAMMA_IDENTITY', ident)
            validation[ident] = dict(frozen)
            path = public / 'wp2' / f'evaluation-{ident}.json'
            if path.exists():
                evidence = envelope(path)
                receipts[ident] = evidence
                envelopes[ident] = evidence
    if len(receipts) != 24:
        missing = sorted({_ident(s, h, w, m) for s, h, w in _cells(spec) for m in METHODS} - set(receipts))
        raise DataIdentityError('INCOMPLETE_EVALUATION_INVENTORY', ','.join(missing))

    def load_new(source, horizon, window, method, receipt):
        ident = _ident(source, horizon, window, method)
        path = private / f'evaluation-{ident}.npz'
        actual = dict(sha256=sha(path), bytes=path.stat().st_size)
        if actual != receipt.get('private_artifact'):
            raise ValueError('PRIVATE_ARTIFACT_IDENTITY')
        with np.load(path, allow_pickle=False) as archive:
            trace = {k: np.array(archive[k], copy=True) for k in ('origins', 'capacities', 'peak', 'floor')}
        actual.update(receipt_sha256=envelopes[ident]['sha256'], receipt_bytes=envelopes[ident]['bytes'])
        return dict(trace=trace, provenance=actual)

    def load_original(source, horizon, window, method):
        phase = 'references' if method == 'frozen_F' else 'evaluation'
        trace = worker.original_trace(source, horizon, window, phase, method)
        entry = worker.trace_entry(source, horizon, window, phase,
                                   'historical_references' if phase == 'references' else method)
        manifest = root / entry['manifest_path']
        return dict(trace=trace, provenance=dict(sha256=entry['sha256'], bytes=entry['bytes'],
                    receipt_sha256=entry['manifest_sha256'], receipt_bytes=manifest.stat().st_size))

    provenance = dict(executable_freeze_sha256=execution_hash,
                      selection_freeze_sha256=sha(selection_path), design_freeze_sha256=sha(design_path),
                      spec_sha256=sha(spec_path), validation=validation,
                      code_fingerprints={name: sha(root / name) for name in
                                         ('v6_wp2_summary.py', 'v6_inference.py', 'v6_worker.py')})
    summary, comparisons = aggregate_wp2(spec, design, receipts, load_new=load_new,
                                         load_original=load_original, provenance=provenance)
    # Fully encode both before exclusively creating either destination.
    encoded = [json.dumps(report, indent=2, allow_nan=False) + '\n' for report in (summary, comparisons)]
    public.mkdir(parents=True, exist_ok=True)
    for path, content in zip(outputs, encoded):
        with path.open('x') as handle:
            handle.write(content)
    print(json.dumps(dict(status=summary['status'], method_rows=24, control_rows=16,
                          complete_methods=summary['complete_method_count'],
                          family_n=56, raw_na_count=comparisons['raw_na_count']), allow_nan=False))
    return summary, comparisons


if __name__ == '__main__':
    main()
