from sqlalchemy import Column, Integer, String
from app.database import Base

class StandardCategory(Base):
    __tablename__ = "standard_categories"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, index=True, nullable=False)  # 품목명
    standard_category = Column(String, nullable=False)  # 표준 카테고리
    
    def __repr__(self):
        return f"<StandardCategory(item_name='{self.item_name}', standard_category='{self.standard_category}')>" 