import React, { useState } from 'react';
import { motion } from 'framer-motion';
import SimpleConsciousnessCanvas from '../components/SimpleConsciousnessCanvas';
import { RealTimeDataPanel } from '../components/debug/RealTimeDataPanel';
import { useConsciousnessStore } from '../stores/consciousnessStore';
import GlassPanel from '../components/ui/GlassPanel';
import MetricCard from '../components/ui/MetricCard';

const ConsciousnessPage: React.FC = () => {
  const { 
    tickData, 
    isConnected, 
    averageScup, 
    currentTrend, 
    totalTicks, 
    tickRate,
    getScupTrend,
    getEntropyTrend,
    clearHistory
  } = useConsciousnessStore();
  
  const [viewMode, setViewMode] = useState<'overview' | 'detailed' | 'analysis'>('overview');
  const [autoRotate, setAutoRotate] = useState(true);
  
  const scupTrend = getScupTrend();
  const entropyTrend = getEntropyTrend();
  
  const connectionTime = new Date().toLocaleTimeString();
  
  return (
    <div className="consciousness-page min-h-screen p-6 space-y-6">
      <RealTimeDataPanel />
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-white mb-2">
          Consciousness <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">Matrix</span>
        </h1>
        <p className="text-gray-400 text-lg">
          Real-time neural activity visualization and analysis
        </p>
      </motion.div>
      
      {/* Main Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        
        {/* 3D Brain Visualization - Main Focus */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="xl:col-span-2"
        >
          <GlassPanel glow="mixed" className="h-[600px]">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-white">Neural Activity Monitor</h2>
              <div className="flex gap-2">
                <button
                  onClick={() => setAutoRotate(!autoRotate)}
                  className={`px-3 py-1 rounded text-sm transition-all ${
                    autoRotate 
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' 
                      : 'bg-gray-700/20 text-gray-400 border border-gray-600/30'
                  }`}
                >
                  Auto Rotate
                </button>
                <button
                  onClick={clearHistory}
                  className="px-3 py-1 rounded text-sm bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 transition-all"
                >
                  Clear History
                </button>
              </div>
            </div>
            
            <SimpleConsciousnessCanvas />
          </GlassPanel>
        </motion.div>
        
        {/* Metrics Panel */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="space-y-4"
        >
          {/* Connection Status */}
          <GlassPanel glow="cyan" className="p-4">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-lg font-semibold text-white">Connection Status</h3>
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Status:</span>
                <span className={isConnected ? 'text-green-400' : 'text-red-400'}>
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Tick Rate:</span>
                <span className="text-white">{tickRate.toFixed(2)} Hz</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Total Ticks:</span>
                <span className="text-white">{totalTicks.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Session:</span>
                <span className="text-white">{connectionTime}</span>
              </div>
            </div>
          </GlassPanel>
          
          {/* Live Metrics */}
          {tickData && (
            <>
              <MetricCard
                title="SCUP Level"
                value={`${(tickData.scup * 100).toFixed(1)}%`}
                colorScheme="blue"
                icon="🧠"
                subtitle={`Avg: ${(averageScup * 100).toFixed(1)}%`}
                isConnected={isConnected}
                lastUpdate={tickData.timestamp}
                glow="cyan"
              />
              
              <MetricCard
                title="Entropy"
                value={tickData.entropy.toFixed(3)}
                colorScheme="purple"
                icon="🌀"
                subtitle="System Chaos"
                isConnected={isConnected}
                lastUpdate={tickData.timestamp}
                glow="purple"
              />
              
              <MetricCard
                title="Heat Level"
                value={tickData.heat.toFixed(3)}
                colorScheme="orange"
                icon="🔥"
                subtitle="Neural Activity"
                isConnected={isConnected}
                lastUpdate={tickData.timestamp}
              />
              
              <MetricCard
                title="Current Mood"
                value={tickData.mood.toUpperCase()}
                colorScheme="green"
                icon="😊"
                subtitle={`Trend: ${currentTrend}`}
                isConnected={isConnected}
                lastUpdate={tickData.timestamp}
              />
            </>
          )}
          
          {/* View Mode Controls */}
          <GlassPanel glow="mixed" className="p-4">
            <h3 className="text-lg font-semibold text-white mb-3">View Controls</h3>
            <div className="grid grid-cols-1 gap-2">
              {(['overview', 'detailed', 'analysis'] as const).map((mode) => (
                <button
                  key={mode}
                  onClick={() => setViewMode(mode)}
                  className={`p-2 rounded text-sm transition-all capitalize ${
                    viewMode === mode
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                      : 'bg-gray-700/20 text-gray-400 border border-gray-600/30 hover:bg-gray-600/20'
                  }`}
                >
                  {mode} Mode
                </button>
              ))}
            </div>
          </GlassPanel>
        </motion.div>
      </div>
      
      {/* Bottom Analysis Panel */}
      {viewMode === 'analysis' && tickData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <GlassPanel glow="purple" className="p-6">
            <h3 className="text-xl font-semibold text-white mb-4">Advanced Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* SCUP Trend */}
              <div>
                <h4 className="text-lg text-cyan-400 mb-2">SCUP Trend (Last 50)</h4>
                <div className="h-24 bg-gray-900/50 rounded-lg p-2 relative overflow-hidden">
                  <svg className="w-full h-full">
                    <polyline
                      fill="none"
                      stroke="url(#scupGradient)"
                      strokeWidth="2"
                      points={scupTrend.map((val, i) => 
                        `${(i / (scupTrend.length - 1)) * 100},${100 - (val * 100)}`
                      ).join(' ')}
                    />
                    <defs>
                      <linearGradient id="scupGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#00ff88" />
                        <stop offset="100%" stopColor="#00ccff" />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
              </div>
              
              {/* Entropy Trend */}
              <div>
                <h4 className="text-lg text-purple-400 mb-2">Entropy Trend (Last 50)</h4>
                <div className="h-24 bg-gray-900/50 rounded-lg p-2 relative overflow-hidden">
                  <svg className="w-full h-full">
                    <polyline
                      fill="none"
                      stroke="url(#entropyGradient)"
                      strokeWidth="2"
                      points={entropyTrend.map((val, i) => 
                        `${(i / (entropyTrend.length - 1)) * 100},${100 - (val * 100)}`
                      ).join(' ')}
                    />
                    <defs>
                      <linearGradient id="entropyGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#a855f7" />
                        <stop offset="100%" stopColor="#ec4899" />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>
              </div>
              
              {/* Current Stats */}
              <div>
                <h4 className="text-lg text-orange-400 mb-2">Current Stats</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Tick #:</span>
                    <span className="text-white font-mono">#{tickData.tick_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Timestamp:</span>
                    <span className="text-white font-mono">{new Date(tickData.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Mood Duration:</span>
                    <span className="text-white">Active</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">System Health:</span>
                    <span className="text-green-400">Optimal</span>
                  </div>
                </div>
              </div>
            </div>
          </GlassPanel>
        </motion.div>
      )}
    </div>
  );
};

export default ConsciousnessPage; 