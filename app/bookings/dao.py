#!!!скорее всего это мы отделяем работу с бд от эндпойнта в отдельный слой, dao = services = repo
#- это класс абстракция для работы с бд?
from app.dao.base import BaseDAO

from app.bookings.models import Bookings


class BookingDAO(BaseDAO): # - basedao можем переиспользовать по многу раз, удали в этой таблице юзера по ид и тд, ему не важно, какую таблицу мы подставляем сюда
    model = Bookings

    # @classmethod
    # async def find_all(cls):
    #     async with async_session_maker() as session:
    #         query = select(Bookings)
    #         bookings = await session.execute(query)
    #         return bookings.mappings().all()