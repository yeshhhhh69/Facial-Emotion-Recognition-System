"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class BoundingBox(BaseModel):
    """Face bounding box coordinates."""
    x: int = Field(..., description="X coordinate of top-left corner")
    y: int = Field(..., description="Y coordinate of top-left corner")
    width: int = Field(..., description="Width of bounding box")
    height: int = Field(..., description="Height of bounding box")

class EmotionPrediction(BaseModel):
    """Emotion prediction for a single face."""
    bbox: BoundingBox = Field(..., description="Face bounding box")
    emotion: str = Field(..., description="Predicted emotion label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    probabilities: Dict[str, float] = Field(..., description="Probabilities for all emotions")

class PredictionResponse(BaseModel):
    """Response for emotion prediction."""
    success: bool = Field(..., description="Whether prediction was successful")
    num_faces: int = Field(..., description="Number of faces detected")
    predictions: List[EmotionPrediction] = Field(..., description="List of predictions")
    message: Optional[str] = Field(None, description="Optional message")

class EmotionLabel(BaseModel):
    """Emotion label with color."""
    name: str = Field(..., description="Emotion name")
    color: str = Field(..., description="Hex color code")

class ModelInfo(BaseModel):
    """Model information."""
    model_name: str = Field(..., description="Model name")
    version: str = Field(..., description="Model version")
    emotions: List[str] = Field(..., description="List of emotion labels")
    input_shape: List[int] = Field(..., description="Model input shape")
    confidence_threshold: float = Field(..., description="Confidence threshold")

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Error response."""
    success: bool = Field(False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
