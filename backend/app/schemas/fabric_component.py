from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FabricComponentBase(BaseModel):
    major_category_code: str
    major_category_name: str
    minor_category_code: str
    minor_category_name: str
    component_name_en: str
    component_name_ko: Optional[str] = None

class FabricComponentCreate(FabricComponentBase):
    pass

class FabricComponentUpdate(BaseModel):
    major_category_code: Optional[str] = None
    major_category_name: Optional[str] = None
    minor_category_code: Optional[str] = None
    minor_category_name: Optional[str] = None
    component_name_en: Optional[str] = None
    component_name_ko: Optional[str] = None

class FabricComponentResponse(FabricComponentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CategoryInfo(BaseModel):
    """카테고리 정보"""
    code: str
    name: str 