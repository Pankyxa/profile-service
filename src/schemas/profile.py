from datetime import date, datetime

from pydantic import BaseModel


class ProfileCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    birth_date: date


class ProfileUpdate(BaseModel):
    full_name: str
    phone: str
    birth_date: date


class ProfileOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    birth_date: date
    created_at: datetime
    updated_at: datetime
