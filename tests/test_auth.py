"""Tests for the authentication endpoint."""


def test_login_success(client, test_user):
    """Valid credentials should return a JWT token."""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Wrong password should return 401."""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Non-existent user should return 401."""
    response = client.post("/auth/login", json={
        "username": "nobody",
        "password": "whatever",
    })
    assert response.status_code == 401
