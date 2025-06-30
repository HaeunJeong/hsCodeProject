from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class AccessCodeCreate(BaseModel):
    code: str
    role: str
    expiresAt: Optional[str] = None 