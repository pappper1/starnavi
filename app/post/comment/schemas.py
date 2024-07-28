from datetime import datetime

from pydantic import BaseModel, EmailStr


class SComment(BaseModel):
	id: int
	content: str
	post_id: int
	author_id: int | None
	is_blocked: bool
	created_at: datetime


class SCommentCreate(BaseModel):
	content: str
	post_id: int
