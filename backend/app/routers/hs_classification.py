from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import pandas as pd
from app.core.database import get_db
from ..api.auth import get_current_account

router = APIRouter()

# 양식 파일 경로
TEMPLATE_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "resource", "templates", "excel_upload_template.xlsx")

@router.get("/template")
async def download_template():
    """HS코드 분류 양식 다운로드"""
    if not os.path.exists(TEMPLATE_FILE_PATH):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    return FileResponse(
        path=TEMPLATE_FILE_PATH,
        filename="hs_code_template.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_account = Depends(get_current_account),
    db: Session = Depends(get_db)
):
    """파일 업로드 및 HS코드 분류 처리"""
    # 파일 형식 검증
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Excel 파일만 업로드 가능합니다.")
    
    try:
        # 파일 읽기
        contents = await file.read()
        
        # pandas로 엑셀 파일 읽기 (첫 번째 행을 헤더로 사용)
        df = pd.read_excel(contents, header=0)
        
        # 기본적인 데이터 검증
        if df.empty:
            raise HTTPException(status_code=400, detail="빈 파일입니다.")
        
        # HS분류 서비스 초기화
        from ..services.hs_classification_service import HSClassificationService
        hs_service = HSClassificationService(db)
        
        # 1. 템플릿 양식 검증
        template_df = pd.read_excel(TEMPLATE_FILE_PATH, header=0)
        validation_result = hs_service.validate_template(df, template_df)
        
        if not validation_result["valid"]:
            # 오류 타입에 따라 메시지 결정
            if validation_result.get("error_type") == "template":
                message = "템플릿 양식 검증 실패"
            else:  # data 오류 또는 기타
                message = "필수 정보 누락"
            
            return {
                "success": False,
                "message": message,
                "data": {
                    "filename": file.filename,
                    "validation_errors": validation_result["errors"]
                }
            }
        
        # 2. HS코드 분류 수행
        classification_results = hs_service.classify_products(df)
        
        # 3. 성공/실패 통계 계산
        total_count = len(classification_results)
        success_count = len([r for r in classification_results if r["hs_code"] != "unknown"])
        failed_count = total_count - success_count
        
        return {
            "success": True,
            "message": f"HS코드 분류가 완료되었습니다. (성공: {success_count}, 실패: {failed_count})",
            "data": {
                "filename": file.filename,
                "total_count": total_count,
                "success_count": success_count,
                "failed_count": failed_count,
                "results": classification_results
            }
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="유효하지 않은 엑셀 파일입니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류가 발생했습니다: {str(e)}") 