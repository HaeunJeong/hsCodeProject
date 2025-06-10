from typing import Optional
from datetime import datetime, timedelta
import secrets
from sqlalchemy.orm import Session
from ..models import AccessCode

class AccessCodeService:
    @staticmethod
    async def generate_access_code(
        db: Session,
        expires_in_days: Optional[int] = 30
    ) -> AccessCode:
        """새로운 접속 코드를 생성합니다."""
        code = secrets.token_urlsafe(8)  # 8바이트 길이의 랜덤 코드 생성
        expiresAt = datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None
        
        db_code = AccessCode(
            code=code,
            expiresAt=expiresAt
        )
        db.add(db_code)
        await db.commit()
        await db.refresh(db_code)
        return db_code

    @staticmethod
    async def validate_access_code(
        db: Session,
        code: str
    ) -> bool:
        """접속 코드의 유효성을 검증합니다."""
        db_code = await db.query(AccessCode).filter(
            AccessCode.code == code,
            AccessCode.isActive == True
        ).first()

        if not db_code:
            return False

        # 만료 시간 체크
        if db_code.expiresAt and db_code.expiresAt < datetime.utcnow():
            db_code.isActive = False
            await db.commit()
            return False

        # 마지막 사용 시간 업데이트
        db_code.lastUsedAt = datetime.utcnow()
        await db.commit()
        return True

    @staticmethod
    async def deactivate_access_code(
        db: Session,
        code: str
    ) -> bool:
        """접속 코드를 비활성화합니다."""
        db_code = await db.query(AccessCode).filter(AccessCode.code == code).first()
        if not db_code:
            return False

        db_code.isActive = False
        await db.commit()
        return True 