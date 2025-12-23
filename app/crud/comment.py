import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.comments import Comment
from app.models.deals import Deal
from app.schemas.comments import CommentCreateSchema, CommentUpdateSchema
from app.users.models import User, UserRole

logger = logging.getLogger(__name__)


class CRUDComment:

    async def get_comments_deal(self, deal_id: int, session: AsyncSession):
        try:
            query = (
                select(Comment)
                .where(Comment.deal_id == deal_id)
                .order_by(Comment.created_at.asc())
            )
            result = await session.execute(query)
            comment = result.scalars().all()
            return comment
        except SQLAlchemyError as e:
            logger.error(f"Ошибка приполучении комментария: {e}")
            raise

    async def create_comment(
        self, deal_id: int, data: CommentCreateSchema, session: AsyncSession, user: User
    ):
        try:
            if user.role not in (UserRole.manager, UserRole.admin):
                raise PermissionError("Недостаточно прав для добавления комментария")
            deal = await session.get(
                Deal,
                deal_id,
                options=[
                    selectinload(Deal.comments).selectinload(Comment.author),
                    selectinload(Deal.manager),
                    selectinload(Deal.client),
                ],
            )
            if not deal:
                raise ValueError("Сделка не найдена")
            new_comment = Comment(
                text=data.text,
                author_id=user.id,
                deal_id=deal_id,
            )
            session.add(new_comment)
            await session.flush()
            await session.commit()
            await session.refresh(new_comment.deal, attribute_names=["comments"])
            logger.info(f"Добавлен новый комментарий к сделке: {new_comment.deal}")
            return new_comment
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при добавлении комментария: {e}")
            raise

    async def update_comment(
            self, comment_id: int, data: CommentUpdateSchema, session: AsyncSession, user: User
    ):
        try:
            comment = await session.get(Comment, comment_id)
            if not comment:
                raise ValueError("Комментарий не найден")
            if comment.author_id != user.id:
                raise PermissionError("Нельзя редактировать чужой комментарий")
            comment.text = data.text
            await session.commit()
            await session.refresh(comment)
            logger.info(f"Комментарий id = {comment_id} изменён")
            return comment
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при изменении комментария id={comment_id}: {e}")
            raise

    async def delete_comment(
            self, comment_id: int, session: AsyncSession, user: User
    ):
        try:
            comment = await session.get(Comment, comment_id)
            if not comment:
                raise ValueError("Комментарий не найден")
            if user.role != UserRole.admin:
                raise PermissionError("Удалять комментарии может только администратор")
            await session.delete(comment)
            await session.commit()
            logger.info(f"Комментарий id={comment_id} удалён")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении комментария id={comment_id}: {e}")
            raise
