from fastapi_users import schemas

from app.users.models import UserRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole
    clients: list | None = None


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.manager
    clients: list | None = None


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.manager
    clients: list | None = None
