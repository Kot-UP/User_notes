from fastapi import FastAPI
from app.routers import note, auth

app = FastAPI()

app.include_router(note.router)
app.include_router(auth.router)

# uvicorn app.main:app --reload