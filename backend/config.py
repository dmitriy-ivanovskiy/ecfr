from datetime import timedelta

# API Configuration
ECFR_API_BASE = "https://www.ecfr.gov/api"

# Cache Configuration
CORRECTIONS_CACHE_DURATION = timedelta(minutes=30)

# Request Timeouts
API_TIMEOUT = 30
AGENCY_TIMEOUT = 10

# Default Pagination
DEFAULT_CORRECTIONS_LIMIT = 100 