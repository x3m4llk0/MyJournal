from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from app.api.models.user import User
from app.db.base import BaseDAO, async_session_maker
from app.logger import logger


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.name)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot add user"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot add user"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
