from fastapi import FastAPI
from app.routers import note, auth

app = FastAPI(title="My Notes",
              summary="Добавление и просмотр заметок")

@app.get('/')
async def hello():
    return ('Go to SWAGGER ---->')

app.include_router(note.router)
app.include_router(auth.router)

# uvicorn app.main:app --reload