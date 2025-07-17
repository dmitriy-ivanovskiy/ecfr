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
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agencies_router)
app.include_router(corrections_router)
app.include_router(summary_router)

if __name__ == "__main__":
    import uvicorn
    # Load initial data
    fetch_sample_data()
    uvicorn.run(app, host="0.0.0.0", port=8001) 