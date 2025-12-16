"""Импорты класса Base и всех моделей для Alembic."""

from app.core.database import Base  # noqa
from app.models.clients import Client  # noqa
from app.models.comments import Comment  # noqa
from app.models.deals import Deal  # noqa
from app.users.models import User  # noqa
