from sqlalchemy import delete, insert, select, func
from sqlalchemy.orm import aliased

from app.database import async_session_maker
from app.repository.base import BaseRepository
from app.post.models import Post
from app.post.comment.models import Comment
from app.logger import logger

CommentAlias = aliased(Comment)

class PostRepository(BaseRepository):
	model = Post
