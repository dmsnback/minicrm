from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.users import CRUDUser
from app.users.manager import auth_backend, fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate
from app.users.manager import current_superuser


user_router = APIRouter(
    tags=["Пользователи"],
)

crud = CRUDUser()


@user_router.get('/users/all')
async def get_all_users(session: AsyncSession = Depends(get_session), ) -> list[UserRead]:
    users = await crud.get_all_users(session)
    return users

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    dependencies=[Depends(current_superuser)],
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users"
)
