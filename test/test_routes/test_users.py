import json


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
    }
    response = client.post("/users/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True


def test_get_user(client):
    response = client.get("/users/",)
    assert response.status_code == 200
    assert response.json()[0]
