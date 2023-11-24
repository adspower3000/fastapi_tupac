from pydantic import BaseModel, EmailStr

class SUserAuth(BaseModel): # - pydantic схема для тела запроса
    email: EmailStr
    password: str