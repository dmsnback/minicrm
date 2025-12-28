import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.clients import Client
from app.schemas.clients import ClientCreateSchema, ClientUpdateSchema
from app.users.models import User
from app.validators.clients import (
    validate_unique_email_client,
    validate_unique_full_name_client,
    validate_unique_phone_client,
)

logger = logging.getLogger(__name__)


class CRUDClient:

    async def get_all_clients(self, session: AsyncSession, user: User):
        try:
            query = select(Client).options(selectinload(Client.manager))
            if user.role == "manager":
                query = query.where(Client.manager_id == user.id)
            result = await session.execute(query)
            clients = result.scalars().all()
            logger.info("Получен список клиентов")
            return clients
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении списка клиентов: {e}")
            raise

    async def get_client(self, client_id: int, session: AsyncSession, user: User):
        try:
            query = (
                select(Client)
                .where(Client.id == client_id)
                .options(selectinload(Client.manager))
            )
            if user.role == "manager":
                query = query.where(Client.manager_id == user.id)
            result = await session.execute(query)
            client = result.scalars().first()
            if client:
                logger.info(f"Получен клиент id = {client_id}")
            else:
                logger.warning(f"Клиеент id = {client_id} не найден")
            return client
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении клиента: {e}")
            raise

    async def create_client(self, data: ClientCreateSchema, session: AsyncSession):
        try:
            if data.email:
                await validate_unique_email_client(session, data.email)
            if data.phone:
                await validate_unique_phone_client(session, data.phone)
            if data.full_name:
                await validate_unique_full_name_client(session, data.full_name)
            new_client = Client(**data.model_dump())
            session.add(new_client)
            await session.flush()
            await session.commit()
            await session.refresh(new_client, attribute_names=["manager"])
            logger.info(f"Создан клиент {new_client.full_name} id={new_client.id}")
            return new_client
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании клиента: {e}")
            raise

    async def update_client(
        self,
        client: Client,
        data: ClientUpdateSchema,
        session: AsyncSession,
    ):
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(client, key, value)

            session.add(client)
            await session.commit()
            await session.refresh(client)
            logger.info(f"Изменён клиент id={client.id}")
            return client
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при изменении клиента id={client.id}: {e}")
            raise

    async def delete_client(self, client: Client, session: AsyncSession):
        try:
            await session.delete(client)
            await session.commit()
            logger.info(f"Клиент {client.full_name} id = {client.id} удален")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении клиента id={client.id}: {e}")
            raise
