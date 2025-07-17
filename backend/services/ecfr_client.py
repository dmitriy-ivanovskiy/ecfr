import requests
from datetime import datetime
from typing import List, Dict, Any
from config import ECFR_API_BASE, CORRECTIONS_CACHE_DURATION, API_TIMEOUT, AGENCY_TIMEOUT

# Cache for corrections data to avoid redundant API calls
corrections_cache = {
    "data": None,
    "last_fetched": None,
    "cache_duration": CORRECTIONS_CACHE_DURATION
}

def get_corrections_data() -> List[Dict[str, Any]]:
    """Get corrections data with caching to avoid redundant API calls"""
    now = datetime.now()
    
    # Check if we have cached data that's still valid
    if (corrections_cache["data"] is not None and 
        corrections_cache["last_fetched"] is not None and 
        now - corrections_cache["last_fetched"] < corrections_cache["cache_duration"]):
        return corrections_cache["data"]
    
    # Fetch fresh data
    try:
        r = requests.get(f"{ECFR_API_BASE}/admin/v1/corrections.json", timeout=API_TIMEOUT)
        corrections_data = r.json()["ecfr_corrections"]
        
        # Update cache
        corrections_cache["data"] = corrections_data
        corrections_cache["last_fetched"] = now
        
        return corrections_data
    except Exception as e:
        # If we have stale cached data, return it rather than failing
        if corrections_cache["data"] is not None:
            return corrections_cache["data"]
        raise e

def fetch_agencies_from_api() -> List[Dict[str, Any]]:
    """Fetch agencies from the eCFR API"""
    try:
        r = requests.get(f"{ECFR_API_BASE}/admin/v1/agencies.json", timeout=AGENCY_TIMEOUT)
        return r.json()["agencies"]
    except Exception as e:
        raise Exception(f"Failed to fetch agencies: {str(e)}") 