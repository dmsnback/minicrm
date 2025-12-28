from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.users import CRUDUser
from app.schemas.clients import ClientReadSchema
from app.users.manager import auth_backend, current_superuser, fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate

user_router = APIRouter(
    tags=["Пользователи"],
)

crud = CRUDUser()


@user_router.get(
    "/users/all",
    response_model=list[UserRead],
    dependencies=[Depends(current_superuser)],
    summary="Получение списка всех пользователей",
    description="Доступно только администтратору",
)
async def get_all_users(session: AsyncSession = Depends(get_session)) -> list[UserRead]:
    users = await crud.get_all_users(session)
    return users


@user_router.get(
    "/users/{user_id}/clients",
    response_model=list[ClientReadSchema],
    dependencies=[Depends(current_superuser)],
    summary="Получение списка клиентов у конкретного пользователя",
    description="Доступно только Администратору",
)
async def get_all_user_clients(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> list[ClientReadSchema]:
    user = await crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    clients = await crud.get_all_user_clients(session, user_id)
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="У менеджера нет клиентов"
        )
    return clients


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
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users"
)
