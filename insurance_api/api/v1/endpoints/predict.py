from fastapi import APIRouter, Depends
from insurance_api.models.predict import PredictionInput, PredictionOutput
from insurance_api.services.ml_service import MLService, ml_service

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict_charge(
    input_data: PredictionInput,
    model_service: MLService = Depends(lambda: ml_service)
):
    prediction = model_service.predict(
        age=input_data.age,
        bmi=input_data.bmi,
        is_smoker=input_data.is_smoker
    )
    return {"predicted_charge": prediction}