from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class BookSchemaIn(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    published_date: date
    pages: int
    cover: Optional[str] = None
    language: str

    @field_validator('isbn')
    def validate_isbn(cls, v):
        if not v:
            return v
        if not isinstance(v, str) or not v.isdigit() or len(v) != 13:
            raise ValueError('ISBN must be a 13-digit number')
        return v


class BookSchemaOut(BookSchemaIn):
    id: int

