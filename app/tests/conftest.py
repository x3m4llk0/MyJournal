import asyncio
import json
from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.api.models.article import Article
from app.api.models.user import User
from app.core.config import settings
from app.db.base import Base, async_session_maker, engine
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    # Убеждаемся, что работаем с тестовой БД
    assert settings.MODE == "TEST"
    print("Preparing the database")

    async with engine.begin() as conn:
        # Удаляем все заданные таблицы из БД
        await conn.run_sync(Base.metadata.drop_all)
        # Добавляем все заданные таблицы в БД
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        # Загружаем данные из файлов JSON
        users = load_json_data("users")
        articles = load_json_data("articles")

        # Вставляем данные в таблицы
        for data, Model in [(users, User), (articles, Article)]:
            for item in data:
                # Преобразуем дату из текстового формата в объект datetime
                item["publication_date"] = datetime.strptime(item["publication_date"], "%Y-%m-%d")
                query = insert(Model).values(item)
                await session.execute(query)
        # Фиксируем изменения
        await session.commit()


def load_json_data(model: str):
    try:
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File 'mock_{model}.json' not found. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON file 'mock_{model}.json'. Returning empty list.")
        return []


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope="function")
# async def ac():
#     "Асинхронный клиент для тестирования эндпоинтов"
#     async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
#         yield ac
#
#
# @pytest.fixture(scope="session")
# async def authenticated_ac():
#     "Асинхронный аутентифицированный клиент для тестирования эндпоинтов"
#     async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
#         await ac.post("/api/v1/auth/login", json={
#             "email": "test@test.com",
#             "password": "test",
#         })
#         assert ac.cookies["booking_access_token"]
#         yield ac
#
#
