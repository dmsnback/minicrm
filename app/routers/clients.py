from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.clients import CRUDClient
from app.schemas.clients import ClientCreateSchema, ClientReadSchema, ClientUpdateSchema
from app.users.manager import current_superuser, current_user
from app.users.models import User

client_router = APIRouter(
    prefix="/clients",
    tags=[
        "Клиенты",
    ],
)
crud_client = CRUDClient()


@client_router.get(
    "/all",
    response_model=list[ClientReadSchema],
    summary="Получение списка всех клиентов",
    description="Администратор видит всех клиентов, менеджер только своих",
)
async def get_all_clients(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(current_user),
) -> list[ClientReadSchema]:
    clients = await crud_client.get_all_clients(session, current_user)
    return clients


@client_router.get(
    "/{client_id}", response_model=ClientReadSchema, summary="Получение клиента по id"
)
async def get_client(
    client_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(current_user),
) -> ClientReadSchema:
    client = await crud_client.get_client(client_id, session, current_user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    return client


@client_router.post(
    "",
    response_model=ClientReadSchema,
    dependencies=[Depends(current_user)],
    summary="Добавление клиента",
)
async def create_client(
    data: ClientCreateSchema,
    session: AsyncSession = Depends(get_session),
) -> ClientReadSchema:
    try:
        client = await crud_client.create_client(data, session)
        return client
    except Exception as e:
        raise e


@client_router.patch(
    "/{client_id}",
    response_model=ClientReadSchema,
    summary="Обновление клиента",
    description="Передавайте только те поля, которые нужно изменить",
)
async def update_client(
    client_id: int,
    data: ClientUpdateSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> ClientReadSchema:
    client = await crud_client.get_client(client_id, session, user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    try:
        upd_client = await crud_client.update_client(client, data, session)
        return upd_client
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при изменении клиента"
        )


@client_router.delete(
    "/{client_id}",
    summary="Удаление клиента",
    description="Доступно только администратору",
)
async def delete_client(
    client_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_superuser),
) -> dict:
    client = await crud_client.get_client(client_id, session, user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    try:
        await crud_client.delete_client(client, session)
        return {"detail": "Клиент удалён"}
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении клиента"
        )
