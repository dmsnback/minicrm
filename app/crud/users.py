import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User

logger = logging.getLogger(__name__)


class CRUDUser:
    try:
        async def get_all_users(self, session: AsyncSession):
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            logger.info('Получен список пользователей')
            return users
    except SQLAlchemyError as e:
        logger.error(f"Ошибка приполучении списка пользователей: {e}")
        raise
