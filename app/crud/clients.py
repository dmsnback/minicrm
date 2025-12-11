import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.clients import Client
from app.schemas.clients import ClientCreateSchema, ClientUpdateSchema


logger = logging.getLogger(__name__)


class CRUDClient:
    async def get_all_clients(self, session: AsyncSession):
        try:
            query = select(Client)
            result = await session.execute(query)
            clients = result.scalars().all()
            logger.info('Получен список клиентов')
            return clients
        except SQLAlchemyError as e:
            logger.error(f'Ошибка приполучении списка клиентов: {e}')
            raise

    async def get_client(self, client_id: int, session: AsyncSession):
        try:
            query = select(Client).where(Client.id == client_id)
            result = await session.execute(query)
            client = result.scalars().first()
            if client:
                logger.info(f'Получен клиент id = {client_id}')
            else:
                logger.warning(f'Клиеент id = {client_id} не найден')
            return client
        except SQLAlchemyError as e:
            logger.error(f'Ошибка приполучении клиента: {e}')
            raise

    async def create_client(self, data: ClientCreateSchema, session: AsyncSession):
        try:
            new_client = Client(**data.model_dump())
            session.add(new_client)
            await session.flush()
            await session.commit()
            logger.info(f'Создан клиент {new_client.full_name} id={new_client.id}')
            return new_client
        except SQLAlchemyError as e:
            logger.error(f'Ошибка при создании клиента: {e}')
            raise

    async def update_client(self, client: Client, data: ClientUpdateSchema, session: AsyncSession):
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(client, key, value)

            session.add(client)
            await session.commit()
            await session.refresh(client)
            logger.info(f'Изменён клиент id={client.id}')
            return client
        except SQLAlchemyError as e:
            logger.error(f'Ошибка при изменении клиента id={client.id}: {e}')
            raise

    async def delete_client(self, client: Client, session: AsyncSession):
        try:
            await session.delete(client)
            await session.commit()
            logger.info(f'Клиент {client.full_name} id = {client.id} удален')
        except SQLAlchemyError as e:
            logger.error(f'Ошибка при удалении клиента id={client.id}: {e}')
            raise
