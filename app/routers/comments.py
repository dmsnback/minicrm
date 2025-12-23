from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.comment import CRUDComment
from app.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
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
    "/{comment_id}",
    response_model=CommentReadSchema,
    summary="Измеенеение ккомментария",
)
async def update_comment(
    deal_id: int,
    comment_id: int,
    data: CommentUpdateSchema,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_user)
) -> CommentReadSchema:
    try:
        comment = await comment_crud.update_comment(
            comment_id, data, session, user
        )
        return comment
    except ValueError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"{e}"
        )
    except PermissionError as e:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{e}"
        )


@comment_router.delete(
    "/{comment_id}",
    summary="Удаление ккомментария",
    description="Доступно только администратору",
)
async def delete_commennt(
    deal_id: int,
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    user: User = Depends(current_superuser)
) -> dict:
    try:
        await comment_crud.delete_comment(comment_id, session, user)
        return {"detail": "Комментарий удалён"}
    except ValueError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"{e}"
        )
    except PermissionError as e:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail=f"{e}"
        )
