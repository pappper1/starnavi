from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends

from app.exceptions import (
    AccessForbiddenException,
    AnalyticsNotFoundException,
    CommentNotFoundException,
    PostNotFoundException,
)
from app.post.comment.repository import CommentRepository
from app.post.comment.schemas import SComment, SCommentCreate, SCommentsBreakdown
from app.post.repository import PostRepository
from app.services.ai.chat_gpt import chat_gpt
from app.services.scheduler import SchedulerTasks, scheduler
from app.user.dependencies import get_current_user
from app.user.models import User

router = APIRouter(
    prefix="/comment",
    tags=["Comments"],
)


@router.post("/create")
async def create_comment(
    comment_data: SCommentCreate, user: User = Depends(get_current_user)
) -> SComment | dict:
    post = await PostRepository.find_by_id(comment_data.post_id)
    if not post:
        raise PostNotFoundException

    if await chat_gpt.profanity_check(content=comment_data.content):
        await CommentRepository.add(
            content=comment_data.content,
            author_id=user.id,
            post_id=comment_data.post_id,
            is_blocked=True,
        )

        return {"message": "Profanity detected. Comment was blocked."}

    new_comment = await CommentRepository.add(
        **comment_data.model_dump(), author_id=user.id
    )
    if post.author.is_ai_answer_comments:
        scheduler.add_job(
            SchedulerTasks.ai_answer_comment,
            "date",
            run_date=datetime.now()
            + timedelta(seconds=post.author.comments_ai_answer_delay),
            args=[post.id, post.title, post.content, new_comment.content],
        )

    return new_comment


@router.get("/read/{comment_id}")
async def read_comment(
    comment_id: int, user: User = Depends(get_current_user)
) -> SComment | dict:
    comment = await CommentRepository.find_by_id(comment_id)
    if not comment:
        raise CommentNotFoundException

    return comment


@router.get("/read-all/{post_id}")
async def read_all_post_comments(
    post_id: int, user: User = Depends(get_current_user)
) -> list[SComment]:
    comments = await CommentRepository.find_all(post_id=post_id)
    if not comments:
        raise CommentNotFoundException

    return comments


@router.put("/update/{comment_id}")
async def update_comment(
    comment_id: int, content: str, user: User = Depends(get_current_user)
) -> SComment | dict:
    comment = await CommentRepository.find_by_id(comment_id)
    if not comment:
        raise CommentNotFoundException
    if comment.author_id != user.id:
        raise AccessForbiddenException

    if await chat_gpt.profanity_check(content=content):
        return {"message": "Profanity detected."}

    updated_comment = await CommentRepository.update(comment_id, content=content)

    return updated_comment


@router.delete("/delete/{comment_id}")
async def delete_comment(
    comment_id: int, user: User = Depends(get_current_user)
) -> dict:
    comment = await CommentRepository.find_by_id(comment_id)
    if not comment:
        raise CommentNotFoundException
    if comment.author_id != user.id:
        raise AccessForbiddenException

    await CommentRepository.delete(id=comment_id)

    return {"message": "Comment was deleted."}


@router.get("/daily-breakdown")
async def daily_comments_breakdown(
    date_from: date, date_to: date, user: User = Depends(get_current_user)
) -> list[SCommentsBreakdown]:
    analytics = await CommentRepository.find_comment_analytics(date_from, date_to)
    if not analytics:
        raise AnalyticsNotFoundException

    return analytics
