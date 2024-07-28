from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SPost(BaseModel):
    id: int
    title: str
    content: str
    photo_uid: str | None
    author_id: int
    is_blocked: bool
    created_at: datetime


class SPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    photo_uid: Optional[str] = None
