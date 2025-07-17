from fastapi import APIRouter, HTTPException
from services.data_processor import get_agencies, get_agencies_with_metrics, get_agency_metrics

router = APIRouter(prefix="/agencies", tags=["agencies"])

@router.get("")
def list_agencies():
    """Get list of all agencies"""
    return get_agencies()

@router.get("/with-metrics")
def list_agencies_with_metrics():
    """Get all agencies with their latest metrics in one call"""
    return get_agencies_with_metrics()

@router.get("/{aid}/latest")
def latest_metrics(aid: int):
    """Get latest metrics for a specific agency"""
    metrics = get_agency_metrics(aid)
    if not metrics:
        raise HTTPException(404, "No data found for this agency")
    return metrics 