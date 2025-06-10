from sqlalchemy.orm import Session
from app.models.access_code import AccessCode
from datetime import datetime, timedelta

def init_db(db: Session) -> None:
    # 기본 관리자 코드 생성
    admin_code = db.query(AccessCode).filter(
        AccessCode.code == "admin123",
        AccessCode.role == "admin"
    ).first()
    
    if not admin_code:
        admin_code = AccessCode(
            code="admin123",
            role="admin",
            is_active=True
        )
        db.add(admin_code)
        db.commit()
        print("기본 관리자 코드가 생성되었습니다: admin123")
    else:
        print("관리자 코드가 이미 존재합니다.")

    # 기존 관리자 코드가 있는지 확인
    admin_code = db.query(AccessCode).filter(
        AccessCode.role == "admin",
        AccessCode.is_active == True
    ).first()

    # 관리자 코드가 없으면 생성
    if not admin_code:
        admin_code = AccessCode(
            code="admin123",  # 초기 관리자 코드
            role="admin",
            is_active=True,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=365)  # 1년 후 만료
        )
        db.add(admin_code)
        db.commit()
        print("기본 관리자 코드가 생성되었습니다: admin123")
    else:
        print("관리자 코드가 이미 존재합니다.") 