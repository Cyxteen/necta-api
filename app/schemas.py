from pydantic import EmailStr, BaseModel
from datetime import datetime

from sqlalchemy import String


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str