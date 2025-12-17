from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.comment import CRUDComment
from app.schemas.comments import (
    CommentCreateSchema,
    CommentReadSchema
)
from app.users.manager import current_superuser, current_user
from app.users.models import User

comment_router = APIRouter(
    prefix="/deals/{deal_id}/comments",
    tags=[
        "Комментарии",
    ],
)

comment_crud = CRUDComment()


@comment_router.get(
    "", response_model=list[CommentReadSchema], summary="Получить комментарии сдделки"
)
async def get_comments_deal(
    deal_id: int,
    session: AsyncSession = Depends(get_session),
) -> list[CommentReadSchema]:
    comments = await comment_crud.get_comments_deal(deal_id, session)
    return comments


@comment_router.post(
    "",
    response_model=CommentReadSchema,
    dependencies=[Depends(current_user)],
    summary="Добавление ккомментария",
)
async def create_comment(
    deal_id: int,
    data: CommentCreateSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user),
) -> CommentReadSchema:
    try:
        comment = await comment_crud.create_comment(deal_id, data, session, user)
        return comment
    except Exception as e:
        raise e


@comment_router.patch(
    "",
    response_model=CommentReadSchema,
    dependencies=[Depends(current_user)],
    summary="Измеенеение ккомментария",
)
async def update_comment() -> CommentReadSchema:
    pass


@comment_router.delete(
    "",
    dependencies=[Depends(current_superuser)],
    summary="Удаление ккомментария",
    description="Доступно только администратору",
)
async def delete_commennt() -> dict:
    pass
