from sqlalchemy import delete, insert, select, func
from sqlalchemy.orm import aliased

from app.database import async_session_maker
from app.repository.base import BaseDAO
from app.post.models import Post
from app.post.comment.models import Comment
from app.logger import logger

CommentAlias = aliased(Comment)

class PostDAO(BaseDAO):
	model = Post
