# Quick Start Guide - Backend Issues

## The Problem
Your frontend is working but can't connect to the backend because the backend server isn't responding properly.

## Solution: Restart the Backend

### Step 1: Stop the Current Backend
In the terminal where you ran the backend command, press `Ctrl+C` to stop it.

### Step 2: Start the Backend Correctly

**Option A: Using the run.py script (Recommended)**
```bash
cd backend
python run.py
```

**Option B: Using uvicorn directly**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 3: Wait for Success Message

You should see:
```
======================================================================
Starting Facial Emotion Recognition API v1.0.0
======================================================================

Loading model from: saved_models\emotion_model.h5
✓ Model loaded successfully

======================================================================
Server is ready!
API Documentation: http://127.0.0.1:8000/docs
WebSocket endpoint: ws://127.0.0.1:8000/ws/predict
======================================================================

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 4: Test the Backend

Open your browser and go to:
- `http://127.0.0.1:8000/docs` - You should see the API documentation

### Step 5: Refresh Your Frontend

Once the backend is running, refresh your frontend page at `http://localhost:5173`

---

## If You See Errors

**Error: "Address already in use"**
```bash
# Find and kill the process using port 8000
netstat -ano | findstr :8000
# Then kill the process (replace PID with the number from above)
taskkill /PID <PID> /F
```

**Error: "Module not found"**
```bash
cd backend
pip install -r requirements.txt
```

**Error: "Model not found"**
Make sure the model file exists at `backend/saved_models/emotion_model.h5`

---

## Quick Test

After starting the backend, run this in a new terminal:
```bash
cd backend
python test_api.py
```

You should see successful responses from all 3 endpoints.
