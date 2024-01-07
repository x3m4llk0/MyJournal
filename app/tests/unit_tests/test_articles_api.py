import pytest
from httpx import AsyncClient


async def test_get_all_articles(ac: AsyncClient):
    response = await ac.get("/articles/all")
    assert response.status_code == 200