from datetime import date, datetime

from pydantic import BaseModel


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


class SCommentsBreakdown(BaseModel):
    created_comments: int
    blocked_comments: int
    day: date
