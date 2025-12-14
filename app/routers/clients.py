from typing import Annotated

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
crud = CRUDClient()


@client_router.get("/all", dependencies=[Depends(current_user)])
async def get_all_clients(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(current_user),
) -> list[ClientReadSchema]:
    clients = await crud.get_all_clients(session, current_user)
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет ниодного клиента"
        )
    return clients


@client_router.get("/{client_id}", dependencies=[Depends(current_user)])
async def get_client(
    client_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(current_user),
) -> ClientReadSchema:
    client = await crud.get_client(client_id, session, current_user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    return client


@client_router.post("", dependencies=[Depends(current_user)])
async def create_client(
    data: Annotated[ClientCreateSchema, Depends()],
    session: AsyncSession = Depends(get_session),
) -> ClientCreateSchema:
    try:
        client = await crud.create_client(data, session)
        return client
    except Exception as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при добавлении клиента",
        )


@client_router.patch("/{client_id}", dependencies=[Depends(current_user)])
async def update_client(
    client_id: int,
    data: Annotated[ClientUpdateSchema, Depends()],
    session: AsyncSession = Depends(get_session),
) -> ClientReadSchema:
    client = await crud.get_client(client_id, session, current_user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    try:
        upd_client = await crud.update_client(client, data, session)
        return upd_client
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при изменении клиента"
        )


@client_router.delete("/{client_id}", dependencies=[Depends(current_superuser)])
async def delete_cliennt(
    client_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_superuser),
):
    client = await crud.get_client(client_id, session, user)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден"
        )
    try:
        await crud.delete_client(client, session)
        return {"detail": "Клиент удалён"}
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при удалении клиента"
        )
