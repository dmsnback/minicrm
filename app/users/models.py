import enum
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clients import Client
    from app.models.comments import Comment
    from app.models.deals import Deal


class UserRole(str, enum.Enum):
    manager = "manager"
    admin = "admin"


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"), default=UserRole.manager, nullable=False
    )
    clients: Mapped[list["Client"]] = relationship(
        back_populates="manager", lazy="selectin"
    )
    deals: Mapped[list["Deal"]] = relationship(back_populates="manager", lazy="selectin")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author", lazy="selectin"
    )
