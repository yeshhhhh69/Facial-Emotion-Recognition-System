"""
CNN Model Architecture for Facial Emotion Recognition.

This module defines the Convolutional Neural Network architecture
for classifying facial expressions into 7 emotion categories.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dense, Dropout, Flatten,
    BatchNormalization, Activation, Input
)
from tensorflow.keras.regularizers import l2

def create_emotion_cnn(input_shape=(48, 48, 1), num_classes=7):
    """
    Create CNN model for emotion recognition.
    
    Architecture:
        - 4 Convolutional blocks with BatchNorm and MaxPooling
        - Dropout for regularization
        - 2 Dense layers
        - Softmax output for 7 emotions
    
    Args:
        input_shape: Input image shape (height, width, channels)
        num_classes: Number of emotion classes (default: 7)
    
    Returns:
        Keras model
    """
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), padding='same', kernel_regularizer=l2(0.01),
               input_shape=input_shape),
        BatchNormalization(),
        Activation('relu'),
        Conv2D(32, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 2
        Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        Conv2D(64, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 3
        Conv2D(128, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        Conv2D(128, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 4
        Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        Conv2D(256, (3, 3), padding='same', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Fully connected layers
        Flatten(),
        Dense(512, kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        Dropout(0.5),
        
        Dense(256, kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Activation('relu'),
        Dropout(0.5),
        
        # Output layer
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def create_lightweight_cnn(input_shape=(48, 48, 1), num_classes=7):
    """
    Create a lightweight CNN model for faster training and inference.
    
    Args:
        input_shape: Input image shape
        num_classes: Number of emotion classes
    
    Returns:
        Keras model
    """
    model = Sequential([
        # Block 1
        Conv2D(32, (3, 3), padding='same', activation='relu',
               input_shape=input_shape),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 2
        Conv2D(64, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 3
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Fully connected
        Flatten(),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        
        Dense(num_classes, activation='softmax')
    ])
    
    return model

def get_model_summary(model):
    """
    Get detailed model summary.
    
    Args:
        model: Keras model
    
    Returns:
        String with model summary
    """
    from io import StringIO
    import sys
    
    # Capture model summary
    old_stdout = sys.stdout
    sys.stdout = summary_buffer = StringIO()
    model.summary()
    sys.stdout = old_stdout
    
    summary_str = summary_buffer.getvalue()
    return summary_str

if __name__ == '__main__':
    print("Creating Emotion Recognition CNN Model...")
    print("=" * 60)
    
    # Create model
    model = create_emotion_cnn()
    
    # Display summary
    print("\nModel Architecture:")
    print("=" * 60)
    model.summary()
    
    # Count parameters
    trainable_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
    non_trainable_params = sum([tf.size(w).numpy() for w in model.non_trainable_weights])
    total_params = trainable_params + non_trainable_params
    
    print("\n" + "=" * 60)
    print("Parameter Summary:")
    print("=" * 60)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Non-trainable parameters: {non_trainable_params:,}")
    print("=" * 60)
    
    # Create lightweight model
    print("\n\nLightweight Model:")
    print("=" * 60)
    lightweight_model = create_lightweight_cnn()
    lightweight_model.summary()
