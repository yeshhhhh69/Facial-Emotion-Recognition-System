# ML Pipeline - Model Training and Evaluation

Machine learning pipeline for training the emotion recognition CNN model.

## Setup

1. **Create Virtual Environment**

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Up Kaggle API**

Download your Kaggle API credentials:
1. Go to https://www.kaggle.com/account
2. Click "Create New API Token"
3. Place `kaggle.json` in `~/.kaggle/` directory

## Download Dataset

```bash
python data/download_data.py --download --verify --create-samples
```

This will:
- Download the FER2013 dataset from Kaggle
- Verify the data integrity
- Display dataset statistics
- Create sample images for visualization

## Train Model

### Full Model (Recommended)

```bash
python models/train.py --epochs 100 --batch-size 64
```

### Lightweight Model (Faster)

```bash
python models/train.py --model-type lightweight --epochs 50 --batch-size 64
```

### Training Options

```bash
python models/train.py --help

Options:
  --data-path PATH          Path to FER2013 CSV file
  --model-type TYPE         Model architecture (full/lightweight)
  --epochs N                Number of training epochs
  --batch-size N            Batch size for training
  --learning-rate FLOAT     Initial learning rate
  --output-dir PATH         Output directory for models
```

## Evaluate Model

```bash
python models/evaluate.py
```

This generates:
- Confusion matrix
- Per-class metrics (precision, recall, F1-score)
- Sample predictions visualization
- Evaluation metrics JSON

## Model Architecture

### Full CNN Model

- **Input**: 48x48 grayscale images
- **Conv Block 1**: 2x Conv2D(32) + BatchNorm + MaxPool + Dropout(0.25)
- **Conv Block 2**: 2x Conv2D(64) + BatchNorm + MaxPool + Dropout(0.25)
- **Conv Block 3**: 2x Conv2D(128) + BatchNorm + MaxPool + Dropout(0.25)
- **Conv Block 4**: 2x Conv2D(256) + BatchNorm + MaxPool + Dropout(0.25)
- **Dense 1**: 512 units + BatchNorm + Dropout(0.5)
- **Dense 2**: 256 units + BatchNorm + Dropout(0.5)
- **Output**: 7 units (softmax)

**Total Parameters**: ~3-4 million

### Training Configuration

- **Optimizer**: Adam (lr=0.0001)
- **Loss**: Categorical Crossentropy
- **Callbacks**:
  - ModelCheckpoint: Save best model
  - EarlyStopping: Patience 15 epochs
  - ReduceLROnPlateau: Reduce LR by 0.5
  - CSVLogger: Log metrics
  - TensorBoard: Visualize training

### Data Augmentation

- Rotation: ±15 degrees
- Width/Height shift: 10%
- Shear: 10%
- Zoom: 10%
- Horizontal flip
- Fill mode: nearest

## Dataset Information

**FER2013 (Facial Expression Recognition 2013)**

- **Total Images**: ~35,000
- **Image Size**: 48x48 pixels (grayscale)
- **Classes**: 7 emotions
- **Split**:
  - Training: ~28,000 images
  - Validation: ~3,500 images
  - Test: ~3,500 images

### Class Distribution

- Angry: ~4,000 images
- Disgust: ~500 images (imbalanced)
- Fear: ~5,000 images
- Happy: ~9,000 images
- Sad: ~6,000 images
- Surprise: ~4,000 images
- Neutral: ~6,000 images

## Outputs

After training, the following files are created in `../backend/saved_models/`:

- `emotion_model.h5` - Final model (H5 format)
- `emotion_model/` - SavedModel format
- `best_model_*.h5` - Best model checkpoint
- `training_history_*.json` - Training metrics
- `test_results.json` - Test set results
- `evaluation_metrics.json` - Detailed metrics
- `confusion_matrix.png` - Confusion matrix plot
- `per_class_metrics.png` - Metrics visualization
- `sample_predictions.png` - Sample predictions

## View Training Progress

Use TensorBoard to monitor training:

```bash
tensorboard --logdir=../backend/saved_models/logs
```

Then open `http://localhost:6006` in your browser.
