import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
	("testuser@gmail.com", "test_password", 200),
	("testuser2@gmail.com", "testpassword_2", 200),
	("", "test_password", 422),
	("test_user", "", 422),
	("blakejasmine@example.net", "&%dZV1ox_0", 409),
])
async def test_create_user(email: str, password: str, status_code: int, client: AsyncClient):
	response = await client.post("/user/signup", json={
		"email": email,
		"password": password,
	})
	assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
	("blakejasmine@example.net", "&%dZV1ox_0", 200),
	("hayesrandy@example.net", "_t5H%I$j7%", 200),
	("test_user", "", 422),
	("", "", 422),
	("test_user_5121@example.com", "test_password_12937", 401)
])
async def test_login_user(email: str, password: str, status_code: int, client: AsyncClient):
	response = await client.post("/user/login", json={
		"email": email,
		"password": password,
	})
	assert response.status_code == status_code
