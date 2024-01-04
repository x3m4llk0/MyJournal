from datetime import date
from pydantic import BaseModel


class SArticle(BaseModel):
    title: str
    contents: str
    publication_date: date
    author: str
    class Config:
        orm_mode = True


class SUserRegister(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class SUserLogin(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True
