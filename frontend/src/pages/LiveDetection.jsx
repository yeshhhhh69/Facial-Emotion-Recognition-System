import { useState } from 'react';
import { motion } from 'framer-motion';
import { Camera, Upload } from 'lucide-react';
import WebcamCapture from '../components/WebcamCapture';
import ImageUpload from '../components/ImageUpload';
import EmotionDisplay from '../components/EmotionDisplay';
import StatsDashboard from '../components/StatsDashboard';
import useEmotionStore from '../store/emotionStore';

const LiveDetection = () => {
    const [activeTab, setActiveTab] = useState('webcam');
    const { currentPrediction } = useEmotionStore();

    return (
        <div className="container mx-auto px-4 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h1 className="text-4xl font-bold mb-8 text-center">
                    <span className="gradient-text">Live Emotion Detection</span>
                </h1>

                {/* Tab Selector */}
                <div className="flex justify-center mb-8">
                    <div className="glass-card p-1 inline-flex rounded-lg">
                        <button
                            onClick={() => setActiveTab('webcam')}
                            className={`px-6 py-3 rounded-lg flex items-center space-x-2 transition-all ${activeTab === 'webcam'
                                    ? 'bg-purple-600 text-white'
                                    : 'text-gray-300 hover:text-white'
                                }`}
                        >
                            <Camera className="w-5 h-5" />
                            <span>Webcam</span>
                        </button>

                        <button
                            onClick={() => setActiveTab('upload')}
                            className={`px-6 py-3 rounded-lg flex items-center space-x-2 transition-all ${activeTab === 'upload'
                                    ? 'bg-purple-600 text-white'
                                    : 'text-gray-300 hover:text-white'
                                }`}
                        >
                            <Upload className="w-5 h-5" />
                            <span>Upload Image</span>
                        </button>
                    </div>
                </div>

                {/* Main Content */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Left: Webcam/Upload */}
                    <div className="lg:col-span-2">
                        {activeTab === 'webcam' ? (
                            <WebcamCapture />
                        ) : (
                            <ImageUpload />
                        )}
                    </div>

                    {/* Right: Results */}
                    <div className="space-y-6">
                        {currentPrediction ? (
                            <>
                                <EmotionDisplay prediction={currentPrediction} />
                                <StatsDashboard />
                            </>
                        ) : (
                            <div className="glass-card p-8 text-center">
                                <p className="text-gray-400">
                                    {activeTab === 'webcam'
                                        ? 'Start webcam to detect emotions'
                                        : 'Upload an image to detect emotions'}
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default LiveDetection;
