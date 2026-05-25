from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_students_api(client):
    response = client.get("/students/")
    assert response.status_code == 200

def test_create_student_api(client):

    response = client.post(
        "/students/",
        json={
            "name": "John",
            "age": 20,
            "branch": "CSE"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "John"

def test_create_student_invalid(client):

    response = client.post(
        "/students/",
        json={
            "name": "",
            "age": -1,
            "branch": ""
        }
    )

    assert response.status_code == 422

