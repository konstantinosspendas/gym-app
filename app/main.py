from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import workouts, exercises, performances, stats


Base.metadata.create_all(bind=engine)

app = FastAPI(title="GymLogger Lite")

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(performances.router)
app.include_router(stats.router)


@app.get("/")
def home():
    return {"message": "GymLogger Lite API"}

