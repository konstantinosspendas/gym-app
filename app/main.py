from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database import Base, engine
from app import models
from app.routers import workouts, exercises, performances, stats


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Καταγραφή Προπονήσεων")

app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(performances.router)
app.include_router(stats.router)


@app.get("/")
def home():
    return FileResponse("static/index.html")

