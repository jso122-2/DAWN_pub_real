import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import UnifiedVisualSubprocessManager from './UnifiedVisualSubprocessManager';
import { useConsciousnessStore } from '../stores/consciousnessStore';

/**
 * Example integration showing how to use the UnifiedVisualSubprocessManager
 * in your main DAWN application for port 3000
 */
export const SubprocessIntegrationExample: React.FC = () => {
  const { tickData, isConnected } = useConsciousnessStore();
  const [processLog, setProcessLog] = useState<string[]>([]);
  
  // Use real consciousness data or fallback
  const globalEntropy = tickData?.entropy ?? 0.5;
  const globalSCUP = tickData?.scup ?? 0.5;
  const currentMood = tickData?.mood ?? 'calm';
  const tickNumber = tickData ? Object.keys(tickData).length : 0;

  // Handle process toggle events
  const handleProcessToggle = (processId: string, enabled: boolean) => {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] Process ${processId} ${enabled ? 'ENABLED' : 'DISABLED'}`;
    setProcessLog(prev => [logEntry, ...prev.slice(0, 9)]); // Keep last 10 entries
    
    console.log(`🔄 Process Toggle: ${processId} -> ${enabled ? 'ON' : 'OFF'}`);
  };

  // Simulate entropy changes (you'd replace this with real entropy data)
  const simulateEntropyChange = () => {
    // This would trigger a consciousness state change in the real system
    console.log('🎲 Simulating entropy change - would trigger consciousness update');
  };

  return (
    <div className="w-full h-screen bg-gray-900 p-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h1 className="text-3xl font-bold text-white mb-2">
          🌊 DAWN Visual Subprocess Manager
        </h1>
        <p className="text-gray-400">
          Unified control interface for all visual subprocesses (Port 3000)
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-full">
        {/* Main Subprocess Manager */}
        <div className="lg:col-span-3">
          <UnifiedVisualSubprocessManager
            port={8001}
            onProcessToggle={handleProcessToggle}
            globalEntropy={globalEntropy}
          />
        </div>

        {/* Side Panel - System Info & Logs */}
        <div className="space-y-4">
          {/* System Stats */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-black/50 backdrop-blur-sm border border-blue-500/30 rounded-xl p-4"
          >
            <h3 className="text-lg font-semibold text-white mb-3">🧠 System State</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Global Entropy:</span>
                <span className="text-blue-400 font-mono">
                  {globalEntropy.toFixed(3)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">SCUP Level:</span>
                <span className="text-purple-400 font-mono">
                  {globalSCUP.toFixed(3)}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Mood:</span>
                <span className="text-yellow-400 font-mono">{currentMood}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Port:</span>
                <span className="text-green-400 font-mono">8001</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Connection:</span>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full animate-pulse ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
                  <span className={`text-sm ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
                    {isConnected ? 'LIVE' : 'OFFLINE'}
                  </span>
                </div>
              </div>
            </div>
            
            <button
              onClick={simulateEntropyChange}
              className="w-full mt-4 px-3 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 rounded-lg transition-colors text-sm"
            >
              🎲 Simulate Entropy Change
            </button>
          </motion.div>

          {/* Process Activity Log */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-black/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-4 flex-1"
          >
            <h3 className="text-lg font-semibold text-white mb-3">📝 Activity Log</h3>
            <div className="space-y-1 max-h-64 overflow-y-auto">
              {processLog.length === 0 ? (
                <p className="text-gray-500 text-sm italic">
                  No activity yet. Toggle some processes to see logs.
                </p>
              ) : (
                processLog.map((entry, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="text-xs font-mono text-gray-300 bg-gray-800/30 rounded px-2 py-1"
                  >
                    {entry}
                  </motion.div>
                ))
              )}
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-black/50 backdrop-blur-sm border border-green-500/30 rounded-xl p-4"
          >
            <h3 className="text-lg font-semibold text-white mb-3">⚡ Quick Actions</h3>
            <div className="space-y-2">
              <button className="w-full px-3 py-2 bg-green-600/20 hover:bg-green-600/30 text-green-400 rounded-lg transition-colors text-sm">
                🚀 Enable All Neural
              </button>
              <button className="w-full px-3 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-400 rounded-lg transition-colors text-sm">
                🧠 Toggle Consciousness
              </button>
              <button className="w-full px-3 py-2 bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 rounded-lg transition-colors text-sm">
                🔄 Restart System
              </button>
              <button className="w-full px-3 py-2 bg-red-600/20 hover:bg-red-600/30 text-red-400 rounded-lg transition-colors text-sm">
                🛑 Emergency Stop
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default SubprocessIntegrationExample; 