"""
FastAPI main application for Emotion Recognition.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import settings, MODEL_PATH
from app.core.emotion_detector import get_detector
from app.api import routes, websocket

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("=" * 70)
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print("=" * 70)
    
    # Load model
    print(f"\nLoading model from: {MODEL_PATH}")
    try:
        detector = get_detector(str(MODEL_PATH))
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        print("  Please ensure the model file exists and is valid")
    
    print("\n" + "=" * 70)
    print("Server is ready!")
    print(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"WebSocket endpoint: ws://{settings.host}:{settings.port}/ws/predict")
    print("=" * 70 + "\n")
    
    yield
    
    # Shutdown
    print("\nShutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Real-time facial emotion recognition using deep learning",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router)
app.include_router(websocket.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
