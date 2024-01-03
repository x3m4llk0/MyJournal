from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Article(Base):
    __tablename__ = "article"

    title = Column(String, nullable=False, primary_key=True)
    contents = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    author = Column(ForeignKey("user.name"), nullable=False)

    def __str__(self):
        return f"Статья {self.title}"
