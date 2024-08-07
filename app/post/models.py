from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.post.comment.models import Comment


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    photo_uid = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    is_blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, nullable=False)

    author = relationship("User", back_populates="posts", lazy="joined")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )

    def __str__(self):
        return self.title
