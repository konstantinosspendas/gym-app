from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/exercises",
    tags=["Exercises"]
)


@router.get("/")
def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(models.Exercise).all()
    return exercises


@router.get("/{exercise_id}")
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    return exercise


@router.post("/")
def create_exercise(
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db)
):
    new_exercise = models.Exercise(
        name=exercise.name,
        muscle_group=exercise.muscle_group
    )

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise


@router.put("/{exercise_id}")
def update_exercise(
    exercise_id: int,
    exercise_data: schemas.ExerciseCreate,
    db: Session = Depends(get_db)
):
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    exercise.name = exercise_data.name
    exercise.muscle_group = exercise_data.muscle_group

    db.commit()
    db.refresh(exercise)

    return exercise


@router.delete("/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db)
):
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found"
        )

    db.delete(exercise)
    db.commit()

    return {"message": "Exercise deleted"}

