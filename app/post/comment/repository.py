from datetime import date

from sqlalchemy import func, select, cast, Date

from app.logger import logger
from app.repository.base import BaseDAO
from app.post.comment.models import Comment
from app.database import async_session_maker


class CommentDAO(BaseDAO):
	model = Comment

	@classmethod
	async def find_comment_analytics(cls, date_from: date, date_to: date):
		try:
			async with async_session_maker() as session:
				query = select(
					cast(cls.model.created_at, Date).label("day"),
					func.count(cls.model.id).label("created_comments"),
					func.count().filter(cls.model.is_blocked).label("blocked_comments"),
				).where(
					cast(cls.model.created_at, Date) >= date_from,
					cast(cls.model.created_at, Date) <= date_to,
				).group_by("day")

				result = await session.execute(query)
				await session.commit()

				return result.mappings().all()
		except Exception as e:
			logger.exception(e)

