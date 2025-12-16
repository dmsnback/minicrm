from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.deals import StatusDeal


class ManagerShortSchema(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ClientShortSchema(BaseModel):
    id: int
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class DealBaseSchema(BaseModel):

    name: str
    description: str | None = None
    status: StatusDeal
    price: float


class DealCreateSchema(DealBaseSchema):

    status: StatusDeal = StatusDeal.new
    manager_id: int | None = None
    client_id: int


class DealUpdateSchema(BaseModel):

    name: str | None = None
    description: str | None = None
    status: StatusDeal | None = None
    price: float | None = None
    manager_id: int | None = None
    client_id: int | None = None


class DealReadSchema(DealBaseSchema):

    id: int
    created_at: datetime
    updated_at: datetime
    manager: ManagerShortSchema | None
    client: ClientShortSchema

    model_config = ConfigDict(from_attributes=True)
