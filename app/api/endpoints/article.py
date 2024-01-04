from fastapi import FastAPI, HTTPException, APIRouter, status
from pydantic import BaseModel
from typing import List

from app.api.dao.articledao import ArticleDAO
from app.api.models.schemas import SArticle

app = FastAPI()

router = APIRouter(prefix="/articles", tags=["Статьи"])


@router.get('')
async def get_all_articles() -> list[SArticle]:
    return await ArticleDAO.find_all()


@router.post("/create", status_code=201)
async def create_article(article_data: SArticle):
    existing_title = await ArticleDAO.find_one_or_none(title=article_data.title)
    if existing_title:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Статья с таким названием уже существует")
    new_article = await ArticleDAO.add_article(title=article_data.title,
                                               contents=article_data.contents,
                                               publication_date=article_data.publication_date,
                                               author=article_data.author)
    if not new_article:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось добавить запись")





#
#
# # Модель данных для статьи
# class Article(BaseModel):
#     id: int
#     title: str
#     content: str
#
# # Пример "базы данных" для хранения статей (в реальном проекте здесь будет использоваться SQLAlchemy и реальная база данных)
# articles_db = []
#
# # Создание статьи
# @app.post("/articles/", response_model=Article)
# async def create_article(article: Article):
#     articles_db.append(article)
#     return article
#
# # Получение уникальной статьи по id
# @app.get("/articles/{article_id}", response_model=Article)
# async def read_article(article_id: int):
#     for article in articles_db:
#         if article.id == article_id:
#             return article
#     raise HTTPException(status_code=404, detail="Статья не найдена")
#
# # Получение всех статей
# @app.get("/articles/", response_model=List[Article])
# async def read_articles():
#     return articles_db
#
# # Редактирование статьи по id
# @app.put("/articles/{article_id}", response_model=Article)
# async def update_article(article_id: int, article: Article):
#     for idx, existing_article in enumerate(articles_db):
#         if existing_article.id == article_id:
#             articles_db[idx] = article
#             return article
#     raise HTTPException(status_code=404, detail="Статья не найдена")
#
# # Удаление статьи по id
# @app.delete("/articles/{article_id}")
# async def delete_article(article_id: int):
#     for idx, existing_article in enumerate(articles_db):
#         if existing_article.id == article_id:
#             del articles_db[idx]
#             return {"message": "Статья удалена"}
#     raise HTTPException(status_code=404, detail="Статья не найдена")