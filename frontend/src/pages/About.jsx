import { motion } from 'framer-motion';
import { Brain, Github, Linkedin, Mail } from 'lucide-react';

const About = () => {
    return (
        <div className="container mx-auto px-4 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="max-w-4xl mx-auto"
            >
                <h1 className="text-4xl font-bold mb-8 text-center">
                    <span className="gradient-text">About This Project</span>
                </h1>

                {/* Project Description */}
                <div className="glass-card p-8 mb-8">
                    <div className="flex items-center space-x-3 mb-4">
                        <Brain className="w-8 h-8 text-purple-500" />
                        <h2 className="text-2xl font-semibold">Facial Emotion Recognition</h2>
                    </div>

                    <p className="text-gray-300 mb-4">
                        This project implements a real-time facial emotion recognition system using deep learning
                        and computer vision techniques. It can detect and classify 7 different emotions from
                        facial expressions: Angry, Disgust, Fear, Happy, Sad, Surprise, and Neutral.
                    </p>

                    <p className="text-gray-300">
                        The system uses a Convolutional Neural Network (CNN) trained on the FER2013 dataset,
                        which contains over 35,000 facial expression images. The model achieves over 60% accuracy
                        on the test set, which is competitive for this challenging task.
                    </p>
                </div>

                {/* Technical Stack */}
                <div className="glass-card p-8 mb-8">
                    <h2 className="text-2xl font-semibold mb-6">Technical Stack</h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 className="text-lg font-semibold text-purple-400 mb-3">Backend</h3>
                            <ul className="space-y-2 text-gray-300">
                                <li>• FastAPI - Modern Python web framework</li>
                                <li>• TensorFlow/Keras - Deep learning framework</li>
                                <li>• OpenCV - Computer vision library</li>
                                <li>• WebSocket - Real-time communication</li>
                            </ul>
                        </div>

                        <div>
                            <h3 className="text-lg font-semibold text-blue-400 mb-3">Frontend</h3>
                            <ul className="space-y-2 text-gray-300">
                                <li>• React 18 - UI library</li>
                                <li>• Vite - Build tool</li>
                                <li>• TailwindCSS - Styling framework</li>
                                <li>• Framer Motion - Animations</li>
                                <li>• Recharts - Data visualization</li>
                                <li>• Zustand - State management</li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Model Architecture */}
                <div className="glass-card p-8 mb-8">
                    <h2 className="text-2xl font-semibold mb-4">Model Architecture</h2>

                    <p className="text-gray-300 mb-4">
                        The CNN model consists of:
                    </p>

                    <ul className="space-y-2 text-gray-300 mb-4">
                        <li>• 4 Convolutional blocks with BatchNormalization and MaxPooling</li>
                        <li>• Dropout layers for regularization (0.25 and 0.5)</li>
                        <li>• 2 Dense layers (512 and 256 units)</li>
                        <li>• Softmax output layer for 7 emotion classes</li>
                        <li>• Total parameters: ~3-4 million</li>
                    </ul>

                    <p className="text-gray-300">
                        The model was trained for 100 epochs with data augmentation (rotation, shifting, flipping)
                        to improve generalization and prevent overfitting.
                    </p>
                </div>

                {/* Dataset */}
                <div className="glass-card p-8 mb-8">
                    <h2 className="text-2xl font-semibold mb-4">Dataset</h2>

                    <p className="text-gray-300 mb-4">
                        <strong>FER2013 (Facial Expression Recognition 2013)</strong>
                    </p>

                    <ul className="space-y-2 text-gray-300">
                        <li>• ~35,000 grayscale images (48x48 pixels)</li>
                        <li>• 7 emotion categories</li>
                        <li>• Split: Training (80%), Validation (10%), Test (10%)</li>
                        <li>• Collected from various sources and labeled by human annotators</li>
                    </ul>
                </div>

                {/* Features */}
                <div className="glass-card p-8 mb-8">
                    <h2 className="text-2xl font-semibold mb-4">Key Features</h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="glass p-4 rounded-lg">
                            <h3 className="font-semibold text-purple-400 mb-2">Real-time Detection</h3>
                            <p className="text-sm text-gray-300">
                                Live webcam feed processing with WebSocket for instant results
                            </p>
                        </div>

                        <div className="glass p-4 rounded-lg">
                            <h3 className="font-semibold text-blue-400 mb-2">Multi-face Support</h3>
                            <p className="text-sm text-gray-300">
                                Detect and analyze multiple faces in a single frame
                            </p>
                        </div>

                        <div className="glass p-4 rounded-lg">
                            <h3 className="font-semibold text-green-400 mb-2">Analytics Dashboard</h3>
                            <p className="text-sm text-gray-300">
                                Track emotion patterns with interactive charts and statistics
                            </p>
                        </div>

                        <div className="glass p-4 rounded-lg">
                            <h3 className="font-semibold text-yellow-400 mb-2">Export Functionality</h3>
                            <p className="text-sm text-gray-300">
                                Export detection history and statistics as JSON
                            </p>
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div className="glass-card p-6 text-center">
                    <p className="text-gray-300 mb-4">
                        Built as a Deep Learning project for college
                    </p>
                    <p className="text-sm text-gray-400">
                        © 2025 Facial Emotion Recognition Project
                    </p>
                </div>
            </motion.div>
        </div>
    );
};

export default About;
