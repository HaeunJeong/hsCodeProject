from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.database import engine, Base
from app.routers import accounts, standard_categories, fabric_components, hs_classification
from app.api import auth, excel
from app.models.standard_category import StandardCategory
from app.models.hs_code_rule import HSCodeRule

app = FastAPI(title="HS Code Classification System", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Pydantic validation 에러를 400으로 변경하고 사용자 친화적 메시지 제공
    error_messages = []
    for error in exc.errors():
        field = error.get('loc', [''])[-1]  # 필드명
        message = error.get('msg', '')      # 에러 메시지
        
        # value_error인 경우 (예약어 검증 등) 깔끔한 메시지 추출
        if error.get('type') == 'value_error':
            if '예약어로 사용할 수 없습니다' in message:
                # "Value error, " 접두사 제거
                clean_message = message.replace("Value error, ", "")
                error_messages.append(clean_message)
            else:
                clean_message = message.replace("Value error, ", "")
                error_messages.append(f"{field}: {clean_message}")
        else:
            error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": error_messages[0] if error_messages else "입력값이 올바르지 않습니다.",
            "errors": error_messages
        }
    )

# 라우터 등록
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(standard_categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(fabric_components.router, prefix="/api/v1/fabric-components", tags=["fabric-components"])
app.include_router(hs_classification.router, prefix="/api/v1/hs-classification", tags=["hs-classification"])
app.include_router(excel.router, prefix="/api/v1/excel", tags=["excel"])


@app.get("/")
async def root():
    return {"message": "HS Code Classification System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 