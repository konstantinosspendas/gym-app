from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.routers.stats import clear_stats_cache

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/")
def get_exercises(db: Session = Depends(get_db)):
    return db.query(models.Exercise).all()


@router.get("/{exercise_id}")
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

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
    clear_stats_cache()
    db.refresh(new_exercise)

    return new_exercise


@router.put("/{exercise_id}")
def update_exercise(
    exercise_id: int,
    exercise: schemas.ExerciseCreate,
    db: Session = Depends(get_db)
):
    existing_exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if existing_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    existing_exercise.name = exercise.name
    existing_exercise.muscle_group = exercise.muscle_group

    db.commit()
    clear_stats_cache()
    db.refresh(existing_exercise)

    return existing_exercise


@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(
        models.Exercise.id == exercise_id
    ).first()

    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    db.query(models.WorkoutExercise).filter(
        models.WorkoutExercise.exercise_id == exercise_id
    ).delete()

    db.delete(exercise)
    db.commit()
    clear_stats_cache()

    return {"message": "Exercise deleted"}
