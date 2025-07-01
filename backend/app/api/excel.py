from fastapi import APIRouter
from ..routers import hs_classification

router = APIRouter()

# HS 분류 라우터를 포함
router.include_router(hs_classification.router, prefix="/hs-classification", tags=["hs-classification"]) 