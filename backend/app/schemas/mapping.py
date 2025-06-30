from pydantic import BaseModel
from typing import Optional

class MappingRuleRequest(BaseModel):
    styleNo: str
    name: str
    fabricType: str
    category: str
    gender: str
    materialDetail: str
    note: Optional[str] = ""

class MappingRuleResponse(BaseModel):
    styleNo: str
    name: str
    fabricType: str
    category: str
    gender: str
    materialDetail: str
    hsCode: str
    note: Optional[str] = ""

class MaterialClassificationSchema(BaseModel):
    id: Optional[int] = None
    material_name: str
    major_category: str
    minor_category: str

class StandardCategorySchema(BaseModel):
    id: Optional[int] = None
    item_name: str
    standard_category: str

class HsCodeRuleSchema(BaseModel):
    id: Optional[int] = None
    fabric_type: str
    standard_category: str
    gender: str
    major_material: str
    minor_material: str
    hs_code: str
    priority: int = 0 