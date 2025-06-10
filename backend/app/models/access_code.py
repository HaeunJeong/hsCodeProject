from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    CLIENT = "client"

class AccessCode(Base):
    __tablename__ = "access_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    role = Column(String)  # 'admin' or 'user'
    isActive = Column(Boolean, default=True)
    companyName = Column(String, nullable=True)  # 고객사명 (고객사인 경우에만 사용)
    expiresAt = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    lastLogin = Column(DateTime(timezone=True), nullable=True)
    lastUsedAt = Column(DateTime, nullable=True) 