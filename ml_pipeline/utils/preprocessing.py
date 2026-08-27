"""
Updated preprocessing utilities for FER2013 dataset in directory format.

This module provides functions for loading, preprocessing, and augmenting
the emotion recognition dataset from image directories.
"""

import numpy as np
import cv2
from pathlib import Path
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
import os

# Emotion labels
EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
EMOTION_MAP = {emotion: idx for idx, emotion in enumerate(EMOTIONS)}

def load_images_from_directory(data_dir, target_size=(48, 48)):
    """
    Load images from directory structure.
    
    Args:
        data_dir: Path to directory containing emotion subdirectories
        target_size: Target size for images
    
    Returns:
        X: Images array (N, height, width, 1)
        y: Labels array (N,)
    """
    images = []
    labels = []
    
    data_path = Path(data_dir)
    
    # Iterate through emotion directories
    for emotion_dir in data_path.iterdir():
        if not emotion_dir.is_dir():
            continue
        
        emotion_name = emotion_dir.name.lower()
        if emotion_name not in EMOTION_MAP:
            continue
        
        emotion_label = EMOTION_MAP[emotion_name]
        
        # Load all images in this emotion directory
        for img_path in emotion_dir.glob('*.jpg'):
            try:
                # Read image in grayscale
                img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                
                if img is None:
                    continue
                
                # Resize to target size
                img = cv2.resize(img, target_size)
                
                images.append(img)
                labels.append(emotion_label)
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
                continue
    
    # Convert to numpy arrays
    X = np.array(images, dtype=np.float32)
    y = np.array(labels, dtype=np.int32)
    
    # Add channel dimension and normalize
    X = np.expand_dims(X, axis=-1)
    X = X / 255.0
    
    return X, y

def load_fer2013_splits(base_dir):
    """
    Load FER2013 dataset split into train and test sets.
    
    Args:
        base_dir: Base directory containing train/ and test/ folders
    
    Returns:
        (X_train, y_train), (X_test, y_test)
    """
    base_path = Path(base_dir)
    
    print("Loading FER2013 dataset from directories...")
    
    # Load training data
    train_dir = base_path / 'train'
    if train_dir.exists():
        print(f"Loading training data from {train_dir}...")
        X_train, y_train = load_images_from_directory(train_dir)
        print(f"✓ Loaded {len(X_train)} training images")
    else:
        raise FileNotFoundError(f"Training directory not found: {train_dir}")
    
    # Load test data
    test_dir = base_path / 'test'
    if test_dir.exists():
        print(f"Loading test data from {test_dir}...")
        X_test, y_test = load_images_from_directory(test_dir)
        print(f"✓ Loaded {len(X_test)} test images")
    else:
        raise FileNotFoundError(f"Test directory not found: {test_dir}")
    
    # Create validation split from training data (10%)
    val_split = int(0.9 * len(X_train))
    X_val = X_train[val_split:]
    y_val = y_train[val_split:]
    X_train = X_train[:val_split]
    y_train = y_train[:val_split]
    
    print(f"Train set: {X_train.shape[0]} samples")
    print(f"Validation set: {X_val.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Convert labels to categorical
    y_train_cat = to_categorical(y_train, num_classes=7)
    y_val_cat = to_categorical(y_val, num_classes=7)
    y_test_cat = to_categorical(y_test, num_classes=7)
    
    return (X_train, y_train_cat), (X_val, y_val_cat), (X_test, y_test_cat)

def create_data_generators(X_train, y_train, X_val, y_val, batch_size=64):
    """
    Create data generators with augmentation for training.
    
    Args:
        X_train, y_train: Training data
        X_val, y_val: Validation data
        batch_size: Batch size for generators
    
    Returns:
        train_generator, val_generator
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # No augmentation for validation
    val_datagen = ImageDataGenerator()
    
    # Create generators
    train_generator = train_datagen.flow(
        X_train, y_train,
        batch_size=batch_size,
        shuffle=True
    )
    
    val_generator = val_datagen.flow(
        X_val, y_val,
        batch_size=batch_size,
        shuffle=False
    )
    
    return train_generator, val_generator

def preprocess_image(image, target_size=(48, 48)):
    """
    Preprocess a single image for prediction.
    
    Args:
        image: Input image (numpy array or path)
        target_size: Target size for resizing
    
    Returns:
        Preprocessed image array
    """
    # Load image if path is provided
    if isinstance(image, (str, Path)):
        image = cv2.imread(str(image), cv2.IMREAD_GRAYSCALE)
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize to target size
    image = cv2.resize(image, target_size)
    
    # Normalize to [0, 1]
    image = image.astype(np.float32) / 255.0
    
    # Add channel dimension
    image = np.expand_dims(image, axis=-1)
    
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    
    return image

def detect_faces(image, face_cascade_path=None):
    """
    Detect faces in an image using Haar Cascade.
    
    Args:
        image: Input image (BGR or grayscale)
        face_cascade_path: Path to Haar Cascade XML file
    
    Returns:
        List of face bounding boxes (x, y, w, h)
    """
    # Load Haar Cascade
    if face_cascade_path is None:
        # Use OpenCV's default frontal face cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    else:
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    return faces

def extract_face_roi(image, bbox, target_size=(48, 48)):
    """
    Extract and preprocess face region of interest.
    
    Args:
        image: Input image
        bbox: Bounding box (x, y, w, h)
        target_size: Target size for face
    
    Returns:
        Preprocessed face image
    """
    x, y, w, h = bbox
    
    # Extract face region
    face = image[y:y+h, x:x+w]
    
    # Convert to grayscale if needed
    if len(face.shape) == 3:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
    # Resize to target size
    face = cv2.resize(face, target_size)
    
    # Normalize
    face = face.astype(np.float32) / 255.0
    
    # Add channel dimension
    face = np.expand_dims(face, axis=-1)
    
    return face

def get_emotion_color(emotion_name):
    """
    Get color for emotion visualization.
    
    Args:
        emotion_name: Name of the emotion
    
    Returns:
        BGR color tuple
    """
    colors = {
        'angry': (0, 0, 255),      # Red
        'disgust': (0, 255, 0),    # Green
        'fear': (128, 0, 128),     # Purple
        'happy': (0, 215, 255),    # Gold
        'sad': (255, 0, 0),        # Blue
        'surprise': (0, 165, 255), # Orange
        'neutral': (128, 128, 128) # Gray
    }
    return colors.get(emotion_name.lower(), (255, 255, 255))

if __name__ == '__main__':
    # Test loading data
    data_dir = Path(__file__).parent.parent / 'data' / 'fer2013'
    
    if data_dir.exists():
        print("Testing data loading...")
        try:
            (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_fer2013_splits(str(data_dir))
            print("\n✓ Data loading successful!")
            print(f"Train shape: {X_train.shape}, {y_train.shape}")
            print(f"Val shape: {X_val.shape}, {y_val.shape}")
            print(f"Test shape: {X_test.shape}, {y_test.shape}")
            
            # Display class distribution
            print("\nClass distribution in training set:")
            for i, emotion in enumerate(EMOTIONS):
                count = np.sum(np.argmax(y_train, axis=1) == i)
                print(f"  {emotion.capitalize()}: {count}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Dataset not found at {data_dir}")
        print("Run download_data.py first to download the dataset")
