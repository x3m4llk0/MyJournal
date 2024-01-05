from datetime import date
from pydantic import BaseModel


class SArticle(BaseModel):
    id: int
    title: str
    contents: str
    publication_date: date
    author: str


class SArticleCreate(BaseModel):
    title: str
    contents: str


class SArticleEdit(BaseModel):
    title: str
    contents: str


class SUserRegister(BaseModel):
    name: str
    email: str
    password: str


class SUserLogin(BaseModel):
    name: str
    password: str
