"""
Configuration settings for the FastAPI backend.
"""

from typing import List
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "Facial Emotion Recognition API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # CORS Settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    
    # Model Settings
    model_path: str = "saved_models/emotion_model.h5"
    confidence_threshold: float = 0.3
    
    # Upload Settings
    max_upload_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_extensions: List[str] = [".jpg", ".jpeg", ".png", ".bmp"]
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Get absolute model path
BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = BASE_DIR / settings.model_path

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Emotion colors (for frontend)
EMOTION_COLORS = {
    'Angry': '#EF4444',      # Red
    'Disgust': '#10B981',    # Green
    'Fear': '#8B5CF6',       # Purple
    'Happy': '#F59E0B',      # Amber
    'Sad': '#3B82F6',        # Blue
    'Surprise': '#F97316',   # Orange
    'Neutral': '#6B7280'     # Gray
}
