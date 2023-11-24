#скорее всего это мы отделяем работу с бд от эндпойнта в отдельный слой, dao = services = repo
# сюда мы выносим часто встречающийся find_all
# паттерн, для выделения работы с бд в отдельынй слой или
# скорее всего это класс абстракция для работы с бд???????
from app.database import async_session_maker

from sqlalchemy import select, insert


#- здесь нам не нужно указание конкретной модели,
# мы будем просто сюда передаввать csl.model,
# cls = self, только в ситуации с класс методами
class BaseDAO:
    model = None# - вот здесь мы задаем или определяем пустой модель

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id) # - здесь мы передаем перегруженную модель и тут же добавляем фильтры, можем их явно передавать, а можем передавть из роутера
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by): #- верни одну запись или нон, если такой нету
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by): # принимаем данные в аргументы функции()- вместо того, чтобы создавать экземпляр класса, мы сразу ебашим через точку с цлс(также здесь мы принимаем фильтры, которые потом передаются в query
        async with async_session_maker() as session: # - здесь мы юзаем контекстный менеджер для открытия соедение с бд через фабрику, заданную в датабейс
            query = select(cls.model.__table__.columns).filter_by(**filter_by) # - параметры фильтра: user_id=1, price=24500, здесь мы уже передаем любую модель и селектим все по этой модели, так как метод называется файнд олл( также с учетом фильтров, которые передаем из приема главной функции)
            result = await session.execute(query) #- здесь мы обобщаем через result вместо bookings, так как у нас нет конкретного ответа
            return result.mappings().all() # - здесь возвращаются результаты от алхимии по факту запроса в бд

    @classmethod
    async def add(cls, **data): # - до этого мы занимались фильтрацией инфы по бд, здесь теперь мы ее вставляем в бд
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)# - здесь мы передаем values как в скл запросе
            await session.execute(query)
            await session.commit()# - когда обновляем данные, всегда делаем коммит











# recs = result.mappings().all()
            # list = []
            # for rec in recs:
            #     list2 = rec.Bookings # - здесь мы создаем дополнительную переменную прокладку для основной, так как mapping and sckallars нельзя вызвать по два раза(прихуярить к ним точку в конце нельзя)
            #     list.append(list2)
            # return list
            #- мы не знаем, что мы здесь возвращаем(мб не знаем, что и принимаем)

# @classmethod
# async def find_all(cls):
#     async with async_session_maker() as session:
#         query = select(Bookings)
#         bookings = await  session.execute(query)
#         return bookings.scalars().all() # - эта конструкция равна предыдущей