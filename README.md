# Facial Emotion Recognition using CNNs

A professional-grade real-time facial emotion recognition system built with deep learning, featuring a modern React frontend and FastAPI backend.

![Project Banner](https://img.shields.io/badge/Deep%20Learning-Emotion%20Recognition-purple?style=for-the-badge)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange?style=flat-square)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=flat-square)

## Overview

This project implements a state-of-the-art emotion recognition system that can detect and classify 7 different emotions from facial expressions in real-time:

- 😠 **Angry**
- 🤢 **Disgust**
- 😨 **Fear**
- 😊 **Happy**
- 😢 **Sad**
- 😲 **Surprise**
- 😐 **Neutral**

### Key Features

- **Real-time Detection**: Live webcam feed processing with WebSocket
- **Multi-face Support**: Detect and analyze multiple faces simultaneously
- **Analytics Dashboard**: Track emotion patterns with interactive charts
- **Modern UI**: Beautiful glassmorphism design with smooth animations
- **Fast & Accurate**: CNN model with 60%+ accuracy on FER2013 dataset
- **Privacy First**: All processing happens locally, no data stored on servers
- **Export Functionality**: Export detection history as JSON

## Architecture

### Technology Stack

**Frontend:**
- React 18 + Vite
- TailwindCSS for styling
- Framer Motion for animations
- Recharts for data visualization
- Zustand for state management
- React Webcam for camera access

**Backend:**
- FastAPI with async/await support
- WebSocket for real-time communication
- TensorFlow/Keras for deep learning
- OpenCV for computer vision
- Pydantic for data validation

**Machine Learning:**
- CNN with 4 convolutional blocks
- Batch normalization and dropout
- Trained on FER2013 dataset
- ~3-4 million parameters

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Webcam (for live detection)
- Kaggle account (for dataset download)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "Emotion Recognition"
```

### 2. Set Up ML Pipeline

```bash
cd ml_pipeline

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Download Dataset

First, set up Kaggle API credentials:

1. Go to https://www.kaggle.com/account
2. Create a new API token (downloads `kaggle.json`)
3. Place `kaggle.json` in `~/.kaggle/` directory

Then download the dataset:

```bash
python data/download_data.py --download --verify
```

### 4. Train the Model

```bash
# Train the full model (takes 30-60 minutes)
python models/train.py --epochs 100 --batch-size 64

# Or train a lightweight model for faster training
python models/train.py --model-type lightweight --epochs 50
```

The trained model will be saved to `backend/saved_models/emotion_model.h5`.

### 5. Set Up Backend

```bash
cd ../backend

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with auto-generated docs at `http://localhost:8000/docs`.

### 6. Set Up Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Usage

### Live Detection

1. Navigate to the **Live Detection** page
2. Click "Start Webcam" to begin real-time detection
3. The system will detect faces and display emotions with confidence scores
4. View real-time statistics in the sidebar

### Image Upload

1. Go to the **Live Detection** page
2. Switch to the "Upload Image" tab
3. Drag and drop an image or click to select
4. View detected emotions and confidence scores

### Analytics

1. Visit the **Analytics** page
2. View comprehensive statistics and charts
3. Export detection history as JSON
4. Clear history when needed

## Project Structure

```
Emotion Recognition/
├── ml_pipeline/              # Machine learning pipeline
│   ├── data/                 # Dataset and download scripts
│   ├── models/               # Model architecture and training
│   ├── utils/                # Preprocessing utilities
│   └── notebooks/            # Jupyter notebooks for analysis
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/              # API routes and WebSocket
│   │   ├── core/             # Core logic and config
│   │   └── models/           # Pydantic schemas
│   └── saved_models/         # Trained model weights
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   ├── store/            # Zustand state management
│   │   └── utils/            # Utilities and API client
│   └── public/               # Static assets
└── README.md                 # This file
```

## API Endpoints

### REST API

- `POST /api/predict/image` - Upload image for emotion prediction
- `GET /api/emotions` - Get list of supported emotions with colors
- `GET /api/model/info` - Get model information and metadata
- `GET /api/health` - Health check endpoint

### WebSocket

- `WS /ws/predict` - Real-time emotion prediction from webcam frames

## Model Performance

- **Dataset**: FER2013 (~35,000 images)
- **Test Accuracy**: >60%
- **Inference Time**: <100ms per image
- **Real-time FPS**: >20 FPS on webcam

### Per-Class Metrics

Detailed metrics are available after training in `backend/saved_models/evaluation_metrics.json`.

## Future Improvements

- [ ] Add emotion intensity detection
- [ ] Implement facial landmark detection
- [ ] Add age and gender prediction
- [ ] Support for video file upload
- [ ] Mobile app version
- [ ] Model quantization for faster inference
- [ ] Multi-language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is created for educational purposes as a college Deep Learning project.

## Acknowledgments

- **FER2013 Dataset**: Challenges in Representation Learning: Facial Expression Recognition Challenge
- **TensorFlow/Keras**: Deep learning framework
- **FastAPI**: Modern Python web framework
- **React**: UI library

## Contact

For questions or feedback, please reach out through the project repository.

---

**Built by Yeshved Salelkar for Deep Learning Course Project**
