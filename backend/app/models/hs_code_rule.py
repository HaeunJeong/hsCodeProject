from sqlalchemy import Column, Integer, String
from app.database import Base

class HsCodeRule(Base):
    __tablename__ = "hs_code_rules"

    id = Column(Integer, primary_key=True, index=True)
    fabric_type = Column(String, nullable=False)  # knit, woven
    standard_category = Column(String, nullable=False)  # 표준 카테고리
    gender = Column(String, nullable=False)  # men, women, any
    major_material = Column(String, nullable=False)  # 주요소재 대분류
    minor_material = Column(String, nullable=False)  # 주요소재 중분류
    hs_code = Column(String, nullable=False)  # HS코드
    priority = Column(Integer, default=0)  # 우선순위 (높을수록 우선)
    
    def __repr__(self):
        return f"<HsCodeRule(fabric_type='{self.fabric_type}', category='{self.standard_category}', hs_code='{self.hs_code}')>" 