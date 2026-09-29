import pytest

from slo_evaluator import BurnRateWindow


@pytest.mark.parametrize("good,total", [(-1, 10), (11, 10), (0, 0)])
def test_invalid_event_counts_rejected(good, total):
    with pytest.raises(ValueError):
        BurnRateWindow(good, total, 0.99).value()


def test_valid_burn_rate():
    assert BurnRateWindow(99, 100, 0.99).value() == pytest.approx(1.0)
