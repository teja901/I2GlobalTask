from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings 

client = None
db = None

users_coll = None
notes_coll = None


async def connect_to_mongo():
    global client, db, users_coll, notes_coll
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    users_coll = db["users"]
    notes_coll = db["notes"]

   
    await users_coll.create_index("user_email", unique=True)
    await notes_coll.create_index("note_id", unique=True)
    await notes_coll.create_index("user_id")

    print("Connected to MongoDB Atlas")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    """Return the database instance."""
    global db
    if db is None:
        raise Exception("Database not initialized. Did you forget startup event?")
    return db
