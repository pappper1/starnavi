from fastapi import APIRouter, Depends, Response

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.user.auth import authenticate_user, create_access_token, get_password_hash
from app.user.dependencies import get_current_user
from app.user.models import User
from app.user.repository import UserRepository
from app.user.schemas import SUser, SUserAuth, SUserUpdate

router = APIRouter(
    prefix="/user",
    tags=["Auth & Users"],
)


@router.post("/signup")
async def register_user(user_data: SUserAuth) -> dict:
    existing_user = await UserRepository.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UserRepository.add(email=user_data.email, hashed_password=hashed_password)

    return {"message": "User created successfully"}


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    user = await authenticate_user(user_data.email, user_data.password)
    print(user)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_user(current_user: User = Depends(get_current_user)) -> SUser:
    user = await UserRepository.find_one_or_none(id=current_user.id)
    if not user:
        raise UserNotFoundException

    return user


@router.put("/update")
async def update_user(
    user_data: SUserUpdate, user: User = Depends(get_current_user)
) -> SUser:
    updated_user = await UserRepository.update(
        user.id, **user_data.dict(exclude_unset=True)
    )

    return updated_user
