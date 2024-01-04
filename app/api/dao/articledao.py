from sqlalchemy import select
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
    async def add_article(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.title)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None