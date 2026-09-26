from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
from service import app

c = TestClient(app)


def test_contract():
    assert c.get("/health/live").status_code == 200


@given(st.text(min_size=1, max_size=32).filter(lambda value: value.strip()))
def test_property(v):
    response = c.post(
        "/v1/reliability",
        json={"key": v, "payload": {"target": 0.99, "total": 1, "successes": 1}},
    )
    assert response.status_code == 200


@given(st.text(min_size=1, max_size=32))
def test_blank_key_rejected(v):
    if not v.strip():
        response = c.post(
            "/v1/reliability",
            json={"key": v, "payload": {"target": 0.99, "total": 1, "successes": 1}},
        )
        assert response.status_code == 422
