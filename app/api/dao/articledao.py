import datetime

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from app.api.models.article import Article
from app.db.base import BaseDAO, async_session_maker
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
                query = (
                    update(cls.model)
                    .where(cls.model.id == article_id)
                    .values(**article_data)
                )
                result = await session.execute(query)
                await session.commit()
                return result
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot update data in table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot update data in table"
            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)


    @classmethod
    async def get_articles_paginated(cls, offset: int, limit: int) -> list[Article]:
        async with async_session_maker() as session:
            query = select(cls.model).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_date(cls, publication_date: datetime) -> list[Article]:
        async with async_session_maker() as session:
            query = select(cls.model).where(
                cls.model.publication_date == publication_date
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_by_author(cls, author_name: str) -> list[Article]:
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.author == author_name)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
