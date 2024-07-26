from datetime import datetime

from sqlalchemy import (
	JSON, Column, Computed, DateTime, ForeignKey, Integer, String, Boolean
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
	comments_ai_answer_delay = Column(Integer, default=5) #in seconds
	signup_date = Column(DateTime, default=datetime.now(), nullable=False)

	posts = relationship("Post", back_populates="author")
	comments = relationship("Comment", back_populates="author")

	def __str__(self):
		return self.email
