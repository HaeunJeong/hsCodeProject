from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models.standard_category import StandardCategory
from ..schemas.standard_category import StandardCategoryUpdate, StandardCategoryResponse
from app.core.database import get_db
from ..api.auth import get_current_account
from ..models import Account

router = APIRouter()

@router.get("/", response_model=List[StandardCategoryResponse])
def get_standard_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """표준 카테고리 목록 조회"""
    categories = db.query(StandardCategory).order_by(StandardCategory.id).offset(skip).limit(limit).all()
    return categories

@router.put("/{category_id}", response_model=StandardCategoryResponse)
def update_standard_category(
    category_id: int, 
    category: StandardCategoryUpdate, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """표준 카테고리 수정 (한글명, 설명, 포함단어만 수정 가능)"""
    db_category = db.query(StandardCategory).filter(StandardCategory.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다")
    
    update_data = category.model_dump(exclude_unset=True)
    
    # keywords 필드의 개행문자를 쉼표로 변환하고 공백 제거
    if 'keywords' in update_data and update_data['keywords']:
        keywords = update_data['keywords']
        # 개행문자를 쉼표로 변환
        keywords = keywords.replace('\n', ',')
        # 쉼표로 분리하여 각 단어의 앞뒤 공백 제거 후 다시 결합
        keywords_list = [keyword.strip() for keyword in keywords.split(',') if keyword.strip()]
        update_data['keywords'] = ', '.join(keywords_list)
        
        # 키워드 중복 체크
        if keywords_list:
            # 1. 같은 카테고리 내에서 중복 체크
            current_keywords_upper = [kw.strip().upper() for kw in keywords_list]
            
            # 중복 키워드 찾기
            seen = set()
            duplicates_within_category = []
            for kw in current_keywords_upper:
                if kw in seen:
                    duplicates_within_category.append(kw)
                else:
                    seen.add(kw)
            
            if duplicates_within_category:
                duplicate_list = ', '.join(duplicates_within_category)
                raise HTTPException(
                    status_code=400, 
                    detail=f"포함 단어가 중복됩니다. 중복 단어 : {duplicate_list}"
                )
            
            # 2. 다른 카테고리들의 키워드와 중복 확인
            other_categories = db.query(StandardCategory).filter(
                StandardCategory.id != category_id,
                StandardCategory.keywords.isnot(None)
            ).all()
            
            for other_cat in other_categories:
                if other_cat.keywords:
                    other_keywords = [kw.strip().upper() for kw in other_cat.keywords.split(',') if kw.strip()]
                    
                    # 중복 키워드 찾기
                    duplicates = set(current_keywords_upper) & set(other_keywords)
                    if duplicates:
                        duplicate_list = ', '.join(duplicates)
                        raise HTTPException(
                            status_code=400, 
                            detail=f"다른 카테고리에 이미 등록된 단어가 있습니다. 중복 단어 : {duplicate_list}"
                        )
    
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category 