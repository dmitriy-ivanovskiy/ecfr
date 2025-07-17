from fastapi import APIRouter
from services.data_processor import get_summary_stats

router = APIRouter(tags=["summary"])

@router.get("/summary")
def get_summary():
    """Get summary statistics across all agencies"""
    return get_summary_stats() 