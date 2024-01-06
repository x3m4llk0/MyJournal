from datetime import datetime

import pytest

from app.api.dao.articledao import ArticleDAO


@pytest.mark.parametrize("id, title, contents, author", [
    (5, "Test_title", "Test_contents", "testuser"),
    (6, "Test_title_2", "Test_contents_2", "testuser2"),

])
async def test_article_crud(id, title, contents, author):
    # Добавление брони
    new_article = await ArticleDAO.add_article(
        id=id,
        title=title,
        contents=contents,
        publication_date=datetime.strptime("2024-01-07", "%Y-%m-%d"),
        author=author,
    )

    assert new_article.title == title
    assert new_article.contents == contents
    assert new_article.author == author

    # Проверка добавления брони
    new_article = await ArticleDAO.find_one_or_none(id=new_article.id)

    assert new_article is not None

    # Удаление брони
    await ArticleDAO.delete(
        id=new_article.id,
    )

    # Проверка удаления брони
    deleted_booking = await ArticleDAO.find_one_or_none(id=new_article.id)
    assert deleted_booking is None
