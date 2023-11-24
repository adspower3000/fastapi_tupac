from datetime import date

from pydantic import BaseModel


# S - shemas
# здесь происходит валидация через pydantic
# так как модели орм и схемы валидации пайдантик полностью совпадают,
# то уже есть библиотека, способная обьединить изх в едино - SQLModel
# но так как мы будем пилить и другие схемы валидации, то мы не будет ее юзать


class SBooking(BaseModel):
    #model_config = ConfigDict(from_attributes=True)
    id: int# = Field(exclude=True)
    room_id: int# = Field(exclude=True)
    user_id: int# = Field(exclude=True)
    date_from: date# = Field(exclude=True)
    date_to: date# = Field(exclude=True)
    price: int# = Field(exclude=True)
    total_cost: int# = Field(exclude=True)
    total_days: int# = Field(exclude=True)


    class Config:

        orm_mode = True
