from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)

sync_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class PreBase(Model):
    __abstract__ == True # type: ignore

    @declared_attr
    def __tablename__(cls)->str:
        return cls.__name__.lower()
    
    id: Mapped[int] = mapped_column(primary_key=True)


async def get_session():
    async with sync_session as session:
        yield session
