from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

# --- Models for Aggregation ---
class NumericColumn(str, Enum):
    age = 'age'
    bmi = 'bmi'
    charges = 'charges'

class GroupByColumn(str, Enum):
    sex = 'sex'
    smoker = 'smoker'
    region = 'region'
    children = 'children'

class Aggregation(BaseModel):
    columns: List[NumericColumn] = Field(..., description="Numeric columns to aggregate.")
    functions: List[str] = Field(..., description="List of aggregation functions (e.g., ['mean', 'std']).")

class AggregationRequest(BaseModel):
    group_by: List[GroupByColumn] = Field(..., description="Columns to group by.")
    aggregations: Aggregation

# --- Models for Outliers ---
class Region(str, Enum):
    southwest = "southwest"
    southeast = "southeast"
    northwest = "northwest"
    northeast = "northeast"

class Outlier(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str
    charges: float
    reason: str

class OutlierResponse(BaseModel):
    filter_region: Optional[str]
    outlier_count: int
    outliers: List[Outlier]