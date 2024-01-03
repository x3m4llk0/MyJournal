from sqlalchemy import select
from app.api.models.article import Article
from app.db.base import BaseDAO, async_session_maker, engine

class ArticleDAO(BaseDAO):
    model = Article

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()