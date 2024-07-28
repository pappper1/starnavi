import os
import shutil
import uuid
from typing import Union

from fastapi import APIRouter, Depends, UploadFile, Form
from PIL import Image

from app.post.repository import PostDAO
from app.post.schemas import SPost, SPostUpdate
from app.user.dependencies import get_current_user
from app.user.models import User
from app.services.ai.chat_gpt import chat_gpt
from app.utils.image import is_image
from app.exceptions import FileNotAnImageException, PostNotFoundException, \
	AccessForbiddenException

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
		await PostDAO.add(title=title, content=content, author_id=user.id, is_blocked=True)

		return {"message": "Profanity detected. Post was blocked."}

	if not file is None:
		if not is_image(file):
			raise FileNotAnImageException

		uuid4 = uuid.uuid4()
		image_path = f"app/static/images/{str(uuid4)}.jpg"
		image = Image.open(file.file)
		if image.mode != "RGB":
			image = image.convert("RGB")
		image.save(image_path)

		post = await PostDAO.add(
			title=title, content=content, author_id=user.id, photo_uid=str(uuid4)
		)
	else:
		post = await PostDAO.add(title=title, content=content, author_id=user.id)

	return post


@router.get("/read/{post_id}")
async def read_post(post_id: int, user: User = Depends(get_current_user)) -> SPost:
	post = await PostDAO.find_by_id(post_id)
	if not post:
		raise PostNotFoundException

	return post


@router.get("/read-all")
async def read_all_user_posts(user: User = Depends(get_current_user)) -> list[SPost]:
	posts = await PostDAO.find_all(author_id=user.id)
	if not posts:
		raise PostNotFoundException

	return posts


@router.put("/update/{post_id}")
async def update_post(
		post_id: int,
		title: str = Form(...),
		content: str = Form(...),
		file: Union[UploadFile, None] = None,
		user: User = Depends(get_current_user)
) -> SPost | dict:
	post = await PostDAO.find_by_id(post_id)
	if not post:
		raise PostNotFoundException
	elif post.author_id != user.id:
		raise AccessForbiddenException

	if await chat_gpt.profanity_check(title=title, content=content):
		return {"message": "Profanity detected"}

	post_data = SPostUpdate(title=title, content=content)

	if not file is None:
		if not is_image(file):
			raise FileNotAnImageException

		if post.photo_uid:
			image_path = f"app/static/images/{post.photo_uid}.jpg"
		else:
			uuid4 = uuid.uuid4()
			post_data.photo_uid = str(uuid4)
			image_path = f"app/static/images/{str(uuid4)}.jpg"

		image = Image.open(file.file)
		if image.mode != "RGB":
			image = image.convert("RGB")
		image.save(image_path)

		updated_post = await PostDAO.update(
			post_id, **post_data.dict(exclude_unset=True)
		)
	else:
		updated_post = await PostDAO.update(
			post_id, **post_data.dict(exclude_unset=True)
		)

	return updated_post


@router.delete("/delete/{post_id}")
async def delete_post(post_id: int, user: User = Depends(get_current_user)) -> dict:
	post = await PostDAO.find_by_id(post_id)
	if not post:
		raise PostNotFoundException
	elif post.author_id != user.id:
		raise AccessForbiddenException

	if post.photo_uid:
		image_path = f"app/static/images/{post.photo_uid}.jpg"
		if os.path.exists(image_path):
			os.remove(image_path)

	await PostDAO.delete(id=post_id)

	return {"message": "Post deleted successfully"}
