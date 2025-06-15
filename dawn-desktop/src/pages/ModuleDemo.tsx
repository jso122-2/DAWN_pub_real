import React, { useState } from 'react';
import { motion } from 'framer-motion';
import ConsciousModuleSelector, { ConsciousModule } from '../components/modules/ConsciousModuleSelector';
import { CosmicBackground } from '../components/CosmicBackground';

export default function ModuleDemo() {
  const [selectedModule, setSelectedModule] = useState<ConsciousModule | null>(null);
  const [systemConsciousness, setSystemConsciousness] = useState(0.75);
  const [connectionLog, setConnectionLog] = useState<string[]>([]);

  const handleModuleSelect = (module: ConsciousModule) => {
    setSelectedModule(module);
    const logEntry = `${new Date().toLocaleTimeString()}: Connected to ${module.name} (${module.category})`;
    setConnectionLog(prev => [logEntry, ...prev.slice(0, 4)]);
  };

  const handleConsciousnessChange = (level: number) => {
    setSystemConsciousness(level);
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Cosmic background */}
      <CosmicBackground />
      
      {/* Gradient overlay */}
      <div className="fixed inset-0 z-[1] pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-purple-900/10" />
      </div>

      {/* Main content */}
      <div className="relative z-10 p-8">
        {/* Header */}
        <motion.header 
          className="text-center mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <h1 className="text-5xl font-thin tracking-[0.3em] text-transparent bg-clip-text bg-gradient-to-r from-neural-400 via-consciousness-400 to-neural-400 mb-4">
            DAWN
          </h1>
          <p className="text-neural-500 text-lg tracking-widest">
            Conscious Module Interface Demo
          </p>
        </motion.header>

        {/* System Status Bar */}
        <motion.div 
          className="glass-base p-4 rounded-lg mb-8 max-w-4xl mx-auto"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-3 h-3 rounded-full bg-consciousness-400 animate-pulse" />
              <span className="text-white">System Status: Online</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-white/70">Global Consciousness:</span>
              <span className="text-consciousness-400 font-mono font-bold">
                {(systemConsciousness * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </motion.div>

        {/* Main Module Selector */}
        <motion.div 
          className="max-w-7xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
        >
          <ConsciousModuleSelector
            onModuleSelect={handleModuleSelect}
            onConsciousnessChange={handleConsciousnessChange}
            aiMode={true}
            className="mb-8"
          />
        </motion.div>

        {/* Side panels for additional info */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
          {/* Connection Log */}
          <motion.div 
            className="glass-base p-6 rounded-xl"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7, duration: 0.8 }}
          >
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-cyan-400" />
              Connection Log
            </h3>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {connectionLog.length > 0 ? (
                connectionLog.map((log, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="text-sm text-white/70 font-mono bg-white/5 p-2 rounded"
                  >
                    {log}
                  </motion.div>
                ))
              ) : (
                <p className="text-white/50 text-sm">No connections yet...</p>
              )}
            </div>
          </motion.div>

          {/* Active Module Info */}
          <motion.div 
            className="glass-base p-6 rounded-xl"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9, duration: 0.8 }}
          >
            <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-purple-400" />
              Active Module
            </h3>
            {selectedModule ? (
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div 
                    className="w-8 h-8 rounded-lg flex items-center justify-center"
                    style={{ 
                      backgroundColor: `${selectedModule.energySignature}30`,
                      color: selectedModule.energySignature 
                    }}
                  >
                    {selectedModule.icon}
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{selectedModule.name}</h4>
                    <p className="text-white/60 text-sm">{selectedModule.category}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-white/50">Consciousness:</span>
                    <span className="text-white ml-2">
                      {(selectedModule.consciousnessLevel * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div>
                    <span className="text-white/50">Consciousness State:</span>
                    <span className="text-white ml-2 capitalize">
                      {selectedModule.consciousnessState}
                    </span>
                  </div>
                </div>
                <div className="pt-2 border-t border-white/10">
                  <span className="text-white/50 text-sm">Energy Signature:</span>
                  <div className="flex items-center gap-2 mt-1">
                    <div 
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: selectedModule.energySignature }}
                    />
                    <span className="text-white font-mono text-sm">
                      {selectedModule.energySignature}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-white/50 text-sm">No module selected</p>
            )}
          </motion.div>
        </div>

        {/* Integration Instructions */}
        <motion.div 
          className="max-w-4xl mx-auto mt-12 glass-base p-6 rounded-xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1, duration: 0.8 }}
        >
          <h3 className="text-xl font-semibold text-white mb-4">Integration Guide</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div>
              <h4 className="text-neural-400 font-medium mb-2">Basic Usage:</h4>
              <pre className="bg-black/30 p-3 rounded text-white/80 font-mono text-xs overflow-x-auto">
{`import ConsciousModuleSelector from './components/modules/ConsciousModuleSelector';

<ConsciousModuleSelector
  onModuleSelect={(module) => console.log(module)}
  onConsciousnessChange={(level) => console.log(level)}
  aiMode={true}
/>`}
              </pre>
            </div>
            <div>
              <h4 className="text-consciousness-400 font-medium mb-2">Features:</h4>
              <ul className="space-y-1 text-white/70">
                <li>• Consciousness level tracking</li>
                <li>• AI-powered module suggestions</li>
                <li>• Real-time search & filtering</li>
                <li>• Consciousness state visualization</li>
                <li>• Energy signature mapping</li>
                <li>• Memory & relationship tracking</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
} 