from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Client(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str | None] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(nullable=True)
    phone: Mapped[int | None] = mapped_column(nullable=True)
