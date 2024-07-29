import asyncpg

from app.config import settings

class AsyncPgClient:

	@staticmethod
	async def connect():
		return await asyncpg.connect(
			user=settings.TEST_DB_USER,
			password=settings.TEST_DB_PASS,
			database=settings.DB_NAME,
			host=settings.TEST_DB_HOST,
			port=settings.TEST_DB_PORT
		)

	@classmethod
	async def create_test_db(cls):
		try:
			conn = await cls.connect()
			await conn.execute(f"CREATE DATABASE {settings.TEST_DB_NAME}")

			await conn.close()
		except Exception:
			pass
