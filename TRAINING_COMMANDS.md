# Training Commands Guide

## Current Model
- **Location**: `backend/saved_models/emotion_model.h5`
- **Accuracy**: 67%
- **Epochs Trained**: 46 (stopped early)

---

## Train for Full 100 Epochs

### Method 1: Quick Command (Recommended)

```bash
cd ml_pipeline
python models/train.py --epochs 100 --batch-size 64
```

**Note**: This will still use Early Stopping. If validation doesn't improve for 15 epochs, it will stop early.

---

### Method 2: Train WITHOUT Early Stopping (Force 100 Epochs)

To disable early stopping and train all 100 epochs:

```bash
cd ml_pipeline
python models/train_no_early_stop.py --epochs 100 --batch-size 64
```

I'll create this script for you below.

---

### Method 3: Continue Training from Current Model

To continue training from your current 67% model:

```bash
cd ml_pipeline
python models/train.py --epochs 100 --batch-size 64 --resume-from ../backend/saved_models/emotion_model.h5
```

---

## Training Options

### Full Model (Best Accuracy)
```bash
python models/train.py --model-type full --epochs 100 --batch-size 64
```

### Lightweight Model (Faster)
```bash
python models/train.py --model-type lightweight --epochs 100 --batch-size 32
```

### With Custom Learning Rate
```bash
python models/train.py --epochs 100 --batch-size 64 --learning-rate 0.0001
```

---

## What Happens During Training

1. **Epochs 1-20**: Model learns basic features (edges, shapes)
2. **Epochs 20-40**: Model learns emotion patterns
3. **Epochs 40-60**: Fine-tuning and refinement
4. **Epochs 60-100**: Risk of overfitting (why early stopping exists)

---

## Expected Results

- **With Early Stopping**: Likely stops at 45-50 epochs (~65-70% accuracy)
- **Without Early Stopping**: Runs full 100 epochs (~68-72% accuracy, but may overfit)

---

## After Training Completes

The new model will be saved to:
- `backend/saved_models/emotion_model.h5` (overwrites old one)
- `backend/saved_models/best_model_[timestamp].h5` (best checkpoint)

To use the new model:
1. Restart the backend server
2. The new model will be loaded automatically

---

## Monitoring Training

### View Progress in Real-time
```bash
# In another terminal
cd ml_pipeline
tensorboard --logdir=../backend/saved_models/logs
```

Then open: `http://localhost:6006`

---

## Quick Copy-Paste Commands

**Standard Training (with early stopping):**
```bash
cd "C:\Users\salel\OneDrive\Desktop\College files & projects\DL Project\Emotion Recognition\ml_pipeline"
python models/train.py --epochs 100 --batch-size 64
```

**Force 100 Epochs (no early stopping):**
```bash
cd "C:\Users\salel\OneDrive\Desktop\College files & projects\DL Project\Emotion Recognition\ml_pipeline"
python models/train_no_early_stop.py --epochs 100 --batch-size 64
```

---

## Time Estimates

- **Full 100 epochs**: ~45-60 minutes
- **With early stopping**: ~30-40 minutes (stops around epoch 45-50)
