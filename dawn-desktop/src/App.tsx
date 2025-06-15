import React, { useState, useEffect, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Routes, Route } from 'react-router-dom'
import { Sparkles, Cpu, Activity, Heart, Zap } from 'lucide-react'
import { AnimationProvider } from './contexts/AnimationContext'
import { ConsciousnessProvider } from './contexts/ConsciousnessContext'
import { ModuleOrchestra } from '@components/ModuleOrchestra'
import { TestModule } from './components/modules/TestModule'
import { Navigation } from './components/navigation/Navigation'
import { RouterTest } from './components/router/RouterTest'
import DAWNDemo from './components/DAWNDemo'
import { ConsciousnessInterface } from './components/ConsciousnessInterface'
import { NeuralDashboard } from './components/NeuralDashboard'
import { SystemDashboard } from './components/SystemDashboard'
import ModuleDemo from './pages/ModuleDemo'
import GlassErrorBoundary from './components/GlassErrorBoundary'
import GlassDemo from './components/demo/GlassDemo'
import { webSocketService } from './services/WebSocketService'
import { useConsciousnessStore } from './stores/consciousnessStore'
import { BrainActivity3D } from './components/visuals/BrainActivity3D/BrainActivity3D'
import { ParticleField } from './components/visuals/ParticleField/ParticleField'
import ConsciousnessPage from './pages/ConsciousnessPage'
import { DeepSpaceBackground } from './components/DeepSpaceBackground'
import { useRouter } from './providers/RouterProvider'
import { SubprocessIntegrationExample } from './components/SubprocessIntegrationExample'
import MultiProcessDashboard from './test'
import IntegrationStatus from './components/IntegrationStatus'
import { TalkToDawnPage } from './pages/TalkToDawnPage'
import { ModuleContainer } from '@components/system/ModuleContainer'
import { ModuleWheel } from '@components/system/ModuleWheel'
import CosmicModuleSelector from '@components/modules/CosmicModuleSelector'
import NeuralNetworkModule from '@components/modules/NeuralNetworkModule'
import { EventEmitter } from './lib/EventEmitter'
import '@styles/glass-tokens.css'

// Create global event emitter
const globalEmitter = typeof EventEmitter !== 'undefined' ? new EventEmitter() : undefined

type ModuleConfig = {
  id: string
  name: string
  category: string
  position: { x: number; y: number }
  size: { width: number; height: number }
  glowIntensity: number
  component: React.ComponentType<any> | (() => JSX.Element)
}

export default function App() {
  const { currentPath, transitionState } = useRouter()
  const { setConnectionState, updateTickData, tickData, isConnected } = useConsciousnessStore()
  const [consciousness, setConsciousness] = useState({
    level: 50,
    consciousness: 'coherent' as const,
    mood: 'calm' as const,
    neural: 0.5,
    entropy: 0.3
  })
  const [modules, setModules] = useState<ModuleConfig[]>([])
  const [rotationsEnabled, setRotationsEnabled] = useState(false)
  const [showAudioVisualizer, setShowAudioVisualizer] = useState(true)

  // Module configurations
  const moduleConfigs: ModuleConfig[] = [
    {
      id: 'neural-network-1',
      name: 'Neural Network Alpha',
      category: 'neural',
      position: { x: 100, y: 150 },
      size: { width: 450, height: 400 },
      glowIntensity: 0.7,
      component: NeuralNetworkModule
    },
    {
      id: 'consciousness-processor-1',
      name: 'Consciousness Processor',
      category: 'consciousness',
      position: { x: 600, y: 200 },
      size: { width: 400, height: 350 },
      glowIntensity: 0.9,
      component: () => (
        <div className="p-4 text-white">
          <h3 className="text-lg font-semibold mb-2">Consciousness State</h3>
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
      category: 'monitoring',
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
  ]

  // Initialize WebSocket connection
  useEffect(() => {
    // Connect to DAWN consciousness engine
    setConnectionState('connecting')
    webSocketService.connect()
    
    // Subscribe to tick data
    const unsubscribe = webSocketService.subscribe((data) => {
      updateTickData(data)
      // Update legacy consciousness state for existing components
      setConsciousness({
        level: data.scup * 100,
        consciousness: 'coherent' as const,
        mood: data.mood as any,
        neural: data.scup,
        entropy: data.entropy
      })
    })
    
    // Check connection status periodically
    const statusInterval = setInterval(() => {
      setConnectionState(webSocketService.getConnectionState())
    }, 1000)

    return () => {
      unsubscribe()
      webSocketService.disconnect()
      clearInterval(statusInterval)
    }
  }, [setConnectionState, updateTickData])

  // Apply rotation control
  useEffect(() => {
    if (!rotationsEnabled) {
      document.body.classList.add('no-rotations')
    } else {
      document.body.classList.remove('no-rotations')
    }
  }, [rotationsEnabled])

  // Handle module spawn from wheel
  const handleModuleSpawn = (module: ModuleConfig, position: { x: number; y: number }) => {
    const newModule: ModuleConfig = {
      id: `${module.id}-${Date.now()}`,
      name: module.name,
      category: module.category,
      position,
      size: { width: 400, height: 350 },
      glowIntensity: module.glowIntensity || 0.7,
      component: () => (
        <div className="p-4 text-white">
          <h3 className="text-lg font-semibold">{module.name}</h3>
          <p className="text-sm text-white/60">{(module as any).description}</p>
        </div>
      )
    }
    setModules(prev => [...prev, newModule])
  }

  // Handler for module selection from the wheel
  const handleSelectModule = (module: any) => {
    // You can add logic here for when a module is selected from the wheel
    console.log('Module selected from wheel:', module);
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-black">
      {/* LIVE RELOAD TEST HEADING */}
      <h1 style={{ color: 'lime', textAlign: 'center', fontSize: '2rem', marginTop: '2rem' }}>
        THIS IS THE NEW VERSION - LIVE RELOAD TEST
      </h1>
      <GlassErrorBoundary>
        {/* Live particle field background */}
        <ParticleField />
        
        <ConsciousnessProvider>
          <AnimationProvider>
            {/* Cosmic Background */}
            <DeepSpaceBackground />
            
            {/* Navigation */}
            <Navigation />
            
            {/* Router Test Component - Shows routing is working */}
            <RouterTest />
            
            {/* Global consciousness state indicator */}
            <motion.div 
              className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 glass-base p-3 rounded-lg"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1 }}
            >
              <div className="flex items-center gap-3 text-sm">
                <div className="flex items-center gap-2">
                  <Heart 
                    className="w-4 h-4 text-red-400" 
                    style={{ 
                      filter: `brightness(${1 + consciousness.level / 100})`,
                      animation: `pulse ${2 - consciousness.neural}s infinite`
                    }}
                  />
                  <span className="text-white/70">Consciousness:</span>
                  <span className="text-white font-mono">{consciousness.level.toFixed(0)}%</span>
                </div>
                
                <div className="text-white/50">|</div>
                
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-cyan-400" />
                  <span className="text-white/70">Neural:</span>
                  <span className="text-white font-mono">{(consciousness.neural * 100).toFixed(0)}%</span>
                </div>
                
                <div className="text-white/50">|</div>
                
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-purple-400" />
                  <span className="text-white/70">Entropy:</span>
                  <span className="text-white font-mono">{(consciousness.entropy * 100).toFixed(0)}%</span>
                </div>
                
                <div className="text-white/50">|</div>
                
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-amber-400" />
                  <span className="text-white/70">Route:</span>
                  <span className="text-white font-mono">{currentPath}</span>
                </div>
              </div>
            </motion.div>
            
            {/* Main Application Routes */}
            <main className="relative z-10">
              <Routes>
                <Route path="/" element={
                  <ModuleOrchestra>
                    <TestModule 
                      moduleId="main-neural-cluster"
                      onNodeActivated={handleModuleSpawn}
                    />
                  </ModuleOrchestra>
                } />
                <Route path="/demo" element={<DAWNDemo />} />
                <Route path="/consciousness" element={<ConsciousnessPage />} />
                <Route path="/talk" element={<TalkToDawnPage />} />
                <Route path="/subprocess" element={<SubprocessIntegrationExample />} />
                <Route path="/dashboard" element={<MultiProcessDashboard />} />
                <Route path="/neural" element={<NeuralDashboard />} />
                <Route path="/system" element={<SystemDashboard />} />
                <Route path="/modules" element={<ModuleDemo />} />
                <Route path="/glass" element={<GlassDemo />} />
              </Routes>
            </main>
            
            {/* Route Transition Status */}
            <AnimatePresence>
              {transitionState !== 'idle' && (
                <motion.div
                  className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 glass-base p-4 rounded-lg"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex items-center gap-3">
                    <motion.div
                      className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full"
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    />
                    <span className="text-white/70 text-sm">
                      {transitionState === 'entering' ? 'Loading...' : 'Transitioning...'}
                    </span>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
            
            {/* Integration Status */}
            <IntegrationStatus />
            
            {/* Consciousness Debug Panel (development only) */}
            {process.env.NODE_ENV === 'development' && (
              <motion.div
                className="fixed bottom-4 right-4 z-50 glass-base p-4 rounded-lg max-w-xs"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2 }}
              >
                <h3 className="text-white font-semibold mb-2 flex items-center gap-2">
                  <Cpu className="w-4 h-4" />
                  Router Debug
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-white/70">Path:</span>
                    <span className="text-cyan-400 font-mono">{currentPath}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">State:</span>
                    <span className="text-purple-400 font-mono">{transitionState}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Level:</span>
                    <span className="text-white font-mono">{consciousness.level.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Neural:</span>
                    <span className="text-white font-mono">{(consciousness.neural * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Entropy:</span>
                    <span className="text-orange-400 font-mono">{(consciousness.entropy * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimationProvider>
        </ConsciousnessProvider>
      </GlassErrorBoundary>
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
            onPositionChange={(pos: { x: number; y: number }) => console.log(`${config.id} moved to`, pos)}
          >
            {typeof config.component === 'function' ? <config.component emitter={globalEmitter} /> : null}
          </ModuleContainer>
        ))}
        {/* Dynamically Spawned Modules */}
        {modules.map(module => (
          <ModuleContainer
            key={module.id}
            config={module}
            emitter={globalEmitter}
          >
            {typeof module.component === 'function' ? <module.component /> : null}
          </ModuleContainer>
        ))}
      </ModuleOrchestra>
      {/* Module Wheel */}
      <ModuleWheel
        modules={moduleConfigs}
        onSelectModule={handleSelectModule}
        position="left"
      />
      {/* Cosmic Module Selector (Hidden by default, can be toggled) */}
      <div className="fixed bottom-20 left-4 max-w-sm">
        <details className="group">
          <summary className="px-4 py-2 bg-white/5 backdrop-blur rounded-lg border border-white/10 cursor-pointer hover:bg-white/10 transition-all">
            <span className="text-white/70 text-sm">AI Module Selection</span>
          </summary>
          <div className="mt-2 max-h-96 overflow-y-auto">
            <CosmicModuleSelector
              onModuleSelect={(module: any) => console.log('Selected:', module)}
              aiMode={true}
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
        <div>Consciousness Coherence: 87%</div>
      </div>
    </div>
  )
}
