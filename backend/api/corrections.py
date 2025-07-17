from fastapi import APIRouter
from services.ecfr_client import get_corrections_data
from services.data_processor import process_corrections_for_pagination, process_corrections_stats
from config import DEFAULT_CORRECTIONS_LIMIT

router = APIRouter(prefix="/corrections", tags=["corrections"])

@router.get("")
def get_corrections(limit: int = DEFAULT_CORRECTIONS_LIMIT, offset: int = 0):
    """Get historical corrections from the eCFR API with pagination support"""
    try:
        corrections_data = get_corrections_data()
        return process_corrections_for_pagination(corrections_data, limit, offset)
    except Exception as e:
        return {
            "error": f"Failed to fetch corrections: {str(e)}",
            "corrections": [],
            "total_available": 0,
            "showing": 0,
            "limit": limit,
            "offset": offset,
            "has_next": False,
            "has_previous": False,
            "total_pages": 0,
            "current_page": 1
        }

@router.get("/stats")
def get_corrections_stats():
    """Get statistics about historical corrections"""
    try:
        corrections_data = get_corrections_data()
        return process_corrections_stats(corrections_data)
    except Exception as e:
        return {"error": f"Failed to fetch correction statistics: {str(e)}"} 