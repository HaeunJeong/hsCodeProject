from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..core.database import Base

class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True, unique=True)
    category = Column(String, index=True)
    hsCode = Column(String, index=True)
    description = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 