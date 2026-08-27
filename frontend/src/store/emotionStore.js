import { create } from 'zustand';

const useEmotionStore = create((set, get) => ({
    // State
    detections: [],
    currentPrediction: null,
    isDetecting: false,
    wsConnected: false,

    // Statistics
    stats: {
        totalDetections: 0,
        emotionCounts: {
            Angry: 0,
            Disgust: 0,
            Fear: 0,
            Happy: 0,
            Sad: 0,
            Surprise: 0,
            Neutral: 0,
        },
        averageConfidence: 0,
        dominantEmotion: null,
    },

    // Actions
    addDetection: (prediction) => {
        const timestamp = new Date().toISOString();
        const detection = { ...prediction, timestamp };

        set((state) => {
            const newDetections = [detection, ...state.detections].slice(0, 100); // Keep last 100

            // Update statistics
            const newStats = { ...state.stats };
            newStats.totalDetections += 1;

            // Update emotion counts
            prediction.predictions.forEach((pred) => {
                newStats.emotionCounts[pred.emotion] += 1;
            });

            // Calculate dominant emotion
            const maxEmotion = Object.entries(newStats.emotionCounts).reduce((a, b) =>
                a[1] > b[1] ? a : b
            );
            newStats.dominantEmotion = maxEmotion[0];

            // Calculate average confidence
            const totalConfidence = newDetections.reduce((sum, det) => {
                const avgConf = det.predictions.reduce((s, p) => s + p.confidence, 0) / det.predictions.length;
                return sum + avgConf;
            }, 0);
            newStats.averageConfidence = totalConfidence / newDetections.length;

            return {
                detections: newDetections,
                currentPrediction: prediction,
                stats: newStats,
            };
        });
    },

    setCurrentPrediction: (prediction) => set({ currentPrediction: prediction }),

    setIsDetecting: (isDetecting) => set({ isDetecting }),

    setWsConnected: (connected) => set({ wsConnected: connected }),

    clearHistory: () =>
        set({
            detections: [],
            stats: {
                totalDetections: 0,
                emotionCounts: {
                    Angry: 0,
                    Disgust: 0,
                    Fear: 0,
                    Happy: 0,
                    Sad: 0,
                    Surprise: 0,
                    Neutral: 0,
                },
                averageConfidence: 0,
                dominantEmotion: null,
            },
        }),

    exportData: () => {
        const state = get();
        const data = {
            detections: state.detections,
            stats: state.stats,
            exportedAt: new Date().toISOString(),
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `emotion-detections-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    },
}));

export default useEmotionStore;
