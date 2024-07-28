from datetime import datetime, timedelta

from fastapi.encoders import jsonable_encoder
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.user.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = jsonable_encoder((datetime.now() + timedelta(minutes=30)).timestamp())
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserRepository.find_one_or_none(email=email)
    if not user and not verify_password(password, user.hashed_password):
        return None

    return user
