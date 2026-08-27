"""
Model evaluation script for Emotion Recognition CNN.

This script evaluates the trained model and generates detailed metrics,
confusion matrix, and visualization of results.
"""

import os
import sys
import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, precision_recall_fscore_support
)
import tensorflow as tf

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.preprocessing import load_fer2013_splits

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def evaluate_model(model_path, data_path, output_dir='../../backend/saved_models'):
    """
    Evaluate the trained model on test set.
    
    Args:
        model_path: Path to saved model
        data_path: Path to FER2013 CSV file
        output_dir: Directory to save evaluation results
    """
    print("=" * 70)
    print("Facial Emotion Recognition - Model Evaluation")
    print("=" * 70)
    
    # Create output directory
    output_path = Path(__file__).parent / output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load model
    print(f"\n[1/4] Loading model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    print("✓ Model loaded successfully")
    
    # Load test data
    print("\n[2/4] Loading test dataset...")
    (X_train, y_train), (X_val, y_val), (X_test, y_test) = load_fer2013_splits(data_path)
    
    # Convert one-hot to class indices
    y_test_labels = np.argmax(y_test, axis=1)
    
    print(f"✓ Test set loaded: {X_test.shape[0]} samples")
    
    # Make predictions
    print("\n[3/4] Making predictions...")
    y_pred_probs = model.predict(X_test, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Calculate metrics
    print("\n[4/4] Calculating metrics...")
    
    # Overall accuracy
    accuracy = accuracy_score(y_test_labels, y_pred)
    
    # Per-class metrics
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test_labels, y_pred, average=None, labels=range(7)
    )
    
    # Confusion matrix
    cm = confusion_matrix(y_test_labels, y_pred, labels=range(7))
    
    # Print results
    print("\n" + "=" * 70)
    print("Evaluation Results")
    print("=" * 70)
    print(f"\nOverall Accuracy: {accuracy*100:.2f}%\n")
    
    print("Per-Class Metrics:")
    print("-" * 70)
    print(f"{'Emotion':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 70)
    
    for i, emotion in enumerate(EMOTIONS):
        print(f"{emotion:<12} {precision[i]:<12.4f} {recall[i]:<12.4f} "
              f"{f1[i]:<12.4f} {support[i]:<10}")
    
    print("-" * 70)
    avg_precision = np.mean(precision)
    avg_recall = np.mean(recall)
    avg_f1 = np.mean(f1)
    print(f"{'Average':<12} {avg_precision:<12.4f} {avg_recall:<12.4f} "
          f"{avg_f1:<12.4f} {np.sum(support):<10}")
    print("=" * 70)
    
    # Save metrics to JSON
    metrics = {
        'overall_accuracy': float(accuracy),
        'per_class_metrics': {
            emotion: {
                'precision': float(precision[i]),
                'recall': float(recall[i]),
                'f1_score': float(f1[i]),
                'support': int(support[i])
            }
            for i, emotion in enumerate(EMOTIONS)
        },
        'average_metrics': {
            'precision': float(avg_precision),
            'recall': float(avg_recall),
            'f1_score': float(avg_f1)
        }
    }
    
    metrics_path = output_path / 'evaluation_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n✓ Metrics saved to: {metrics_path}")
    
    # Plot confusion matrix
    print("\nGenerating confusion matrix plot...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=EMOTIONS, yticklabels=EMOTIONS)
    plt.title('Confusion Matrix - Emotion Recognition')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    cm_path = output_path / 'confusion_matrix.png'
    plt.savefig(cm_path, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to: {cm_path}")
    plt.close()
    
    # Plot normalized confusion matrix
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=EMOTIONS, yticklabels=EMOTIONS)
    plt.title('Normalized Confusion Matrix - Emotion Recognition')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    cm_norm_path = output_path / 'confusion_matrix_normalized.png'
    plt.savefig(cm_norm_path, dpi=300, bbox_inches='tight')
    print(f"✓ Normalized confusion matrix saved to: {cm_norm_path}")
    plt.close()
    
    # Plot per-class metrics
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    x = np.arange(len(EMOTIONS))
    width = 0.6
    
    # Precision
    axes[0].bar(x, precision, width, color='skyblue')
    axes[0].set_ylabel('Precision')
    axes[0].set_title('Precision per Emotion')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(EMOTIONS, rotation=45, ha='right')
    axes[0].set_ylim([0, 1])
    axes[0].grid(axis='y', alpha=0.3)
    
    # Recall
    axes[1].bar(x, recall, width, color='lightcoral')
    axes[1].set_ylabel('Recall')
    axes[1].set_title('Recall per Emotion')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(EMOTIONS, rotation=45, ha='right')
    axes[1].set_ylim([0, 1])
    axes[1].grid(axis='y', alpha=0.3)
    
    # F1-Score
    axes[2].bar(x, f1, width, color='lightgreen')
    axes[2].set_ylabel('F1-Score')
    axes[2].set_title('F1-Score per Emotion')
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(EMOTIONS, rotation=45, ha='right')
    axes[2].set_ylim([0, 1])
    axes[2].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    metrics_plot_path = output_path / 'per_class_metrics.png'
    plt.savefig(metrics_plot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Per-class metrics plot saved to: {metrics_plot_path}")
    plt.close()
    
    # Visualize some predictions
    print("\nGenerating sample predictions visualization...")
    visualize_predictions(model, X_test, y_test_labels, y_pred, output_path)
    
    print("\n" + "=" * 70)
    print("Evaluation Complete!")
    print("=" * 70)
    
    return metrics

def visualize_predictions(model, X_test, y_true, y_pred, output_path, num_samples=20):
    """Visualize sample predictions."""
    # Get random samples
    indices = np.random.choice(len(X_test), num_samples, replace=False)
    
    fig, axes = plt.subplots(4, 5, figsize=(15, 12))
    axes = axes.ravel()
    
    for i, idx in enumerate(indices):
        img = X_test[idx].squeeze()
        true_label = EMOTIONS[y_true[idx]]
        pred_label = EMOTIONS[y_pred[idx]]
        
        axes[i].imshow(img, cmap='gray')
        axes[i].axis('off')
        
        # Color code: green if correct, red if wrong
        color = 'green' if y_true[idx] == y_pred[idx] else 'red'
        axes[i].set_title(f'True: {true_label}\nPred: {pred_label}',
                         fontsize=8, color=color)
    
    plt.suptitle('Sample Predictions (Green=Correct, Red=Incorrect)', fontsize=14)
    plt.tight_layout()
    
    pred_viz_path = output_path / 'sample_predictions.png'
    plt.savefig(pred_viz_path, dpi=300, bbox_inches='tight')
    print(f"✓ Sample predictions saved to: {pred_viz_path}")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='Evaluate Emotion Recognition Model')
    parser.add_argument('--model-path', type=str,
                        default='../../backend/saved_models/emotion_model.h5',
                        help='Path to trained model')
    parser.add_argument('--data-path', type=str,
                        default='../data/fer2013/fer2013.csv',
                        help='Path to FER2013 CSV file')
    parser.add_argument('--output-dir', type=str,
                        default='../../backend/saved_models',
                        help='Output directory for evaluation results')
    
    args = parser.parse_args()
    
    # Check if model exists
    model_path = Path(__file__).parent / args.model_path
    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        print("\nPlease train the model first:")
        print("  python models/train.py")
        sys.exit(1)
    
    # Check if data exists
    data_path = Path(__file__).parent / args.data_path
    if not data_path.exists():
        print(f"Error: Data file not found at {data_path}")
        print("\nPlease download the dataset first:")
        print("  python data/download_data.py --download")
        sys.exit(1)
    
    # Evaluate model
    evaluate_model(
        model_path=str(model_path),
        data_path=str(data_path),
        output_dir=args.output_dir
    )

if __name__ == '__main__':
    main()
