from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base

class MaterialClassification(Base):
    __tablename__ = "material_classifications"

    id = Column(Integer, primary_key=True, index=True)
    material_name = Column(String, unique=True, index=True, nullable=False)  # 상세 소재명
    major_category = Column(String, nullable=False)  # 대분류
    minor_category = Column(String, nullable=False)  # 중분류
    
    def __repr__(self):
        return f"<MaterialClassification(material_name='{self.material_name}', major_category='{self.major_category}', minor_category='{self.minor_category}')>" 