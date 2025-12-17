from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.deals import CRUDDeal
from app.schemas.deals import DealCreateSchema, DealReadSchema, DealUpdateSchema
from app.users.manager import current_superuser, current_user
from app.users.models import User

deal_router = APIRouter(
    prefix="/deals",
    tags=[
        "Сделки",
    ],
)

crud_deal = CRUDDeal()


@deal_router.get(
    "/all",
    response_model=list[DealReadSchema],
    summary="Получение списка всех сдеелок",
    description="Администратор видит все сделки, менеджер только свои",
)
async def get_all_deals(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(current_user),
) -> list[DealReadSchema]:
    deals = await crud_deal.get_all_deals(session, current_user)
    return deals


@deal_router.get(
    "/{deal_id}",
    dependencies=[Depends(current_user)],
    response_model=DealReadSchema,
    summary="Получение сделки по id",
)
async def get_deal(
    deal_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> DealReadSchema:
    try:
        deal = await crud_deal.get_deal(deal_id, session, user)
        if not deal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Сделка не найдена"
            )
        return deal
    except Exception as e:
        raise e


@deal_router.post(
    "",
    response_model=DealReadSchema,
    dependencies=[Depends(current_user)],
    summary="Добавление сделки",
)
async def create_deal(
    data: DealCreateSchema, session: AsyncSession = Depends(get_session)
) -> DealReadSchema:
    try:
        deal = await crud_deal.create_deal(data, session)
        return deal
    except Exception as e:
        raise e


@deal_router.patch(
    "/{deal_id}",
    response_model=DealReadSchema,
    dependencies=[Depends(current_user)],
    summary="Обновление сделки",
    description="Передавайте только те поля, которые нужно изменить",
)
async def update_deal(
    deal_id: int,
    data: DealUpdateSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> DealReadSchema:
    deal = await crud_deal.get_deal(deal_id, session, user)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Сдедка не найдена"
        )
    try:
        upd_deal = await crud_deal.update_deal(deal, data, session)
        return upd_deal
    except Exception as e:
        return e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при изменении сделки",
        )


@deal_router.delete(
    "/{deal_id}", summary="Удаление сделки", description="Доступно только администратору"
)
async def delete_deal(
    deal_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_superuser),
) -> dict:
    deal = await crud_deal.get_deal(deal_id, session, user)
    if not deal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Сдедка не найдена"
        )
    try:
        await crud_deal.delete_deal(deal, session)
        return {"detail": "Сделка удалена"}
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении сделки"
        )
