from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models import Account
from ..schemas.account import AccountCreate, AccountUpdate, AccountResponse
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """새 계정 생성"""
    # 코드 중복 검증
    existing_code = db.query(Account).filter(Account.code == account.code).first()
    if existing_code:
        raise HTTPException(
            status_code=400, 
            detail="이미 존재하는 계정 코드입니다. 다른 코드를 사용해주세요."
        )
    
    db_account = Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=List[AccountResponse])
def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """계정 목록 조회"""
    accounts = db.query(Account).offset(skip).limit(limit).all()
    return accounts

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    """특정 계정 조회"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    return account

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    """계정 정보 수정"""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    
    # 코드를 변경하는 경우 중복 검증
    if account.code and account.code != db_account.code:
        existing_code = db.query(Account).filter(Account.code == account.code).first()
        if existing_code:
            raise HTTPException(
                status_code=400, 
                detail="이미 존재하는 계정 코드입니다. 다른 코드를 사용해주세요."
            )
    
    update_data = account.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """계정 삭제"""
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다")
    
    db.delete(db_account)
    db.commit()
    return None 