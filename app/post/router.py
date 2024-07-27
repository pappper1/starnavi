import shutil
import uuid
from PIL import Image
from typing import Union

from fastapi import APIRouter, Depends, UploadFile, Form

from app.post.repository import PostDAO
from app.post.schemas import SPost
from app.user.dependencies import get_current_user
from app.user.models import User
from app.services.ai.chat_gpt import chat_gpt
from app.utils.image import is_image
from app.exceptions import FileNotAnImageException

router = APIRouter(
	prefix="/post",
	tags=["Posts"],
)


@router.post("/new")
async def create_post(
		title: str = Form(...),
		content: str = Form(...),
		file: Union[UploadFile, None] = None,
		user: User = Depends(get_current_user)
) -> SPost | dict:
	if await chat_gpt.profanity_check(title=title, content=content):
		return {"message": "Profanity detected"}

	if not file is None:
		if not is_image(file):
			raise FileNotAnImageException

		uuid4 = uuid.uuid4()
		image_path = f"app/static/images/{str(uuid4)}.jpg"
		image = Image.open(file.file)
		image.save(image_path)

		post = await PostDAO.add(
			title=title, content=content, author_id=user.id, photo_uid=str(uuid4)
		)
	else:
		post = await PostDAO.add(title=title, content=content, author_id=user.id)

	return post
