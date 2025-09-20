from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import uuid

from app.auth.models import UserCreate, LoginRequest, UserPublic, TokenResponse
from app.auth.utils import hash_password, verify_password, create_access_token, decode_access_token
from app.db.connection import get_database 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()


async def get_user_by_email(email: str):
    db = get_database()
    return await db["users"].find_one({"user_email": email})

async def get_user_by_id(user_id: str):
    db = get_database()
    return await db["users"].find_one({"user_id": user_id})

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    user_id = decode_access_token(token)
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return UserPublic(
        user_id=user["user_id"],
        user_name=user["user_name"],
        user_email=user["user_email"],
        created_on=user["created_on"],
        last_update=user["last_update"],
    )


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate):
    if await get_user_by_email(data.user_email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    now = datetime.utcnow()
    hashed_pw = hash_password(data.password)

    doc = {
        "user_id": user_id,
        "user_name": data.user_name,
        "user_email": data.user_email,
        "hashed_password": hashed_pw,
        "created_on": now,
        "last_update": now,
    }
    db = get_database()
    await db["users"].insert_one(doc)
    return UserPublic(**doc)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest = Body(...)):
    user = await get_user_by_email(data.user_email)
    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(user["user_id"])
    return TokenResponse(access_token=token, expires_in=3600)


@router.get("/me", response_model=UserPublic)
async def me(current_user: UserPublic = Depends(get_current_user)):
    return current_user
