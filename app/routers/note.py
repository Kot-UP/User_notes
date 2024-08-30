from sqlalchemy import insert, select, update
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from app.routers.auth import get_current_username
from app.backend.db_depends import get_db
from app.models import *
from app.schemas.note import CreateNote
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from pyaspeller import YandexSpeller
import pyaspeller


router = APIRouter(prefix="/notes", tags=["notes"])
speller = pyaspeller.YandexSpeller(lang="ru")


"""
    Получение всех заметок пользователя
"""


@router.get("/all_notes")
async def all_notes(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_username)],
):

    if get_user:
        notes = await db.scalars(
            select(Note).where(Note.user_note == get_user.username)
        )
        if notes is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no notes"
            )
        return notes.all()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )


"""
    Добавление заметки
"""


@router.post("/create")
async def create_note(
    db: Annotated[AsyncSession, Depends(get_db)],
    create_note: CreateNote,
    get_user: Annotated[dict, Depends(get_current_username)],
):

    if get_user:
        try:
            result = speller.spell(create_note.note)
            if len(list(result)) != 0:
                return {"error": "Орфографическая ошибка"}

            await db.execute(
                insert(Note).values(user_note=get_user.username, note=create_note.note)
            )
            await db.commit()
            return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
        except Exception:
            return {"error": "Что то не так!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to use this method",
        )
