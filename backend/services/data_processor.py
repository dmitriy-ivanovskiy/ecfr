import hashlib
from datetime import date
from typing import List, Dict, Any, Optional
from services.ecfr_client import fetch_agencies_from_api

# In-memory storage for testing
agencies_data = []
versions_data = []

def fetch_sample_data(max_agencies: Optional[int] = None) -> bool:
    """Fetch sample data from eCFR API, max_agencies=None means load all"""
    global agencies_data, versions_data
    
    try:
        # Get agency list from the API
        agencies_response = fetch_agencies_from_api()
        
        # Clear existing data
        agencies_data = []
        versions_data = []
        
        # Process agencies up to max_agencies limit
        if max_agencies is None:
            agencies_to_process = agencies_response  # Load all agencies
            print(f"Processing ALL {len(agencies_to_process)} agencies")
        else:
            agencies_to_process = agencies_response[:max_agencies]
            print(f"Processing {len(agencies_to_process)} agencies out of {len(agencies_response)} total available")
        
        for i, agency_info in enumerate(agencies_to_process):
            agency_id = i + 1
            agency = {
                "id": agency_id,
                "name": agency_info["name"],
                "short_name": agency_info.get("short_name", ""),
                "slug": agency_info["slug"]
            }
            agencies_data.append(agency)
            
            # Create sample metrics for each agency
            # In a real implementation, we'd fetch actual CFR content
            sample_text = f"Sample regulation text for {agency_info['name']} " * 100
            words = sample_text.split()
            word_count = len(words)
            unique_words = len(set(words))
            
            version = {
                "id": agency_id,
                "agency_id": agency_id,
                "fetched_on": str(date.today()),
                "checksum": hashlib.sha256(sample_text.encode()).hexdigest(),
                "word_count": word_count + (agency_id * 100),  # Add some variation
                "unique_words": unique_words + (agency_id * 20),
                "lexical_diversity": (unique_words + (agency_id * 20)) / (word_count + (agency_id * 100))
            }
            versions_data.append(version)
            
        return True
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Create fallback dummy data
        agencies_data = [
            {"id": 1, "name": "Department of Agriculture", "short_name": "USDA", "slug": "agriculture-department"},
            {"id": 2, "name": "Department of Commerce", "short_name": "DOC", "slug": "commerce-department"},
            {"id": 3, "name": "Environmental Protection Agency", "short_name": "EPA", "slug": "environmental-protection-agency"},
        ]
        
        versions_data = [
            {
                "id": 1, "agency_id": 1, "fetched_on": str(date.today()),
                "checksum": "abc123...", "word_count": 15000, "unique_words": 3000,
                "lexical_diversity": 0.2
            },
            {
                "id": 2, "agency_id": 2, "fetched_on": str(date.today()),
                "checksum": "def456...", "word_count": 22000, "unique_words": 4500,
                "lexical_diversity": 0.205
            },
            {
                "id": 3, "agency_id": 3, "fetched_on": str(date.today()),
                "checksum": "ghi789...", "word_count": 35000, "unique_words": 8000,
                "lexical_diversity": 0.229
            },
        ]
        return False

def get_agencies() -> List[Dict[str, Any]]:
    """Get list of all agencies"""
    return agencies_data

def get_agencies_with_metrics() -> List[Dict[str, Any]]:
    """Get all agencies with their latest metrics in one call"""
    result = []
    for agency in agencies_data:
        version = next((v for v in versions_data if v["agency_id"] == agency["id"]), None)
        if version:
            result.append({
                **agency,
                "metrics": version
            })
        else:
            result.append({
                **agency,
                "metrics": None
            })
    return result

def get_agency_metrics(agency_id: int) -> Optional[Dict[str, Any]]:
    """Get latest metrics for a specific agency"""
    return next((v for v in versions_data if v["agency_id"] == agency_id), None)

def get_summary_stats() -> Dict[str, Any]:
    """Get summary statistics across all agencies"""
    if not versions_data:
        return {
            "total_agencies": 0,
            "total_words": 0,
            "average_lexical_diversity": 0,
            "agencies_with_data": 0
        }
    
    total_words = sum(v["word_count"] for v in versions_data)
    avg_lexical_diversity = sum(v["lexical_diversity"] for v in versions_data) / len(versions_data)
    
    return {
        "total_agencies": len(agencies_data),
        "total_words": total_words,
        "average_lexical_diversity": avg_lexical_diversity,
        "agencies_with_data": len(versions_data)
    }

def process_corrections_for_pagination(corrections_data: List[Dict[str, Any]], limit: int, offset: int) -> Dict[str, Any]:
    """Process corrections data for paginated response"""
    # Sort by correction date (most recent first)
    sorted_corrections = sorted(corrections_data, key=lambda x: x["error_corrected"], reverse=True)
    
    # Apply pagination
    total_available = len(sorted_corrections)
    paginated_corrections = sorted_corrections[offset:offset + limit]
    
    # Transform data for easier frontend consumption
    processed_corrections = []
    for correction in paginated_corrections:
        processed_corrections.append({
            "id": correction["id"],
            "title": correction["title"],
            "cfr_reference": correction["cfr_references"][0]["cfr_reference"] if correction["cfr_references"] else "N/A",
            "corrective_action": correction["corrective_action"],
            "error_corrected": correction["error_corrected"],
            "error_occurred": correction["error_occurred"],
            "fr_citation": correction["fr_citation"],
            "year": correction["year"],
            "last_modified": correction["last_modified"]
        })
    
    return {
        "corrections": processed_corrections,
        "total_available": total_available,
        "showing": len(processed_corrections),
        "limit": limit,
        "offset": offset,
        "has_next": offset + limit < total_available,
        "has_previous": offset > 0,
        "total_pages": (total_available + limit - 1) // limit,  # Ceiling division
        "current_page": (offset // limit) + 1
    }

def process_corrections_stats(corrections_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process corrections data for statistics"""
    total_corrections = len(corrections_data)
    
    # Group by year
    years = {}
    titles = {}
    for correction in corrections_data:
        year = correction["year"]
        title = correction["title"]
        years[year] = years.get(year, 0) + 1
        titles[title] = titles.get(title, 0) + 1
    
    # Get most recent corrections
    recent_corrections = sorted(corrections_data, key=lambda x: x["error_corrected"], reverse=True)[:10]
    
    return {
        "total_corrections": total_corrections,
        "corrections_by_year": dict(sorted(years.items(), reverse=True)[:10]),  # Last 10 years
        "corrections_by_title": dict(sorted(titles.items(), key=lambda x: x[1], reverse=True)[:10]),  # Top 10 titles
        "date_range": {
            "earliest": min(corrections_data, key=lambda x: x["error_corrected"])["error_corrected"],
            "latest": max(corrections_data, key=lambda x: x["error_corrected"])["error_corrected"]
        },
        "recent_corrections": [
            {
                "cfr_reference": c["cfr_references"][0]["cfr_reference"] if c["cfr_references"] else "N/A",
                "action": c["corrective_action"][:50] + "..." if len(c["corrective_action"]) > 50 else c["corrective_action"],
                "date": c["error_corrected"]
            }
            for c in recent_corrections
        ]
    } 