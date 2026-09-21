"""Smoke tests for the intentionally faulty demo service."""

from fastapi.testclient import TestClient

from app import SERVICE_NAME, app

client = TestClient(app)


def test_root_reports_ready():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": SERVICE_NAME, "status": "ready"}


def test_health_is_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_work_completes_and_reports_latency():
    response = client.get("/work")

    assert response.status_code == 200
    result = response.json()
    assert result["service"] == SERVICE_NAME
    assert result["result"] == "done"
    assert result["elapsed_ms"] >= 100
    assert result["worker_limit"] >= 1
