import { motion } from 'framer-motion';
import { BarChart, Bar, PieChart, Pie, Cell, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { Download, Trash2 } from 'lucide-react';
import useEmotionStore from '../store/emotionStore';
import { EMOTION_COLORS } from '../utils/constants';

const Analytics = () => {
    const { detections, stats, clearHistory, exportData } = useEmotionStore();

    // Prepare data for charts
    const emotionData = Object.entries(stats.emotionCounts).map(([emotion, count]) => ({
        emotion,
        count,
        color: EMOTION_COLORS[emotion],
    }));

    return (
        <div className="container mx-auto px-4 py-8">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold">
                        <span className="gradient-text">Analytics Dashboard</span>
                    </h1>

                    <div className="flex gap-3">
                        <button
                            onClick={exportData}
                            className="px-4 py-2 glass-card rounded-lg flex items-center space-x-2 hover:bg-white/10 transition-colors"
                        >
                            <Download className="w-4 h-4" />
                            <span>Export</span>
                        </button>

                        <button
                            onClick={clearHistory}
                            className="px-4 py-2 glass-card rounded-lg flex items-center space-x-2 hover:bg-red-500/20 transition-colors text-red-400"
                        >
                            <Trash2 className="w-4 h-4" />
                            <span>Clear</span>
                        </button>
                    </div>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="glass-card p-6">
                        <p className="text-gray-400 text-sm mb-2">Total Detections</p>
                        <p className="text-3xl font-bold">{stats.totalDetections}</p>
                    </div>

                    <div className="glass-card p-6">
                        <p className="text-gray-400 text-sm mb-2">Dominant Emotion</p>
                        <p className="text-3xl font-bold" style={{ color: EMOTION_COLORS[stats.dominantEmotion] }}>
                            {stats.dominantEmotion || 'N/A'}
                        </p>
                    </div>

                    <div className="glass-card p-6">
                        <p className="text-gray-400 text-sm mb-2">Avg Confidence</p>
                        <p className="text-3xl font-bold">
                            {(stats.averageConfidence * 100).toFixed(1)}%
                        </p>
                    </div>

                    <div className="glass-card p-6">
                        <p className="text-gray-400 text-sm mb-2">Unique Emotions</p>
                        <p className="text-3xl font-bold">
                            {Object.values(stats.emotionCounts).filter(c => c > 0).length}
                        </p>
                    </div>
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Bar Chart */}
                    <div className="glass-card p-6">
                        <h2 className="text-xl font-semibold mb-4">Emotion Distribution</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={emotionData}>
                                <XAxis dataKey="emotion" stroke="#9ca3af" />
                                <YAxis stroke="#9ca3af" />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'rgba(30, 41, 59, 0.9)',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '8px',
                                    }}
                                />
                                <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                                    {emotionData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    {/* Pie Chart */}
                    <div className="glass-card p-6">
                        <h2 className="text-xl font-semibold mb-4">Emotion Breakdown</h2>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={emotionData.filter(d => d.count > 0)}
                                    dataKey="count"
                                    nameKey="emotion"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={100}
                                    label
                                >
                                    {emotionData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: 'rgba(30, 41, 59, 0.9)',
                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                        borderRadius: '8px',
                                    }}
                                />
                                <Legend />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Detection History */}
                <div className="glass-card p-6">
                    <h2 className="text-xl font-semibold mb-4">Recent Detections</h2>

                    {detections.length === 0 ? (
                        <p className="text-gray-400 text-center py-8">No detections yet</p>
                    ) : (
                        <div className="space-y-3 max-h-96 overflow-y-auto">
                            {detections.slice(0, 20).map((detection, index) => (
                                <div key={index} className="glass p-4 rounded-lg">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <p className="text-sm text-gray-400">
                                                {new Date(detection.timestamp).toLocaleString()}
                                            </p>
                                            <div className="flex flex-wrap gap-2 mt-2">
                                                {detection.predictions.map((pred, idx) => (
                                                    <span
                                                        key={idx}
                                                        className="px-3 py-1 rounded-full text-sm"
                                                        style={{
                                                            backgroundColor: `${EMOTION_COLORS[pred.emotion]}20`,
                                                            color: EMOTION_COLORS[pred.emotion],
                                                        }}
                                                    >
                                                        {pred.emotion}: {(pred.confidence * 100).toFixed(1)}%
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                        <span className="text-sm text-gray-400">
                                            {detection.num_faces} face(s)
                                        </span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default Analytics;
