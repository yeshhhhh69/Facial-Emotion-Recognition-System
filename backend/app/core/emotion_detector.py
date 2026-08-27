"""
Emotion Detector - Core inference engine for emotion recognition.

This module provides the EmotionDetector class for loading the trained model
and performing inference on images with face detection.
"""

import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path
from typing import List, Tuple, Dict

# Emotion labels and colors
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

EMOTION_COLORS = {
    'Angry': (0, 0, 255),      # Red
    'Disgust': (0, 255, 0),    # Green
    'Fear': (128, 0, 128),     # Purple
    'Happy': (0, 215, 255),    # Gold
    'Sad': (255, 0, 0),        # Blue
    'Surprise': (0, 165, 255), # Orange
    'Neutral': (128, 128, 128) # Gray
}

class EmotionDetector:
    """Emotion detection and inference engine."""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.3):
        """
        Initialize the emotion detector.
        
        Args:
            model_path: Path to the trained Keras model
            confidence_threshold: Minimum confidence for predictions
        """
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.face_cascade = None
        
        # Load model
        self._load_model()
        
        # Load face detector
        self._load_face_detector()
    
    def _load_model(self):
        """Load the trained Keras model."""
        try:
            self.model = tf.keras.models.load_model(str(self.model_path))
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def _load_face_detector(self):
        """Load Haar Cascade face detector."""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier")
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in an image.
        
        Args:
            image: Input image (BGR or grayscale)
        
        Returns:
            List of face bounding boxes (x, y, w, h)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def preprocess_face(self, face: np.ndarray) -> np.ndarray:
        """
        Preprocess face for model input.
        
        Args:
            face: Face image
        
        Returns:
            Preprocessed face array
        """
        # Convert to grayscale if needed
        if len(face.shape) == 3:
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        
        # Resize to 48x48
        face = cv2.resize(face, (48, 48))
        
        # Normalize to [0, 1]
        face = face.astype(np.float32) / 255.0
        
        # Add channel and batch dimensions
        face = np.expand_dims(face, axis=-1)
        face = np.expand_dims(face, axis=0)
        
        return face
    
    def predict_emotion(self, face: np.ndarray) -> Dict:
        """
        Predict emotion for a single face.
        
        Args:
            face: Preprocessed face array
        
        Returns:
            Dictionary with emotion prediction and probabilities
        """
        # Get predictions
        predictions = self.model.predict(face, verbose=0)[0]
        
        # Get top emotion
        emotion_idx = np.argmax(predictions)
        emotion = EMOTIONS[emotion_idx]
        confidence = float(predictions[emotion_idx])
        
        # Get all probabilities
        probabilities = {
            EMOTIONS[i]: float(predictions[i])
            for i in range(len(EMOTIONS))
        }
        
        return {
            'emotion': emotion,
            'confidence': confidence,
            'probabilities': probabilities
        }
    
    def detect_and_predict(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces and predict emotions.
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            List of predictions with bounding boxes
        """
        # Detect faces
        faces = self.detect_faces(image)
        
        results = []
        
        for (x, y, w, h) in faces:
            # Extract face ROI
            face_roi = image[y:y+h, x:x+w]
            
            # Preprocess face
            face_preprocessed = self.preprocess_face(face_roi)
            
            # Predict emotion
            prediction = self.predict_emotion(face_preprocessed)
            
            # Only include if confidence is above threshold
            if prediction['confidence'] >= self.confidence_threshold:
                results.append({
                    'bbox': {
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h)
                    },
                    'emotion': prediction['emotion'],
                    'confidence': prediction['confidence'],
                    'probabilities': prediction['probabilities']
                })
        
        return results
    
    def draw_predictions(self, image: np.ndarray, predictions: List[Dict]) -> np.ndarray:
        """
        Draw predictions on image.
        
        Args:
            image: Input image
            predictions: List of predictions
        
        Returns:
            Image with drawn predictions
        """
        output = image.copy()
        
        for pred in predictions:
            bbox = pred['bbox']
            emotion = pred['emotion']
            confidence = pred['confidence']
            
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            
            # Get color for emotion
            color = EMOTION_COLORS.get(emotion, (255, 255, 255))
            
            # Draw bounding box
            cv2.rectangle(output, (x, y), (x+w, y+h), color, 2)
            
            # Draw label
            label = f"{emotion}: {confidence*100:.1f}%"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            # Draw label background
            cv2.rectangle(
                output,
                (x, y - label_size[1] - 10),
                (x + label_size[0], y),
                color,
                -1
            )
            
            # Draw label text
            cv2.putText(
                output,
                label,
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        return output

# Singleton instance
_detector_instance = None

def get_detector(model_path: str = None) -> EmotionDetector:
    """
    Get or create the emotion detector singleton.
    
    Args:
        model_path: Path to model (only used on first call)
    
    Returns:
        EmotionDetector instance
    """
    global _detector_instance
    
    if _detector_instance is None:
        if model_path is None:
            raise ValueError("model_path must be provided on first call")
        _detector_instance = EmotionDetector(model_path)
    
    return _detector_instance
