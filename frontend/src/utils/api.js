import axios from 'axios';
import { API_BASE_URL } from './constants';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Predict emotion from image file
export const predictImage = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/predict/image', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

// Get list of emotions
export const getEmotions = async () => {
    const response = await api.get('/api/emotions');
    return response.data;
};

// Get model information
export const getModelInfo = async () => {
    const response = await api.get('/api/model/info');
    return response.data;
};

// Health check
export const healthCheck = async () => {
    const response = await api.get('/api/health');
    return response.data;
};

export default api;
