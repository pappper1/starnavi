from environs import Env
from pydantic import model_validator, root_validator
from typing_extensions import Literal


class Settings:

	def __init__(self):
		self.env = Env()
		self.env.read_env()

		self.LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = self.env.str("LOG_LEVEL")

		self.DB_HOST = self.env.str("DB_HOST")
		self.DB_PORT = self.env.int("DB_PORT")
		self.DB_NAME = self.env.str("DB_NAME")
		self.DB_USER = self.env.str("DB_USER")
		self.DB_PASS = self.env.str("DB_PASS")
		self.DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

		self.JWT_SECRET_KEY = self.env.str("JWT_SECRET_KEY")
		self.JWT_ALGORITHM = self.env.str("JWT_ALGORITHM")

settings = Settings()
