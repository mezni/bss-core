from refund_agent.health import liveness_check, readiness_check


def test_liveness_check():
    assert liveness_check() == {"status": "ok"}


def test_readiness_check():
    result = readiness_check()

    assert result["status"] == "ok"
    assert result["metrics"] == "available"
