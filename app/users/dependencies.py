import os
from datetime import datetime

from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError

from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, \
    UserIsNotPresentException
from app.users.dao import UsersDAO
from app.users.models import Users


# здесь у нас три этапа, если получение куки проебется,
# о не отработает получение юзера а следовательно
# и не отработает роутер эндпойнт

# в зависимостях мы сслыаемся на другие функции
def get_token(request: Request): # - здесь мы работаем с запросом от юзера, разбираем его на куски и добываем куку
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

# - с каждой отправкой запроса от юзера, нам будет приходить его кука, мы проверяем этот запрос на истичение жизни токена(если истек, кикаем юзера)
# - что он валидный
# - что у него есть все нобходимые данные и дальше позволять работать юзеру с нашей системой, с нашим апи
# - если нет, то возвращать ему ошибку
async def get_current_user(token: str = Depends(get_token)): # - эта функция возвращает нам пользователя из бд, и она зависит от get_token
    try:
        payload = jwt.decode( # - здесь мы декодируем токен
            token, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM")
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()): # - приводим дейттайм к таймстемпу(флоату) и можем сравнить с интом
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentException
    return user # - мы получили данные пользователя(почту) из его куки,
    # и так как здесь класс алхимия,
    # мы можем обращаться к нему через точку(user.email, user.id, то есть доставать все возможные параметры, которые у него есть)

# роли, прииложением могут пользоваться модеры и админы(блок юзеров, или удаление пользователей)
# эта зависимость прокидывается только в защищенный эндпойнт

# async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
#     if current_user.role != "admin": # - так как у нас нету поля role, то представим, что мы сидими как админ
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     return current_user

async def get_current_admin_user(current_user: Users = Depends(get_current_user)): # - перед тем, как запуститься любой код, сначала запустяться депендс, и с самых нижних уровней поднимется или ошибка, или код будет выполняться по нижним уровням последовательно
    # if current_user.role != "admin": # - так как у нас нету поля role, то представим, что мы сидими как админ
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user