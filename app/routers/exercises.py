from fastapi import APIRouter, Depends
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
