from pydantic import BaseModel


class WorkoutCreate(BaseModel):
    title: str
    date: str
    duration: int | None = None
    notes: str | None = None


class ExerciseCreate(BaseModel):
    name: str
    muscle_group: str | None = None


class PerformanceCreate(BaseModel):
    workout_id: int
    exercise_id: int
    sets: int
    reps: int
    weight: float | None = None
