# Kaggle API Setup Guide

## Option 1: Set Up Kaggle API (Recommended)

### Step 1: Get Your Kaggle API Token

1. Go to https://www.kaggle.com/ and sign in (create an account if you don't have one)
2. Click on your profile picture in the top right
3. Select "Settings" from the dropdown
4. Scroll down to the "API" section
5. Click "Create New API Token"
6. This will download a file called `kaggle.json`

### Step 2: Place the kaggle.json File

**On Windows:**
1. Create the `.kaggle` directory if it doesn't exist:
   ```powershell
   mkdir C:\Users\salel\.kaggle
   ```

2. Move the downloaded `kaggle.json` file to `C:\Users\salel\.kaggle\`

3. Verify the file is in the correct location:
   ```powershell
   dir C:\Users\salel\.kaggle\kaggle.json
   ```

### Step 3: Download the Dataset

```bash
cd ml_pipeline
python data/download_data.py --download --verify
```

---

## Option 2: Manual Dataset Download (Alternative)

If you prefer not to use the Kaggle API, you can download the dataset manually:

### Step 1: Download from Kaggle Website

1. Go to https://www.kaggle.com/datasets/msambare/fer2013
2. Click the "Download" button (you'll need to sign in)
3. Extract the downloaded ZIP file

### Step 2: Place the Dataset

1. Create the data directory:
   ```powershell
   mkdir ml_pipeline\data\fer2013
   ```

2. Copy the CSV file(s) to `ml_pipeline\data\fer2013\`
   - The main file should be `fer2013.csv` or similar

### Step 3: Verify the Dataset

```bash
python data/download_data.py --verify
```

---

## Option 3: Use a Pre-trained Model (Fastest)

If you want to skip training and just test the application, I can provide instructions to use a lightweight pre-trained model or train a smaller model quickly.

---

## Troubleshooting

### Kaggle API Not Found
```bash
pip install kaggle
```

### Permission Issues
Make sure the `kaggle.json` file has the correct permissions. On Windows, this is usually automatic.

### Dataset Not Found
Verify the CSV file is in the correct location:
```powershell
dir ml_pipeline\data\fer2013\*.csv
```

---

## Next Steps After Dataset Setup

Once you have the dataset ready:

1. **Verify the data**:
   ```bash
   python data/download_data.py --verify
   ```

2. **Train the model**:
   ```bash
   python models/train.py --epochs 100
   ```

   Or for a quick test (5 epochs):
   ```bash
   python models/train.py --epochs 5 --batch-size 32
   ```
