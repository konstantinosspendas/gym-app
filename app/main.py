from fastapi import FastAPI

from app.routers import workouts


app = FastAPI(title="GymLogger Lite")

app.include_router(workouts.router)


@app.get("/")
def home():
    return {"message": "GymLogger Lite API"}

