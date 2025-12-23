import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.comments import Comment
from app.models.deals import Deal
from app.schemas.deals import DealCreateSchema, DealUpdateSchema
from app.users.models import User

logger = logging.getLogger(__name__)


class CRUDDeal:

    async def get_all_deals(self, session: AsyncSession, user: User):
        try:
            query = select(Deal).options(
                selectinload(Deal.manager), selectinload(Deal.comments)
            )
            if user.role == "manager":
                query = query.where(Deal.manager_id == user.id)
            result = await session.execute(query)
            deals = result.scalars().all()
            logger.info("Получен список сделок")
            return deals
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении списка сделок: {e}")
            raise

    async def get_deal(self, deal_id: int, session: AsyncSession, user: User):
        try:
            query = (
                select(Deal)
                .where(Deal.id == deal_id)
                .options(
                    selectinload(Deal.manager),
                    selectinload(Deal.client),
                    selectinload(Deal.comments).selectinload(Comment.author),
                )
            )
            if user.role == "manager":
                query = query.where(Deal.manager_id == user.id)
            result = await session.execute(query)
            deal = result.scalars().first()
            if deal:
                logger.info(f"Получена сделка id = {deal_id}")
            else:
                logger.warning(f"Сделка id = {deal_id} не найдена")
            return deal
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении сделки: {e}")
            raise

    async def create_deal(self, data: DealCreateSchema, session: AsyncSession):
        try:
            new_deal = Deal(**data.model_dump())
            session.add(new_deal)
            await session.flush()
            await session.commit()
            await session.refresh(
                new_deal,
                attribute_names=[
                    "manager",
                    "client",
                    "comment",
                ],
            )
            logger.info(f"Создана сделка {new_deal.name} id={new_deal.id}")
            return new_deal
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании сделки: {e}")
            raise

    async def update_deal(
        self, deal: Deal, data: DealUpdateSchema, session: AsyncSession
    ):
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(deal, key, value)

            session.add(deal)
            await session.commit()
            await session.refresh(deal)
            logger.info(f"Сделка id={deal.id} изменена")
            return deal
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при изменении сделки id={deal.id}: {e}")
            raise

    async def delete_deal(self, deal: Deal, session: AsyncSession):
        try:
            await session.delete(deal)
            await session.commit()
            logger.info(f"Сделка {deal.name} id = {deal.id} удалена")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении сделки id={deal.id}: {e}")
            raise
