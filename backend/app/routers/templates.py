from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
from typing import Optional

router = APIRouter()

TEMPLATE_DIR = "templates"
TEMPLATE_FILE = "template.xlsx"
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, TEMPLATE_FILE)

# 디렉토리가 없으면 생성
os.makedirs(TEMPLATE_DIR, exist_ok=True)

@router.get("/download")
async def download_template():
    """템플릿 파일 다운로드"""
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=404, detail="템플릿 파일이 존재하지 않습니다.")
    
    return FileResponse(
        TEMPLATE_PATH,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=TEMPLATE_FILE
    )

@router.post("/upload")
async def upload_template(file: UploadFile = File(...)):
    """템플릿 파일 업로드"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="엑셀 파일만 업로드 가능합니다.")
    
    try:
        with open(TEMPLATE_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {str(e)}")
    finally:
        file.file.close()
    
    return {"message": "템플릿이 성공적으로 업로드되었습니다."} 