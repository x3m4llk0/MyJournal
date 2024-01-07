import asyncio
import json
from datetime import datetime
from unittest import mock

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import insert

from app.api.models.article import Article
from app.api.models.user import User
from app.core.config import settings
from app.db.base import Base, async_session_maker, engine
from app.main import app as fastapi_app


def mock_cache():
    mock.patch(
        "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
    ).start()


def pytest_sessionstart(session):
    mock_cache()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Обязательно убеждаемся, что работаем с тестовой БД
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        # Удаление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    articles = open_mock_json("articles")

    # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
    for article in articles:
        article["publication_date"] = datetime.strptime(
            article["publication_date"], "%Y-%m-%d"
        )

    async with async_session_maker() as session:
        for Model, values in [
            (User, users),
            (Article, articles),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    "Асинхронный клиент для тестирования эндпоинтов"
    async with AsyncClient(
        app=fastapi_app, base_url="http://test"
    ) as ac, LifespanManager(fastapi_app):
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post(
            "/login",
            json={
                "name": "testuser",
                "password": "test",
            },
        )
        assert ac.cookies["my_journal_access_token"]
        yield ac
