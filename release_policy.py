"""Distinguished-level multi-window SLO release policy.

The policy turns SLO evidence into a deterministic, fail-closed release decision.
"""

from dataclasses import dataclass

from slo_evaluator import BurnRateWindow


@dataclass(frozen=True)
class ReleaseSLOPolicy:
    fast_burn_limit: float = 14.4
    slow_burn_limit: float = 6.0

    def evaluate(self, *, fast: BurnRateWindow, slow: BurnRateWindow) -> dict[str, object]:
        fast_burn = fast.value()
        slow_burn = slow.value()
        blocked = fast_burn > self.fast_burn_limit or slow_burn > self.slow_burn_limit
        return {
            "decision": "BLOCK" if blocked else "ALLOW",
            "fast_burn": fast_burn,
            "slow_burn": slow_burn,
            "reason": "error-budget burn exceeds release policy" if blocked else "within error budget",
        }
