import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

engine = create_async_engine(os.getenv('DATABASE_URL')) # - асихронный движок, принимает урл

async_session_maker = sessionmaker(class_=AsyncSession, expire_on_commit=False, bind=engine) # - фабрика, генератор сессий(транзакции в бд)
# (транзакции- первод денег - уодного человека обязательно должно списаться со счета, другому прибавиться иначе роллбэк

Base = declarative_base() # - наследуемся от этого класса при создании моделей,
# здесь будут аккумулираваться все метаданные таблиц,
# для удобной работы с миграциями
