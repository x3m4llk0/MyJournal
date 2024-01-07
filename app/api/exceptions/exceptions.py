from fastapi import HTTPException, status

class ArticleAndUserException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ArticleAndUserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectNameOrPasswordException(ArticleAndUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверное имя или пароль"


class TokenExpiredException(ArticleAndUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(ArticleAndUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необходимо авторизоваться"


class IncorrectTokenFormatException(ArticleAndUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ArticleAndUserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Необходимо авторизоваться"


class ArticleAlreadyExistsException(ArticleAndUserException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Статья с таким названием уже существует"


class ArticleNotExistsException(ArticleAndUserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Статья с таким ID не существует"


class NoPermissionToDeleteException(ArticleAndUserException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет прав для удаления статьи"


class NoPermissionToEditException(ArticleAndUserException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет прав для редактирования статьи"


class IncorrectDateFormatException(ArticleAndUserException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Некорректный формат даты"


class CannotAddDataToDatabase(ArticleAndUserException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class UserNotFoundException(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)

