from refund_agent.metrics import agent_metrics


def liveness_check() -> dict[str, str]:
    """Confirm that the application process can respond."""
    return {"status": "ok"}


def readiness_check() -> dict[str, str]:
    """Report whether the basic application components are configured."""
    return {
        "status": "ok",
        "metrics": "available",
    }


def metrics_snapshot() -> dict:
    return agent_metrics.snapshot()
