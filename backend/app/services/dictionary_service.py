from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Dictionary

class DictionaryService:
    @staticmethod
    async def create_dictionary_entry(
        db: Session,
        keyword: str,
        category: str,
        hs_code: str,
        description: Optional[str] = None
    ) -> Dictionary:
        """새로운 사전 항목을 생성합니다."""
        db_entry = Dictionary(
            keyword=keyword,
            category=category,
            hs_code=hs_code,
            description=description
        )
        db.add(db_entry)
        await db.commit()
        await db.refresh(db_entry)
        return db_entry

    @staticmethod
    async def get_dictionary_entries(
        db: Session,
        category: Optional[str] = None
    ) -> List[Dictionary]:
        """사전 항목들을 조회합니다."""
        query = db.query(Dictionary)
        if category:
            query = query.filter(Dictionary.category == category)
        return await query.all()

    @staticmethod
    async def update_dictionary_entry(
        db: Session,
        entry_id: int,
        **kwargs
    ) -> Optional[Dictionary]:
        """사전 항목을 업데이트합니다."""
        entry = await db.query(Dictionary).filter(Dictionary.id == entry_id).first()
        if not entry:
            return None
        
        for key, value in kwargs.items():
            setattr(entry, key, value)
        
        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def delete_dictionary_entry(
        db: Session,
        entry_id: int
    ) -> bool:
        """사전 항목을 삭제합니다."""
        entry = await db.query(Dictionary).filter(Dictionary.id == entry_id).first()
        if not entry:
            return False
        
        await db.delete(entry)
        await db.commit()
        return True 