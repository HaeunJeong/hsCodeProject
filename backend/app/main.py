from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import accounts, templates
from .api import auth
from . import models
from .database import engine

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(templates.router, prefix="/templates", tags=["templates"]) 