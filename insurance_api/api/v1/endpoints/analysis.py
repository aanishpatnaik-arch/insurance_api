from fastapi import APIRouter, Depends, Query, Body, HTTPException
from typing import List, Optional, Dict, Any
from insurance_api.models.analysis import AggregationRequest, OutlierResponse, Region
from insurance_api.services.analysis_service import AnalysisService, analysis_service

router = APIRouter()

@router.post("/aggregate", response_model=List[Dict[str, Any]], tags=["Analysis"])
async def dynamic_aggregation(
    request: AggregationRequest = Body(...),
    service: AnalysisService = Depends(lambda: analysis_service)
):
    """Performs dynamic grouping and aggregation on the insurance dataset."""
    if not request.group_by:
        raise HTTPException(status_code=400, detail="'group_by' cannot be empty.")
    
    result = service.perform_aggregation(
        group_by_cols=[col.value for col in request.group_by],
        agg_cols=[col.value for col in request.aggregations.columns],
        agg_funcs=request.aggregations.functions
    )
    return result

@router.get("/outliers", response_model=OutlierResponse, tags=["Analysis"])
async def find_charge_outliers(
    region: Optional[Region] = Query(None, description="Filter results by region."),
    service: AnalysisService = Depends(lambda: analysis_service)
):
    """Identifies individuals with statistically high charges for their group."""
    region_value = region.value if region else None
    return service.find_outliers(region=region_value)