from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.routers.stats import clear_stats_cache

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/")
def get_workouts(db: Session = Depends(get_db)):
    return db.query(models.Workout).all()


@router.get("/{workout_id}")
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.post("/")
def create_workout(
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db)
):
    new_workout = models.Workout(
        title=workout.title,
        date=workout.date,
        duration=workout.duration,
        notes=workout.notes
    )

    db.add(new_workout)
    db.commit()
    clear_stats_cache()
    db.refresh(new_workout)

    return new_workout


@router.put("/{workout_id}")
def update_workout(
    workout_id: int,
    workout: schemas.WorkoutCreate,
    db: Session = Depends(get_db)
):
    existing_workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if existing_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    existing_workout.title = workout.title
    existing_workout.date = workout.date
    existing_workout.duration = workout.duration
    existing_workout.notes = workout.notes

    db.commit()
    clear_stats_cache()
    db.refresh(existing_workout)

    return existing_workout


@router.delete("/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")

    db.query(models.WorkoutExercise).filter(
        models.WorkoutExercise.workout_id == workout_id
    ).delete()

    db.delete(workout)
    db.commit()
    clear_stats_cache()

    return {"message": "Workout deleted"}
