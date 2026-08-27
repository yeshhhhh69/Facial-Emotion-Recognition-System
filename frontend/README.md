# Frontend - Emotion Recognition UI

Modern React frontend for the Facial Emotion Recognition system.

## Setup

1. **Install Dependencies**

```bash
npm install
```

2. **Configure API URL (Optional)**

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

3. **Run Development Server**

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Build for Production

```bash
# Build the app
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components
│   │   ├── Header.jsx
│   │   ├── WebcamCapture.jsx
│   │   ├── ImageUpload.jsx
│   │   ├── EmotionDisplay.jsx
│   │   └── StatsDashboard.jsx
│   ├── pages/               # Page components
│   │   ├── Home.jsx
│   │   ├── LiveDetection.jsx
│   │   ├── Analytics.jsx
│   │   └── About.jsx
│   ├── store/               # State management
│   │   └── emotionStore.js
│   ├── utils/               # Utilities
│   │   ├── api.js
│   │   └── constants.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Features

### Pages

- **Home**: Landing page with features and tech stack
- **Live Detection**: Real-time webcam and image upload detection
- **Analytics**: Statistics dashboard with charts
- **About**: Project information and documentation

### Components

- **WebcamCapture**: Real-time webcam feed with WebSocket
- **ImageUpload**: Drag-and-drop image upload
- **EmotionDisplay**: Emotion results with confidence bars
- **StatsDashboard**: Session statistics and breakdown
- **Header**: Navigation with active tab highlighting

### State Management

Using Zustand for global state:
- Detection history
- Current prediction
- Session statistics
- WebSocket connection status

## Styling

- **TailwindCSS**: Utility-first CSS framework
- **Glassmorphism**: Modern glass-like UI elements
- **Framer Motion**: Smooth animations and transitions
- **Custom Theme**: Dark mode with purple/pink gradients

## Scripts

```bash
# Development
npm run dev

# Build
npm run build

# Preview production build
npm run preview

# Lint
npm run lint
```
