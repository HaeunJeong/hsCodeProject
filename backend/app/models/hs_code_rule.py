from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from app.core.database import Base

class HSCodeRule(Base):
    __tablename__ = "hs_code_rules"

    id = Column(Integer, primary_key=True, index=True)
    weaving_type = Column(String, nullable=False)  # 직조방식 (knit/woven)
    standard_category = Column(String, nullable=False)  # 표준카테고리
    gender = Column(String, nullable=False)  # 성별 구분 (men/women/any)
    major_category = Column(String, nullable=False)  # 주요 소재 대분류
    minor_category = Column(String, nullable=False)  # 주요 소재 중분류
    hs_code = Column(String(10), nullable=False)  # HS부호
    is_active = Column(Boolean, default=True)  # 활성화 여부
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 