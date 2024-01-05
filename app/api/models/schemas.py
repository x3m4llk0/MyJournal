from datetime import date
from pydantic import BaseModel, EmailStr


class SArticle(BaseModel):
    id: int
    title: str
    contents: str
    publication_date: date
    author: str


class SArticleCreateEdit(BaseModel):
    title: str
    contents: str


class SUserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class SUserLogin(BaseModel):
    name: str
    password: str
