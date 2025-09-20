from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
import uuid

from app.notes.models import NoteCreate, NoteUpdate, NoteInDB
from app.auth.routes import get_current_user
from app.auth.models import UserPublic
from app.db import connection  

router = APIRouter()


def get_notes_coll():
    if connection.notes_coll is None:
        raise Exception("MongoDB not initialized")
    return connection.notes_coll



@router.post("/", response_model=NoteInDB)
async def create_note(note: NoteCreate, current_user: UserPublic = Depends(get_current_user)):
    notes_coll = get_notes_coll()
    
    note_id = str(uuid.uuid4())
    now = datetime.utcnow()
    doc = {
        "note_id": note_id,
        "user_id": current_user.user_id,
        "note_title": note.note_title,
        "note_content": note.note_content,
        "created_on": now,
        "last_update": now,
    }
    await notes_coll.insert_one(doc)
    return NoteInDB(**doc)



@router.get("/", response_model=List[NoteInDB])
async def list_notes(current_user: UserPublic = Depends(get_current_user)):
    notes_coll = get_notes_coll()
    cursor = notes_coll.find({"user_id": current_user.user_id}).sort("last_update", -1)
    notes = []
    async for doc in cursor:
        notes.append(NoteInDB(**doc))
    return notes



@router.get("/{note_id}", response_model=NoteInDB)
async def get_note(note_id: str, current_user: UserPublic = Depends(get_current_user)):
    notes_coll = get_notes_coll()
    doc = await notes_coll.find_one({"note_id": note_id, "user_id": current_user.user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteInDB(**doc)


@router.put("/{note_id}", response_model=NoteInDB)
async def update_note(note_id: str, data: NoteUpdate, current_user: UserPublic = Depends(get_current_user)):
    notes_coll = get_notes_coll()
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="Nothing to update")
    update_data["last_update"] = datetime.utcnow()

    await notes_coll.update_one(
        {"note_id": note_id, "user_id": current_user.user_id},
        {"$set": update_data}
    )

    updated = await notes_coll.find_one({"note_id": note_id, "user_id": current_user.user_id})
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteInDB(**updated)



@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: str, current_user: UserPublic = Depends(get_current_user)):
    notes_coll = get_notes_coll()
    result = await notes_coll.delete_one({"note_id": note_id, "user_id": current_user.user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
