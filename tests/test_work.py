"""Tests for the work CRUD endpoints."""

import uuid


def test_list_work_empty(client):
    response = client.get("/work/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_work_sorted_by_start_desc(client, auth_headers):
    """Work entries should be sorted by start date descending (newest first)."""
    client.post("/work/", json={
        "company": "Old Corp",
        "role": "Junior",
        "description": "Old job",
        "start": "2019-01-01",
        "end": "2020-01-01",
        "location": "Remote",
    }, headers=auth_headers)

    client.post("/work/", json={
        "company": "New Corp",
        "role": "Senior",
        "description": "New job",
        "start": "2024-01-01",
        "location": "Remote",
    }, headers=auth_headers)

    response = client.get("/work/")
    data = response.json()
    assert len(data) == 2
    assert data[0]["company"] == "New Corp"  # newest first
    assert data[1]["company"] == "Old Corp"


def test_work_camel_case_response(client, auth_headers):
    """Response fields should be camelCased (techStack, not tech_stack)."""
    client.post("/work/", json={
        "company": "Acme",
        "role": "Dev",
        "description": "Work",
        "start": "2023-01-01",
        "location": "Remote",
        "tech_stack": "Python, FastAPI",
    }, headers=auth_headers)

    response = client.get("/work/")
    data = response.json()
    assert "techStack" in data[0]
    assert data[0]["techStack"] == "Python, FastAPI"


def test_get_work_by_id(client, auth_headers):
    create_resp = client.post("/work/", json={
        "company": "Acme",
        "role": "Dev",
        "description": "Work",
        "start": "2023-01-01",
        "location": "Remote",
    }, headers=auth_headers)
    work_id = create_resp.json()["id"]

    response = client.get(f"/work/{work_id}")
    assert response.status_code == 200
    assert response.json()["company"] == "Acme"


def test_get_work_not_found(client):
    response = client.get(f"/work/{uuid.uuid4()}")
    assert response.status_code == 404


def test_create_work_no_auth(client):
    response = client.post("/work/", json={
        "company": "Acme",
        "role": "Dev",
        "description": "Work",
        "start": "2023-01-01",
        "location": "Remote",
    })
    assert response.status_code == 401


def test_create_work(client, auth_headers):
    response = client.post("/work/", json={
        "company": "Acme",
        "role": "Dev",
        "description": "Work",
        "start": "2023-01-01",
        "end": "2024-01-01",
        "location": "Remote",
        "tech_stack": "Python, FastAPI",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["company"] == "Acme"
    assert data["techStack"] == "Python, FastAPI"


def test_update_work(client, auth_headers):
    create_resp = client.post("/work/", json={
        "company": "Acme",
        "role": "Junior Dev",
        "description": "Work",
        "start": "2023-01-01",
        "location": "Remote",
    }, headers=auth_headers)
    work_id = create_resp.json()["id"]

    response = client.patch(f"/work/{work_id}", json={
        "role": "Senior Dev",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["role"] == "Senior Dev"
    assert response.json()["company"] == "Acme"  # unchanged


def test_delete_work(client, auth_headers):
    create_resp = client.post("/work/", json={
        "company": "To Delete",
        "role": "Dev",
        "description": "Work",
        "start": "2023-01-01",
        "location": "Remote",
    }, headers=auth_headers)
    work_id = create_resp.json()["id"]

    response = client.delete(f"/work/{work_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get(f"/work/{work_id}")
    assert response.status_code == 404
