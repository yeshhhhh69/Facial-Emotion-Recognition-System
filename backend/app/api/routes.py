"""
API routes for emotion prediction.
"""

import io
import base64
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image

from app.core.emotion_detector import get_detector
from app.core.config import settings, EMOTIONS, EMOTION_COLORS
from app.models.schemas import (
    PredictionResponse, EmotionPrediction, BoundingBox,
    EmotionLabel, ModelInfo, ErrorResponse
)

router = APIRouter(prefix="/api", tags=["predictions"])

def load_image_from_upload(file: UploadFile) -> np.ndarray:
    """Load image from uploaded file."""
    try:
        # Read file content
        contents = file.file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(contents, np.uint8)
        
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")
        
        return image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image file: {str(e)}"
        )

def load_image_from_base64(base64_str: str) -> np.ndarray:
    """Load image from base64 string."""
    try:
        # Remove data URL prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(base64_str)
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode image
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise ValueError("Failed to decode image")
        
        return image
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid base64 image: {str(e)}"
        )

@router.post("/predict/image", response_model=PredictionResponse)
async def predict_image(file: UploadFile = File(...)):
    """
    Predict emotions from uploaded image.
    
    Detects faces in the image and predicts emotions for each face.
    """
    try:
        # Validate file extension
        if file.filename:
            ext = '.' + file.filename.split('.')[-1].lower()
            if ext not in settings.allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File type not allowed. Allowed types: {settings.allowed_extensions}"
                )
        
        # Load image
        image = load_image_from_upload(file)
        
        # Get detector
        detector = get_detector()
        
        # Detect and predict
        predictions = detector.detect_and_predict(image)
        
        # Convert to response format
        emotion_predictions = [
            EmotionPrediction(
                bbox=BoundingBox(**pred['bbox']),
                emotion=pred['emotion'],
                confidence=pred['confidence'],
                probabilities=pred['probabilities']
            )
            for pred in predictions
        ]
        
        return PredictionResponse(
            success=True,
            num_faces=len(predictions),
            predictions=emotion_predictions,
            message=f"Detected {len(predictions)} face(s)" if predictions else "No faces detected"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/emotions", response_model=list[EmotionLabel])
async def get_emotions():
    """Get list of supported emotions with colors."""
    return [
        EmotionLabel(name=emotion, color=EMOTION_COLORS[emotion])
        for emotion in EMOTIONS
    ]

@router.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get model information and metadata."""
    detector = get_detector()
    
    return ModelInfo(
        model_name="Emotion Recognition CNN",
        version="1.0.0",
        emotions=EMOTIONS,
        input_shape=[48, 48, 1],
        confidence_threshold=settings.confidence_threshold
    )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        detector = get_detector()
        model_loaded = detector.model is not None
    except:
        model_loaded = False
    
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "version": settings.app_version
    }
