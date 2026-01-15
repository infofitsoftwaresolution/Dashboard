"""
FastAPI Application Entry Point
Main application file that sets up FastAPI, CORS, and includes all API routes
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routes
from api.routes import dashboard, data

# Create FastAPI app
app = FastAPI(title="Dashboard API", version="1.0.0")

# Configure CORS - Allow all localhost ports for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development (change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(data.router, prefix="/api/data", tags=["Data"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Dashboard API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
