from app.repository.base import BaseDAO
from app.post.comment.models import Comment


class CommentDAO(BaseDAO):
	model = Comment
