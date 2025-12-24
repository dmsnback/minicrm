import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clients import Client
    from app.models.comments import Comment
    from app.users.models import User


class StatusDeal(str, enum.Enum):
    new = "Новая"
    in_progress = "В процессе"
    success = "Выполнена"
    canceled = "Отменена"


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[StatusDeal] = mapped_column(
        Enum(StatusDeal, name="status_deal_enum"), default=StatusDeal.new, nullable=False
    )
    price: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    manager: Mapped["User"] = relationship(back_populates="deals", lazy="selectin")
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    client: Mapped["Client"] = relationship(back_populates="deals", lazy="selectin")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="deal", lazy="selectin", cascade="all, delete-orphan"
    )
