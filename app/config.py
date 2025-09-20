import os
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()

# print(os.getenv("MONGO_URI"),"jjjjjjjjjjj")

class Settings(BaseSettings):
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "notesdb")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_MINUTES: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))  


settings = Settings()

