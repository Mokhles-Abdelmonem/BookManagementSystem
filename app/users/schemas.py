from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from datetime import date, datetime


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=100)
    address: Optional[str]
    birthdate: Optional[date]

    @field_validator('password')
    def password_complexity(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    address: Optional[str] = None
    birthdate: Optional[date] = None
    created_at: datetime

