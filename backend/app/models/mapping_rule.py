from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
from ..core.database import Base

class MappingRule(Base):
    __tablename__ = "mapping_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # 룰 이름
    category = Column(String, index=True)  # 적용 카테고리
    conditionField = Column(String)  # 조건 필드 (예: name, description 등)
    conditionType = Column(String)  # 조건 타입 (contains, equals, startswith 등)
    conditionValue = Column(String)  # 조건 값
    hsCode = Column(String, index=True)  # 매핑될 HS 코드
    priority = Column(Integer, default=0)  # 우선순위 (높을수록 먼저 적용)
    isActive = Column(Boolean, default=True)  # 활성화 여부
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 