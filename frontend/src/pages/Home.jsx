import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Brain, Video, BarChart3, Sparkles, Zap, Shield } from 'lucide-react';

const Home = () => {
    const features = [
        {
            icon: Video,
            title: 'Real-time Detection',
            description: 'Detect emotions from live webcam feed with instant results',
            color: 'text-purple-400',
        },
        {
            icon: BarChart3,
            title: 'Analytics Dashboard',
            description: 'Track and visualize emotion patterns over time',
            color: 'text-blue-400',
        },
        {
            icon: Sparkles,
            title: 'Multi-face Support',
            description: 'Analyze multiple faces simultaneously in one frame',
            color: 'text-pink-400',
        },
        {
            icon: Zap,
            title: 'Fast & Accurate',
            description: 'Powered by deep learning CNN with 60%+ accuracy',
            color: 'text-yellow-400',
        },
        {
            icon: Shield,
            title: 'Privacy First',
            description: 'All processing happens locally, no data stored',
            color: 'text-green-400',
        },
        {
            icon: Brain,
            title: '7 Emotions',
            description: 'Recognizes Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral',
            color: 'text-orange-400',
        },
    ];

    return (
        <div className="container mx-auto px-4 py-12">
            {/* Hero Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-center mb-16"
            >
                <h1 className="text-5xl md:text-7xl font-bold mb-6">
                    <span className="gradient-text">Facial Emotion</span>
                    <br />
                    <span className="text-white">Recognition</span>
                </h1>

                <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                    Experience the power of deep learning with real-time emotion detection
                    using state-of-the-art Convolutional Neural Networks
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link to="/live">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg font-semibold text-white shadow-lg hover:shadow-purple-500/50 transition-shadow"
                        >
                            Start Detection
                        </motion.button>
                    </Link>

                    <Link to="/analytics">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 glass-card rounded-lg font-semibold text-white hover:bg-white/10 transition-colors"
                        >
                            View Analytics
                        </motion.button>
                    </Link>
                </div>
            </motion.div>

            {/* Features Grid */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3, duration: 0.6 }}
                className="mb-16"
            >
                <h2 className="text-3xl font-bold text-center mb-12">
                    <span className="gradient-text">Features</span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {features.map((feature, index) => {
                        const Icon = feature.icon;

                        return (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index, duration: 0.5 }}
                                whileHover={{ y: -5 }}
                                className="glass-card p-6 hover:bg-white/10 transition-all cursor-pointer"
                            >
                                <Icon className={`w-12 h-12 ${feature.color} mb-4`} />
                                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                                <p className="text-gray-400">{feature.description}</p>
                            </motion.div>
                        );
                    })}
                </div>
            </motion.div>

            {/* Tech Stack */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6, duration: 0.6 }}
                className="glass-card p-8 text-center"
            >
                <h2 className="text-2xl font-bold mb-4">
                    <span className="gradient-text">Powered By</span>
                </h2>
                <p className="text-gray-300 mb-6">
                    Built with modern technologies for optimal performance
                </p>
                <div className="flex flex-wrap justify-center gap-4 text-sm">
                    <span className="px-4 py-2 bg-purple-500/20 rounded-full">TensorFlow</span>
                    <span className="px-4 py-2 bg-blue-500/20 rounded-full">React</span>
                    <span className="px-4 py-2 bg-green-500/20 rounded-full">FastAPI</span>
                    <span className="px-4 py-2 bg-yellow-500/20 rounded-full">OpenCV</span>
                    <span className="px-4 py-2 bg-pink-500/20 rounded-full">TailwindCSS</span>
                </div>
            </motion.div>
        </div>
    );
};

export default Home;
