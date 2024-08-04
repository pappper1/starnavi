from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base
from app.post.models import Post


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_ai_answer_comments = Column(Boolean, default=False)
    comments_ai_answer_delay = Column(Integer, default=5)  # in seconds
    signup_date = Column(DateTime, nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    def __str__(self):
        return self.email
