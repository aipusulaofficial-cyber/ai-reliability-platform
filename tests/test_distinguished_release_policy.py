import pytest

from release_policy import ReleaseSLOPolicy
from slo_evaluator import BurnRateWindow


def window(good: int, total: int, target: float = 0.99) -> BurnRateWindow:
    return BurnRateWindow(good, total, target)


def test_release_allowed_when_both_windows_are_within_budget():
    result = ReleaseSLOPolicy().evaluate(fast=window(999, 1000), slow=window(999, 1000))
    assert result["decision"] == "ALLOW"


def test_release_blocks_on_fast_burn_even_when_slow_window_is_healthy():
    result = ReleaseSLOPolicy().evaluate(fast=window(850, 1000), slow=window(999, 1000))
    assert result["decision"] == "BLOCK"
    assert result["fast_burn"] > 14.4


def test_release_blocks_on_sustained_slow_burn():
    result = ReleaseSLOPolicy().evaluate(fast=window(999, 1000), slow=window(930, 1000))
    assert result["decision"] == "BLOCK"
    assert result["slow_burn"] > 6.0
