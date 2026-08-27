import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Image as ImageIcon, X } from 'lucide-react';
import { motion } from 'framer-motion';
import { predictImage } from '../utils/api';
import useEmotionStore from '../store/emotionStore';
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE } from '../utils/constants';

const ImageUpload = () => {
    const [preview, setPreview] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const { addDetection } = useEmotionStore();

    const onDrop = useCallback(async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];

        // Validate file size
        if (file.size > MAX_FILE_SIZE) {
            setError('File size exceeds 10MB limit');
            return;
        }

        // Create preview
        const reader = new FileReader();
        reader.onload = () => {
            setPreview(reader.result);
        };
        reader.readAsDataURL(file);

        // Upload and predict
        setLoading(true);
        setError(null);

        try {
            const result = await predictImage(file);
            addDetection(result);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to predict emotion');
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [addDetection]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.jpeg', '.jpg', '.png', '.bmp']
        },
        maxFiles: 1,
        multiple: false,
    });

    const clearImage = () => {
        setPreview(null);
        setError(null);
    };

    return (
        <div className="glass-card p-6">
            <h2 className="text-2xl font-semibold mb-4">Upload Image</h2>

            {error && (
                <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 mb-4">
                    <p className="text-red-400 text-sm">{error}</p>
                </div>
            )}

            {!preview ? (
                <div
                    {...getRootProps()}
                    className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all ${isDragActive
                            ? 'border-purple-500 bg-purple-500/10'
                            : 'border-gray-600 hover:border-purple-500/50 hover:bg-white/5'
                        }`}
                >
                    <input {...getInputProps()} />

                    <Upload className="w-16 h-16 text-gray-500 mx-auto mb-4" />

                    {isDragActive ? (
                        <p className="text-purple-400 text-lg">Drop the image here...</p>
                    ) : (
                        <>
                            <p className="text-gray-300 text-lg mb-2">
                                Drag & drop an image here
                            </p>
                            <p className="text-gray-500 text-sm mb-4">
                                or click to select a file
                            </p>
                            <p className="text-gray-600 text-xs">
                                Supported formats: JPEG, PNG, BMP (Max 10MB)
                            </p>
                        </>
                    )}
                </div>
            ) : (
                <div className="space-y-4">
                    <div className="relative aspect-video bg-gray-900 rounded-lg overflow-hidden">
                        <img
                            src={preview}
                            alt="Preview"
                            className="w-full h-full object-contain"
                        />

                        <button
                            onClick={clearImage}
                            className="absolute top-2 right-2 p-2 bg-red-600 rounded-full hover:bg-red-700 transition-colors"
                        >
                            <X className="w-4 h-4" />
                        </button>
                    </div>

                    {loading && (
                        <div className="flex items-center justify-center py-4">
                            <div className="spinner"></div>
                            <span className="ml-3 text-gray-400">Analyzing image...</span>
                        </div>
                    )}

                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={clearImage}
                        className="w-full px-4 py-3 glass-card rounded-lg font-semibold hover:bg-white/10 transition-colors flex items-center justify-center space-x-2"
                    >
                        <ImageIcon className="w-5 h-5" />
                        <span>Upload Another Image</span>
                    </motion.button>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
