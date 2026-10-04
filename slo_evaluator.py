import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BurnRateWindow:
    good_events: int
    total_events: int
    target: float

    def value(self) -> float:
        if (
            isinstance(self.good_events, bool)
            or not isinstance(self.good_events, int)
            or isinstance(self.total_events, bool)
            or not isinstance(self.total_events, int)
            or self.total_events < 1
            or self.good_events < 0
            or self.good_events > self.total_events
            or isinstance(self.target, bool)
            or not isinstance(self.target, (int, float))
            or not math.isfinite(self.target)
            or not 0 < self.target < 1
        ):
            raise ValueError("invalid SLO window")
        error_rate = 1 - self.good_events / self.total_events
        return error_rate / (1 - self.target)

    def breaching(self, threshold: float = 1.0) -> bool:
        if (
            isinstance(threshold, bool)
            or not isinstance(threshold, (int, float))
            or not math.isfinite(threshold)
            or threshold <= 0
        ):
            raise ValueError("threshold must be finite and positive")
        return self.value() > threshold
