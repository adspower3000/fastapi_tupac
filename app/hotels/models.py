from sqlalchemy import JSON, Column, Integer, String, ForeignKey
from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels" # - с этой таблы мы никуда пока не ссылаемся, внешних ключей особо нет

    id = Column(Integer, primary_key=True) # - первичный ключ, ид, автогенерирующийся
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)


class Rooms(Base):
    __tablename__ = "rooms" # - с этой таблы мы ссылаемся на hotels_id

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    services = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
