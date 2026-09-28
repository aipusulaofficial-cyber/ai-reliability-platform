from slo_evaluator import BurnRateWindow


def test_burn_rate_is_computed_from_error_rate():
    window = BurnRateWindow(good_events=99, total_events=100, target=0.99)
    assert window.value() == 1.0
    assert window.breaching() is False


def test_burn_rate_detects_breach():
    window = BurnRateWindow(good_events=98, total_events=100, target=0.99)
    assert window.value() == 2.0
    assert window.breaching() is True
