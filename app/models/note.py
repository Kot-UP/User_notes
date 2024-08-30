from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.user import User
from app.backend.db import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_note = Column(String, ForeignKey("users.username"))
    note = Column(String)