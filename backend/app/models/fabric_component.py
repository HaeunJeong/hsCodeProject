from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class FabricComponent(Base):
    __tablename__ = "fabric_components"

    id = Column(Integer, primary_key=True, index=True)
    major_category_code = Column(String(20), nullable=False, index=True)  # 대분류 코드
    major_category_name = Column(String(100), nullable=False)             # 대분류명
    minor_category_code = Column(String(20), nullable=False, index=True)  # 중분류 코드  
    minor_category_name = Column(String(100), nullable=False)             # 중분류명
    component_name_en = Column(String(100), nullable=False, index=True)   # 성분 영문명
    component_name_ko = Column(String(100), nullable=True)                # 성분 한글명
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 