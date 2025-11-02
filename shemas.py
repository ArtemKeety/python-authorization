from pydantic import BaseModel, Field, EmailStr, model_validator
from fastapi import HTTPException
from enum import Enum, IntEnum

class Role(IntEnum):
    user = 1
    admin = 2




class Base(BaseModel):
    pass


class UpdateRole(Base):
    user_id: int = Field(ge=1)
    role: Role


class Login(Base):
    login: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=3, max_length=100)


class DBUser(Login):
    email: EmailStr
    is_active: bool
    role_id: int
    id: int

class Registration(Login):
    rep_password: str = Field(..., min_length=3, max_length=100 )
    email: EmailStr

    @model_validator(mode='after')
    def validate(self) -> 'Registration':
        if self.rep_password != self.password:
            raise HTTPException(detail='Passwords do not match', status_code=400)
        return self

