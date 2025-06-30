from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from ..database import Base
from .standard_category import StandardCategory

__all__ = [
    "Account",
    "StandardCategory"
]

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String(10), unique=True, nullable=False, index=True)
    role = Column(String, default="client")  # "admin" 또는 "client"
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
