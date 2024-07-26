from app.repository.base import BaseDAO
from app.user.models import User


class UserDAO(BaseDAO):
	model = User
