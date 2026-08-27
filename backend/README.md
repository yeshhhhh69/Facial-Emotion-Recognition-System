# Backend - Facial Emotion Recognition API

FastAPI backend for real-time emotion recognition.

## Setup

1. **Install Dependencies**

```bash
pip install -r requirements.txt
```

2. **Ensure Model is Trained**

The model should be located at `saved_models/emotion_model.h5`. If not, train it first:

```bash
cd ../ml_pipeline
python models/train.py
```

3. **Run the Server**

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the backend directory:

```env
# API Settings
DEBUG=True

# Model Settings
MODEL_PATH=saved_models/emotion_model.h5
CONFIDENCE_THRESHOLD=0.3

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## API Endpoints

### REST Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `POST /api/predict/image` - Upload image for prediction
- `GET /api/emotions` - Get list of emotions with colors
- `GET /api/model/info` - Get model information

### WebSocket

- `WS /ws/predict` - Real-time prediction stream

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes.py         # REST API endpoints
│   │   └── websocket.py      # WebSocket endpoint
│   ├── core/
│   │   ├── config.py         # Configuration
│   │   └── emotion_detector.py  # Inference engine
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   └── main.py               # FastAPI app
├── saved_models/             # Trained models
└── requirements.txt
```

## Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/api/health

# Get emotions
curl http://localhost:8000/api/emotions

# Predict from image
curl -X POST -F "file=@path/to/image.jpg" http://localhost:8000/api/predict/image
```
