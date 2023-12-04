from fastapi import HTTPException, status

# - отлов исключений нам не нужен только тогда,
# когда у нас простой немногоэтапный софт
# когда у нас сервис сложный, этапов много, то нам требуется отлов возможных исключений,
# иначе мы просто запутаемся, на каком этапе у нас ломается логика


class BookingException(HTTPException):
    status_code = 500# - задаем значение по умолчанию, которое будем менять, а если не будем менять, они будут передаваться по умолчанию дальше в потомков
    detail = ""

    def __init__(self): # - через супер мы пересобираем инит данного класса, который вызывает HTTPException с заданными нами параметрами
        super().__init__(
            status_code=self.status_code,
            detail=self.detail) # - здесь мы пересобираем инит функции,
        # а не как в пайкт, инит класса


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class IncorrectPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"



class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomFullyBooked(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных номеров"

# - !!!!пример функций c параметрами, который мы переделываем в классы
# и забрасываем эти параметры в инит

# IncorrectTokenFormatException = HTTPException(
#     status_code=status.HTTP_401_UNAUTHORIZED,
#     detail="Неверный формат токена",
# )
#
# UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)