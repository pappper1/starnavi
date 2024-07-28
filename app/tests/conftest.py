import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.user.models import User
from app.post.models import Post
from app.post.comment.models import Comment


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
	assert settings.MODE == 'TEST'

	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

	def open_mock_json(model: str):
		with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
			return json.load(file)

	users = open_mock_json('users')
	posts = open_mock_json('posts')
	comments = open_mock_json('comments')

	for comment in comments:
		comment['created_at'] = datetime.strptime(
			comment['created_at'], "%Y-%m-%d %H:%M:%S.%f"
		)

	async with async_session_maker() as session:
		add_users = insert(User).values(users)
		add_posts = insert(Post).values(posts)
		add_comments = insert(Comment).values(comments)

		await session.execute(add_users)
		await session.execute(add_posts)
		await session.execute(add_comments)

		await session.commit()


@pytest.fixture(scope='session')
def event_loop(request):
	loop = asyncio.get_event_loop_policy().new_event_loop()
	yield loop
	loop.close()


@pytest.fixture(scope="function")
async def client():
	async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
		yield client


@pytest.fixture(scope="session")
async def auth_client():
	async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
		response = await client.post("/user/login", json={
			"email": "testuser@example.com",
			"password": "test_password"
		})
		print(response.json())
		assert client.cookies.get("access_token")
		yield client


@pytest.fixture(scope="session")
async def session():
	async with async_session_maker() as session:
		yield session
