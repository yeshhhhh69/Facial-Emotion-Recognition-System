import { Link, useLocation } from 'react-router-dom';
import { Brain, Home, Video, BarChart3, Info } from 'lucide-react';
import { motion } from 'framer-motion';

const Header = () => {
    const location = useLocation();

    const navItems = [
        { path: '/', label: 'Home', icon: Home },
        { path: '/live', label: 'Live Detection', icon: Video },
        { path: '/analytics', label: 'Analytics', icon: BarChart3 },
        { path: '/about', label: 'About', icon: Info },
    ];

    return (
        <header className="glass-card sticky top-0 z-50 mx-4 mt-4">
            <nav className="container mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2 group">
                        <Brain className="w-8 h-8 text-purple-500 group-hover:text-purple-400 transition-colors" />
                        <span className="text-xl font-bold gradient-text">
                            Emotion Recognition
                        </span>
                    </Link>

                    {/* Navigation */}
                    <div className="hidden md:flex items-center space-x-1">
                        {navItems.map((item) => {
                            const Icon = item.icon;
                            const isActive = location.pathname === item.path;

                            return (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className="relative px-4 py-2 rounded-lg transition-colors"
                                >
                                    <div className={`flex items-center space-x-2 ${isActive ? 'text-purple-400' : 'text-gray-300 hover:text-white'
                                        }`}>
                                        <Icon className="w-4 h-4" />
                                        <span>{item.label}</span>
                                    </div>

                                    {isActive && (
                                        <motion.div
                                            layoutId="activeTab"
                                            className="absolute inset-0 bg-purple-500/20 rounded-lg -z-10"
                                            transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                                        />
                                    )}
                                </Link>
                            );
                        })}
                    </div>

                    {/* Mobile menu button */}
                    <button className="md:hidden p-2 rounded-lg hover:bg-white/10 transition-colors">
                        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </nav>
        </header>
    );
};

export default Header;
