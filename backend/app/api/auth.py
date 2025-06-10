from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.database import get_db
from app.models.user import User
from app.models.access_code import AccessCode
from app.models import Account
from app.schemas import Token, UserCreate, User as UserSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ADMIN_CODE = "admin123"

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

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
            "role": "user",
            "access_token": create_access_token(subject=code),
            "token_type": "bearer",
            "expiresAt": (datetime.now() + timedelta(days=1)).isoformat()
        }
    }

@router.get("/codes")
async def get_access_codes(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all access codes (admin only)
    """
    codes = db.query(AccessCode).all()
    return {
        "success": True,
        "data": codes
    }

@router.post("/codes")
async def create_access_code(
    *,
    db: Session = Depends(get_db),
    code: str = Body(...),
    role: str = Body(...),
    expires_at: str = Body(None)
) -> Any:
    """
    Create new access code (admin only)
    """
    db_code = AccessCode(
        code=code,
        role=role,
        expires_at=datetime.fromisoformat(expires_at) if expires_at else None
    )
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    
    return {
        "success": True,
        "data": db_code
    }

@router.post("/deactivate")
async def deactivate_access_code(
    *,
    db: Session = Depends(get_db),
    code: str = Body(..., embed=True)
) -> Any:
    """
    Deactivate access code (admin only)
    """
    db_code = db.query(AccessCode).filter(AccessCode.code == code).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Access code not found")
    
    db_code.is_active = False
    db.commit()
    
    return {
        "success": True,
        "data": True
    }

@router.post("/register", response_model=UserSchema)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    from app.core.security import get_password_hash
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 