from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, FastAPI, Query
from fastapi_cache.decorator import cache

from app.api.auth.dependencies import get_current_user
from app.api.dao.articledao import ArticleDAO
from app.api.exceptions.exceptions import (
    ArticleNotExistsException,
    IncorrectDateFormatException,
    NoPermissionToDeleteException,
    NoPermissionToEditException,
)
from app.api.models.schemas import SArticle, SArticleCreateEdit
from app.api.models.user import User

app = FastAPI()

router = APIRouter(prefix="/articles", tags=["Статьи"])


# Объединение всех методов в один
@router.get("/articles", response_model=List[SArticle])
@cache(expire=30)
async def get_articles(
    page: Optional[int] = Query(None, ge=1),
    per_page: Optional[int] = Query(None, le=10),
    author_name: Optional[str] = None,
    publication_date: Optional[str] = None
):
    """
    Получает статьи с возможностью фильтрации по автору, дате и пагинации.\n
    Args:\n
        page: Номер страницы для пагинации.
        per_page: Количество статей на странице (максимум 10).
        author_name: Имя автора для фильтрации.
        publication_date: Дата публикации в формате YYYY-MM-DD для фильтрации.
    Returns:\n
        Список статей, отфильтрованных по указанным параметрам.
    Raises:\n
        403: Некорректный формат даты.
    """
    if author_name:
        return await ArticleDAO.find_by_author(author_name)
    elif publication_date:
        try:
            publication_date = datetime.strptime(publication_date, "%Y-%m-%d")
            return await ArticleDAO.find_by_date(publication_date)
        except ValueError:
            raise IncorrectDateFormatException
    elif page is not None and per_page is not None:
        offset = (page - 1) * per_page
        return await ArticleDAO.get_articles_paginated(offset=offset, limit=per_page)
    else:
        return await ArticleDAO.find_all()


# Получение всех статей
@router.get("/all")
@cache(expire=60)
async def get_all_articles() -> list[SArticle]:
    """
    Получает все статьи.\n
    Returns:\n
        :return: Список всей статей
    """
    return await ArticleDAO.find_all()


# Получение всех статей c пагинацией
@router.get("/page", response_model=list[SArticle])
@cache(expire=30)
async def get_articles_with_pagination(
        page: int = Query(1, ge=1), per_page: int = Query(5, le=10)
):
    """
    Получает список статей с пагинацией.\n
    Args:\n
        :param page: Номер страницы
        :param per_page: Количество статей на странице (максимум 10)
    Returns:\n
        :return: Список статей с пагинацией
    """
    offset = (page - 1) * per_page
    articles = await ArticleDAO.get_articles_paginated(offset=offset, limit=per_page)
    return articles


# Получение всех статей по автору
@router.get("/sort_by_author/{author_name}")
@cache(expire=30)
async def get_articles_by_author(author_name: str) -> list[SArticle]:
    """
    Получает статьи по имени автора.\n
    Args:\n
        author_name: Имя автора
    Returns:\n
        :return: Список статей, написанных указанным автором
    """
    return await ArticleDAO.find_by_author(author_name)


# Получение всех статей по дате
@router.get("/sort_by_date/{publication_date}")
@cache(expire=30)
async def get_articles_by_date(publication_date: str) -> list[SArticle]:
    """
    Получает статьи по дате публикации.\n
    Args:\n
        publish_date: Дата публикации в формате YYYY-MM-DD
    Returns:\n
        :return: Список статей, опубликованных в указанную дату
    Raises: \n
        :raises 403: Некорректный формат даты.
    """
    try:
        publication_date = datetime.strptime(publication_date, "%Y-%m-%d")
        return await ArticleDAO.find_by_date(publication_date)
    except:
        raise IncorrectDateFormatException


# Создание статьи
@router.post("/create", status_code=201)
async def create_article(
        article_data: SArticleCreateEdit, author: User = Depends(get_current_user)
) -> SArticle:
    """
    Создает статью.\n
    Args: \n
        :param author: Текущий пользователь
        :param article_data: Название, текст статьи
    Returns: \n
        Dict: Словарь объектов статьи
    Raises: \n
        :raises 401: Если пользователь не авторизован.
    """
    current_date = datetime.now().date()
    new_article = await ArticleDAO.add_article(
        title=article_data.title,
        contents=article_data.contents,
        publication_date=current_date,
        author=author.name,
    )
    return new_article


# Редактирование статьи по id
@router.put("/edit/{article_id}")
async def edit_article(
        article_id: int,
        article_data: SArticleCreateEdit,
        current_user: User = Depends(get_current_user),
) -> str:
    """
    Редактирует статью по её идентификатору.\n
    Args:\n
        :param article_id: Идентификатор редактируемой статьи
        :param article_data: Данные для редактирования статьи
        :param current_user: Текущий пользователь
    Returns:\n
        str: Строка с сообщением об успешном редактировании.
    Raises:\n
        :raises 404: Если статья не найдена.
        :raises 403: Если нет прав для редактирования статьи.
        :raises 401: Если пользователь не авторизован.
    """
    existing_article = await ArticleDAO.find_one_or_none(id=article_id)
    if existing_article:
        if (
                current_user.name == existing_article["author"]
                or current_user.role == "admin"
        ):
            await ArticleDAO.update_article(
                article_id=article_id, article_data=article_data.dict()
            )
            return "Success edited"
        else:
            raise NoPermissionToEditException
    else:
        raise ArticleNotExistsException


# Удаление статьи по id
@router.delete("/delete/{article_id}")
async def remove_article(
        article_id: int,
        current_user: User = Depends(get_current_user),
) -> str:
    """
    Удаляет статью по её идентификатору.\n
    Args: \n
        :param current_user: Текукий пользователь
        :param article_id: Идентификатор удаляемой статьи
    Returns: \n
        str: Cтрока с сообщением об успешном удалении.
    Raises: \n
        :raises 404: Если статья не найдена.
        :raises 403: Если нет прав для удаления статьи.
    """
    existing_id = await ArticleDAO.find_one_or_none(id=article_id)
    if existing_id:
        if current_user.name == existing_id["author"] or current_user.role == "admin":
            await ArticleDAO.delete(id=article_id)
            return "Success deleted"
        else:
            raise NoPermissionToDeleteException
    else:
        raise ArticleNotExistsException
