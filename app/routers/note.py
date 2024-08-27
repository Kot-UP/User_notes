from sqlalchemy import insert, select, update
from fastapi import APIRouter, Depends, status
from typing import Annotated
#from sqlalchemy.orm import Session
from app.routers.auth import get_current_user
from app.backend.db_depends import get_db
from app.models import *
from app.schemas.note import CreateNote
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get('/all_notes')
async def all_notes(db: Annotated[AsyncSession, Depends(get_db)]):
    notes = await db.scalars(select(Note).where(Note.user_note))

    if notes is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no notes"
        )
    return notes.all()


@router.post('/create')
async def create_note(db: Annotated[AsyncSession, Depends(get_db)], create_note: CreateNote,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get_user:
        await db.execute(insert(Note).values(user_note=create_note.user_note))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not authorized to use this method'
        )