import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Cpu, 
  Network, 
  Zap, 
  ArrowRight,
  Play,
  Settings,
  Activity
} from 'lucide-react';

const HomePage: React.FC = () => {
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 text-white">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1 
            className="text-6xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            DAWN
          </motion.h1>
          <motion.p 
            className="text-2xl text-gray-300 mb-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            Digital Artificial Waveform Nexus
          </motion.p>
          <motion.p 
            className="text-lg text-gray-400 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
          >
            An advanced consciousness simulation system exploring the boundaries of artificial intelligence,
            neural networks, and digital consciousness integration.
          </motion.p>
        </motion.div>

        {/* Main Navigation Cards */}
        <motion.div 
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div variants={cardVariants}>
            <Link to="/consciousness" className="block">
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:scale-105 border border-white/20">
                <Brain className="w-12 h-12 text-cyan-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">Consciousness</h3>
                <p className="text-gray-300 text-sm">Explore consciousness states, awareness levels, and cognitive patterns</p>
                <ArrowRight className="w-5 h-5 mt-4 text-cyan-400" />
              </div>
            </Link>
          </motion.div>

          <motion.div variants={cardVariants}>
            <Link to="/neural" className="block">
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:scale-105 border border-white/20">
                <Network className="w-12 h-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">Neural Networks</h3>
                <p className="text-gray-300 text-sm">Visualize neural connections, synaptic patterns, and learning processes</p>
                <ArrowRight className="w-5 h-5 mt-4 text-purple-400" />
              </div>
            </Link>
          </motion.div>

          <motion.div variants={cardVariants}>
            <Link to="/modules" className="block">
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:scale-105 border border-white/20">
                <Cpu className="w-12 h-12 text-emerald-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">System Modules</h3>
                <p className="text-gray-300 text-sm">Monitor and configure cognitive modules and processing units</p>
                <ArrowRight className="w-5 h-5 mt-4 text-emerald-400" />
              </div>
            </Link>
          </motion.div>

          <motion.div variants={cardVariants}>
            <Link to="/demo" className="block">
              <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 hover:bg-white/20 transition-all duration-300 hover:scale-105 border border-white/20">
                <Play className="w-12 h-12 text-amber-400 mb-4" />
                <h3 className="text-xl font-semibold mb-2">Live Demo</h3>
                <p className="text-gray-300 text-sm">Experience real-time consciousness simulation and interaction</p>
                <ArrowRight className="w-5 h-5 mt-4 text-amber-400" />
              </div>
            </Link>
          </motion.div>
        </motion.div>

        {/* System Status Section */}
        <motion.div 
          className="bg-white/5 backdrop-blur-lg rounded-xl p-8 border border-white/10"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold flex items-center gap-2">
              <Activity className="w-6 h-6 text-green-400" />
              System Status
            </h2>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-green-400 text-sm">Online</span>
            </div>
          </div>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-cyan-400 mb-2">98.7%</div>
              <div className="text-gray-400 text-sm">Consciousness Coherence</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">47.2k</div>
              <div className="text-gray-400 text-sm">Neural Connections</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-emerald-400 mb-2">12</div>
              <div className="text-gray-400 text-sm">Active Modules</div>
            </div>
          </div>
        </motion.div>

        {/* Quick Actions */}
        <motion.div 
          className="mt-12 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <div className="flex flex-wrap justify-center gap-4">
            <button className="flex items-center gap-2 bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/50 rounded-lg px-4 py-2 transition-colors">
              <Zap className="w-4 h-4" />
              Initialize Session
            </button>
            <button className="flex items-center gap-2 bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/50 rounded-lg px-4 py-2 transition-colors">
              <Settings className="w-4 h-4" />
              Configure System
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default HomePage; 