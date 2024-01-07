import pytest

from app.api.dao.userdao import UserDAO


@pytest.mark.parametrize(
    "name,is_present", [("testuser", True), ("admin", True), (".....", False)]
)
async def test_find_user_by_name(name, is_present):
    user = await UserDAO.find_one_or_none(name=name)

    if is_present:
        assert user
        assert user["name"] == name
    else:
        assert not user


async def test_add_new_user():
    new_user = await UserDAO.add_user(
        name="testuser3",
        email="example@mail.ru",
        hashed_password="$2b$12$SwAOsDqK",
        role="user",
    )
    assert new_user
