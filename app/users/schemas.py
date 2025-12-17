from fastapi_users import schemas
from pydantic import ConfigDict

from app.schemas.clients import ClientReadSchema
from app.users.models import UserRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole
    clients: list[ClientReadSchema] | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.manager


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.manager
    clients: list | None = None
