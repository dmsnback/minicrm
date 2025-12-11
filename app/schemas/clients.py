from pydantic import BaseModel, ConfigDict, EmailStr


class ManagerShortSchema(BaseModel):
    id: int
    email: str
    username: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ClientBaseSchema(BaseModel):
    full_name: str
    email: EmailStr | None = None
    phone: str | None = None
    manager_id: int | None = None


class ClientCreateSchema(ClientBaseSchema):
    pass


class ClientUpdateSchema(BaseModel):

    full_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    manager_id: int | None = None


class ClientReadSchema(ClientBaseSchema):
    id: int
    manager: ManagerShortSchema | None

    model_config = ConfigDict(from_attributes=True)
