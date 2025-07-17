import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.agencies import router as agencies_router
from api.corrections import router as corrections_router
from api.summary import router as summary_router
from services.data_processor import fetch_sample_data

app = FastAPI(title="eCFR Analysis API", description="API for analyzing Federal Regulations")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Render will need this for cross-origin requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agencies_router)
app.include_router(corrections_router)
app.include_router(summary_router)

# Health check endpoint for Render
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Load initial data
    fetch_sample_data()
    # Use PORT environment variable if available (Render), otherwise default to 8001
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 