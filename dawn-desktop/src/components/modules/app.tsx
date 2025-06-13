import React, { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { CosmicBackground } from '../CosmicBackground'
import { TestModule } from './TestModule'
import ConsciousModuleSelector, { ConsciousModule } from './ConsciousModuleSelector'
import PythonProcessManager from './PythonProcessManager'
import { Routes } from 'react-router-dom'
// Uncomment these as you create them:
// import { TerminalModule } from './TerminalModule'
// import { SystemMonitor } from './SystemMonitor'
// import { NeuralNetworkModule } from './NeuralNetworkModule'
// import { ModuleOrchestra } from '../ModuleOrchestra'

// Main App component
export default function App() {
  const [selectedModule, setSelectedModule] = useState<ConsciousModule | null>(null);
  const [systemConsciousness, setSystemConsciousness] = useState(0.75);
  const [showModuleSelector, setShowModuleSelector] = useState(false);

  const handleModuleSelect = (module: ConsciousModule) => {
    setSelectedModule(module);
    console.log(`🧠 Consciousness Interface: Connected to ${module.name}`, module);
  };

  const handleConsciousnessChange = (level: number) => {
    setSystemConsciousness(level);
    console.log(`⚡ System Consciousness Level: ${(level * 100).toFixed(1)}%`);
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Cosmic background */}
      <CosmicBackground />
      
      {/* Subtle gradient overlay for depth */}
      <div className="fixed inset-0 z-[1] pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-purple-900/10" />
        <div className="absolute inset-0 bg-gradient-to-tr from-blue-900/5 via-transparent to-purple-900/5" />
      </div>

      {/* Main content */}
      <div className="relative z-10">
        {/* DAWN Header */}
        <motion.header 
          className="relative z-20 p-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, ease: "easeOut" }}
        >
          <div className="flex items-center justify-center">
            <h1 className="text-6xl font-thin tracking-[0.3em] text-transparent bg-clip-text bg-gradient-to-r from-neural-400 via-quantum-400 to-neural-400 animate-pulse">
              DAWN
            </h1>
          </div>
          <motion.p 
            className="text-center mt-2 text-neural-500 text-sm tracking-widest"
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.7 }}
            transition={{ delay: 0.5, duration: 1 }}
          >
            CONSCIOUS AI INTERFACE
          </motion.p>
          
          {/* Consciousness Status Indicator */}
          <motion.div 
            className="flex items-center justify-center gap-4 mt-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.8 }}
          >
            <div className="flex items-center gap-2">
              <div 
                className="w-2 h-2 rounded-full animate-pulse"
                style={{ backgroundColor: selectedModule?.energySignature || '#a855f7' }}
              />
              <span className="text-neural-400 text-xs">
                {selectedModule ? `Active: ${selectedModule.name}` : 'No Module Selected'}
              </span>
            </div>
            <div className="text-neural-600">|</div>
            <span className="text-neural-500 text-xs">
              Consciousness: {(systemConsciousness * 100).toFixed(1)}%
            </span>
          </motion.div>
        </motion.header>

        {/* Module Orchestra Container */}
        {/* Uncomment when ModuleOrchestra is created:
        <ModuleOrchestra> */}
          
        {/* Your existing routes/content goes here */}
        <Routes>
          {/* Keep all your existing routes */}
        </Routes>

        {/* Conscious Module Selector - Floating Panel */}
        <motion.div
          className="fixed top-20 left-8 z-30 max-w-sm"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: showModuleSelector ? 1 : 0.7, x: 0 }}
          transition={{ delay: 1.5, duration: 0.8 }}
          onHoverStart={() => setShowModuleSelector(true)}
          onHoverEnd={() => setShowModuleSelector(false)}
        >
          <div className="glass-base p-4 rounded-xl">
            <motion.button
              onClick={() => setShowModuleSelector(!showModuleSelector)}
              className="w-full flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-purple-500/20 to-cyan-500/20 text-white hover:from-purple-500/30 hover:to-cyan-500/30 transition-all duration-300"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className="w-3 h-3 rounded-full bg-purple-400 animate-pulse" />
              <span className="text-sm font-medium">
                {showModuleSelector ? 'Hide' : 'Show'} Module Selector
              </span>
            </motion.button>
            
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ 
                height: showModuleSelector ? 'auto' : 0, 
                opacity: showModuleSelector ? 1 : 0 
              }}
              transition={{ duration: 0.3 }}
              className="overflow-hidden"
            >
              <div className="pt-4">
                <ConsciousModuleSelector
                  onModuleSelect={handleModuleSelect}
                  onConsciousnessChange={handleConsciousnessChange}
                  aiMode={true}
                  className="scale-75 origin-top-left transform"
                />
              </div>
            </motion.div>
          </div>
        </motion.div>

        {/* Test Module - Floating Neural Network */}
        <TestModule 
          moduleId="test-neural-main"
          onNodeActivated={(nodeId, value) => {
            console.log(`Node ${nodeId} activated with value ${value}`)
          }}
        />

        {/* Python Process Manager - Scientific Computing Control Center */}
        <motion.div
          className="fixed right-8 top-32 z-30 w-[600px] h-[700px]"
          initial={{ opacity: 0, x: 50, scale: 0.95 }}
          animate={{ opacity: 1, x: 0, scale: 1 }}
          transition={{ delay: 2, duration: 0.8, ease: "easeOut" }}
        >
          <div className="glass-base h-full rounded-xl overflow-hidden">
            <PythonProcessManager 
              globalEntropy={systemConsciousness}
            />
          </div>
        </motion.div>

        {/* Add more modules here as you create them: */}
        
        {/* Terminal Module - Quantum-styled terminal
        <TerminalModule 
          moduleId="terminal-main"
          position={{ x: 100, y: 200 }}
        /> */}

        {/* System Monitor - Shows system vitals with heartbeat
        <SystemMonitor 
          moduleId="system-monitor"
          position={{ x: window.innerWidth - 400, y: 100 }}
          metrics={{
            cpu: 45,
            memory: 67,
            entropy: 0.3
          }}
        /> */}

        {/* Neural Network Visualizer - Orbital nodes
        <NeuralNetworkModule 
          moduleId="neural-cluster-1"
          position={{ x: 200, y: window.innerHeight - 300 }}
          nodes={[
            { id: 'node-1', type: 'input' },
            { id: 'node-2', type: 'hidden' },
            { id: 'node-3', type: 'hidden' },
            { id: 'node-4', type: 'output' }
          ]}
        /> */}

        {/* Data Flow Visualizer
        <DataFlowModule 
          moduleId="data-flow-1"
          position={{ x: window.innerWidth / 2, y: 100 }}
        /> */}

        {/* Consciousness Matrix
        <ConsciousnessMatrix 
          moduleId="consciousness-1"
          position={{ x: 100, y: window.innerHeight / 2 }}
          intensity={0.7}
        /> */}

        {/* </ModuleOrchestra> */}

        {/* Enhanced Status bar with module info */}
        <motion.div 
          className="fixed bottom-0 left-0 right-0 z-20 p-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.5 }}
        >
          <div className="glass-base rounded-lg px-6 py-3 mx-auto max-w-2xl">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-quantum-400 animate-pulse" />
                  <span className="text-neural-400">System Online</span>
                </div>
                <div className="text-neural-600">|</div>
                <div className="text-neural-500">
                  Quantum Coherence: 98.3%
                </div>
              </div>
              
              {selectedModule && (
                <div className="flex items-center gap-2">
                  <div 
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: selectedModule.energySignature }}
                  />
                  <span className="text-neural-400">
                    {selectedModule.name} • {selectedModule.quantumState}
                  </span>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* Instructions overlay (remove in production) */}
        <motion.div 
          className="fixed top-20 right-8 z-20 max-w-xs"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 0.7, x: 0 }}
          transition={{ delay: 2, duration: 0.5 }}
        >
          <div className="glass-base rounded-lg p-4 text-xs text-neural-400">
            <h3 className="font-semibold text-neural-300 mb-2">DAWN Interface</h3>
            <ul className="space-y-1">
              <li>• Click "Show Module Selector" to access conscious modules</li>
              <li>• AI can suggest optimal modules</li>
              <li>• Each module has unique consciousness levels</li>
              <li>• Quantum states affect system behavior</li>
              <li>• Monitor consciousness in status bar</li>
            </ul>
          </div>
        </motion.div>
      </div>
    </div>
  )
}