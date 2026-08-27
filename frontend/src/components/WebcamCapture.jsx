import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, CameraOff, Wifi, WifiOff } from 'lucide-react';
import { motion } from 'framer-motion';
import useEmotionStore from '../store/emotionStore';
import { WS_BASE_URL } from '../utils/constants';

const WebcamCapture = () => {
    const webcamRef = useRef(null);
    const wsRef = useRef(null);
    const [isActive, setIsActive] = useState(false);
    const [error, setError] = useState(null);
    const { addDetection, setWsConnected, wsConnected } = useEmotionStore();

    const connectWebSocket = useCallback(() => {
        try {
            const ws = new WebSocket(`${WS_BASE_URL}/ws/predict`);

            ws.onopen = () => {
                console.log('WebSocket connected');
                setWsConnected(true);
                setError(null);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.success && data.predictions) {
                    addDetection(data);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                setError('WebSocket connection failed');
                setWsConnected(false);
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                setWsConnected(false);
            };

            wsRef.current = ws;
        } catch (err) {
            setError('Failed to connect to server');
            console.error(err);
        }
    }, [addDetection, setWsConnected]);

    const disconnectWebSocket = useCallback(() => {
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
    }, []);

    const startDetection = useCallback(() => {
        setIsActive(true);
        connectWebSocket();

        // Send frames every 500ms
        const interval = setInterval(() => {
            if (webcamRef.current && wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
                const imageSrc = webcamRef.current.getScreenshot();
                if (imageSrc) {
                    wsRef.current.send(JSON.stringify({
                        image: imageSrc,
                        timestamp: Date.now()
                    }));
                }
            }
        }, 500);

        return () => clearInterval(interval);
    }, [connectWebSocket]);

    const stopDetection = useCallback(() => {
        setIsActive(false);
        disconnectWebSocket();
    }, [disconnectWebSocket]);

    return (
        <div className="glass-card p-6">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-semibold">Webcam Feed</h2>

                <div className="flex items-center space-x-2">
                    {wsConnected ? (
                        <div className="flex items-center space-x-2 text-green-400">
                            <Wifi className="w-4 h-4" />
                            <span className="text-sm">Connected</span>
                        </div>
                    ) : (
                        <div className="flex items-center space-x-2 text-gray-400">
                            <WifiOff className="w-4 h-4" />
                            <span className="text-sm">Disconnected</span>
                        </div>
                    )}
                </div>
            </div>

            {error && (
                <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 mb-4">
                    <p className="text-red-400 text-sm">{error}</p>
                </div>
            )}

            <div className="relative aspect-video bg-gray-900 rounded-lg overflow-hidden mb-4">
                {isActive ? (
                    <Webcam
                        ref={webcamRef}
                        audio={false}
                        screenshotFormat="image/jpeg"
                        className="w-full h-full object-cover"
                        mirrored
                        onUserMediaError={(err) => {
                            setError('Failed to access webcam. Please grant camera permissions.');
                            console.error(err);
                        }}
                    />
                ) : (
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                            <Camera className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                            <p className="text-gray-400">Webcam is off</p>
                        </div>
                    </div>
                )}
            </div>

            <div className="flex justify-center">
                {!isActive ? (
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={startDetection}
                        className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-semibold flex items-center space-x-2"
                    >
                        <Camera className="w-5 h-5" />
                        <span>Start Webcam</span>
                    </motion.button>
                ) : (
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={stopDetection}
                        className="px-6 py-3 bg-red-600 rounded-lg font-semibold flex items-center space-x-2"
                    >
                        <CameraOff className="w-5 h-5" />
                        <span>Stop Webcam</span>
                    </motion.button>
                )}
            </div>
        </div>
    );
};

export default WebcamCapture;
