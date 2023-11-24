from fastapi import APIRouter, Request, Depends


from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)

# это есть эндпойнт, мы здесь получаем данные и валидируем их для дальнейшей передачи на фронт например,
# или то, что заходят два человека, и хотят получить свои брони, им похуй на броин других(валидация),
# распознование, какой пользователь делает запрос(аутентификация),
# соотвестно, нам нельзя в эндпойнте держать работу с бд, плюс они не должный быть гигантские(жирные),
# плюс можно будет отдельно тестировать энпойнты'

# !!! при каждом заходе по роутеру система должна проверять,
# что пользователь зашел к нам в систему
# чтобы мы могли его распознать
# и так мы с ним сможем работать. Юзер должен !!зависеть от другой функции(get_current_user из депенсисис)
#! здесь мы принимаем модель юзер


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]: # - ожидаем возвращения списка схем или моделей
    #return user# - возвращает все данны о юзере(емайл, айди, хешпассворд), и можно возвращать конркетные данные, а не все
    #print(user, type(user), user.email)
    return await BookingDAO.find_all(user_id=user.id)#1 - можно тупо хардкодить(а если не хардкодим, а получаем по данным от нашего авторизированного юзера, то работают депендс)
                                                        # и передать айди (1)# и здесь мы по фильтрам отдаем шарику букинги шарика, а не чьи то другие


@router.post("")
async def add_booking(
        user: Users = Depends(get_current_user),
):
    await BookingDAO.add(user_id=user.id)



    #print(request.cookies)
    #print(request.url)
    #print(request.client)
    #return dir(request)

        #result = await BookingDAO.find_all()# - здесь мы просто подставляем методы из букингдао класса, не вдаваясь в конкретную реализацию
        #return result


# @router.get("")
# async def get_bookings() -> list[SBooking]:  # - ожидаем возвращения списка схем или моделей
#         try:
#             result = await BookingDAO.find_all()  # - здесь мы просто подставляем методы из букингдао класса, не вдаваясь в конкретную реализацию
#             return result
#         except ValidationError as exc:
#             print(repr(exc.errors()[0]['type']))



    # - здесь мы выносим работу с бд в отдельный слой
    #1
    # async with async_session_maker() as session:
    #     query = select(Bookings)
    #     result = await session.execute(query)
    #     return result.mappings().all()
    #2
    # result = BookingsService.get_all_bookings()
    # return result




