"""Tests for the skills CRUD endpoints."""

import uuid


def test_list_skills_empty(client):
    response = client.get("/skills/")
    assert response.status_code == 200
    assert response.json() == {}


def test_list_skills_grouped(client, auth_headers):
    """Skills should be grouped by type (front, language, other)."""
    client.post("/skills/", json={
        "title": "React",
        "start": "2020-01-01",
        "type": "front",
    }, headers=auth_headers)

    client.post("/skills/", json={
        "title": "Python",
        "start": "2024-01-01",
        "type": "language",
    }, headers=auth_headers)

    response = client.get("/skills/")
    data = response.json()
    assert "front" in data
    assert "language" in data
    assert data["front"][0]["title"] == "React"


def test_list_skills_filter_by_type(client, auth_headers):
    client.post("/skills/", json={
        "title": "React",
        "start": "2020-01-01",
        "type": "front",
    }, headers=auth_headers)

    client.post("/skills/", json={
        "title": "Python",
        "start": "2024-01-01",
        "type": "language",
    }, headers=auth_headers)

    response = client.get("/skills/?type=front")
    data = response.json()
    assert "front" in data
    assert "language" not in data


def test_get_skill_by_id(client, auth_headers):
    create_resp = client.post("/skills/", json={
        "title": "Docker",
        "start": "2021-04-01",
        "type": "other",
    }, headers=auth_headers)
    skill_id = create_resp.json()["id"]

    response = client.get(f"/skills/{skill_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Docker"


def test_get_skill_not_found(client):
    response = client.get(f"/skills/{uuid.uuid4()}")
    assert response.status_code == 404


def test_create_skill_no_auth(client):
    response = client.post("/skills/", json={
        "title": "Go",
        "start": "2025-01-01",
        "type": "language",
    })
    assert response.status_code == 401


def test_create_skill(client, auth_headers):
    response = client.post("/skills/", json={
        "title": "TypeScript",
        "start": "2021-04-01",
        "end": None,
        "type": "language",
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "TypeScript"


def test_update_skill(client, auth_headers):
    create_resp = client.post("/skills/", json={
        "title": "JS",
        "start": "2020-01-01",
        "type": "language",
    }, headers=auth_headers)
    skill_id = create_resp.json()["id"]

    response = client.patch(f"/skills/{skill_id}", json={
        "title": "JavaScript",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "JavaScript"


def test_delete_skill(client, auth_headers):
    create_resp = client.post("/skills/", json={
        "title": "To Delete",
        "start": "2020-01-01",
        "type": "other",
    }, headers=auth_headers)
    skill_id = create_resp.json()["id"]

    response = client.delete(f"/skills/{skill_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/skills/{skill_id}")
    assert response.status_code == 404
