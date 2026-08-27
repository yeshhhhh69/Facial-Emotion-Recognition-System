# FACIAL EMOTION RECOGNITION USING CONVOLUTIONAL NEURAL NETWORKS

**A Deep Learning Project Report**

---

## TABLE OF CONTENTS

1. Introduction
2. Requirement Analysis
3. Software Requirement Specification
4. Analysis and Design
5. Implementation
6. Testing and Results
7. Conclusion
8. References

---

## 1. INTRODUCTION

### 1.1 Background

Facial emotion recognition is a critical component of affective computing that enables machines to understand human emotions through facial expressions [1]. With the advancement of deep learning, particularly Convolutional Neural Networks (CNNs), automated emotion recognition has achieved significant accuracy improvements [2].

### 1.2 Problem Statement

Traditional emotion recognition systems rely on handcrafted features and classical machine learning algorithms, which have limited accuracy and generalization capabilities. This project aims to develop a real-time facial emotion recognition system using deep CNNs that can classify seven distinct emotions with high accuracy.

### 1.3 Objectives

1. Develop a CNN-based model for 7-class emotion classification
2. Achieve >60% accuracy on the FER2013 benchmark dataset
3. Implement a real-time web-based application with webcam support
4. Create a scalable backend API for emotion prediction
5. Design an intuitive user interface for emotion visualization

### 1.4 Scope

The system classifies facial expressions into seven emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, and Neutral. It supports both real-time webcam detection and static image upload, with multi-face detection capabilities.

---

## 2. REQUIREMENT ANALYSIS

### 2.1 Functional Requirements

**FR1: Model Training**
- Train CNN on FER2013 dataset with data augmentation
- Implement early stopping and learning rate scheduling
- Save best model checkpoints during training

**FR2: Emotion Detection**
- Detect faces in images using Haar Cascade classifier
- Preprocess detected faces to 48x48 grayscale
- Predict emotion with confidence scores

**FR3: Real-time Processing**
- Process webcam frames at >15 FPS
- WebSocket-based streaming for low latency
- Handle multiple concurrent users

**FR4: User Interface**
- Webcam capture with live preview
- Image upload with drag-and-drop
- Real-time emotion visualization
- Analytics dashboard with charts

**FR5: Data Management**
- Track detection history (last 100 detections)
- Calculate session statistics
- Export data as JSON

### 2.2 Non-Functional Requirements

**NFR1: Performance**
- Inference latency: <100ms per image
- API response time: <200ms
- Model size: <50MB

**NFR2: Accuracy**
- Test accuracy: >60% on FER2013
- Per-class F1-score: >0.50

**NFR3: Usability**
- Intuitive interface with minimal learning curve
- Responsive design for all screen sizes
- Clear error messages and feedback

**NFR4: Scalability**
- Support multiple concurrent WebSocket connections
- Stateless API design for horizontal scaling

**NFR5: Maintainability**
- Modular architecture with clear separation of concerns
- Comprehensive documentation
- Version-controlled codebase

---

## 3. SOFTWARE REQUIREMENT SPECIFICATION

### 3.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                        │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│   │   Webcam     │  │    Upload    │  │  Analytics   │      │
│   │   Capture    │  │    Image     │  │  Dashboard   │      │
│   └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                    │                    │
                    │   HTTP/WebSocket   │
                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                       │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│   │  REST API    │  │  WebSocket   │  │    CORS      │      │
│   │  Endpoints   │  │   Handler    │  │  Middleware  │      │
│   └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Emotion Detector                        │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│   │ Face Detect  │  │  Preprocess  │  │  CNN Model   │      │
│   │ (Haar)       │  │  (48x48)     │  │  (TF/Keras)  │      │
│   └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Figure 3.1**: System Architecture Diagram

### 3.2 Technology Stack

**Table 3.1**: Software Components

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Deep Learning | TensorFlow/Keras | 2.13+ | Model training & inference |
| Backend Framework | FastAPI | 0.104+ | REST API & WebSocket |
| Frontend Framework | React | 18 | User interface |
| Build Tool | Vite | 5.x | Frontend bundling |
| Styling | TailwindCSS | 3.3+ | UI styling |
| Animations | Framer Motion | 10.x | UI animations |
| Charts | Recharts | 2.10+ | Data visualization |
| State Management | Zustand | 4.4+ | Global state |
| Computer Vision | OpenCV | 4.8+ | Face detection |
| HTTP Client | Axios | 1.6+ | API requests |
| Webcam | react-webcam | 7.2+ | Camera access |

### 3.3 Hardware Requirements

**Minimum:**
- Processor: Intel Core i5 or equivalent
- RAM: 8 GB
- Storage: 5 GB free space
- GPU: Not required (CPU inference)
- Webcam: Any USB/integrated camera

**Recommended:**
- Processor: Intel Core i7 or equivalent
- RAM: 16 GB
- Storage: 10 GB SSD
- GPU: NVIDIA GTX 1050 or better
- Webcam: HD (720p or higher)

---

## 4. ANALYSIS AND DESIGN

### 4.1 Dataset Analysis

**FER2013 Dataset Characteristics:**
- Total images: ~35,000
- Image size: 48×48 pixels (grayscale)
- Classes: 7 emotions
- Format: Directory structure (train/test)

**Table 4.1**: Class Distribution

| Emotion | Training | Test | Total | Percentage |
|---------|----------|------|-------|------------|
| Angry | 3,995 | 467 | 4,462 | 12.8% |
| Disgust | 436 | 56 | 492 | 1.4% |
| Fear | 4,097 | 496 | 4,593 | 13.1% |
| Happy | 7,215 | 895 | 8,110 | 23.2% |
| Sad | 4,830 | 653 | 5,483 | 15.7% |
| Surprise | 3,171 | 415 | 3,586 | 10.3% |
| Neutral | 4,965 | 626 | 5,591 | 16.0% |

**Key Observations:**
- Class imbalance: "Disgust" has only 1.4% of samples
- "Happy" is the dominant class (23.2%)
- Requires data augmentation to handle imbalance

### 4.2 CNN Architecture Design

**Model: Emotion Recognition CNN**

```
Input (48×48×1)
    ↓
[Conv Block 1] → 2×Conv2D(32) → BatchNorm → MaxPool → Dropout(0.25)
    ↓
[Conv Block 2] → 2×Conv2D(64) → BatchNorm → MaxPool → Dropout(0.25)
    ↓
[Conv Block 3] → 2×Conv2D(128) → BatchNorm → MaxPool → Dropout(0.25)
    ↓
[Conv Block 4] → 2×Conv2D(256) → BatchNorm → MaxPool → Dropout(0.25)
    ↓
Flatten
    ↓
Dense(512) → BatchNorm → Dropout(0.5)
    ↓
Dense(256) → BatchNorm → Dropout(0.5)
    ↓
Dense(7, softmax)
```

**Figure 4.1**: CNN Architecture

**Table 4.2**: Model Specifications

| Parameter | Value |
|-----------|-------|
| Total Parameters | ~3.4 million |
| Trainable Parameters | ~3.4 million |
| Model Size | ~30 MB |
| Input Shape | (48, 48, 1) |
| Output Classes | 7 |
| Activation (Hidden) | ReLU |
| Activation (Output) | Softmax |

### 4.3 API Design

**REST Endpoints:**

**Table 4.3**: API Endpoints

| Method | Endpoint | Purpose | Response |
|--------|----------|---------|----------|
| GET | `/api/health` | Health check | Status + model info |
| GET | `/api/emotions` | List emotions | Emotion labels + colors |
| GET | `/api/model/info` | Model metadata | Architecture details |
| POST | `/api/predict/image` | Upload prediction | Predictions + bboxes |
| WS | `/ws/predict` | Real-time stream | Live predictions |

### 4.4 Database Schema

**In-Memory State (Zustand):**

```javascript
{
  detections: [
    {
      timestamp: "ISO-8601",
      num_faces: 1,
      predictions: [{
        emotion: "Happy",
        confidence: 0.85,
        probabilities: {...},
        bbox: {x, y, w, h}
      }]
    }
  ],
  stats: {
    totalDetections: 150,
    emotionCounts: {...},
    averageConfidence: 0.72,
    dominantEmotion: "Happy"
  }
}
```

---

*[Continue to next section...]*

**Note**: Due to length constraints, I'll create the report in multiple files. Shall I continue with Implementation, Testing, and Results sections?
