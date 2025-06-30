from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models.standard_category import StandardCategory
from ..schemas.standard_category import StandardCategoryUpdate, StandardCategoryResponse
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[StandardCategoryResponse])
def get_standard_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """표준 카테고리 목록 조회"""
    categories = db.query(StandardCategory).offset(skip).limit(limit).all()
    return categories

@router.put("/{category_id}", response_model=StandardCategoryResponse)
def update_standard_category(category_id: int, category: StandardCategoryUpdate, db: Session = Depends(get_db)):
    """표준 카테고리 수정 (한글명, 설명, 포함단어만 수정 가능)"""
    db_category = db.query(StandardCategory).filter(StandardCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category 