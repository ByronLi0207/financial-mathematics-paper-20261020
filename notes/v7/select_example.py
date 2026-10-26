"""V7 S5 whitelist (e), deterministic real-window selection without forecasting.

Rule fixed before this invocation: scan the original Treasury-bill H6/W260
evaluation origins in increasing order. Select the first whose absolute
endpoint is <= its already saved fixed-window historical-headroom capacity,
while its sampled absolute peak is > that capacity. Use all original origins;
never rank by gap, visual appearance, loss, year, or forecast performance.
Read saved capacities only: no call to a forecasting routine or new fitting.
"""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TRACE = ROOT / ".scratch/revision-20261022/replication-revision-v3-b5-full/references-nyfed_weekly-h6-w260"
SOURCE = ROOT / "data/nyfed-pdposgs-b-20261022/PDPOSGS-B.csv"
PRIOR = ROOT / "results/revision-20261023/v5-novelty/motivating-window-final.json"


def main():
    old = json.loads(PRIOR.read_text())
    spec = json.loads((ROOT / "protocol/revision-20261022/study-spec.json").read_text())
    cfg = spec["sources"]["nyfed_weekly"]
    source_bytes = SOURCE.read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == cfg["sha256"]
    rows = list(csv.DictReader(source_bytes.decode().splitlines()))
    x = np.array([float(row["Value (millions)"]) for row in rows])
    assert len(x) == cfg["record_count"]
    manifest = json.loads((TRACE / "public/manifest.json").read_text())
    artifact = next(item for item in manifest["artifacts"] if item["name"] == "numeric-traces.npz")
    trace = TRACE / "private/numeric-traces.npz"
    raw = trace.read_bytes()
    assert len(raw) == artifact["bytes"] and hashlib.sha256(raw).hexdigest() == artifact["sha256"]
    horizon = cfg["primary_contrast"]["horizon"]
    selected = None
    with np.load(trace, allow_pickle=False) as saved:
        origins = saved["frozen_F_origins"]
        assert np.array_equal(origins, np.arange(cfg["evaluation_origin_first"], cfg["evaluation_origin_last"] + 1))
        capacities, peaks = saved["frozen_F_capacity"], saved["frozen_F_peak"]
        for j, t in enumerate(origins):
            t = int(t)
            path = np.abs(x[t:t + horizon + 1])
            peak, endpoint, capacity = float(max(path)), float(path[-1]), float(capacities[j])
            assert peak == float(peaks[j])
            if endpoint <= capacity < peak:
                selected = dict(origin=t, horizon=horizon, report=capacity, floor=float(path[0]),
                                peak=peak, endpoint_absolute=endpoint,
                                positions=[float(v) for v in x[t:t + horizon + 1]],
                                absolute_positions=[float(v) for v in path],
                                dates=[row["As Of Date"] for row in rows[t:t + horizon + 1]],
                                selection_rule="earliest eligible issue origin; absolute endpoint <= saved fixed-window historical headroom report < sampled peak")
                break
    if selected is None:
        raise RuntimeError("NO_QUALIFYING_WINDOW; no substitute selection allowed")
    for key in ("origin", "horizon", "report", "floor", "peak", "endpoint_absolute", "positions", "absolute_positions"):
        assert selected[key] == old["example"][key], key
    result = dict(status="PASS", selection=selected, saved_trace_sha256=artifact["sha256"],
                  source_sha256=cfg["sha256"], existing_illustration_identical=True,
                  forecasts_computed=0, models_fitted=0, new_data=0)
    with (HERE / "example-selection.json").open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps({k: v for k, v in result.items() if k != "selection"}, indent=2))
    print(json.dumps({k: selected[k] for k in ("origin", "horizon", "report", "peak", "endpoint_absolute")}, indent=2))


if __name__ == "__main__":
    main()
