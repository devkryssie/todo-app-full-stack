from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router








app = FastAPI(
    title="Todo API",
    description="Production-grade MVP Todo API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Configure CORS Middleware (crucial for web-facing APIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register versioned routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Todo API MVP",
        "version": "1.0.0"
    }
