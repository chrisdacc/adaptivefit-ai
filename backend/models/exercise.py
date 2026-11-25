from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db.base import Base

if TYPE_CHECKING:
    from backend.models.workout_set import WorkoutSet


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )
    muscle_group: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    equipment: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    workout_sets: Mapped[list[WorkoutSet]] = relationship(
        back_populates="exercise"
    )
