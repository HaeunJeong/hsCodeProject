from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, excel
from app.core.database import Base, engine, SessionLocal
from app.core.init_db import init_db
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 초기 데이터 생성
db = SessionLocal()
try:
    init_db(db)
finally:
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 설정
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(excel.router, prefix=settings.API_V1_STR + "/excel", tags=["excel"])

@app.get("/")
async def root():
    return {"message": "의류 HS코드 자동 분류 시스템 API"}

# 상태 확인 엔드포인트
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 