import { motion } from 'framer-motion';
import { TrendingUp, Target, Award } from 'lucide-react';
import useEmotionStore from '../store/emotionStore';
import { EMOTION_COLORS } from '../utils/constants';

const StatsDashboard = () => {
    const { stats } = useEmotionStore();

    return (
        <div className="glass-card p-6">
            <h3 className="text-xl font-semibold mb-4">Session Statistics</h3>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-4 mb-6">
                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="glass p-4 rounded-lg"
                >
                    <div className="flex items-center space-x-2 mb-2">
                        <TrendingUp className="w-4 h-4 text-blue-400" />
                        <span className="text-xs text-gray-400">Total</span>
                    </div>
                    <p className="text-2xl font-bold">{stats.totalDetections}</p>
                </motion.div>

                <motion.div
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="glass p-4 rounded-lg"
                >
                    <div className="flex items-center space-x-2 mb-2">
                        <Target className="w-4 h-4 text-green-400" />
                        <span className="text-xs text-gray-400">Confidence</span>
                    </div>
                    <p className="text-2xl font-bold">
                        {(stats.averageConfidence * 100).toFixed(0)}%
                    </p>
                </motion.div>
            </div>

            {/* Dominant Emotion */}
            {stats.dominantEmotion && (
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="glass p-4 rounded-lg mb-4"
                >
                    <div className="flex items-center space-x-2 mb-2">
                        <Award className="w-4 h-4 text-yellow-400" />
                        <span className="text-xs text-gray-400">Dominant Emotion</span>
                    </div>
                    <p
                        className="text-xl font-bold"
                        style={{ color: EMOTION_COLORS[stats.dominantEmotion] }}
                    >
                        {stats.dominantEmotion}
                    </p>
                    <p className="text-sm text-gray-400">
                        {stats.emotionCounts[stats.dominantEmotion]} detections
                    </p>
                </motion.div>
            )}

            {/* Emotion Breakdown */}
            <div className="space-y-2">
                <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    Emotion Breakdown
                </h4>

                {Object.entries(stats.emotionCounts)
                    .filter(([_, count]) => count > 0)
                    .sort((a, b) => b[1] - a[1])
                    .map(([emotion, count], index) => {
                        const percentage = stats.totalDetections > 0
                            ? (count / stats.totalDetections) * 100
                            : 0;

                        return (
                            <motion.div
                                key={emotion}
                                initial={{ x: -20, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                transition={{ delay: 0.3 + index * 0.05 }}
                                className="flex items-center justify-between"
                            >
                                <div className="flex items-center space-x-2 flex-1">
                                    <div
                                        className="w-3 h-3 rounded-full"
                                        style={{ backgroundColor: EMOTION_COLORS[emotion] }}
                                    />
                                    <span className="text-sm text-gray-300">{emotion}</span>
                                </div>

                                <div className="flex items-center space-x-2">
                                    <div className="w-16 h-1.5 bg-gray-700 rounded-full overflow-hidden">
                                        <div
                                            className="h-full rounded-full"
                                            style={{
                                                width: `${percentage}%`,
                                                backgroundColor: EMOTION_COLORS[emotion],
                                            }}
                                        />
                                    </div>
                                    <span className="text-xs text-gray-400 w-8 text-right">
                                        {count}
                                    </span>
                                </div>
                            </motion.div>
                        );
                    })}
            </div>

            {stats.totalDetections === 0 && (
                <p className="text-center text-gray-400 py-8 text-sm">
                    No detections yet. Start detecting to see statistics.
                </p>
            )}
        </div>
    );
};

export default StatsDashboard;
