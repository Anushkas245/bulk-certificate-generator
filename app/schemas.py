from pydantic import BaseModel, EmailStr
from datetime import date
from typing import List


class RecipientCreate(BaseModel):
    name: str
    email: EmailStr


class JobCreate(BaseModel):
    event_name: str
    event_date: date
    issuer: str
    recipients: List[RecipientCreate]