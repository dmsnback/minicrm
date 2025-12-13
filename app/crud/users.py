import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.clients import Client
from app.users.models import User

logger = logging.getLogger(__name__)


class CRUDUser:
    async def get_user_by_id(swlf, session: AsyncSession, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().all()
        return user

    async def get_all_users(self, session: AsyncSession):
        try:
            query = select(User).options(selectinload(User.clients))
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info('Получен список пользователей')
            return users
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении списка пользователей: {e}")
            raise

    async def get_all_user_clients(self, session: AsyncSession, user_id):
        try:
            query = select(Client).where(Client.manager_id == user_id).options(selectinload(Client.manager))
            result = await session.execute(query)
            clients = result.scalars().all()
            logger.info("Получен список клиентов менеджера")
            return clients
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении списка клиентов менеджера: {e}")
            raise
