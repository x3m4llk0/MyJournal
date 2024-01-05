from sqlalchemy import select, update
from app.api.models.article import Article
from app.db.base import BaseDAO, async_session_maker
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger

class ArticleDAO(BaseDAO):
    model = Article

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def add_article(cls, **data) -> Article:
        try:
            query = insert(cls.model).values(**data).returning(cls.model)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None

    @classmethod
    async def update_article(cls, article_id: int, article_data: dict):
        try:
            async with async_session_maker() as session:
                query = update(cls.model).where(cls.model.id == article_id).values(**article_data)
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot update data in table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot update data in table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)

    @classmethod
    async def get_articles_paginated(cls, offset: int, limit: int) -> list[Article]:
        """
        Получает список статей с пагинацией.

        Args:
            :param offset: Смещение (начиная с 0)
            :param limit: Количество статей для выборки
            :return: Список статей
        """
        async with async_session_maker() as session:
            query = select(cls.model).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()