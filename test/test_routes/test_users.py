import json

from fastapi import status

from app.core.config import settings


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
        "is_superuser": True
    }
    response = client.post("/users/", json.dumps(data))
    settings.id = response.json()['id']
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True


def test_get_user(client):
    response = client.get("/users/", )
    assert response.status_code == 200
    assert response.json()[0]
