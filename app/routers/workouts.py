from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.get("/")
def get_workouts(db: Session = Depends(get_db)):
    workouts = db.query(models.Workout).all()
    return workouts


@router.get("/{workout_id}")
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

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
    db.refresh(new_workout)

    return new_workout


@router.put("/{workout_id}")
def update_workout(
    workout_id: int,
    workout_data: schemas.WorkoutCreate,
    db: Session = Depends(get_db)
):
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    workout.title = workout_data.title
    workout.date = workout_data.date
    workout.duration = workout_data.duration
    workout.notes = workout_data.notes

    db.commit()
    db.refresh(workout)

    return workout


@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db)
):
    workout = db.query(models.Workout).filter(
        models.Workout.id == workout_id
    ).first()

    if workout is None:
        raise HTTPException(
            status_code=404,
            detail="Workout not found"
        )

    db.delete(workout)
    db.commit()

    return {"message": "Workout deleted"}
