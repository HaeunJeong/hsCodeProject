from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    code: str      # 계정코드
    role: str = "client"  # "admin" 또는 "client"
    isActive: bool = True

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    role: Optional[str] = None
    isActive: Optional[bool] = None

class AccountResponse(AccountBase):
    id: int
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True 