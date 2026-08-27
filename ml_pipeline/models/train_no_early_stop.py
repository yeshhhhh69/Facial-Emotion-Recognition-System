"""
Updated training script for Emotion Recognition CNN with directory-based dataset.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau,
    CSVLogger, TensorBoard
)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from models.cnn_model import create_emotion_cnn, create_lightweight_cnn
from utils.preprocessing import load_fer2013_splits, create_data_generators

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def train_model(
    data_path,
    model_type='full',
    epochs=100,
    batch_size=64,
    learning_rate=0.0001,
    output_dir='../../backend/saved_models'
):
    """
    Train the emotion recognition model.
    
    Args:
        data_path: Path to FER2013 directory with train/test folders
        model_type: 'full' or 'lightweight'
        epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Initial learning rate
        output_dir: Directory to save model and logs
    """
    print("=" * 70)
    print("Facial Emotion Recognition - Model Training")
    print("=" * 70)
    
    # Create output directory
    output_path = Path(__file__).parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create logs directory
    logs_dir = output_path / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Load data
    print("\n[1/5] Loading dataset from directories...")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_fer2013_splits(data_path)
    
    print(f"\nDataset loaded successfully!")
    print(f"  Training samples: {X_train.shape[0]}")
    print(f"  Validation samples: {X_val.shape[0]}")
    print(f"  Test samples: {X_test.shape[0]}")
    
    # Create data generators
    print("\n[2/5] Creating data generators with augmentation...")
    train_gen, val_gen = create_data_generators(
        X_train, y_train, X_val, y_val, batch_size=batch_size
    )
    
    # Create model
    print(f"\n[3/5] Creating {model_type} CNN model...")
    if model_type == 'lightweight':
        model = create_lightweight_cnn()
    else:
        model = create_emotion_cnn()
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Display model summary
    print("\nModel Architecture:")
    print("-" * 70)
    model.summary()
    
    # Setup callbacks
    print("\n[4/5] Setting up training callbacks...")
    
    callbacks = [
        # Save best model
        ModelCheckpoint(
            filepath=str(output_path / f'best_model_{timestamp}.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # NOTE: Early stopping is DISABLED - will train for full epoch count
        
        # Reduce learning rate on plateau
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        
        # CSV logger
        CSVLogger(
            filename=str(logs_dir / f'training_log_{timestamp}.csv'),
            append=False
        ),
        
        # TensorBoard
        TensorBoard(
            log_dir=str(logs_dir / f'tensorboard_{timestamp}'),
            histogram_freq=1,
            write_graph=True
        )
    ]
    
    print("Callbacks configured:")
    print("  ✓ ModelCheckpoint - Save best model")
    print("  ✓ EarlyStopping - DISABLED (will train full epochs)")
    print("  ✓ ReduceLROnPlateau - Reduce LR by 0.5")
    print("  ✓ CSVLogger - Log metrics to CSV")
    print("  ✓ TensorBoard - Visualize training")
    
    # Train model
    print("\n[5/5] Starting training...")
    print("=" * 70)
    
    history = model.fit(
        train_gen,
        steps_per_epoch=len(X_train) // batch_size,
        epochs=epochs,
        validation_data=val_gen,
        validation_steps=len(X_val) // batch_size,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    print("\n" + "=" * 70)
    print("Training completed!")
    print("=" * 70)
    
    final_model_path = output_path / 'emotion_model.h5'
    model.save(str(final_model_path))
    print(f"\n✓ Final model saved to: {final_model_path}")
    
    # Save in SavedModel format for production (using export for TF compatibility)
    saved_model_path = output_path / 'emotion_model_saved'
    try:
        model.export(str(saved_model_path))
        print(f"✓ SavedModel format exported to: {saved_model_path}")
    except:
        # Fallback: save as .keras format
        keras_model_path = output_path / 'emotion_model.keras'
        model.save(str(keras_model_path))
        print(f"✓ Keras format saved to: {keras_model_path}")
    print(f"✓ SavedModel format saved to: {saved_model_path}")
    
    # Save training history
    history_path = output_path / f'training_history_{timestamp}.json'
    with open(history_path, 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        history_dict = {
            key: [float(val) for val in values]
            for key, values in history.history.items()
        }
        json.dump(history_dict, f, indent=2)
    print(f"✓ Training history saved to: {history_path}")
    
    # Evaluate on test set
    print("\n" + "=" * 70)
    print("Evaluating on test set...")
    print("=" * 70)
    
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\nTest Results:")
    print(f"  Loss: {test_loss:.4f}")
    print(f"  Accuracy: {test_accuracy*100:.2f}%")
    
    # Save test results
    results = {
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'model_type': model_type,
        'epochs_trained': len(history.history['loss']),
        'batch_size': batch_size,
        'learning_rate': learning_rate,
        'timestamp': timestamp
    }
    
    results_path = output_path / 'test_results.json'
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Test results saved to: {results_path}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("Training Summary")
    print("=" * 70)
    print(f"Model type: {model_type}")
    print(f"Total epochs: {len(history.history['loss'])}")
    print(f"Best validation accuracy: {max(history.history['val_accuracy'])*100:.2f}%")
    print(f"Final test accuracy: {test_accuracy*100:.2f}%")
    print(f"\nModel saved to: {final_model_path}")
    print("=" * 70)
    
    return model, history

def main():
    parser = argparse.ArgumentParser(description='Train Emotion Recognition CNN')
    parser.add_argument('--data-path', type=str,
                        default='../data/fer2013',
                        help='Path to FER2013 directory')
    parser.add_argument('--model-type', type=str, default='full',
                        choices=['full', 'lightweight'],
                        help='Model architecture type')
    parser.add_argument('--epochs', type=int, default=100,
                        help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=64,
                        help='Batch size for training')
    parser.add_argument('--learning-rate', type=float, default=0.0001,
                        help='Initial learning rate')
    parser.add_argument('--output-dir', type=str,
                        default='../../backend/saved_models',
                        help='Output directory for model and logs')
    
    args = parser.parse_args()
    
    # Check if data directory exists
    data_path = Path(__file__).parent / args.data_path
    if not data_path.exists():
        print(f"Error: Data directory not found at {data_path}")
        print("\nPlease run the data download script first:")
        print("  python data/download_data.py --download")
        sys.exit(1)
    
    # Check for train and test directories
    if not (data_path / 'train').exists() or not (data_path / 'test').exists():
        print(f"Error: train/ or test/ directories not found in {data_path}")
        print("\nExpected structure:")
        print("  fer2013/")
        print("    train/")
        print("      angry/")
        print("      disgust/")
        print("      ...")
        print("    test/")
        print("      angry/")
        print("      ...")
        sys.exit(1)
    
    # Train model
    train_model(
        data_path=str(data_path),
        model_type=args.model_type,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        output_dir=args.output_dir
    )

if __name__ == '__main__':
    main()
