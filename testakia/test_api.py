from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GymLogger Lite API"}


def test_get_workouts():
    response = client.get("/workouts/")
    assert response.status_code == 200


def test_workout_not_found():
    response = client.get("/workouts/999")
    assert response.status_code == 404


def test_get_exercises():
    response = client.get("/exercises/")
    assert response.status_code == 200


def test_get_stats():
    response = client.get("/stats/")
    assert response.status_code == 200
