from pydantic import BaseModel, Field, EmailStr, model_validator
from fastapi import HTTPException

class Base(BaseModel):
    pass


class Login(Base):
    login: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=3, max_length=100)


class DBUser(Login):
    email: EmailStr
    is_active: bool
    role_id: int

class Registration(Login):
    rep_password: str = Field(..., min_length=3, max_length=100 )
    email: EmailStr

    @model_validator(mode='after')
    def validate(self) -> 'Registration':
        if self.rep_password != self.password:
            raise HTTPException(detail='Passwords do not match', status_code=400)
        return self