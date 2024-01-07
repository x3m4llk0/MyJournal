import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("name, email,password,status_code", [
    ("testuser4", "user@example.com", "test", 201),
    ("testuser5", "....", "test", 409),
    ("testuser5", "user@example.com", "test", 409), ])
async def test_register_user(name, email, password, status_code, ac: AsyncClient):
    response = await ac.post("/register", json={
        "name": "test1",
        "email": "user@example.com",
        "password": "password",
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("name,password,status_code", [
    ("testuser", "test", 200),
    ("admin", "artem", 200),
    ("adminski", "artem", 401), ])
async def test_login_user(name, password, status_code, ac: AsyncClient):
    response = await ac.post("/login", json={
        "name": name,
        "password": password,
    })
    assert response.status_code == status_code
