import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Wifi, WifiOff, Activity, Zap, Brain, Gauge, Play, Pause, RotateCcw } from 'lucide-react';
import { useRealTimeConsciousness, useConsciousnessTestData } from '../../hooks/useRealTimeConsciousness';
import { consciousnessDataService } from '../../services/ConsciousnessDataService';

export const RealTimeDataPanel: React.FC = () => {
  const consciousness = useRealTimeConsciousness();
  const { injectTestData, generateRandomData } = useConsciousnessTestData();
  const [isTestMode, setIsTestMode] = useState(false);
  const [testInterval, setTestInterval] = useState<NodeJS.Timeout | null>(null);

  // Connection status indicator
  const getConnectionColor = () => {
    switch (consciousness.connectionStatus) {
      case 'connected': return 'text-green-400';
      case 'connecting': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getConnectionIcon = () => {
    if (consciousness.isConnected) {
      return <Wifi className="w-4 h-4" />;
    }
    return <WifiOff className="w-4 h-4" />;
  };

  // Test data generation
  const startTestMode = () => {
    if (testInterval) return;
    
    setIsTestMode(true);
    const interval = setInterval(() => {
      generateRandomData();
    }, 1000);
    setTestInterval(interval);
  };

  const stopTestMode = () => {
    if (testInterval) {
      clearInterval(testInterval);
      setTestInterval(null);
    }
    setIsTestMode(false);
  };

  useEffect(() => {
    return () => {
      if (testInterval) {
        clearInterval(testInterval);
      }
    };
  }, [testInterval]);

  // Manual test data injection
  const injectSpecificData = (preset: string) => {
    const presets = {
      calm: { entropy: 0.2, neuralActivity: 0.3, systemUnity: 0.8, systemLoad: 0.1, mood: 'serene' },
      active: { entropy: 0.6, neuralActivity: 0.8, systemUnity: 0.7, systemLoad: 0.4, mood: 'excited' },
      critical: { entropy: 0.9, neuralActivity: 0.9, systemUnity: 0.3, systemLoad: 0.9, mood: 'critical' },
      chaotic: { entropy: 0.95, neuralActivity: 0.6, systemUnity: 0.2, systemLoad: 0.7, mood: 'chaotic' },
      euphoric: { entropy: 0.3, neuralActivity: 0.9, systemUnity: 0.9, systemLoad: 0.2, mood: 'euphoric' }
    };
    
    const data = presets[preset as keyof typeof presets];
    if (data) {
      injectTestData(data);
    }
  };

  return (
    <motion.div
      className="fixed bottom-4 left-4 z-50 glass-base p-4 rounded-lg max-w-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5, duration: 0.8 }}
    >
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-white font-semibold flex items-center gap-2">
            <Brain className="w-4 h-4" />
            Real-time Data
          </h3>
          <div className={`flex items-center gap-2 ${getConnectionColor()}`}>
            {getConnectionIcon()}
            <span className="text-xs capitalize">{consciousness.connectionStatus}</span>
          </div>
        </div>

        {/* Connection Status */}
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="flex justify-between">
            <span className="text-white/70">Connected:</span>
            <span className={consciousness.isConnected ? 'text-green-400' : 'text-red-400'}>
              {consciousness.isConnected ? 'Yes' : 'No'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-white/70">Last Update:</span>
            <span className="text-white">
              {consciousness.lastUpdate ? `${Math.round((Date.now() - consciousness.lastUpdate) / 1000)}s` : 'Never'}
            </span>
          </div>
        </div>

        {/* Current Metrics */}
        <div className="space-y-2">
          <h4 className="text-white text-sm font-medium">Current Metrics</h4>
          
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-2">
              <Activity className="w-3 h-3 text-cyan-400" />
              <span className="text-white/70">SCUP:</span>
              <span className="text-white font-mono">{consciousness.scup.toFixed(1)}%</span>
            </div>
            
            <div className="flex items-center gap-2">
              <Zap className="w-3 h-3 text-yellow-400" />
              <span className="text-white/70">Neural:</span>
              <span className="text-white font-mono">{(consciousness.neuralActivity * 100).toFixed(0)}%</span>
            </div>
            
            <div className="flex items-center gap-2">
              <Gauge className="w-3 h-3 text-purple-400" />
              <span className="text-white/70">Entropy:</span>
              <span className="text-white font-mono">{(consciousness.entropy * 100).toFixed(0)}%</span>
            </div>
            
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-blue-400" />
              <span className="text-white/70">Consciousness:</span>
              <span className="text-white font-mono">{(consciousness.systemUnity * 100).toFixed(0)}%</span>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-purple-400 to-pink-400" />
            <span className="text-white/70">Mood:</span>
            <span className="text-white capitalize">{consciousness.mood}</span>
          </div>
        </div>

        {/* Test Controls */}
        <div className="space-y-2 border-t border-white/10 pt-2">
          <h4 className="text-white text-sm font-medium">Test Controls</h4>
          
          <div className="flex gap-2">
            <motion.button
              className={`flex-1 flex items-center justify-center gap-1 px-2 py-1 rounded text-xs ${
                isTestMode 
                  ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                  : 'bg-green-500/20 text-green-400 border border-green-500/40'
              }`}
              onClick={isTestMode ? stopTestMode : startTestMode}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isTestMode ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
              {isTestMode ? 'Stop' : 'Start'} Test
            </motion.button>
            
            <motion.button
              className="px-2 py-1 rounded text-xs bg-blue-500/20 text-blue-400 border border-blue-500/40"
              onClick={generateRandomData}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <RotateCcw className="w-3 h-3" />
            </motion.button>
          </div>

          {/* Preset buttons */}
          <div className="grid grid-cols-3 gap-1">
            {['calm', 'active', 'critical'].map(preset => (
              <motion.button
                key={preset}
                className="px-2 py-1 rounded text-xs bg-purple-500/20 text-purple-400 border border-purple-500/40"
                onClick={() => injectSpecificData(preset)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {preset}
              </motion.button>
            ))}
            {['chaotic', 'euphoric'].map(preset => (
              <motion.button
                key={preset}
                className="px-2 py-1 rounded text-xs bg-orange-500/20 text-orange-400 border border-orange-500/40"
                onClick={() => injectSpecificData(preset)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {preset}
              </motion.button>
            ))}
          </div>
        </div>

        {/* WebSocket Controls */}
        <div className="space-y-2 border-t border-white/10 pt-2">
          <div className="flex gap-2">
            <motion.button
              className="flex-1 px-2 py-1 rounded text-xs bg-cyan-500/20 text-cyan-400 border border-cyan-500/40"
              onClick={() => consciousnessDataService.start()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Connect WS
            </motion.button>
            
            <motion.button
              className="flex-1 px-2 py-1 rounded text-xs bg-gray-500/20 text-gray-400 border border-gray-500/40"
              onClick={() => consciousnessDataService.stop()}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Disconnect
            </motion.button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}; 