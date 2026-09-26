import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/stats", tags=["Stats"])

stats_cache = {"data": None, "time": 0}
CACHE_TIME = 30


def clear_stats_cache():
    stats_cache["data"] = None
    stats_cache["time"] = 0


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    current_time = time.time()

    if (
        stats_cache["data"] is not None
        and current_time - stats_cache["time"] < CACHE_TIME
    ):
        return stats_cache["data"]

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

    result = {
        "total_workouts": workouts,
        "total_exercises": exercises,
        "total_performances": len(performances),
        "total_volume": total_volume
    }

    stats_cache["data"] = result
    stats_cache["time"] = current_time

    return result
