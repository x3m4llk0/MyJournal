from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings
from app.api.exceptions.exceptions import *
from app.api.dao.userdao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("my_journal_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    name: str = payload.get("sub")
    if not name:
        raise UserIsNotPresentException
    user = await UserDAO.find_one_or_none(name=name)
    if not user:
        raise UserIsNotPresentException

    return user
