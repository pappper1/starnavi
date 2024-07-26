from datetime import datetime

from sqlalchemy import JSON, Column, Computed, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Comment(Base):
	__tablename__ = "comment"

	id = Column(Integer, primary_key=True, index=True)
	content = Column(String, nullable=False)
	post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
	author_id = Column(Integer, ForeignKey("user.id"), nullable=True)
	created_at = Column(DateTime, default=datetime.now(), nullable=False)

	post = relationship("Post", back_populates="comments")
	author = relationship("User", back_populates="comments")

	def __str__(self):
		return self.id
