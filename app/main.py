from fastapi import FastAPI

from app.routers import workouts, exercises, performances, stats


app = FastAPI(title="GymLogger Lite")

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(performances.router)
app.include_router(stats.router)


@app.get("/")
def home():
    return {"message": "GymLogger Lite API"}

