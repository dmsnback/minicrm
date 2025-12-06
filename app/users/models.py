import enum

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(str, enum.Enum):
    user = "user"
    admin = "admin"


class User(SQLAlchemyBaseUserTable[int]):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[int | None] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), default=UserRole.user, nullable=False
    )
