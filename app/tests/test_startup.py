import pytest
from sqlalchemy import text
from app.api.models.article import Article
from app.db.base import engine, async_session_maker


def test_prepare_database():
    print("Success startup")

#Устанавливаем autoincrement после внесения данных в базу
@pytest.mark.asyncio
async def test_sequence_handling():
    async with engine.begin() as conn:
        pass

    # Установка значения последовательности в 4
    async with async_session_maker() as session:
        await session.execute(text("SELECT setval('article_id_seq', 3, true)"))

    # Получение значения из последовательности
    async with async_session_maker() as session:
        next_val = await session.execute(text("SELECT nextval('article_id_seq')"))
        next_id = next_val.scalar()
    # Проверка полученного значения
    assert next_id == 4