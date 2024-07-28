from app.post.comment.repository import CommentRepository
from app.services.ai.chat_gpt import chat_gpt


class SchedulerTasks:

    @staticmethod
    async def ai_answer_comment(
        post_id: int, post_title: str, post_content: str, comment_content: str
    ) -> None:
        ai_answer = await chat_gpt.answer_post_comment(
            post_title=post_title,
            post_content=post_content,
            comment_content=comment_content,
        )

        await CommentRepository.add(content=ai_answer, post_id=post_id)
