from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)

sync_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


async def get_session():
    async with sync_session as session:
        yield session
