import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRealTimeConsciousness } from '../../../dawn-desktop/src/hooks/useRealTimeConsciousness';
import { moduleCommunicationHub } from '../../services/ModuleCommunicationHub';

export const LiveDataDebugOverlay: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const consciousness = useRealTimeConsciousness();
  const [modules] = useState(() => moduleCommunicationHub.getModules());
  const [recentMessages] = useState(() => moduleCommunicationHub.getRecentMessages(10));

  return (
    <>
      {/* Toggle Button */}
      <motion.button
        className="fixed bottom-4 right-4 z-30 bg-purple-600/80 backdrop-blur-sm rounded-full p-3 text-white hover:bg-purple-500/80 transition-colors"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </motion.button>

      {/* Debug Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-20 right-4 z-30 bg-black/90 backdrop-blur-sm rounded-lg p-4 w-80 max-h-96 overflow-y-auto"
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ duration: 0.2 }}
          >
            <div className="text-white">
              <h3 className="text-lg font-bold mb-4 text-purple-300">Live Debug Data</h3>
              
              {/* Consciousness Data */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold mb-2 text-blue-300">Consciousness State</h4>
                <div className="space-y-1 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-white/60">SCUP:</span>
                    <span className={`${consciousness.scup > 70 ? 'text-green-400' : consciousness.scup > 40 ? 'text-yellow-400' : 'text-red-400'}`}>
                      {consciousness.scup.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">Entropy:</span>
                    <span className="text-cyan-400">{consciousness.entropy.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">Neural Activity:</span>
                    <span className="text-purple-400">{(consciousness.neuralActivity * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">Mood:</span>
                    <span className={`${
                      consciousness.mood === 'critical' ? 'text-red-400' :
                      consciousness.mood === 'excited' ? 'text-yellow-400' :
                      consciousness.mood === 'active' ? 'text-blue-400' :
                      'text-green-400'
                    }`}>
                      {consciousness.mood.toUpperCase()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">Connected:</span>
                    <span className={consciousness.isConnected ? 'text-green-400' : 'text-red-400'}>
                      {consciousness.isConnected ? 'YES' : 'NO'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Active Modules */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold mb-2 text-green-300">Active Modules</h4>
                <div className="space-y-1 text-xs">
                  {modules.length > 0 ? modules.map(module => (
                    <div key={module.id} className="flex justify-between">
                      <span className="text-white/60 truncate">{module.id}</span>
                      <span className="text-green-400">{module.type}</span>
                    </div>
                  )) : (
                    <div className="text-white/40">No modules registered</div>
                  )}
                </div>
              </div>

              {/* Recent Messages */}
              <div className="mb-4">
                <h4 className="text-sm font-semibold mb-2 text-orange-300">Message Flow</h4>
                <div className="space-y-1 text-xs max-h-32 overflow-y-auto">
                  {recentMessages.length > 0 ? recentMessages.slice(-5).reverse().map(msg => (
                    <div key={msg.id} className="border-l-2 border-orange-400/30 pl-2">
                      <div className="flex justify-between">
                        <span className={`${
                          msg.type === 'consciousness_update' ? 'text-blue-400' :
                          msg.type === 'neural_spike' ? 'text-purple-400' :
                          msg.type === 'memory_access' ? 'text-orange-400' :
                          'text-gray-400'
                        }`}>
                          {msg.type}
                        </span>
                        <span className="text-white/40">
                          {new Date(msg.timestamp).toLocaleTimeString().slice(-8)}
                        </span>
                      </div>
                      <div className="text-white/60 truncate">
                        {msg.sourceModuleId} → {msg.targetModuleId || 'broadcast'}
                      </div>
                    </div>
                  )) : (
                    <div className="text-white/40">No recent messages</div>
                  )}
                </div>
              </div>

              {/* Performance */}
              <div>
                <h4 className="text-sm font-semibold mb-2 text-yellow-300">Performance</h4>
                <div className="space-y-1 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-white/60">Last Update:</span>
                    <span className="text-yellow-400">
                      {consciousness.lastUpdate ? `${Date.now() - consciousness.lastUpdate}ms ago` : 'Never'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/60">Status:</span>
                    <span className={`${
                      consciousness.connectionStatus === 'connected' ? 'text-green-400' :
                      consciousness.connectionStatus === 'connecting' ? 'text-yellow-400' :
                      'text-red-400'
                    }`}>
                      {consciousness.connectionStatus.toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}; 