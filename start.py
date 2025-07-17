import os
import sys
import uvicorn

# Add backend directory to Python path
sys.path.insert(0, 'backend')

# Import from backend
from main import app
from services.data_processor import fetch_sample_data

if __name__ == "__main__":
    # Load initial data
    print("Loading initial agency data...")
    fetch_sample_data()
    print("Data loading complete!")
    
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get("PORT", 10000))
    
    # Run the app
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    ) 