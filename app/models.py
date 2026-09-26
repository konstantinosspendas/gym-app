from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Workout(Base):
    __tablename__ = "προπονησεις"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    duration = Column(Integer)
    notes = Column(String)

    exercises = relationship("WorkoutExercise", back_populates="workout")


class Exercise(Base):
    __tablename__ = "ασκησεις"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    muscle_group = Column(String)

    workouts = relationship("WorkoutExercise", back_populates="exercise")


class WorkoutExercise(Base):
    __tablename__ = "επιδόσεις"

    id = Column(Integer, primary_key=True, index=True)

    workout_id = Column(
        Integer,
        ForeignKey("προπονησεις.id"),
        nullable=False,
        index=True
    )

    exercise_id = Column(
        Integer,
        ForeignKey("ασκησεις.id"),
        nullable=False,
        index=True
    )

    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float)

    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workouts")
