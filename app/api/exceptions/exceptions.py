from fastapi import HTTPException, status


# Создание собственных исключений (exceptions) было изменено
# на предпочтительный подход.
# Подробнее в курсе: https://stepik.org/lesson/919993/step/15?unit=925776

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


class RoomCannotBeBooked(ArticleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class DateFromCannotBeAfterDateTo(ArticleException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть позже даты выезда"


class CannotBookHotelForLongPeriod(ArticleException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать отель сроком более месяца"


class CannotAddDataToDatabase(ArticleException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


