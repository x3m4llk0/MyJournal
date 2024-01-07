import pytest
from httpx import AsyncClient

async def test_register_login_logout_user(ac: AsyncClient):
        response = await ac.post("/register", json={
            "name": "testuser6",
            "email": "user@example.com",
            "password": "password",
        })
        assert response.status_code == 201

        response = await ac.post("/login", json={
            "name": "testuser6",
            "password": "password",
        })
        assert response.status_code == 200

        response = await ac.post("/logout")
        assert response.status_code == 200


