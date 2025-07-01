from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.database import get_db
from app.models import Account
from app.schemas import Token, AccessCodeCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/validate")

ADMIN_CODE = "admin123"

def get_current_account(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Account:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        code: str = payload.get("sub")
        if code is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # admin123 코드의 경우 가상 Account 객체 반환
    if code == ADMIN_CODE:
        # 가상 admin 계정 객체 생성
        admin_account = Account()
        admin_account.id = 0
        admin_account.code = ADMIN_CODE
        admin_account.name = "관리자"
        admin_account.role = "admin"
        admin_account.isActive = True
        admin_account.createdAt = datetime.now()
        admin_account.updatedAt = datetime.now()
        return admin_account
    
    # 일반 계정의 경우 데이터베이스에서 조회
    account = db.query(Account).filter(Account.code == code).first()
    if account is None:
        raise credentials_exception
    return account

@router.post("/validate")
async def validate_access_code(
    *,
    db: Session = Depends(get_db),
    code: str = Body(..., embed=True)
) -> Any:
    # Account 테이블에서 코드 체크
    account = db.query(Account).filter(Account.code == code).first()
    
    # admin123 코드 체크 (항상 활성화)
    if code == ADMIN_CODE:
        return {
            "success": True,
            "data": {
                "accessCode": code,
                "role": "admin",
                "access_token": create_access_token(subject=code),
                "token_type": "bearer",
                "expiresAt": (datetime.now() + timedelta(days=1)).isoformat()
            }
        }
    
    # 계정이 존재하는지 체크
    if not account:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "유효하지 않은 접속코드입니다",
                "code": "INVALID_CODE"
            }
        )
    
    # 계정이 비활성화 상태인지 체크
    if not account.isActive:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "비활성화된 접속코드입니다",
                "code": "INACTIVE_CODE"
            }
        )
    
    # 유효한 계정인 경우
    return {
        "success": True,
        "data": {
            "accessCode": code,
            "role": account.role,
            "access_token": create_access_token(subject=code),
            "token_type": "bearer",
            "expiresAt": (datetime.now() + timedelta(days=1)).isoformat()
        }
    }
