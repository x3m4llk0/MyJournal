from fastapi import FastAPI, APIRouter, Depends, Query

from datetime import datetime

from app.api.auth.dependencies import get_current_user
from app.api.dao.articledao import ArticleDAO
from app.api.exceptions.exceptions import *
from app.api.models.schemas import SArticle, SArticleCreateEdit
from app.api.models.user import User
from fastapi_cache.decorator import cache

app = FastAPI()

router = APIRouter(prefix="/articles", tags=["Статьи"])


# Получение всех статей
@router.get('/all')
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
async def get_articles_with_pagination(page: int = Query(1, ge=1), per_page: int = Query(5, le=10)):
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
@router.get('/sort_by_author/{author_name}')
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
@router.get('/sort_by_date/{publication_date}')
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
async def create_article(article_data: SArticleCreateEdit, author: User = Depends(get_current_user)) -> SArticle:
    """
    Создает статью.\n
    Args: \n
        :param author: Текущий пользователь
        :param article_data: Название, текст статьи
    Returns: \n
        Dict: Словарь объектов статьи
    Raises: \n
        :raises 409: Статья с таким названием уже существует.
        :raises 500: Не удалось добавить запись.
        """
    current_date = datetime.now().date()
    new_article = await ArticleDAO.add_article(title=article_data.title,
                                               contents=article_data.contents,
                                               publication_date=current_date,
                                               author=author.name)
    return new_article


# Редактирование статьи по id
@router.put("/edit/{article_id}")
async def edit_article(article_id: int, article_data: SArticleCreateEdit,
                       current_user: User = Depends(get_current_user)) -> str:
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
    """
    existing_article = await ArticleDAO.find_one_or_none(id=article_id)
    if existing_article:
        if current_user.name == existing_article['author'] or current_user.role == 'admin':
            await ArticleDAO.update_article(article_id=article_id, article_data=article_data.dict())
            return "Success edited"
        else:
            raise NoPermissionToEditException
    else:
        raise ArticleNotExistsException


# Удаление статьи по id
@router.delete("/delete/{article_id}")
async def remove_article(article_id: int, current_user: User = Depends(get_current_user), ) -> str:
    """
    Удаляет статью по её идентификатору.\n
    Args: \n
        :param current_user: Текукий пользователь
        :param article_id: Идентификатор удаляемой статьи
    Returns: \n
        str: Cтрока с сообщением об успешном удалении.
    Raises: \n
        :raises 500: Если статья не найдена.
        :raises 403: Если нет прав для удаления статьи.
    """
    existing_id = await ArticleDAO.find_one_or_none(id=article_id)
    if existing_id:
        if current_user.name == existing_id['author'] or current_user.role == 'admin':
            await ArticleDAO.delete(id=article_id)
            return "Success deleted"
        else:
            raise NoPermissionToDeleteException
    else:
        raise ArticleNotExistsException
