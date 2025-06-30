from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import accounts, mapping, standard_categories
from app.api import auth
from app.models.material_classification import MaterialClassification
from app.models.standard_category import StandardCategory
from app.models.hs_code_rule import HsCodeRule

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

# 라우터 등록
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["accounts"])
app.include_router(standard_categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(mapping.router, prefix="/mapping", tags=["mapping"])

@app.get("/")
async def root():
    return {"message": "HS Code Classification System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 