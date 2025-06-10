from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from app.core.database import get_db
from app.models.product import Product
from app.models.dictionary import Dictionary
import io
from fastapi.responses import FileResponse
from datetime import datetime
import os
from tempfile import NamedTemporaryFile
from ..schemas.excel import ExcelData, ExcelResponse
from ..core.config import settings
import logging
import traceback

# 로거 설정
logger = logging.getLogger(__name__)

router = APIRouter()

def map_hs_code(structure: str, gender: str, category: str, composition: str) -> str:
    """
    HS코드 매핑 규칙:
    - 조직구조: 니트 61 / 우븐 62
    - 성별: 남성 05 / 여성 06
    - 제품 분류: 외투 0001 / 바지 0002 등
    - 성분 비율에 따라 분류
    """
    # 기본 구조 매핑
    base_code = "61" if structure.lower() == "니트" else "62"
    
    # 성별 매핑
    gender_code = "05" if gender.lower() == "남성" else "06"
    
    # 카테고리 매핑 (임시 매핑, 실제 규칙은 추후 업데이트 필요)
    category_mapping = {
        "자켓": "0001",
        "바지": "0002",
        "스웨터": "0003",
        "점퍼": "0004",
        "원피스": "0005"
    }
    category_code = category_mapping.get(category, "0000")
    
    # 전체 HS코드 조합
    hs_code = f"{base_code}{gender_code}{category_code}"
    
    return hs_code

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="올바른 엑셀 파일이 아닙니다.")
    
    temp_file = None
    try:
        # 임시 파일로 저장
        temp_file = NamedTemporaryFile(delete=False, suffix='.xlsx')
        contents = await file.read()
        temp_file.write(contents)
        temp_file.seek(0)
        
        logger.info(f"파일 '{file.filename}' 업로드 시작")
        
        try:
            # pandas로 엑셀 파일 읽기
            df = pd.read_excel(temp_file.name)
            
            # 필수 컬럼 확인
            required_columns = ['상품명', '성분']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=400, 
                    detail=f"필수 컬럼이 없습니다: {', '.join(missing_columns)}"
                )
            
            # HS코드 컬럼 추가 (빈 값으로)
            df['HS코드'] = ''
            
            logger.info(f"엑셀 파일 읽기 성공. 컬럼: {list(df.columns)}")
            
            # 데이터 변환
            excel_data = []
            for _, row in df.iterrows():
                # 모든 컬럼의 데이터를 딕셔너리로 변환
                row_dict = row.to_dict()
                # NaN 값을 빈 문자열로 변환
                row_dict = {k: str(v) if pd.notna(v) else '' for k, v in row_dict.items()}
                excel_data.append(ExcelData(row=row_dict))
            
            logger.info(f"파일 '{file.filename}' 처리 완료. {len(excel_data)}개의 행이 처리됨")
            
            return {
                "success": True,
                "data": excel_data,
                "message": f"엑셀 파일이 성공적으로 업로드되었습니다. {len(excel_data)}개의 행이 처리되었습니다."
            }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"엑셀 파일 읽기 실패: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=f"엑셀 파일을 읽을 수 없습니다: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"파일 처리 중 예외 발생: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"파일 처리 중 오류가 발생했습니다: {str(e)}")
    finally:
        if temp_file:
            try:
                os.unlink(temp_file.name)
                logger.info("임시 파일 삭제 완료")
            except Exception as e:
                logger.error(f"임시 파일 삭제 실패: {str(e)}")

@router.post("/export")
async def export_excel(data: List[ExcelData]):
    try:
        # 모든 행의 키를 수집하여 전체 컬럼 목록 생성
        all_columns = set()
        for item in data:
            all_columns.update(item.row.keys())
        
        # HS코드 컬럼이 없는 경우 추가
        if 'HS코드' not in all_columns:
            all_columns.add('HS코드')
        
        # DataFrame 생성
        rows = []
        for item in data:
            row_data = {col: item.row.get(col, '') for col in all_columns}
            rows.append(row_data)
        
        df = pd.DataFrame(rows)
        
        # 컬럼 순서 조정 (HS코드를 마지막 컬럼으로)
        if 'HS코드' in df.columns:
            cols = [col for col in df.columns if col != 'HS코드'] + ['HS코드']
            df = df[cols]
        
        # 임시 파일로 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"export_{timestamp}.xlsx"
        temp_path = os.path.join(settings.TEMP_DIR, filename)
        
        # 디렉토리가 없으면 생성
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        
        # 엑셀 파일로 저장
        df.to_excel(temp_path, index=False, engine='openpyxl')
        logger.info(f"엑셀 파일 생성 완료: {filename}")
        
        return FileResponse(
            temp_path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"엑셀 파일 생성 중 오류 발생: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"파일 생성 중 오류가 발생했습니다: {str(e)}")

@router.get("/template")
async def download_template():
    try:
        # 고정된 컬럼으로 데이터프레임 생성 (HS코드 제외)
        df = pd.DataFrame(columns=[
            '상품명', '성분'
        ])
        
        # 임시 파일로 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"template_{timestamp}.xlsx"
        temp_path = os.path.join(settings.TEMP_DIR, filename)
        
        # 디렉토리가 없으면 생성
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
        
        # 엑셀 파일로 저장
        df.to_excel(temp_path, index=False, engine='openpyxl')
        logger.info(f"템플릿 파일 생성 완료: {filename}")
        
        return FileResponse(
            temp_path,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            filename="excel_template.xlsx"
        )
        
    except Exception as e:
        logger.error(f"템플릿 파일 생성 중 오류 발생: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"템플릿 파일 생성 중 오류가 발생했습니다: {str(e)}")

@router.post("/map-hs-codes")
async def map_hs_codes(data: List[ExcelData]):
    """
    엑셀 데이터에 HS 코드를 매핑하는 엔드포인트
    현재는 mockup으로 임의의 HS 코드를 반환
    """
    try:
        # 각 행에 임의의 HS 코드 매핑 (mockup)
        for item in data:
            # 실제 매핑 로직은 나중에 구현
            # 기존 HS코드가 있으면 업데이트
            item.row['HS코드'] = '6106.10.0000'  # 임시 코드
        
        return {
            "success": True,
            "data": data,
            "message": "HS 코드 매핑이 완료되었습니다."
        }
    except Exception as e:
        logger.error(f"HS 코드 매핑 중 오류 발생: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"HS 코드 매핑 중 오류가 발생했습니다: {str(e)}") 