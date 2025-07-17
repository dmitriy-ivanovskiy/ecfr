import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Include API routers with /api prefix
app.include_router(agencies_router, prefix="/api")
app.include_router(corrections_router, prefix="/api")
app.include_router(summary_router, prefix="/api")

# Health check endpoint for Render
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount static files (frontend)
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    
    # Serve frontend at root
    @app.get("/")
    async def serve_frontend():
        return FileResponse("frontend/index.html")
    
    # Serve frontend files
    @app.get("/{file_path:path}")
    async def serve_frontend_files(file_path: str):
        frontend_file = f"frontend/{file_path}"
        if os.path.exists(frontend_file) and os.path.isfile(frontend_file):
            return FileResponse(frontend_file)
        # If file doesn't exist, serve index.html (for SPA routing)
        return FileResponse("frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    # Load initial data
    fetch_sample_data()
    # Use PORT environment variable if available (Render), otherwise default to 8001
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 