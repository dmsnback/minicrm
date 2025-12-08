from typing import Annotated

from fastapi import APIRouter, Depends

from app.users.manager import auth_backend, fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate

user_router = APIRouter(
    tags=["Пользователи"],
)

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, Annotated[UserCreate, Depends()]),
    prefix="/auth",
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, Annotated[UserUpdate, Depends()]),
    prefix="/users",
)
