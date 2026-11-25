import pytest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.models import User, WorkoutSet


def test_create_user(db, user):
    saved_user = db.get(User, user.id)

    assert saved_user is not None
    assert saved_user.name == "Test Athlete"
    assert saved_user.email == "athlete@example.com"


def test_duplicate_email_is_rejected(db, user):
    duplicate = User(
        name="Another Athlete",
        email=user.email,
    )

    db.add(duplicate)

    with pytest.raises(IntegrityError):
        db.commit()

    db.rollback()


def test_workout_belongs_to_user(user, workout):
    assert workout.user_id == user.id
    assert workout in user.workouts


@pytest.mark.parametrize(
    "weight_kg,reps,rir",
    [
        (-10, 10, 2),
        (80, 0, 2),
        (80, 10, -1),
        (80, 10, 11),
    ],
)
def test_invalid_workout_set_is_rejected(
    db, workout, exercise, weight_kg, reps, rir
):
    workout_set = WorkoutSet(
        workout=workout,
        exercise=exercise,
        set_number=1,
        weight_kg=weight_kg,
        reps=reps,
        rir=rir,
    )

    db.add(workout_set)

    with pytest.raises(IntegrityError):
        db.commit()

    db.rollback()


def test_duplicate_set_is_rejected(
    db, workout, exercise
):
    for _ in range(2):
        db.add(
            WorkoutSet(
                workout=workout,
                exercise=exercise,
                set_number=1,
                weight_kg=80,
                reps=10,
                rir=2,
            )
        )

    with pytest.raises(IntegrityError):
        db.commit()

    db.rollback()


def test_delete_workout_cascades_to_sets(
    db, workout, exercise
):
    workout_set = WorkoutSet(
        workout=workout,
        exercise=exercise,
        set_number=1,
        weight_kg=80,
        reps=10,
        rir=2,
    )

    db.add(workout_set)
    db.commit()

    set_id = workout_set.id

    db.delete(workout)
    db.commit()

    result = db.scalar(
        select(WorkoutSet).where(
            WorkoutSet.id == set_id
        )
    )

    assert result is None
