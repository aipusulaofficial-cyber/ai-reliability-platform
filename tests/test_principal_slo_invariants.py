import math

import pytest

from slo_evaluator import BurnRateWindow


@pytest.mark.parametrize(
    "good,total,target",
    [
        (-1, 10, 0.99),
        (11, 10, 0.99),
        (0, 0, 0.99),
        (8, 10, 1.0),
        (8, 10, math.nan),
        (True, 10, 0.99),
    ],
)
def test_rejects_invalid_window(good, total, target):
    with pytest.raises(ValueError, match="invalid SLO window"):
        BurnRateWindow(good, total, target).value()


@pytest.mark.parametrize("threshold", [0.0, -1.0, math.nan, math.inf, True, "1"])
def test_rejects_invalid_threshold(threshold):
    with pytest.raises(ValueError, match="threshold"):
        BurnRateWindow(99, 100, 0.99).breaching(threshold)


def test_valid_window_has_expected_burn_rate():
    assert BurnRateWindow(99, 100, 0.99).value() == pytest.approx(1.0)
