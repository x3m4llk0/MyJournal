from fastapi import HTTPException, status

class ArticleException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectNameOrPasswordException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверное имя или пароль"


class TokenExpiredException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необходимо авторизоваться"


class IncorrectTokenFormatException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ArticleException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необходимо авторизоваться"


class ArticleAlreadyExistsException(ArticleException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Статья с таким названием уже существует"


class ArticleNotExistsException(ArticleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Статья с таким ID не существует"


class NoPermissionToDeleteException(ArticleException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет прав для удаления статьи"


class NoPermissionToEditException(ArticleException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет прав для редактирования статьи"


class IncorrectDateFormatException(ArticleException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Некорректный формат даты"


class CannotAddDataToDatabase(ArticleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


