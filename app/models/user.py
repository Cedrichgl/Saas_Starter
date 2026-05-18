from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserRole(str, Enum):  # ← Enum de Python (pas SAEnum)
    ADMIN = "admin"
    USER = "user"
    SUPERADMIN = "superadmin"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
