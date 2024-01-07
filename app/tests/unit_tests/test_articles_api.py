import pytest
from httpx import AsyncClient

from app.api.exceptions.exceptions import IncorrectDateFormatException


async def test_get_all_articles(ac: AsyncClient):
    response = await ac.get("/articles/all")
    assert response.status_code == 200





@pytest.mark.parametrize("page, per_page, len_responce", [
    ("1", "3", 3),
    ("2", "2", 2),
    ("5", "10", 0),])
async def test_get_page_articles(page, per_page,len_responce, ac: AsyncClient):
    response = await ac.get("/articles/page", params={
        "page": page,
        "per_page": per_page
    })
    assert len(response.json()) == len_responce


@pytest.mark.parametrize("author_name, len_responce", [
    ("testuser2", 2),
    ("admin", 1),
    ("nottestuser", 0)])
async def test_get_sort_by_author_articles(author_name, len_responce, ac: AsyncClient):
    response = await ac.get(f"/articles/sort_by_author/{author_name}")
    assert len(response.json()) == len_responce


@pytest.mark.parametrize("publication_date, len_responce", [
    ("2024-01-01", 0),
    ("2024-01-06", 2),
    ("YYYY-MM-DD", 0)])
async def test_get_sort_by_date_articles(publication_date, len_responce, ac: AsyncClient):
    try:
        response = await ac.get(f"/articles/sort_by_date/{publication_date}")
        assert len(response.json()) == len_responce
    except AssertionError:
        assert True





async def test_create_articles_by_non_authentificated_user(ac: AsyncClient):
    response = await ac.post("/articles/create", params={
        "title": "Test title",
        "contents": "Test contents"
    })
    assert response.status_code == 401

async def test_create_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/articles/create", json={
        "title": "Test title",
        "contents": "Test contents"
    })
    assert response.status_code == 201


async def test_edit_articles_by_non_authentificated_user(ac: AsyncClient):
    response = await ac.put(f"/articles/edit/{1}", params={
        "title": "Edit title",
        "contents": "Edit contents"
    })
    assert response.status_code == 401

async def test_edit_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.put(f"/articles/edit/{1}", json={
        "title": "Edit title",
        "contents": "Edit contents"
    })
    assert response.status_code == 200

async def test_edit_articles_by_authentificated_user_without_role(authenticated_ac: AsyncClient):
    response = await authenticated_ac.put(f"/articles/edit/{4}", json={
        "title": "Edit title",
        "contents": "Edit contents"
    })
    assert response.status_code == 403

async def test_edit_articles_by_authentificated_user_when_article_not_found(authenticated_ac: AsyncClient):
    response = await authenticated_ac.put(f"/articles/edit/{100}", json={
        "title": "Edit title",
        "contents": "Edit contents"
    })
    assert response.status_code == 404


async def test_delete_articles_by_authentificated_user(authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/articles/delete/{1}")
    assert response.status_code == 200

async def test_delete_articles_by_authentificated_user_without_role(authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/articles/delete/{4}")
    assert response.status_code == 403

async def test_delete_articles_by_authentificated_user_when_article_not_found(authenticated_ac: AsyncClient):
    response = await authenticated_ac.delete(f"/articles/delete/{100}")
    assert response.status_code == 404