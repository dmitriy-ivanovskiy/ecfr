# eCFR Analysis Dashboard

A web application for analyzing federal regulations from the Electronic Code of Federal Regulations (eCFR), providing insights for deregulation research.

## Features

### Agency Analysis
- Analyzes data from all 153 federal agencies
- Calculate word counts, unique words, and lexical diversity metrics
- Generate checksums for change detection
- Real-time dashboard with comprehensive agency coverage

### Historical Corrections Tracking
- Access 3,327+ historical regulatory corrections (2005-2025)
- Statistics by year and CFR title
- Track corrective actions, error dates, and Federal Register citations
- Most corrected title: Title 40 Environmental Protection (623 corrections)

## Technical Stack

- **Backend**: FastAPI with Python 3.13
- **Frontend**: Vanilla HTML/JavaScript with Tailwind CSS
- **Styling**: Tailwind CSS utility-first framework
- **Data Source**: eCFR.gov APIs
- **Storage**: In-memory (no database required)

## Quick Start

### Option 1: One-Command Startup
```bash
./start.sh
```
This will start both servers and display the URLs.

### Option 2: Manual Startup
1. **Start the backend server:**
   ```bash
   cd backend
   source .venv/bin/activate
   python main_simple.py
   ```
   Server runs on http://localhost:8001

2. **Start the frontend server:**
   ```bash
   cd frontend
   python3 -m http.server 9000
   ```
   Dashboard available at http://localhost:9000

## Usage

1. **View Agency Data**: Comprehensive analysis of all 153 federal agencies
2. **Analyze Metrics**: Review word counts, lexical diversity, and checksums
3. **Historical Changes**: Explore regulatory corrections and modifications over time
4. **Refresh Data**: Update dashboard with latest information from eCFR APIs

## API Endpoints

- `GET /agencies` - List all 153 agencies
- `GET /agencies/with-metrics` - Get all agencies with metrics in one call (optimized)
- `GET /agency/{id}/latest` - Get latest metrics for a specific agency
- `GET /summary` - Dashboard summary statistics
- `GET /corrections` - Historical corrections data
- `GET /corrections/stats` - Corrections statistics

## Data Sources

- **Agencies**: https://www.ecfr.gov/api/admin/v1/agencies.json
- **Corrections**: https://www.ecfr.gov/api/admin/v1/corrections.json

## Custom Metrics

- **Lexical Diversity**: Unique words / Total words (higher = more diverse vocabulary)
- **Checksum**: SHA-256 hash for detecting content changes
- **Error Tracking**: Systematic tracking of regulatory corrections and amendments 