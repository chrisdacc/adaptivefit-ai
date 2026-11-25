import pytest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from backend.db.base import Base
from backend.models import User, Exercise, Workout


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()


@pytest.fixture
def user(db):
    user = User(
        name="Test Athlete",
        email="athlete@example.com",
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def exercise(db):
    exercise = Exercise(
        name="Bench Press",
        muscle_group="Chest",
        equipment="Barbell",
    )
    db.add(exercise)
    db.commit()
    return exercise


@pytest.fixture
def workout(db, user):
    workout = Workout(user=user)
    db.add(workout)
    db.commit()
    return workout
