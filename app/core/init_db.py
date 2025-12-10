import contextlib
import logging
from typing import Literal

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.database import get_session
from app.users.manager import get_user_manager
from app.users.schemas import UserCreate
from app.users.utils import get_user_db

logger = logging.getLogger(__name__)

get_session_context = contextlib.asynccontextmanager(get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    username: str,
    email: EmailStr,
    password: str,
    is_superuser: bool = False,
    role: Literal["admin", "user"] = "user",
):
    try:
        async with get_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    try:
                        await user_manager.create(
                            UserCreate(
                                username=username,
                                email=email,
                                password=password,
                                is_superuser=is_superuser,
                                role=role,
                            )
                        )
                        logger.info(f"Пользователь {username} создан")
                    except UserAlreadyExists:
                        logger.warning(f"Пользователь {username} уже сужествует")
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя {username}: {e}")


async def create_first_superuser() -> None:
    """Создание первого суперпользователя при запуске приложения"""
    first_superuser_data = {
        "username": settings.first_superuser_username,
        "email": settings.first_superuser_email,
        "password": settings.first_superuser_password,
        "role": settings.first_superuser_role,
    }
    if (
        settings.first_superuser_username is not None
        and settings.first_superuser_email is not None
        and settings.first_superuser_password is not None
        and settings.first_superuser_role is not None
    ):
        try:
            await create_user(
                username=settings.first_superuser_username,
                email=settings.first_superuser_email,
                password=settings.first_superuser_password,
                is_superuser=True,
                role=settings.first_superuser_role,
            )
            logger.info("Первый суперюзер создан или уже существует")
        except Exception as e:
            logger.error(f"Ошибка при создании первого суперюзера: {e}")
    else:
        missing_value = [k for k, v in first_superuser_data.items() if not v]
        logger.warning(
            f'Невозможно создать первого суперпользователя, отсутствуют данные: {", ".join(missing_value)}'
        )
