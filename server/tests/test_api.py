import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import pytest

from app import app
from models import db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Workout Application API is running"
    )


def test_get_workouts(client):
    response = client.get("/workouts")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_exercises(client):
    response = client.get("/exercises")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_missing_workout(client):
    response = client.get("/workouts/999")

    assert response.status_code == 404


def test_missing_exercise(client):
    response = client.get("/exercises/999")

    assert response.status_code == 404