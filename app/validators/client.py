from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clients import Client


async def validate_unique_email_client(
        session: AsyncSession,
        email: str
) -> None:
    "Проверка уникальности email клиента"
    result = await session.execute(
        select(Client).where(Client.email == email)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Клиент с таким email уже существует'
        )


async def validate_unique_phone_client(
        session: AsyncSession,
        phone: str
) -> None:
    "Проверка уникальности телефона клиента"
    result = await session.execute(
        select(Client).where(Client.phone == phone)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Клиент с таким телефоном уже существует'
        )


async def validate_unique_full_name_client(
        session: AsyncSession,
        full_name: str
) -> None:
    "Проверка уникальности имени клиента"
    result = await session.execute(
        select(Client).where(Client.full_name == full_name)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Клиент с таким именем уже существует'
        )
