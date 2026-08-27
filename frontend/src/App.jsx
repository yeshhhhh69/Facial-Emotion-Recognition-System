import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import Home from './pages/Home'
import LiveDetection from './pages/LiveDetection'
import Analytics from './pages/Analytics'
import About from './pages/About'

function App() {
    return (
        <Router>
            <div className="min-h-screen">
                <Header />
                <AnimatePresence mode="wait">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/live" element={<LiveDetection />} />
                        <Route path="/analytics" element={<Analytics />} />
                        <Route path="/about" element={<About />} />
                    </Routes>
                </AnimatePresence>
            </div>
        </Router>
    )
}

export default App
