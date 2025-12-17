from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuthorCommentSchema(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class CommentBaseSchema(BaseModel):

    text: str


class CommentCreateSchema(CommentBaseSchema):
    pass


class CommentUpdateSchema(BaseModel):
    text: str | None = None


class CommentReadSchema(CommentBaseSchema):

    id: int
    created_at: datetime
    updated_at: datetime
    author: AuthorCommentSchema

    model_config = ConfigDict(from_attributes=True)
