from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.exercise import Exercise
    from backend.models.workout import Workout


class WorkoutSet(Base):
    __tablename__ = "workout_sets"

    __table_args__ = (
        CheckConstraint(
            "weight_kg >= 0", name="ck_set_weight"
        ),
        CheckConstraint(
            "reps > 0", name="ck_set_reps"
        ),
        CheckConstraint(
            "rir >= 0 AND rir <= 10", name="ck_set_rir"
        ),
        CheckConstraint(
            "set_number > 0", name="ck_set_number"
        ),
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            "set_number",
            name="uq_workout_exercise_set",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    workout_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("exercises.id"),
        nullable=False,
        index=True,
    )
    set_number: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    weight_kg: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    reps: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    rir: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    workout: Mapped[Workout] = relationship(
        back_populates="sets"
    )
    exercise: Mapped[Exercise] = relationship(
        back_populates="workout_sets"
    )
