import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("title, content, file, status_code", [
	("Test title", "Test content", None, 200),
	("Test title", "Test content", "app/tests/integration_tests/post_tests/images/test.png", 200),
	("", "Test content", None, 422),
	(12, "Test content", None, 200),
	("Shit", "Test content", None, 400),
	("Shit", "Test content", None, 400),
])
async def test_create_post(
		title: str,
		content: str,
		file: str | None,
		status_code: int,
		auth_client: AsyncClient
):
	headers = {
		'accept': 'application/json',
	}
	response = await auth_client.post(url="/post/create", headers=headers, files={
		"title": (None, str(title)),
		"content": (None, str(content)),
		"file": ("test.png", open(file, "rb"), "image/png") if file else (file, "")
	})
	print(response.json())

	assert response.status_code == status_code
