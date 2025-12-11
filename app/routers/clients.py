from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.clients import CRUDClient
from app.schemas.clients import ClientReadSchema, ClientCreateSchema, ClientUpdateSchema


client_router = APIRouter(
    prefix='/clients',
    tags=['Клиенты',]
)
crud = CRUDClient()


@client_router.get('/all')
async def get_all_clients(session: AsyncSession = Depends(get_session)) -> list[ClientReadSchema]:
    clients = await crud.get_all_clients(session)
    return clients


@client_router.get('/{client_id}')
async def get_client(client_id: int, session: AsyncSession = Depends(get_session)) -> ClientReadSchema:
    client = await crud.get_client(client_id, session)
    if not client:
        raise HTTPException(404, 'Клиент не найден')
    return client


@client_router.post('')
async def create_client(
    data: Annotated[ClientCreateSchema, Depends()], session: AsyncSession = Depends(get_session)
) -> ClientCreateSchema:
    try:
        client = await crud.create_client(data, session)
        return client
    except Exception:
        raise HTTPException(500, 'Ошибка при добавлении клиента')


@client_router.patch('/{client_id}')
async def update_client(
    client_id: int, data: Annotated[ClientUpdateSchema, Depends()], session: AsyncSession = Depends(get_session)
) -> ClientReadSchema:
    client = await crud.get_client(client_id, session)
    if not client:
        raise HTTPException(404, 'Клиент не найден')
    try:
        upd_client = await crud.update_client(client, data, session)
        return upd_client
    except Exception:
        raise HTTPException(500, 'Ошибка при изменении клиента')


@client_router.delete('/{client_id}')
async def delete_cliennt(
    client_id: int, session: AsyncSession = Depends(get_session)
):
    client = await crud.get_client(client_id, session)
    if not client:
        raise HTTPException(404, 'Клиент не найден')
    try:
        await crud.delete_client(client, session)
        return {"message": "Клиент удалён"}
    except Exception:
        raise HTTPException(500, 'Ошибка при удалении клиента')
