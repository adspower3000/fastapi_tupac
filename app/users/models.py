from sqlalchemy import Column, Integer, String
from app.database import Base


class Users(Base):
    __tablename__ = "users" # - с этой таблы мы никуда пока не ссылаемся, внешних ключей особо нет

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)