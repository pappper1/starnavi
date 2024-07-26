from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class SUserAuth(BaseModel):
	email: EmailStr
	password: str


class SUser(BaseModel):
	id: int
	email: EmailStr
	is_ai_answer_comments: bool
	comments_ai_answer_delay: int
	signup_date: datetime


class SUserUpdate(BaseModel):
	email: Optional[EmailStr] = None
	is_ai_answer_comments: Optional[bool] = None
	comments_ai_answer_delay: Optional[int] = None
