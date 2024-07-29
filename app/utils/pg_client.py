import asyncpg

from app.config import settings

class AsyncPgClient:

	@staticmethod
	async def connect():
		return await asyncpg.connect(
			user=settings.DB_USER,
			password=settings.DB_PASS,
			database=settings.DB_NAME,
			host=settings.DB_HOST,
			port=settings.DB_PORT
		)

	@classmethod
	async def create_test_db(cls):
		try:
			conn = await cls.connect()
			await conn.execute(f"CREATE DATABASE {settings.TEST_DB_NAME}")

			await conn.close()
		except Exception:
			pass
