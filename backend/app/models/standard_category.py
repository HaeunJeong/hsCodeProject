from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class StandardCategory(Base):
    __tablename__ = "standard_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String(10), unique=True, index=True, nullable=False)  # 카테고리 번호 (CAT001, CAT002 등)
    category_name_en = Column(String(100), nullable=False)  # 카테고리 영문명
    category_name_ko = Column(String(100), nullable=True)   # 카테고리 한글명 (수정 가능)
    description = Column(Text, nullable=True)               # 설명 (수정 가능)
    keywords = Column(Text, nullable=True)                  # 포함 단어 (수정 가능)
    
    def __repr__(self):
        return f"<StandardCategory(code='{self.category_code}', name_en='{self.category_name_en}', name_ko='{self.category_name_ko}')>" 