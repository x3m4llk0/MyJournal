import pytest

from app.api.dao.articledao import ArticleDAO
from app.api.exceptions.exceptions import UserNotFoundException


@pytest.mark.parametrize("id,is_present", [(2, True), (4, True), (100, False)])
async def test_find_article_by_id(id, is_present):
    article = await ArticleDAO.find_one_or_none(id=id)

    if is_present:
        assert article
        assert article.id == id
    else:
        assert not article


async def test_find_all_articles():
    articles = await ArticleDAO.find_all()
    assert articles


async def test_update_articles():
    updated_article = await ArticleDAO.update_article(
        article_id=2,
        article_data={"title": "Код давинчи", "contents": "Описание кода давинчи"},
    )
    assert updated_article


@pytest.mark.parametrize("author", ["testuser", "testuser2", "sqsqsqsqs"])
async def test_find_articles_by_author(author):
    try:
        find_article = await ArticleDAO.find_by_author(author)
        assert find_article is not None
    except UserNotFoundException as e:
        assert False, f"User '{author}' not found in the database: {e}"
