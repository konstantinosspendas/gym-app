from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.routers.stats import clear_stats_cache

router = APIRouter(prefix="/performances", tags=["Performances"])


@router.get("/")
def get_performances(db: Session = Depends(get_db)):
    return db.query(models.WorkoutExercise).all()


@router.post("/")
def create_performance(
    performance: schemas.PerformanceCreate,
    db: Session = Depends(get_db)
):
    workout = db.query(models.Workout).filter(
        models.Workout.id == performance.workout_id
    ).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == performance.exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    new_performance = models.WorkoutExercise(
        workout_id=performance.workout_id,
        exercise_id=performance.exercise_id,
        sets=performance.sets,
        reps=performance.reps,
        weight=performance.weight
    )

    db.add(new_performance)
    db.commit()
    clear_stats_cache()
    db.refresh(new_performance)

    return new_performance
