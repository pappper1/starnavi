from datetime import datetime

from pydantic import BaseModel
from fastapi import Form


class SPost(BaseModel):
	id: int
	title: str
	content: str
	photo_uid: str | None
	author_id: int
	created_at: datetime
