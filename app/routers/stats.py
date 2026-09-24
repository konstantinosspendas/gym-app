from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models


router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    workouts = db.query(models.Workout).count()
    exercises = db.query(models.Exercise).count()

    performances = db.query(models.WorkoutExercise).all()

    total_volume = 0

    for performance in performances:
        if performance.weight is not None:
            total_volume += (
                performance.sets
                * performance.reps
                * performance.weight
            )

    return {
        "total_workouts": workouts,
        "total_exercises": exercises,
        "total_performances": len(performances),
        "total_volume": total_volume
    }

