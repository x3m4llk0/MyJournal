from sqlalchemy import Column, String
from sqlalchemy_utils import EmailType

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    name = Column(String, nullable=False, primary_key=True)
    email = Column(EmailType, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    def __str__(self):
        return f"Пользователь {self.name}"
