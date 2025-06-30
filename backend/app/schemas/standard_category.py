from pydantic import BaseModel
from typing import Optional

class StandardCategoryBase(BaseModel):
    category_code: str
    category_name_en: str
    category_name_ko: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None

class StandardCategoryCreate(StandardCategoryBase):
    pass

class StandardCategoryUpdate(BaseModel):
    category_name_ko: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None

class StandardCategoryResponse(StandardCategoryBase):
    id: int

    class Config:
        from_attributes = True 