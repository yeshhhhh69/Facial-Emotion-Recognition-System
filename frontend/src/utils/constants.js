// Emotion labels and colors
export const EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'];

export const EMOTION_COLORS = {
    Angry: '#EF4444',
    Disgust: '#10B981',
    Fear: '#8B5CF6',
    Happy: '#F59E0B',
    Sad: '#3B82F6',
    Surprise: '#F97316',
    Neutral: '#6B7280',
};

export const EMOTION_EMOJIS = {
    Angry: '😠',
    Disgust: '🤢',
    Fear: '😨',
    Happy: '😊',
    Sad: '😢',
    Surprise: '😲',
    Neutral: '😐',
};

// API base URL
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
export const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

// File upload settings
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
