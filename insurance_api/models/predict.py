from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    age: int = Field(..., gt=0, description="Age of the person.")
    bmi: float = Field(..., gt=0, description="Body Mass Index (BMI).")
    is_smoker: bool = Field(..., description="Whether the person is a smoker.")

class PredictionOutput(BaseModel):
    predicted_charge: float