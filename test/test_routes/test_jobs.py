import json
import uuid

from fastapi import status

from app.core.config import settings


def test_create_job(client, normal_user_token_headers):
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    response = client.post(
        "/jobs/create-job/", data=json.dumps(data), headers=normal_user_token_headers
    )
    settings.id = response.json()['id']
    assert response.status_code == 200
    assert response.json()["company"] == "doogle"
    assert response.json()["description"] == "python"


def test_update_a_job(client, normal_user_token_headers):
    data = {"title": "test new title", "company": "doogle", "company_url": "www.doogle.com", "location": "USA,NY",
            "description": "fastapi", "date_posted": "2022-03-20"}
    response = client.put(f"/jobs/update/{settings.id}", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["title"] == "test new title"


def test_read_jobs(client, normal_user_token_headers):
    response = client.get("/jobs/all/")
    assert response.status_code == 200
    assert response.json()[0]


def test_delete_a_job(client, normal_user_token_headers):
    client.delete(f"/jobs/delete/{settings.id}", headers=normal_user_token_headers)
    response = client.get(f"/jobs/get/{settings.id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
