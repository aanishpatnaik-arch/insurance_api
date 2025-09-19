from contextlib import asynccontextmanager
from fastapi import FastAPI
from insurance_api.api.router import router as api_router
from insurance_api.services.ml_service import ml_service



app = FastAPI(
    title="Insurance Analysis API",
    description="A robust API for analyzing insurance data and predicting charges.",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/hbtChk", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Insurance Analysis API"}