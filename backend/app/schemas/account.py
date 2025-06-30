from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    role: str = "client"  # "admin" 또는 "client"

class AccountCreate(AccountBase):
    code: str  # 수동 입력받는 코드

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    role: Optional[str] = None
    isActive: Optional[bool] = None

class AccountResponse(AccountBase):
    id: int
    code: str
    isActive: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True 