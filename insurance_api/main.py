from fastapi import FastAPI
from insurance_api.api.router import router as api_router
from insurance_api.services.ml_service import ml_service

app = FastAPI(
    title="Insurance Analysis API ",
    description="A robust API for analyzing insurance data and predicting charges.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Event handler to train the model on application startup."""
    ml_service.get_model() # This will trigger the training if the model isn't loaded

app.include_router(api_router)

@app.get("/", tags=["Root"])
async def read_root():
    """A welcome message to check if the API is running."""
    return {"message": "Welcome to the Insurance Analysis API"}