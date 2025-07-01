from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from app.core.database import Base
from .standard_category import StandardCategory
from .fabric_component import FabricComponent
from .hs_code_rule import HSCodeRule

__all__ = [
    "Account",
    "StandardCategory",
    "FabricComponent",
    "HSCodeRule"
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
