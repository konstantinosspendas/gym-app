from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)


@router.get("/")
def get_workouts(db: Session = Depends(get_db)):
    workouts = db.query(models.Workout).all()
    return workouts
