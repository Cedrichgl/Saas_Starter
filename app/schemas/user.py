import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


# Socle commun
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None


# Ce que l'API renvoie
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole
    created_at: datetime.datetime
