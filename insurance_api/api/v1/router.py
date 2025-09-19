from fastapi import APIRouter
from insurance_api.api.v1.endpoints import predict, analysis

router = APIRouter()
router.include_router(predict.router)
router.include_router(analysis.router)