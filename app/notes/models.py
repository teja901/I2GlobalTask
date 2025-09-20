from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    note_title: str = Field(..., min_length=1, max_length=200)
    note_content: Optional[str] = ""

class NoteUpdate(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]


class NoteInDB(BaseModel):
    note_id: str
    user_id: str
    note_title: str
    note_content: Optional[str]
    created_on: datetime
    last_update: datetime
