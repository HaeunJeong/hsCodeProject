from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AccountBase(BaseModel):
    name: str
    isActive: bool = True

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    name: Optional[str] = None
    isActive: Optional[bool] = None

class Account(AccountBase):
    id: int
    code: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True

# Excel 관련 스키마
class ExcelData(BaseModel):
    content: str

class ExcelResponse(BaseModel):
    result: str

# User 관련 스키마
class UserBase(BaseModel):
    email: EmailStr
    isAdmin: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    isAdmin: bool
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str 