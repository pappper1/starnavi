from openai import AsyncOpenAI

from app.config import settings


class ChatGPT:
	def __init__(self):
		self.client = AsyncOpenAI(api_key=settings.OPENAI_KEY)

	async def profanity_check(
			self, title: str | None = "Default", content: str | None = "Default"
	) -> bool | str:
		"""
		Checks if the title and content have profanity
		:param title: The title of the post
		:param content: The content of the post
		:return: True if profanity is detected, False otherwise
		"""
		prompt = ("Hi you are an expert in foul language, "
				  "next I will attach the title and text to you. "
				  "If there is profanity in it answer 1, if not answer 0. "
				  "Check very carefully.")
		response = await self.client.chat.completions.create(
			model="gpt-4o-mini",
			messages=[{
				"role": "assistant",
				"content": f"{prompt}"
						   f"Title: {title}"
						   f"content: {content}"
			}]
		)

		if response.choices[0].message.content == "1":
			return True
		elif response.choices[0].message.content == "0":
			return False
		else:
			return response.choices[0].message.content


chat_gpt = ChatGPT()
