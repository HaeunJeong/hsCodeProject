from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from datetime import datetime

# 예약어 목록 (의류 부위 라벨)
RESERVED_WORDS = {'SHELL', 'MAIN', 'RIB', 'LINING', 'ATTACHED'}

class FabricComponentBase(BaseModel):
    major_category_code: str
    major_category_name: str
    minor_category_code: str
    minor_category_name: str
    component_name_en: str
    component_name_ko: Optional[str] = None

    @field_validator('component_name_en')
    @classmethod
    def validate_component_name_en(cls, v):
        if v and v.strip().upper() in RESERVED_WORDS:
            raise ValueError(f"'{v}'는 예약어로 사용할 수 없습니다. 예약어: {', '.join(RESERVED_WORDS)}")
        return v

class FabricComponentCreate(FabricComponentBase):
    pass

class FabricComponentUpdate(BaseModel):
    major_category_code: Optional[str] = None
    major_category_name: Optional[str] = None
    minor_category_code: Optional[str] = None
    minor_category_name: Optional[str] = None
    component_name_en: Optional[str] = None
    component_name_ko: Optional[str] = None

    @field_validator('component_name_en')
    @classmethod
    def validate_component_name_en(cls, v):
        if v and v.strip().upper() in RESERVED_WORDS:
            raise ValueError(f"'{v}'는 예약어로 사용할 수 없습니다. 예약어: {', '.join(RESERVED_WORDS)}")
        return v

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