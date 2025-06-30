from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.hs_code_service import HsCodeService
from app.schemas.mapping import MappingRuleRequest, MappingRuleResponse

router = APIRouter(prefix="/api/v1/mapping", tags=["mapping"])

@router.post("/map-to-hs-code", response_model=List[MappingRuleResponse])
async def map_to_hs_code(
    request: List[MappingRuleRequest],
    db: Session = Depends(get_db)
):
    """
    매핑 규칙 리스트를 받아서 각 항목의 HS코드를 매핑하여 반환
    """
    try:
        hs_code_service = HsCodeService(db)
        results = []
        
        for item in request:
            # HS코드 매핑 수행
            hs_code = hs_code_service.map_to_hs_code(
                fabric_type=item.fabricType,
                category=item.category,
                gender=item.gender,
                material_detail=item.materialDetail
            )
            
            # 결과 생성
            result = MappingRuleResponse(
                styleNo=item.styleNo,
                name=item.name,
                fabricType=item.fabricType,
                category=item.category,
                gender=item.gender,
                materialDetail=item.materialDetail,
                hsCode=hs_code,
                note=item.note
            )
            results.append(result)
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HS코드 매핑 중 오류가 발생했습니다: {str(e)}")

@router.post("/single-map")
async def single_map_to_hs_code(
    request: MappingRuleRequest,
    db: Session = Depends(get_db)
):
    """
    단일 항목의 HS코드 매핑
    """
    try:
        hs_code_service = HsCodeService(db)
        
        hs_code = hs_code_service.map_to_hs_code(
            fabric_type=request.fabricType,
            category=request.category,
            gender=request.gender,
            material_detail=request.materialDetail
        )
        
        return {"hsCode": hs_code}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"HS코드 매핑 중 오류가 발생했습니다: {str(e)}") 