from fastapi_users import schemas

from app.models.users import UserRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.user


class UserUpdate(schemas.BaseUserUpdate):
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    phone: int | None = None
    role: UserRole = UserRole.user
