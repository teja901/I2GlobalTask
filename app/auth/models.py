from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=100)
    user_email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    user_email: EmailStr
    password: str = Field(..., min_length=6)

class UserPublic(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    created_on: datetime
    last_update: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
