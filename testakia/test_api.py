from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Καταγραφή Προπονήσεων" in response.text


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


def test_create_workout():
    response = client.post("/workouts/", json={
        "title": "Test Workout",
        "date": "2026-09-25",
        "duration": 60,
        "notes": "test"
    })

    assert response.status_code == 200
    assert response.json()["title"] == "Test Workout"


def test_create_exercise():
    response = client.post("/exercises/", json={
        "name": "Bench Press",
        "muscle_group": "Chest"
    })

    assert response.status_code == 200
    assert response.json()["name"] == "Bench Press"


def test_delete_workout_with_performance():
    workout = client.post("/workouts/", json={
        "title": "Delete Test Workout",
        "date": "2026-09-25",
        "duration": 60,
        "notes": "test"
    }).json()

    exercise = client.post("/exercises/", json={
        "name": "Delete Test Exercise",
        "muscle_group": "Test"
    }).json()

    client.post("/performances/", json={
        "workout_id": workout["id"],
        "exercise_id": exercise["id"],
        "sets": 3,
        "reps": 10,
        "weight": 50
    })

    response = client.delete(f"/workouts/{workout['id']}")

    assert response.status_code == 200

    client.delete(f"/exercises/{exercise['id']}")


def test_delete_exercise_with_performance():
    workout = client.post("/workouts/", json={
        "title": "Exercise Delete Test",
        "date": "2026-09-25",
        "duration": 45,
        "notes": "test"
    }).json()

    exercise = client.post("/exercises/", json={
        "name": "Exercise To Delete",
        "muscle_group": "Test"
    }).json()

    client.post("/performances/", json={
        "workout_id": workout["id"],
        "exercise_id": exercise["id"],
        "sets": 2,
        "reps": 8,
        "weight": 40
    })

    response = client.delete(f"/exercises/{exercise['id']}")

    assert response.status_code == 200

    client.delete(f"/workouts/{workout['id']}")


def test_empty_workout_title():
    response = client.post("/workouts/", json={
        "title": "",
        "date": "2026-09-25",
        "duration": 60,
        "notes": "test"
    })

    assert response.status_code == 422


def test_invalid_workout_date():
    response = client.post("/workouts/", json={
        "title": "Test Workout",
        "date": "hello",
        "duration": 60,
        "notes": "test"
    })

    assert response.status_code == 422


def test_empty_exercise_name():
    response = client.post("/exercises/", json={
        "name": "",
        "muscle_group": "Test"
    })

    assert response.status_code == 422
