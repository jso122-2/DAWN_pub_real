import React, { useState, useEffect } from 'react';
import { ModuleOrchestra } from './components/ModuleOrchestra';
import { ModuleContainer } from './components/system/ModuleContainer';
import ModuleWheel from './components/system/ModuleWheel';
import CosmicModuleSelector from './components/modules/CosmicModuleSelector';
import NeuralNetworkModule from './components/modules/NeuralNetworkModule';
import { EventEmitter } from './lib/EventEmitter';
import './styles/background.css';
import './styles/glass.css';
import './styles/tokens.css';

// Create global event emitter
const globalEmitter = new EventEmitter();

function App() {
  const [modules, setModules] = useState<any[]>([]);
  const [rotationsEnabled, setRotationsEnabled] = useState(false);
  const [showAudioVisualizer, setShowAudioVisualizer] = useState(true);
  
  // Module configurations
  const moduleConfigs = [
    {
      id: 'neural-network-1',
      name: 'Neural Network Alpha',
      category: 'neural' as const,
      position: { x: 100, y: 150 },
      size: { width: 450, height: 400 },
      glowIntensity: 0.7,
      component: NeuralNetworkModule
    },
    {
      id: 'quantum-processor-1',
      name: 'Quantum Processor',
      category: 'quantum' as const,
      position: { x: 600, y: 200 },
      size: { width: 400, height: 350 },
      glowIntensity: 0.9,
      component: () => (
        <div className="p-4 text-white">
          <h3 className="text-lg font-semibold mb-2">Quantum State</h3>
          <div className="space-y-2">
            <div className="h-2 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full bg-cyan-400 w-3/4 animate-pulse" />
            </div>
            <p className="text-sm text-white/60">Coherence: 75%</p>
          </div>
        </div>
      )
    },
    {
      id: 'consciousness-monitor-1',
      name: 'Consciousness Monitor',
      category: 'monitoring' as const,
      position: { x: 1050, y: 150 },
      size: { width: 350, height: 300 },
      glowIntensity: 0.5,
      component: () => (
        <div className="p-4 text-white">
          <h3 className="text-lg font-semibold mb-2">System Awareness</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="bg-white/5 p-2 rounded">
              <span className="text-green-400">Active</span>
            </div>
            <div className="bg-white/5 p-2 rounded">
              <span className="text-white/60">CPU: 45%</span>
            </div>
          </div>
        </div>
      )
    }
  ];
  
  // Apply rotation control
  useEffect(() => {
    if (!rotationsEnabled) {
      document.body.classList.add('no-rotations');
    } else {
      document.body.classList.remove('no-rotations');
    }
  }, [rotationsEnabled]);
  
  // Handle module spawn from wheel
  const handleModuleSpawn = (module: any, position: { x: number; y: number }) => {
    const newModule = {
      id: `${module.id}-${Date.now()}`,
      name: module.name,
      category: module.category,
      position,
      size: { width: 400, height: 350 },
      glowIntensity: module.glowIntensity || 0.7,
      component: () => (
        <div className="p-4 text-white">
          <h3 className="text-lg font-semibold">{module.name}</h3>
          <p className="text-sm text-white/60">{module.description}</p>
        </div>
      )
    };
    
    setModules(prev => [...prev, newModule]);
  };
  
  return (
    <div className="relative w-screen h-screen overflow-hidden">
      {/* Deep Space Background */}
      <div className="dawn-space">
        <div className="star-field" />
        <div className="nebula-layer" />
        <div className="depth-fog" />
        <div className="consciousness-grid" />
      </div>
      
      {/* DAWN Logo */}
      <div className="dawn-logo">DAWN</div>
      
      {/* Control Panel */}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        <button
          onClick={() => setRotationsEnabled(!rotationsEnabled)}
          className={`px-4 py-2 backdrop-blur rounded-lg transition-all border ${
            rotationsEnabled 
              ? 'bg-green-500/20 border-green-400/50 text-green-400' 
              : 'bg-red-500/20 border-red-400/50 text-red-400'
          }`}
        >
          <div className="flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${
              rotationsEnabled ? 'bg-green-400' : 'bg-red-400'
            }`} />
            <span className="font-medium text-sm">
              Rotations: {rotationsEnabled ? 'ON' : 'OFF'}
            </span>
          </div>
        </button>
        
        <button
          onClick={() => setShowAudioVisualizer(!showAudioVisualizer)}
          className="px-4 py-2 backdrop-blur rounded-lg bg-white/5 border border-white/10 text-white/70 hover:bg-white/10 transition-all"
        >
          <span className="text-sm">Audio: {showAudioVisualizer ? 'ON' : 'OFF'}</span>
        </button>
      </div>
      
      {/* Module Orchestra Container */}
      <ModuleOrchestra>
        {/* Predefined Modules */}
        {moduleConfigs.map(config => (
          <ModuleContainer
            key={config.id}
            config={config}
            emitter={globalEmitter}
            onPositionChange={(pos) => console.log(`${config.id} moved to`, pos)}
          >
            <config.component emitter={globalEmitter} />
          </ModuleContainer>
        ))}
        
        {/* Dynamically Spawned Modules */}
        {modules.map(module => (
          <ModuleContainer
            key={module.id}
            config={module}
            emitter={globalEmitter}
          >
            <module.component />
          </ModuleContainer>
        ))}
      </ModuleOrchestra>
      
      {/* Module Selection Wheel */}
      <ModuleWheel
        onModuleSpawn={handleModuleSpawn}
        emitter={globalEmitter}
      />
      
      {/* Cosmic Module Selector (Hidden by default, can be toggled) */}
      <div className="fixed bottom-20 left-4 max-w-sm">
        <details className="group">
          <summary className="px-4 py-2 bg-white/5 backdrop-blur rounded-lg border border-white/10 cursor-pointer hover:bg-white/10 transition-all">
            <span className="text-white/70 text-sm">AI Module Selection</span>
          </summary>
          <div className="mt-2 max-h-96 overflow-y-auto">
            <CosmicModuleSelector
              onModuleSelect={(module) => console.log('Selected:', module)}
              aiEnabled={true}
            />
          </div>
        </details>
      </div>
      
      {/* Audio Visualizer */}
      {showAudioVisualizer && (
        <div className="audio-visualizer">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="audio-bar" />
          ))}
        </div>
      )}
      
      {/* System Status */}
      <div className="fixed bottom-4 right-4 text-white/50 text-xs space-y-1">
        <div>Modules Active: {moduleConfigs.length + modules.length}</div>
        <div>System Status: Online</div>
        <div>Quantum Coherence: 87%</div>
      </div>
    </div>
  );
}

export default App;