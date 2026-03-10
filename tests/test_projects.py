"""Tests for the projects CRUD endpoints.

Pattern for each resource:
1. Test public GET (list + by id)
2. Test POST requires auth
3. Test POST with auth creates the resource
4. Test PATCH updates the resource
5. Test DELETE removes the resource
6. Test 404 for non-existent resources
"""

import uuid


# -- Public endpoints --

def test_list_projects_empty(client):
    """Empty database should return an empty dict."""
    response = client.get("/projects/")
    assert response.status_code == 200
    assert response.json() == {}


def test_list_projects_grouped(client, auth_headers):
    """Projects should be grouped by type."""
    client.post("/projects/", json={
        "title": "My Site",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)

    client.post("/projects/", json={
        "title": "Experiment",
        "description": "An experiment",
        "link": "https://example.com/exp",
        "year": 2023,
        "type": "exp",
    }, headers=auth_headers)

    response = client.get("/projects/")
    data = response.json()
    assert "project" in data
    assert "exp" in data
    assert len(data["project"]) == 1
    assert len(data["exp"]) == 1


def test_list_projects_filter_by_type(client, auth_headers):
    """Filter projects by type query param."""
    client.post("/projects/", json={
        "title": "My Site",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)

    client.post("/projects/", json={
        "title": "Experiment",
        "description": "An experiment",
        "link": "https://example.com/exp",
        "year": 2023,
        "type": "exp",
    }, headers=auth_headers)

    response = client.get("/projects/?type=project")
    data = response.json()
    assert "project" in data
    assert "exp" not in data


def test_get_project_by_id(client, auth_headers):
    """Get a single project by UUID."""
    create_resp = client.post("/projects/", json={
        "title": "My Site",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "My Site"


def test_get_project_not_found(client):
    """Non-existent UUID should return 404."""
    fake_id = uuid.uuid4()
    response = client.get(f"/projects/{fake_id}")
    assert response.status_code == 404


# -- Protected endpoints --

def test_create_project_no_auth(client):
    """POST without auth should return 401."""
    response = client.post("/projects/", json={
        "title": "My Site",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    })
    assert response.status_code == 401


def test_create_project(client, auth_headers):
    """POST with auth should create and return the project."""
    response = client.post("/projects/", json={
        "title": "My Site",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Site"
    assert "id" in data


def test_update_project(client, auth_headers):
    """PATCH should update only the provided fields."""
    create_resp = client.post("/projects/", json={
        "title": "Old Title",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = client.patch(f"/projects/{project_id}", json={
        "title": "New Title",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["description"] == "A website"  # unchanged


def test_delete_project(client, auth_headers):
    """DELETE should remove the project (204 No Content)."""
    create_resp = client.post("/projects/", json={
        "title": "To Delete",
        "description": "A website",
        "link": "https://example.com",
        "year": 2024,
        "type": "project",
    }, headers=auth_headers)
    project_id = create_resp.json()["id"]

    response = client.delete(f"/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 404
