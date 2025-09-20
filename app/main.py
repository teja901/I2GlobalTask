from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.connection import connect_to_mongo, close_mongo_connection, get_database

from app.auth.routes import router as auth_router

from app.notes.routes import router as notes_router

app = FastAPI(title="FastApi Crud Operations with MongoDB")

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

@app.get("/test-db")
async def test_db():
    db = get_database()
    collections = await db.list_collection_names()
    return {"status": "connected", "collections": collections}
