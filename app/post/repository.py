from app.repository.base import BaseDAO
from app.post.models import Post


class PostDAO(BaseDAO):
	model = Post
