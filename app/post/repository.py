from app.post.models import Post
from app.repository.base import BaseRepository


class PostRepository(BaseRepository):
    model = Post
