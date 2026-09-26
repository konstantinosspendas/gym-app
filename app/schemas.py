from pydantic import BaseModel, Field


class WorkoutCreate(BaseModel):
    title: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    duration: int | None = Field(default=None, gt=0)
    notes: str | None = None


class ExerciseCreate(BaseModel):
    name: str = Field(min_length=1)
    muscle_group: str | None = None


class PerformanceCreate(BaseModel):
    workout_id: int
    exercise_id: int
    sets: int = Field(gt=0)
    reps: int = Field(gt=0)
    weight: float | None = Field(default=None, ge=0)
