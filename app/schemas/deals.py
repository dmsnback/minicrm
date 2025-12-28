from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.deals import StatusDeal
from app.schemas.comments import CommentReadSchema


class ManagerShortSchema(BaseModel):
    id: int
    username: str


class ClientShortSchema(BaseModel):
    id: int
    full_name: str


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
    comments: list | None = None

    model_config = ConfigDict(from_attributes=True)


class DealReadSchema(DealBaseSchema):

    id: int
    created_at: datetime
    updated_at: datetime
    client: ClientShortSchema
    manager: ManagerShortSchema | None
    comments: list[CommentReadSchema] | None = None

    model_config = ConfigDict(from_attributes=True)
