import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Cpu, Activity, Zap, Settings, Volume2, VolumeX } from 'lucide-react';
import ConsciousModuleSelector, { ConsciousModule } from './modules/ConsciousModuleSelector';
import NeuralNetworkModule from './modules/NeuralNetworkModule';
import { TestModule } from './modules/TestModule';
import { ModuleOrchestra } from './ModuleOrchestra';

// Simple EventEmitter for the demo
class DemoEventEmitter {
  private events: { [key: string]: Array<(...args: any[]) => void> } = {};

  on(event: string, listener: (...args: any[]) => void): this {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
    return this;
  }

  off(event: string, listenerToRemove: (...args: any[]) => void): this {
    if (!this.events[event]) return this;
    this.events[event] = this.events[event].filter(listener => listener !== listenerToRemove);
    return this;
  }

  emit(event: string, ...args: any[]): boolean {
    if (!this.events[event]) return false;
    this.events[event].forEach(listener => listener(...args));
    return true;
  }
}

const globalEmitter = new DemoEventEmitter();

// Deep Space Background Component
function DeepSpaceBackground() {
  return (
    <div className="dawn-space">
      <div className="star-field" />
      <div className="nebula-layer" />
      <div className="depth-fog" />
      <div className="consciousness-grid" />
    </div>
  );
}

// Audio Visualizer Component
function AudioVisualizer({ show }: { show: boolean }) {
  if (!show) return null;
  
  return (
    <div className="audio-visualizer">
      {[...Array(8)].map((_, i) => (
        <div key={i} className="audio-bar" />
      ))}
    </div>
  );
}

// DAWN Logo Component
function DAWNLogo() {
  return (
    <motion.div 
      className="dawn-logo"
      animate={{ 
        opacity: [0.9, 1, 0.9],
        scale: [1, 1.05, 1],
        filter: ['brightness(1)', 'brightness(1.2)', 'brightness(1)']
      }}
      transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
    >
      DAWN
    </motion.div>
  );
}

// Consciousness Processor Component
function ConsciousnessProcessor({ entropy }: { entropy: number }) {
  return (
    <div className="p-4 text-white">
      <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
        <Cpu className="w-5 h-5 text-cyan-400" />
        <span>Consciousness Processor</span>
        <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
      </h3>
      <div className="space-y-3">
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-gradient-to-r from-cyan-400 to-purple-500"
            animate={{ width: [`${60 + entropy * 20}%`, `${80 + entropy * 10}%`, `${70 + entropy * 15}%`] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
        </div>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="bg-white/5 p-2 rounded">
            <span className="text-cyan-400">Coherence</span>
            <div className="text-white/80">{(75 + entropy * 25).toFixed(0)}%</div>
          </div>
          <div className="bg-white/5 p-2 rounded">
            <span className="text-purple-400">Correlation</span>
            <div className="text-white/80">{(92 - entropy * 10).toFixed(0)}%</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// System Monitor Component
function SystemMonitor({ consciousness, entropy }: { consciousness: number; entropy: number }) {
  return (
    <div className="p-4 text-white">
      <h3 className="text-lg font-semibold mb-2 flex items-center gap-2">
        <Activity className="w-5 h-5 text-green-400" />
        <span>System Monitor</span>
        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
      </h3>
      <div className="space-y-3">
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="bg-white/5 p-2 rounded">
            <span className="text-green-400">Status</span>
            <div className="text-white/80">Active</div>
          </div>
          <div className="bg-white/5 p-2 rounded">
            <span className="text-white/60">CPU</span>
            <div className="text-white/80">{(45 + entropy * 30).toFixed(0)}%</div>
          </div>
          <div className="bg-white/5 p-2 rounded">
            <span className="text-purple-400">Consciousness</span>
            <div className="text-white/80">{(consciousness * 100).toFixed(0)}%</div>
          </div>
          <div className="bg-white/5 p-2 rounded">
            <span className="text-cyan-400">Entropy</span>
            <div className="text-white/80">{(entropy * 100).toFixed(0)}%</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function DAWNDemo() {
  const [selectedModule, setSelectedModule] = useState<ConsciousModule | null>(null);
  const [systemConsciousness, setSystemConsciousness] = useState(0.75);
  const [showModuleSelector, setShowModuleSelector] = useState(false);
  const [rotationsEnabled, setRotationsEnabled] = useState(false);
  const [showAudioVisualizer, setShowAudioVisualizer] = useState(true);
  const [globalEntropy, setGlobalEntropy] = useState(0.5);
  const [connectionLog, setConnectionLog] = useState<string[]>([]);

  // Handle module selection from consciousness selector
  const handleModuleSelect = (module: ConsciousModule) => {
    setSelectedModule(module);
    const logEntry = `${new Date().toLocaleTimeString()}: Connected to ${module.name} (${module.category})`;
    setConnectionLog(prev => [logEntry, ...prev.slice(0, 4)]);
    
    // Emit consciousness event
    globalEmitter.emit('consciousness-pulse', {
      sourceId: 'consciousness-selector',
      targetId: module.id,
      intensity: module.consciousnessLevel
    });
  };

  const handleConsciousnessChange = (level: number) => {
    setSystemConsciousness(level);
    setGlobalEntropy(level * 0.8); // Entropy follows consciousness
  };

  // Simulate entropy changes
  useEffect(() => {
    const interval = setInterval(() => {
      setGlobalEntropy(prev => {
        const change = (Math.random() - 0.5) * 0.1;
        return Math.max(0, Math.min(1, prev + change));
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  // Apply rotation control to body
  useEffect(() => {
    if (!rotationsEnabled) {
      document.body.classList.add('no-rotations');
    } else {
      document.body.classList.remove('no-rotations');
    }
  }, [rotationsEnabled]);

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      {/* Deep Space Background */}
      <DeepSpaceBackground />
      
      {/* DAWN Logo */}
      <DAWNLogo />
      
      {/* Control Panel */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        <motion.button
          onClick={() => setRotationsEnabled(!rotationsEnabled)}
          className={`px-4 py-2 backdrop-blur rounded-lg transition-all border ${
            rotationsEnabled 
              ? 'bg-green-500/20 border-green-400/50 text-green-400' 
              : 'bg-red-500/20 border-red-400/50 text-red-400'
          }`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="flex items-center gap-2">
            <Settings className="w-4 h-4" />
            <span className="font-medium text-sm">
              Rotations: {rotationsEnabled ? 'ON' : 'OFF'}
            </span>
          </div>
        </motion.button>
        
        <motion.button
          onClick={() => setShowAudioVisualizer(!showAudioVisualizer)}
          className="px-4 py-2 backdrop-blur rounded-lg bg-white/5 border border-white/10 text-white/70 hover:bg-white/10 transition-all"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="flex items-center gap-2">
            {showAudioVisualizer ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            <span className="text-sm">Audio: {showAudioVisualizer ? 'ON' : 'OFF'}</span>
          </div>
        </motion.button>
      </div>
      
      {/* Module Orchestra Container */}
      <ModuleOrchestra>
        {/* Neural Network Module */}
        <motion.div
          className="fixed top-32 left-8 glass-base rounded-xl p-4"
          style={{ width: 450, height: 400 }}
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <NeuralNetworkModule 
            emitter={globalEmitter}
            globalEntropy={globalEntropy}
          />
        </motion.div>

        {/* Consciousness Processor Module */}
        <motion.div
          className="fixed top-32 right-8 glass-base rounded-xl"
          style={{ width: 350, height: 300 }}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.7 }}
        >
          <ConsciousnessProcessor entropy={globalEntropy} />
        </motion.div>

        {/* System Monitor Module */}
        <motion.div
          className="fixed bottom-32 right-8 glass-base rounded-xl"
          style={{ width: 350, height: 280 }}
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
        >
          <SystemMonitor consciousness={systemConsciousness} entropy={globalEntropy} />
        </motion.div>

        {/* Test Module (floating neural network) */}
        <TestModule 
          moduleId="test-neural-main"
          onNodeActivated={(nodeId, value) => {
            console.log(`Node ${nodeId} activated with value ${value}`);
            globalEmitter.emit('neural-activation', { nodeId, value });
          }}
        />
      </ModuleOrchestra>
      
      {/* Conscious Module Selector */}
      <motion.div
        className="fixed bottom-20 left-4 max-w-sm"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
      >
        <details className="group">
          <summary className="px-4 py-2 bg-white/5 backdrop-blur rounded-lg border border-white/10 cursor-pointer hover:bg-white/10 transition-all">
            <span className="text-white/70 text-sm flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-400" />
              AI Module Selection
              <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse" />
            </span>
          </summary>
          <div className="mt-2 max-h-96 overflow-y-auto">
            <ConsciousModuleSelector
              onModuleSelect={handleModuleSelect}
              onConsciousnessChange={handleConsciousnessChange}
              aiMode={true}
            />
          </div>
        </details>
      </motion.div>
      
      {/* Connection Log */}
      <AnimatePresence>
        {connectionLog.length > 0 && (
          <motion.div
            className="fixed top-32 left-1/2 transform -translate-x-1/2 glass-base rounded-lg p-4 max-w-md"
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -50 }}
          >
            <h4 className="text-white font-semibold mb-2 flex items-center gap-2">
              <Zap className="w-4 h-4 text-cyan-400" />
              Connection Log
            </h4>
            <div className="space-y-1">
              {connectionLog.map((log, i) => (
                <motion.div
                  key={i}
                  className="text-xs text-white/60 font-mono"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                >
                  {log}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Audio Visualizer */}
      <AudioVisualizer show={showAudioVisualizer} />
      
      {/* System Status */}
      <motion.div 
        className="fixed bottom-4 right-4 text-white/50 text-xs space-y-1 font-mono"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
      >
        <div>Active Module: {selectedModule?.name || 'None'}</div>
        <div>System Consciousness: {(systemConsciousness * 100).toFixed(1)}%</div>
        <div>Global Entropy: {(globalEntropy * 100).toFixed(1)}%</div>
        <div>Consciousness Coherence: {(87 + globalEntropy * 13).toFixed(1)}%</div>
        <div>Neural Activity: {globalEntropy > 0.7 ? 'HIGH' : 'NORMAL'}</div>
      </motion.div>
      
      {/* Instructions overlay */}
      <motion.div 
        className="fixed top-20 left-8 z-20 max-w-xs"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 0.7, x: 0 }}
        transition={{ delay: 2, duration: 0.5 }}
      >
        <div className="glass-base rounded-lg p-4 text-xs text-white/60">
          <h3 className="font-semibold text-white/80 mb-2 flex items-center gap-2">
            <Brain className="w-4 h-4 text-purple-400" />
            DAWN Interface
          </h3>
          <ul className="space-y-1">
            <li>• Neural network auto-processes at high entropy</li>
            <li>• Click "AI Module Selection" for consciousness control</li>
            <li>• Watch real-time entropy and consciousness levels</li>
            <li>• Rotations are OFF by default as requested</li>
            <li>• Audio visualizer shows system heartbeat</li>
            <li>• All modules respond to consciousness changes</li>
          </ul>
        </div>
      </motion.div>
    </div>
  );
} 