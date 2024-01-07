from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.db.base import Base


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    publication_date = Column(Date, nullable=False)
    author = Column(ForeignKey("user.name"), nullable=False)

    def __str__(self):
        return f"Статья {self.title}"
