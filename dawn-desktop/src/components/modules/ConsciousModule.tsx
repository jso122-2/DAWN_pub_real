import React from 'react'
import { ConsciousMotionDiv } from '../system/ConsciousMotionDiv'
import { cn } from '../../lib/utils'
import { usePropDebugger } from '../../utils/propDebugger'

interface ConsciousModuleProps {
  children: React.ReactNode
  moduleId: string
  className?: string
  
  // Consciousness properties - these are CELEBRATED!
  consciousnessLevel?: number     // 0-100 SCUP override
  quantumState?: 'superposition' | 'collapsed' | 'entangled' | 'coherent'
  neuralActivity?: number         // 0-1 neural firing override
  entropyLevel?: number           // 0-1 chaos override
  mood?: 'calm' | 'active' | 'excited' | 'critical' | 'chaotic' | 'unstable' | 'transcendent'
  
  // Module behavior
  category?: 'neural' | 'quantum' | 'chaos' | 'process' | 'monitor' | 'memory' | 'dream'
  syncGroup?: string              // Breathing synchronization group
  orbitalGroup?: string           // Orbital floating group
  
  // Visual overrides
  breathingIntensity?: number     // Override breathing intensity
  floatingSpeed?: number          // Override floating speed  
  glowIntensity?: number          // Override glow intensity
  particleDensity?: number        // Override particle density
  
  // State flags
  isActive?: boolean              // Module is actively processing
  isCritical?: boolean            // Module in critical state
  isEntangled?: boolean           // Quantum entangled
  isDreaming?: boolean            // In dream state
  
  // Connection data
  dataFlow?: Array<{
    source: string
    target: string
    intensity: number
  }>
  connectionPorts?: Array<{
    x: number
    y: number
    active: boolean
  }>
  neuralConnections?: string[]    // Connected module IDs
  
  // Legacy props for backward compatibility
  breathingPreset?: 'calm' | 'active' | 'critical' | 'quantum' | 'heartbeat'
  floatingPreset?: 'gentle' | 'active' | 'orbital' | 'magnetic'
  enableFloating?: boolean
  enableBreathing?: boolean
  entropy?: number                // Legacy entropy prop
}

export function ConsciousModule({
  children,
  moduleId,
  className,
  
  // Consciousness props
  consciousnessLevel,
  quantumState,
  neuralActivity,
  entropyLevel,
  mood,
  category = 'neural',
  syncGroup,
  orbitalGroup,
  breathingIntensity,
  floatingSpeed,
  glowIntensity,
  particleDensity,
  isActive,
  isCritical,
  isEntangled,
  isDreaming,
  dataFlow,
  connectionPorts,
  neuralConnections,
  
  // Legacy props - convert to new system
  breathingPreset = 'calm',
  floatingPreset = 'gentle',
  enableFloating = true,
  enableBreathing = true,
  entropy
}: ConsciousModuleProps) {
  
  // Debug prop passing to identify issues
  usePropDebugger(arguments[0], {
    componentName: 'ConsciousModule',
    logLevel: 'info',
    highlightDOMIssues: true
  })
  
  // Convert legacy props to new consciousness system
  const legacyMoodMap = {
    'calm': 'calm' as const,
    'active': 'active' as const,
    'critical': 'critical' as const,
    'quantum': 'excited' as const,
    'heartbeat': 'active' as const
  }
  
  const legacyFloatingSpeedMap = {
    'gentle': 0.3,
    'active': 0.7,
    'orbital': 0.5,
    'magnetic': 0.8
  }
  
  // Calculate effective props (new props take precedence over legacy)
  const effectiveMood = mood ?? legacyMoodMap[breathingPreset]
  const effectiveFloatingSpeed = floatingSpeed ?? legacyFloatingSpeedMap[floatingPreset]
  const effectiveEntropyLevel = entropyLevel ?? entropy
  
  // Determine consciousness level from mood if not provided
  const effectiveConsciousnessLevel = consciousnessLevel ?? (() => {
    switch (effectiveMood) {
      case 'critical': return 90
      case 'chaotic': return 85
      case 'excited': return 75
      case 'active': return 60
      case 'unstable': return 70
      case 'transcendent': return 95
      default: return 40 // calm
    }
  })()
  
  // Determine quantum state from mood if not provided
  const effectiveQuantumState = quantumState ?? (() => {
    switch (effectiveMood) {
      case 'critical': return 'collapsed' as const
      case 'chaotic': return 'superposition' as const
      case 'excited': return 'entangled' as const
      case 'transcendent': return 'coherent' as const
      default: return 'coherent' as const
    }
  })()
  
  return (
    <ConsciousMotionDiv
      moduleId={moduleId}
      category={category}
      className={cn(
        "conscious-module",
        "relative",
        className
      )}
      
      // Pass consciousness props - these make the module ALIVE!
      consciousnessLevel={effectiveConsciousnessLevel}
      quantumState={effectiveQuantumState}
      neuralActivity={neuralActivity}
      entropyLevel={effectiveEntropyLevel}
      mood={effectiveMood}
      
      // Synchronization
      syncGroup={syncGroup}
      orbitalGroup={orbitalGroup}
      
      // Visual behavior
      breathingIntensity={enableBreathing ? breathingIntensity : 0}
      floatingSpeed={enableFloating ? effectiveFloatingSpeed : 0}
      glowIntensity={glowIntensity}
      particleDensity={particleDensity}
      
      // State flags
      isActive={isActive}
      isCritical={isCritical}
      isEntangled={isEntangled}
      isDreaming={isDreaming}
      
      // Data connections
      dataFlow={dataFlow}
      connectionPorts={connectionPorts}
      neuralConnections={neuralConnections}
    >
      {children}
    </ConsciousMotionDiv>
  )
} 