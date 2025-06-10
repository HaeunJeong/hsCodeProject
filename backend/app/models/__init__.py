
from .access_code import AccessCode
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from ..database import Base

__all__ = [
    "AccessCode"
]

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String(10), unique=True, nullable=False, index=True)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
