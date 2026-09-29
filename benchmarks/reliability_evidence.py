import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reliability_domain import SLO, burn_rate, error_budget, sli

s = SLO("availability", 0.99, 1000)
observed = sli(980, 1000)
report = {
    "sli": observed,
    "error_budget": error_budget(s, 980, 1000),
    "burn_rate": burn_rate(s, observed),
}
if abs(report["sli"] - 0.98) > 1e-9:
    raise SystemExit(report)
if abs(report["error_budget"] - 0.01) > 1e-9:
    raise SystemExit(report)
print(json.dumps(report, sort_keys=True))
