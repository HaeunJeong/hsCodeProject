from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from typing import List, Optional
from ..models.fabric_component import FabricComponent
from ..schemas.fabric_component import (
    FabricComponentCreate, 
    FabricComponentUpdate, 
    FabricComponentResponse,
    CategoryInfo
)
from app.core.database import get_db
from ..api.auth import get_current_account
from ..models import Account
from ..utils.fabric_category_loader import (
    get_major_categories_from_json,
    get_minor_categories_from_json
)

router = APIRouter()

@router.get("/", response_model=List[FabricComponentResponse])
def get_fabric_components(
    major_category_code: Optional[str] = Query(None, description="대분류 코드"),
    minor_category_code: Optional[str] = Query(None, description="중분류 코드"), 
    component_name_en: Optional[str] = Query(None, description="성분 영문명"),
    component_name_ko: Optional[str] = Query(None, description="성분 한글명"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """의류 성분 사전 목록 조회"""
    query = db.query(FabricComponent)
    
    # 성분명으로 검색하는 경우 카테고리 조건 무시
    if component_name_en or component_name_ko:
        if component_name_en:
            query = query.filter(FabricComponent.component_name_en.ilike(f"%{component_name_en}%"))
        if component_name_ko:
            query = query.filter(FabricComponent.component_name_ko.ilike(f"%{component_name_ko}%"))
    else:
        # 카테고리 조건 적용
        if major_category_code and major_category_code != "all":
            query = query.filter(FabricComponent.major_category_code == major_category_code)
        if minor_category_code and minor_category_code != "all":
            query = query.filter(FabricComponent.minor_category_code == minor_category_code)
    
    components = query.offset(skip).limit(limit).all()
    return components

@router.get("/major-categories", response_model=List[CategoryInfo])
def get_major_categories(
    current_account: Account = Depends(get_current_account)
):
    """대분류 목록 조회 (JSON 파일 기반)"""
    categories = get_major_categories_from_json()
    return [{"code": cat["major_category_code"], "name": cat["major_category_name"]} for cat in categories]

@router.get("/minor-categories", response_model=List[CategoryInfo])
def get_minor_categories(
    major_category_code: Optional[str] = Query(None, description="대분류 코드"),
    current_account: Account = Depends(get_current_account)
):
    """중분류 목록 조회 (JSON 파일 기반)"""
    # major_category_code로 필터링 가능
    categories = get_minor_categories_from_json(major_category_code)
    return [{"code": cat["minor_category_code"], "name": cat["minor_category_name"]} for cat in categories]

@router.post("/", response_model=FabricComponentResponse)
def create_fabric_component(
    component: FabricComponentCreate, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """의류 성분 생성"""
    # 중복 검증
    existing = db.query(FabricComponent).filter(
        FabricComponent.major_category_code == component.major_category_code,
        FabricComponent.minor_category_code == component.minor_category_code,
        FabricComponent.component_name_en == component.component_name_en
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="이미 존재하는 성분입니다."
        )
    
    db_component = FabricComponent(**component.model_dump())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component

@router.get("/{component_id}", response_model=FabricComponentResponse)
def get_fabric_component(
    component_id: int, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """특정 의류 성분 조회"""
    component = db.query(FabricComponent).filter(FabricComponent.id == component_id).first()
    if component is None:
        raise HTTPException(status_code=404, detail="성분을 찾을 수 없습니다")
    return component

@router.put("/{component_id}", response_model=FabricComponentResponse)
def update_fabric_component(
    component_id: int, 
    component: FabricComponentUpdate, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """의류 성분 수정"""
    db_component = db.query(FabricComponent).filter(FabricComponent.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="성분을 찾을 수 없습니다")
    
    update_data = component.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_component, key, value)
    
    db.commit()
    db.refresh(db_component)
    return db_component

@router.delete("/{component_id}")
def delete_fabric_component(
    component_id: int, 
    db: Session = Depends(get_db),
    current_account: Account = Depends(get_current_account)
):
    """의류 성분 삭제"""
    db_component = db.query(FabricComponent).filter(FabricComponent.id == component_id).first()
    if db_component is None:
        raise HTTPException(status_code=404, detail="성분을 찾을 수 없습니다")
    
    db.delete(db_component)
    db.commit()
    return {"message": "성분이 삭제되었습니다"} 