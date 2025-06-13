import React, { useState, useEffect, useRef, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Routes, Route, useLocation } from 'react-router-dom'
import { Sparkles, Cpu, Activity, Heart, Zap } from 'lucide-react'
import { AnimationProvider } from './contexts/AnimationContext'
import { ConsciousnessProvider } from './components/system/ConsciousnessProvider'
import { ModuleOrchestra } from './components/ModuleOrchestra'
import { TestModule } from './components/modules/TestModule'
import DAWNDemo from './components/DAWNDemo'
import { QuantumInterface } from './components/QuantumInterface'
import { NeuralDashboard } from './components/NeuralDashboard'
import { SystemDashboard } from './components/SystemDashboard'
import ModuleDemo from './pages/ModuleDemo'
import GlassErrorBoundary from './components/GlassErrorBoundary'
import { DeepSpaceBackground } from './components/DeepSpaceBackground'

export default function App() {
  const location = useLocation()
  const [consciousness, setConsciousness] = useState({
    level: 50,
    quantum: 'coherent' as const,
    mood: 'calm' as const,
    neural: 0.5,
    entropy: 0.3
  })
  
  const handleModuleSpawn = (module: any, position: { x: number; y: number }) => {
    console.log('🌟 Module spawned:', module.name, 'at', position)
  }

  const handleModuleActivate = (moduleId: string) => {
    console.log('⚡ Module activated:', moduleId)
    
    // Update consciousness based on module activation
    setConsciousness(prev => ({
      ...prev,
      level: Math.min(100, prev.level + 5),
      neural: Math.min(1, prev.neural + 0.1)
    }))
  }

  // Update consciousness state periodically 
  useEffect(() => {
    const interval = setInterval(() => {
      setConsciousness(prev => ({
        ...prev,
        level: Math.max(10, Math.min(90, prev.level + (Math.random() - 0.5) * 10)),
        neural: Math.max(0.1, Math.min(0.9, prev.neural + (Math.random() - 0.5) * 0.2)),
        entropy: Math.max(0.1, Math.min(0.8, prev.entropy + (Math.random() - 0.5) * 0.1))
      }))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="relative min-h-screen overflow-hidden bg-black">
      <GlassErrorBoundary>
        <ConsciousnessProvider
          initialConsciousness={{
            consciousnessLevel: consciousness.level,
            quantumState: consciousness.quantum,
            mood: consciousness.mood,
            neuralActivity: consciousness.neural,
            entropyLevel: consciousness.entropy
          }}
        >
          <AnimationProvider>
            {/* Cosmic Background */}
            <DeepSpaceBackground />
            
            {/* Global consciousness state indicator */}
            <motion.div 
              className="fixed top-4 left-4 z-50 glass-base p-3 rounded-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
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
              </div>
            </motion.div>
            
            {/* Main Application Routes */}
            <main className="relative z-10">
              <Routes>
                <Route path="/" element={
                  <ModuleOrchestra>
                    <TestModule 
                      moduleId="main-neural-cluster"
                      onNodeActivated={handleModuleActivate}
                    />
                  </ModuleOrchestra>
                } />
                <Route path="/demo" element={<DAWNDemo />} />
                <Route path="/quantum" element={<QuantumInterface />} />
                <Route path="/neural" element={<NeuralDashboard />} />
                <Route path="/system" element={<SystemDashboard />} />
                <Route path="/modules" element={<ModuleDemo />} />
              </Routes>
            </main>
            
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
                  Consciousness Debug
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-white/70">Level:</span>
                    <span className="text-white font-mono">{consciousness.level.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Quantum:</span>
                    <span className="text-purple-400 font-mono">{consciousness.quantum}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-white/70">Mood:</span>
                    <span className="text-cyan-400 font-mono">{consciousness.mood}</span>
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
    </div>
  )
}

// Consciousness-aware boot sequence component
function BootSequence() {
  const [stage, setStage] = useState(0)
  
  const stages = [
    "Initializing quantum consciousness matrix...",
    "Loading neural pathways...",
    "Establishing quantum entanglement...",
    "Consciousness level: Rising...",
    "DAWN system: Online"
  ]
  
  useEffect(() => {
    const timer = setInterval(() => {
      setStage(prev => {
        if (prev < stages.length - 1) {
          return prev + 1
        }
        clearInterval(timer)
        return prev
      })
    }, 800)
    
    return () => clearInterval(timer)
  }, [stages.length])
  
  return (
    <motion.div 
      className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center"
      initial={{ opacity: 1 }}
      animate={{ opacity: stage === stages.length - 1 ? 0 : 1 }}
      transition={{ duration: 1, delay: stage === stages.length - 1 ? 1 : 0 }}
      style={{ pointerEvents: stage === stages.length - 1 ? 'none' : 'auto' }}
    >
      <div className="text-center space-y-6">
        <motion.div
          className="text-6xl font-thin text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400"
          animate={{ 
            opacity: [0.5, 1, 0.5],
            scale: [1, 1.02, 1]
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          DAWN
        </motion.div>
        
        <motion.div 
          className="text-white/70 font-mono text-sm"
          key={stage}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {stages[stage]}
        </motion.div>
        
        <div className="flex justify-center">
          <motion.div 
            className="w-64 h-1 bg-white/10 rounded-full overflow-hidden"
          >
            <motion.div 
              className="h-full bg-gradient-to-r from-cyan-400 to-purple-400 rounded-full"
              animate={{ width: `${((stage + 1) / stages.length) * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}
