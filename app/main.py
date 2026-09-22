from fastapi import FastAPI

from app.routers import workouts, exercises, performances


app = FastAPI(title="GymLogger Lite")

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(performances.router)


@app.get("/")
def home():
    return {"message": "GymLogger Lite API"}

