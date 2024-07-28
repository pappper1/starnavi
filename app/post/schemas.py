from datetime import datetime

from pydantic import BaseModel
from fastapi import Form
from typing import Optional


class SPost(BaseModel):
	id: int
	title: str
	content: str
	photo_uid: str | None
	author_id: int
	created_at: datetime


class SPostUpdate(BaseModel):
	title: Optional[str] = None
	content: Optional[str] = None
	photo_uid: Optional[str] = None
