"""Archive date/count budgets from the already-pinned local sources; no fits."""
from pathlib import Path
import sys
import json
import hashlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from supervisor_e3 import source

spec_path = ROOT / "protocol/revision-20261022/study-spec.json"
spec = json.loads(spec_path.read_text())
out = {}
for name, cfg in spec["sources"].items():
    data = source(name, spec)
    item = dict(source_sha256=data.sha256, record_count=len(data.position),
                first_date=str(data.dates[0])[:10], last_date=str(data.dates[-1])[:10],
                windows=cfg["windows"], refit_step=cfg["refit_step"])
    for segment in ("validation", "evaluation"):
        first, last = [cfg[segment + "_origin_" + endpoint] for endpoint in ("first", "last")]
        item[segment] = dict(first_index=first, last_index=last, count=last-first+1,
                             first_date=str(data.dates[first])[:10], last_date=str(data.dates[last])[:10])
    item["all_validation_labels_complete_before_evaluation"] = (
        item["validation"]["last_index"] + max(spec["horizons"]) < item["evaluation"]["first_index"])
    assert item["all_validation_labels_complete_before_evaluation"]
    out[name] = item
out["provenance"] = dict(spec_sha256=hashlib.sha256(spec_path.read_bytes()).hexdigest(),
                          script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          existing_local_sources_only=True, no_new_forecast=True)
destination = ROOT / "results/supervisor-20261023/round2/source-date-budgets.json"
with destination.open("x") as stream:
    json.dump(out, stream, indent=2)
    stream.write("\n")
print(json.dumps(out, indent=2))
