import os
from datetime import datetime, timedelta
from jose import jwt

from passlib.context import CryptContext
from pydantic import EmailStr

from app.exceptions import IncorrectPasswordException, IncorrectEmailException
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
    )
    return encode_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)# - в случае успеха вытаскивает всю строку из таблицы юзер с хешед пассворд
    if user and verify_password(password, user.hashed_password):# - если нет юзера и неверный пароль, то верни нон
        return user
    return None #- если все верно, то возвращается сам юзер





#     user = await UsersDAO.find_one_or_none(email=email)# - если есть логин, то идем проверять пароль, если нет рейзим ошибку
#     if not user:
#         raise IncorrectEmailException
#     if user:
#         password_is_valid = verify_password(password, user.hashed_password) # - tесли пароль валидный запускаем его в систему
#         if not password_is_valid:
#             return IncorrectPasswordException



    # user = await UsersDAO.find_one_or_none(email=email)# - в случае успеха вытаскивает всю строку из таблицы юзер с хешед пассворд
    # if not user and not verify_password(password, user.hashed_password):# - если нет юзера и неверный пароль, то верни нон
    #     return None
    # return user #- если все верно, то возвращается сам юзер

