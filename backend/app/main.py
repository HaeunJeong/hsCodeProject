from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .models import Account
from .schemas import Account as AccountSchema, AccountCreate, AccountUpdate
from . import database, utils
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, dictionary, mapping_rules

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 API 라우터 포함
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(dictionary.router, prefix="/api/v1", tags=["dictionary"])
app.include_router(mapping_rules.router, prefix="/api/v1", tags=["mapping-rules"])

# 계정 관리 API
@app.post("/accounts", response_model=AccountSchema)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # 계정 코드 생성
    while True:
        code = utils.generate_account_code()
        existing = db.query(Account).filter(Account.code == code).first()
        if not existing:
            break
    
    db_account = Account(**account.dict(), code=code)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/accounts", response_model=List[AccountSchema])
def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = db.query(Account).offset(skip).limit(limit).all()
    return accounts

@app.get("/accounts/{account_id}", response_model=AccountSchema)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.put("/accounts/{account_id}", response_model=AccountSchema)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    update_data = account.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@app.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(db_account)
    db.commit()
    return None 