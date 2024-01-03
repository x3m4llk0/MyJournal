from fastapi import APIRouter, Depends, Response, HTTPException, status

from app.api.auth.auth import authenticate_user, create_access_token, get_password_hash
from app.api.dao.userdao import UserDAO
# from app.users.dependencies import get_current_user
from app.api.models.user import User
from app.api.models.schemas import SUserRegister, SUserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router.post("/register", status_code=201)
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.name)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add_user(name=user_data.name, email=user_data.email, hashed_password=hashed_password, role='user')
    if not new_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удалось добавить запись")


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.name, user_data.password)
    access_token = create_access_token({"sub": str(user.name)})
    response.set_cookie("my_journal_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("my_journal_access_token")


