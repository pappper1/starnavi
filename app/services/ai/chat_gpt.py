from openai import AsyncOpenAI

from app.config import settings


class ChatGPT:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_KEY)
        self.model = "gpt-4o-mini"

    async def profanity_check(
        self, title: str | None = "Default", content: str | None = "Default"
    ) -> bool | str:
        """
        Checks if the title and content have profanity
        :param title: The title of the post
        :param content: The content of the post
        :return: True if profanity is detected, False otherwise
        """
        prompt = (
            "Hi you are an expert in foul language, "
            "next I will attach the title and text to you. "
            "If there is profanity in it answer 1, if not answer 0. "
            "Check very carefully."
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "assistant",
                    "content": f"{prompt}" f"Title: {title}" f"content: {content}",
                }
            ],
        )

        if response.choices[0].message.content == "1":
            return True
        elif response.choices[0].message.content == "0":
            return False
        else:
            return response.choices[0].message.content

    async def answer_post_comment(
        self, post_title: str, post_content: str, comment_content: str
    ) -> str:
        """
        Answers the content
        :param post_title: The title of the post
        :param post_content: The content of the post
        :param comment_content: The content of the comment
        :return: The AI answer
        """
        prompt = (
            "I want you to act like a normal social media user. "
            "I'll send you the title, content of the post, "
            "and content of the comment. "
            "You will need to respond to this comment in a relevant way, "
            "taking into account the title of the post, "
            "the content and the content of the comment. "
            "The reply should be in the same language as the comment."
        )
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}"
                    f"Post title: {post_title}"
                    f"Post content: {post_content}"
                    f"Comment content: {comment_content}",
                }
            ],
        )

        return response.choices[0].message.content


chat_gpt = ChatGPT()
