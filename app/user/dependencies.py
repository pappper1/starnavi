from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    ExpiredTokenException,
    IncorrectTokenFormatException,
    TokenAbsentException,
    UserIsNotPresentException,
)
from app.user.repository import UserRepository


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("expire")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise ExpiredTokenException

    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException

    user = await UserRepository.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
