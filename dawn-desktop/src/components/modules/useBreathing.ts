import { useEffect, useRef, useState, useMemo } from 'react'
import { useAnimationFrame } from 'framer-motion'
import type { MotionProps } from 'framer-motion'

export type BreathingPreset = 'calm' | 'active' | 'critical' | 'quantum' | 'heartbeat'

interface BreathingConfig {
  scale: { min: number; max: number }
  opacity: { min: number; max: number }
  duration: number
  easing: string
  glowIntensity: number
  glowColor: string
}

interface UseBreathingOptions {
  preset?: BreathingPreset
  entropy?: number // 0-1, system activity level
  syncGroup?: string // Synchronize with other modules
  disabled?: boolean
  customConfig?: Partial<BreathingConfig>
}

// Global sync state for breathing groups
const breathingGroups = new Map<string, { phase: number; timestamp: number }>()

const BREATHING_PRESETS: Record<BreathingPreset, BreathingConfig> = {
  calm: {
    scale: { min: 1, max: 1.02 },
    opacity: { min: 0.9, max: 1 },
    duration: 4000,
    easing: 'easeInOut',
    glowIntensity: 20,
    glowColor: 'rgba(147, 51, 234, 0.3)'
  },
  active: {
    scale: { min: 0.98, max: 1.04 },
    opacity: { min: 0.85, max: 1 },
    duration: 2000,
    easing: 'easeInOut',
    glowIntensity: 40,
    glowColor: 'rgba(147, 51, 234, 0.5)'
  },
  critical: {
    scale: { min: 0.95, max: 1.05 },
    opacity: { min: 0.8, max: 1 },
    duration: 1000,
    easing: 'easeInOut',
    glowIntensity: 60,
    glowColor: 'rgba(236, 72, 153, 0.6)'
  },
  quantum: {
    scale: { min: 0.97, max: 1.03 },
    opacity: { min: 0.92, max: 1 },
    duration: 3000,
    easing: 'circInOut',
    glowIntensity: 50,
    glowColor: 'rgba(34, 211, 238, 0.4)'
  },
  heartbeat: {
    scale: { min: 0.98, max: 1.06 },
    opacity: { min: 0.9, max: 1 },
    duration: 800,
    easing: 'backOut',
    glowIntensity: 80,
    glowColor: 'rgba(239, 68, 68, 0.7)'
  }
}

export function useBreathing(options: UseBreathingOptions = {}): MotionProps {
  const {
    preset = 'calm',
    entropy = 0,
    syncGroup,
    disabled = false,
    customConfig
  } = options

  const [phase, setPhase] = useState(0)
  const [breathingState, setBreathingState] = useState({
    scale: 1,
    opacity: 1,
    glow: 0
  })

  const startTime = useRef(Date.now())
  const rafRef = useRef<number>()

  // Get configuration with entropy adjustments
  const config = useMemo(() => {
    const baseConfig = { ...BREATHING_PRESETS[preset], ...customConfig }
    
    // Adjust based on entropy
    if (entropy > 0) {
      const entropyMultiplier = 1 + (entropy * 0.5)
      baseConfig.duration = baseConfig.duration / entropyMultiplier
      baseConfig.scale.max = baseConfig.scale.max + (entropy * 0.02)
      baseConfig.glowIntensity = baseConfig.glowIntensity * (1 + entropy)
    }

    return baseConfig
  }, [preset, entropy, customConfig])

  // Breathing calculation function
  const calculateBreathing = (timestamp: number) => {
    let currentPhase = phase

    // Sync with group if specified
    if (syncGroup) {
      const groupData = breathingGroups.get(syncGroup)
      if (groupData) {
        currentPhase = groupData.phase
      } else {
        breathingGroups.set(syncGroup, { phase: 0, timestamp })
      }
    }

    const elapsed = timestamp - startTime.current
    const progress = (elapsed % config.duration) / config.duration
    
    // Calculate breathing curve
    let breathingCurve: number
    
    if (preset === 'heartbeat') {
      // Double pump for heartbeat
      const heartPhase = progress * 2 * Math.PI
      breathingCurve = progress < 0.5
        ? Math.sin(heartPhase * 2) * 0.3 + Math.sin(heartPhase) * 0.7
        : Math.sin(heartPhase) * 0.5
    } else {
      // Smooth sine wave for other presets
      breathingCurve = Math.sin(progress * Math.PI * 2)
    }

    // Apply easing
    const easedCurve = applyEasing(breathingCurve, config.easing)

    // Calculate values
    const scale = lerp(
      config.scale.min,
      config.scale.max,
      (easedCurve + 1) / 2
    )

    const opacity = lerp(
      config.opacity.min,
      config.opacity.max,
      (easedCurve + 1) / 2
    )

    const glow = config.glowIntensity * ((easedCurve + 1) / 2)

    // Update sync group
    if (syncGroup) {
      breathingGroups.set(syncGroup, { phase: progress, timestamp })
    }

    return { scale, opacity, glow }
  }

  // Animation frame loop
  useAnimationFrame((timestamp) => {
    if (disabled) return
    
    const breathing = calculateBreathing(timestamp)
    setBreathingState(breathing)
  })

  // Generate motion props
  const motionProps: MotionProps = useMemo(() => {
    if (disabled) {
      return {}
    }

    return {
      animate: {
        scale: breathingState.scale,
        opacity: breathingState.opacity,
      },
      style: {
        filter: `drop-shadow(0 0 ${breathingState.glow}px ${config.glowColor})`,
      },
      transition: {
        duration: 0.1,
        ease: 'linear'
      }
    }
  }, [breathingState, config.glowColor, disabled])

  return motionProps
}

// Utility functions
function lerp(start: number, end: number, progress: number): number {
  return start + (end - start) * progress
}

function applyEasing(value: number, easing: string): number {
  switch (easing) {
    case 'easeInOut':
      return value < 0 
        ? 0.5 * Math.pow(2, 10 * (value + 1))
        : 0.5 * (-Math.pow(2, -10 * (value - 1)) + 2)
    case 'circInOut':
      return value < 0
        ? -0.5 * (Math.sqrt(1 - value * value) - 1)
        : 0.5 * (Math.sqrt(1 - (value - 2) * (value - 2)) + 1)
    case 'backOut':
      const c1 = 1.70158
      const c3 = c1 + 1
      return 1 + c3 * Math.pow(value - 1, 3) + c1 * Math.pow(value - 1, 2)
    default:
      return value
  }
}

// Hook to get current breathing phase for a sync group
export function useBreathingSync(syncGroup: string): number {
  const [phase, setPhase] = useState(0)

  useAnimationFrame(() => {
    const groupData = breathingGroups.get(syncGroup)
    if (groupData) {
      setPhase(groupData.phase)
    }
  })

  return phase
}

// Cleanup function for removing sync groups
export function cleanupBreathingGroup(syncGroup: string): void {
  breathingGroups.delete(syncGroup)
}