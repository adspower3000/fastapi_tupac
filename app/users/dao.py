from app.dao.base import BaseDAO
from app.users.models import Users # - sql model


class UsersDAO(BaseDAO): # - usersDao наследуясь от BaseDAO наследует все методы, и в том числе и add
    model = Users # а мы бля наследовались от бейс дао прям сюда, развернули все его методы прямо здесь, переняли все его модели, и в них вставили нашу модель и все данные из роутера по методам