"""
Download and prepare the FER2013 dataset for emotion recognition.

This script downloads the FER2013 dataset from Kaggle and organizes it
into a structured format for training.
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import kaggle

# Emotion labels
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def download_fer2013(data_dir='fer2013'):
    """
    Download FER2013 dataset from Kaggle.
    
    Note: Requires Kaggle API credentials (~/.kaggle/kaggle.json)
    """
    print("Downloading FER2013 dataset from Kaggle...")
    
    # Create data directory
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        # Download dataset using Kaggle API
        kaggle.api.dataset_download_files(
            'msambare/fer2013',
            path=data_dir,
            unzip=True
        )
        print(f"✓ Dataset downloaded to {data_dir}/")
        return True
    except Exception as e:
        print(f"✗ Error downloading dataset: {e}")
        print("\nPlease ensure:")
        print("1. Kaggle API is installed: pip install kaggle")
        print("2. API credentials are set up: ~/.kaggle/kaggle.json")
        print("3. You have accepted the dataset terms on Kaggle")
        return False

def load_and_verify_data(csv_path):
    """Load and verify the FER2013 dataset."""
    print(f"\nLoading data from {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} samples")
        
        # Display dataset statistics
        print("\n" + "="*50)
        print("Dataset Statistics:")
        print("="*50)
        print(f"Total samples: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        if 'emotion' in df.columns:
            print("\nEmotion Distribution:")
            emotion_counts = df['emotion'].value_counts().sort_index()
            for emotion_id, count in emotion_counts.items():
                emotion_name = EMOTIONS[emotion_id] if emotion_id < len(EMOTIONS) else f"Unknown({emotion_id})"
                percentage = (count / len(df)) * 100
                print(f"  {emotion_name:10s}: {count:5d} ({percentage:5.2f}%)")
        
        if 'Usage' in df.columns:
            print("\nData Split:")
            split_counts = df['Usage'].value_counts()
            for split, count in split_counts.items():
                percentage = (count / len(df)) * 100
                print(f"  {split:15s}: {count:5d} ({percentage:5.2f}%)")
        
        print("="*50)
        return df
    
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return None

def verify_dataset(data_dir='fer2013'):
    """Verify the downloaded dataset."""
    data_path = Path(data_dir)
    
    # Check for CSV files
    csv_files = list(data_path.glob('*.csv'))
    
    if not csv_files:
        print(f"✗ No CSV files found in {data_dir}/")
        return False
    
    print(f"✓ Found {len(csv_files)} CSV file(s):")
    for csv_file in csv_files:
        print(f"  - {csv_file.name}")
    
    # Load and verify the main dataset
    main_csv = csv_files[0]
    df = load_and_verify_data(main_csv)
    
    return df is not None

def create_sample_images(df, output_dir='fer2013/samples', num_samples=10):
    """Create sample images for visualization."""
    import cv2
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\nCreating {num_samples} sample images per emotion...")
    
    for emotion_id in range(7):
        emotion_name = EMOTIONS[emotion_id]
        emotion_df = df[df['emotion'] == emotion_id]
        
        if len(emotion_df) == 0:
            continue
        
        # Get random samples
        samples = emotion_df.sample(min(num_samples, len(emotion_df)))
        
        for idx, (_, row) in enumerate(samples.iterrows()):
            # Convert pixel string to image
            pixels = np.array([int(p) for p in row['pixels'].split()], dtype=np.uint8)
            img = pixels.reshape(48, 48)
            
            # Save image
            img_path = output_path / f"{emotion_name}_{idx}.png"
            cv2.imwrite(str(img_path), img)
    
    print(f"✓ Sample images saved to {output_dir}/")

def main():
    parser = argparse.ArgumentParser(description='Download and prepare FER2013 dataset')
    parser.add_argument('--data-dir', type=str, default='fer2013',
                        help='Directory to store dataset')
    parser.add_argument('--download', action='store_true',
                        help='Download dataset from Kaggle')
    parser.add_argument('--verify', action='store_true',
                        help='Verify existing dataset')
    parser.add_argument('--create-samples', action='store_true',
                        help='Create sample images for visualization')
    
    args = parser.parse_args()
    
    # Get absolute path
    script_dir = Path(__file__).parent
    data_dir = script_dir / args.data_dir
    
    print("="*60)
    print("FER2013 Dataset Preparation")
    print("="*60)
    
    # Download if requested
    if args.download:
        if not download_fer2013(str(data_dir)):
            sys.exit(1)
    
    # Verify dataset
    if args.verify or args.download:
        csv_path = data_dir / 'fer2013.csv'
        if not csv_path.exists():
            # Try alternative path
            csv_path = data_dir / 'train.csv'
        
        if csv_path.exists():
            df = load_and_verify_data(str(csv_path))
            
            if df is not None and args.create_samples:
                create_sample_images(df, str(data_dir / 'samples'))
        else:
            print(f"✗ Dataset CSV not found in {data_dir}/")
            print("  Run with --download flag to download the dataset")
            sys.exit(1)
    
    print("\n✓ Dataset preparation complete!")
    print("\nNext steps:")
    print("  1. Train the model: python models/train.py")
    print("  2. Evaluate the model: python models/evaluate.py")

if __name__ == '__main__':
    main()
