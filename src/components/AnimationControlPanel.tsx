import React from 'react';
import { motion } from 'framer-motion';
import { Settings, RotateCw, Sparkles, Activity } from 'lucide-react';
import { useAnimationControls } from '../contexts/AnimationContext';

export const AnimationControlPanel: React.FC = () => {
  const { 
    rotationsEnabled, 
    setRotationsEnabled,
    animationsEnabled,
    setAnimationsEnabled,
    particlesEnabled,
    setParticlesEnabled
  } = useAnimationControls();
  
  const [isOpen, setIsOpen] = React.useState(false);
  
  return (
    <motion.div
      className="fixed top-4 right-4 z-50"
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
    >
      {/* Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className="mb-2 p-3 bg-black/50 backdrop-blur rounded-lg border border-white/10"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Settings className={`w-5 h-5 text-white ${isOpen ? 'animate-spin' : ''}`} />
      </motion.button>
      
      {/* Control Panel */}
      <motion.div
        initial={false}
        animate={{ 
          height: isOpen ? 'auto' : 0,
          opacity: isOpen ? 1 : 0
        }}
        className="overflow-hidden"
      >
        <div className="p-4 bg-black/50 backdrop-blur rounded-lg border border-white/10 space-y-3">
          {/* Rotations Toggle */}
          <button
            onClick={() => setRotationsEnabled(!rotationsEnabled)}
            className={`w-full px-4 py-2 rounded-lg flex items-center justify-between transition-all ${
              rotationsEnabled 
                ? 'bg-green-500/20 border border-green-400/50' 
                : 'bg-red-500/20 border border-red-400/50'
            }`}
          >
            <div className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${rotationsEnabled ? 'text-green-400' : 'text-red-400'}`} />
              <span className="text-white text-sm">Rotations</span>
            </div>
            <div className={`w-3 h-3 rounded-full ${
              rotationsEnabled ? 'bg-green-400' : 'bg-red-400'
            }`} />
          </button>
          
          {/* Animations Toggle */}
          <button
            onClick={() => setAnimationsEnabled(!animationsEnabled)}
            className={`w-full px-4 py-2 rounded-lg flex items-center justify-between transition-all ${
              animationsEnabled 
                ? 'bg-green-500/20 border border-green-400/50' 
                : 'bg-red-500/20 border border-red-400/50'
            }`}
          >
            <div className="flex items-center gap-2">
              <Activity className={`w-4 h-4 ${animationsEnabled ? 'text-green-400' : 'text-red-400'}`} />
              <span className="text-white text-sm">Animations</span>
            </div>
            <div className={`w-3 h-3 rounded-full ${
              animationsEnabled ? 'bg-green-400' : 'bg-red-400'
            }`} />
          </button>
          
          {/* Particles Toggle */}
          <button
            onClick={() => setParticlesEnabled(!particlesEnabled)}
            className={`w-full px-4 py-2 rounded-lg flex items-center justify-between transition-all ${
              particlesEnabled 
                ? 'bg-green-500/20 border border-green-400/50' 
                : 'bg-red-500/20 border border-red-400/50'
            }`}
          >
            <div className="flex items-center gap-2">
              <Sparkles className={`w-4 h-4 ${particlesEnabled ? 'text-green-400' : 'text-red-400'}`} />
              <span className="text-white text-sm">Particles</span>
            </div>
            <div className={`w-3 h-3 rounded-full ${
              particlesEnabled ? 'bg-green-400' : 'bg-red-400'
            }`} />
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}; 