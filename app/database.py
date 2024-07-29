from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings
from app.utils.pg_client import AsyncPgClient
import asyncio

if settings.MODE == "TEST":
	asyncio.run(AsyncPgClient.create_test_db())

	DATABASE_URL = settings.TEST_DATABASE_URL
	DATABASE_PARAMS = {"poolclass": NullPool}
else:
	DATABASE_URL = settings.DATABASE_URL
	DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
	pass
