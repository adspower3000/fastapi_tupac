from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, create_access_token, authenticate_user
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import Users
from app.users.shemas import SUserAuth

router = APIRouter( # - этот роутер как и все остальные надо испортировать в майн.пай
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register") #- один эндпойнт для регистрации
async def register_user(user_data: SUserAuth): # - здесь мы явно принимаем пользовательские данные из сваггера
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)#- здесь проверяем совпадения, сходства(в базе есть email, мы сравниваем его с поступающей в функцию user_data
    if existing_user: # - если юзер после проверки существует, то мы рейзим ошибку
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password) # - если проверки пройдены, то 1.хешируем пароль
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)# - и 2. добавляем в базу пользователя


# ! после логина и присвоения юзеру ацесс токена, мы можем этот токен брать и отдавать инфу юзеру( букинги например) по его куке
# здесь мы как раз вызывваем функции из других модулей и передаем в них параметры, которые потом эти функции обрабатывают
@router.post("/login") # - здесь одновременно и аутентифицируем и присваиваем куку, то есть выносим логику в auth и юзаем функции оттуда, передавая данные в эти функции, импортировав их сюда
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password) # - здесь мы распаковываем user_data через точку , вытаскиваем эмейл с паролем, и передаем в аутентификате
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)}) # - здесь мы через респоунс сетим куку юзеру на его айдишник, чтобы понимать к какому юзеру какие брони относятся, точнее чтобы юзер видел конкретно свои брони
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()

# роли, прииложением могут пользоваться модеры и админы(блок юзеров, или удаление пользователей)




    # user = await UsersDAO.find_one_or_none(email=user_data.email)# - если есть логин, то идем проверять пароль, если нет рейзим ошибку
    # if not user:
    #     raise HTTPException(500)
    # if user:
    #     password_is_valid = verify_password(user_data.password, user.password) # - tесли пароль валидный запускаем его в систему
    #     if not password_is_valid:
    #         raise HTTPException(500)
