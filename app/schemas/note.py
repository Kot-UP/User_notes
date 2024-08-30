from pydantic import BaseModel


class CreateNote(BaseModel):
    note: str
