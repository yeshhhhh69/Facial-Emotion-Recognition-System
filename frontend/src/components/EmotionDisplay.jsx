import { motion } from 'framer-motion';
import { EMOTION_COLORS, EMOTION_EMOJIS } from '../utils/constants';

const EmotionDisplay = ({ prediction }) => {
    if (!prediction || !prediction.predictions || prediction.predictions.length === 0) {
        return (
            <div className="glass-card p-6 text-center">
                <p className="text-gray-400">No emotions detected</p>
            </div>
        );
    }

    // Get the first prediction (primary face)
    const primaryPrediction = prediction.predictions[0];
    const { emotion, confidence, probabilities } = primaryPrediction;

    return (
        <div className="glass-card p-6">
            <h3 className="text-xl font-semibold mb-4">Detected Emotion</h3>

            {/* Primary Emotion */}
            <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="text-center mb-6"
            >
                <div className="text-6xl mb-3">{EMOTION_EMOJIS[emotion]}</div>
                <h2
                    className="text-3xl font-bold mb-2"
                    style={{ color: EMOTION_COLORS[emotion] }}
                >
                    {emotion}
                </h2>
                <div className="flex items-center justify-center space-x-2">
                    <div className="w-32 h-2 bg-gray-700 rounded-full overflow-hidden">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${confidence * 100}%` }}
                            transition={{ duration: 0.5 }}
                            className="h-full rounded-full"
                            style={{ backgroundColor: EMOTION_COLORS[emotion] }}
                        />
                    </div>
                    <span className="text-lg font-semibold">
                        {(confidence * 100).toFixed(1)}%
                    </span>
                </div>
            </motion.div>

            {/* All Probabilities */}
            <div className="space-y-2">
                <h4 className="text-sm font-semibold text-gray-400 mb-3">
                    All Emotions
                </h4>

                {Object.entries(probabilities)
                    .sort((a, b) => b[1] - a[1])
                    .map(([emotionName, prob], index) => (
                        <motion.div
                            key={emotionName}
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            transition={{ delay: index * 0.05 }}
                            className="flex items-center space-x-3"
                        >
                            <span className="w-20 text-sm text-gray-400">{emotionName}</span>

                            <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
                                <div
                                    className="h-full rounded-full transition-all duration-300"
                                    style={{
                                        width: `${prob * 100}%`,
                                        backgroundColor: EMOTION_COLORS[emotionName],
                                    }}
                                />
                            </div>

                            <span className="w-12 text-sm text-gray-400 text-right">
                                {(prob * 100).toFixed(1)}%
                            </span>
                        </motion.div>
                    ))}
            </div>

            {/* Multiple Faces Indicator */}
            {prediction.num_faces > 1 && (
                <div className="mt-4 p-3 bg-blue-500/20 border border-blue-500/50 rounded-lg">
                    <p className="text-sm text-blue-400">
                        {prediction.num_faces} faces detected. Showing primary face.
                    </p>
                </div>
            )}
        </div>
    );
};

export default EmotionDisplay;
