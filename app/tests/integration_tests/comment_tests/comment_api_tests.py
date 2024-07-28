from datetime import date

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("date_from, date_to, status_code", [
    ("2024-07-01", "2024-07-07", 200),
    ("2024-07-07", "2024-07-14", 200),
    ("2024-07-14", "2024-07-21", 200),
])
async def test_daily_comments_breakdown(
		date_from: date, date_to: date, status_code: int, auth_client: AsyncClient
):
    response = await auth_client.get(
		f"/comment/daily-breakdown?date_from={date_from}&date_to={date_to}"
	)

    assert response.status_code == status_code
    assert isinstance(response.json(), list)

    for item in response.json():
        assert isinstance(item, dict)
        assert set(item.keys()) == {"day", "created_comments", "blocked_comments"}
