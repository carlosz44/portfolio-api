"""Tests for the health check endpoint.

This is the simplest test — a good starting point to verify the test setup works.
`client` is a fixture from conftest.py (injected automatically by pytest).
"""


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
