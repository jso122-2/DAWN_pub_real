// Add performance monitoring
const PERFORMANCE_MODE = (import.meta as any).env?.VITE_PERFORMANCE_MODE === 'true'

import { useEffect, useRef, useState, useMemo } from 'react'
import { useAnimationFrame, useAnimation, useMotionValue, AnimationControls } from 'framer-motion'
import type { MotionProps } from 'framer-motion'

export type BreathingPreset = 'idle' | 'active' | 'processing' | 'calm' | 'critical' | 'quantum' | 'heartbeat'
export type BreathingState = 'idle' | 'active' | 'processing' | 'error'

interface BreathingConfig {
  scale?: number
  duration?: number
  opacity?: number
  glowIntensity?: number
}

export interface UseBreathingOptions {
  preset?: BreathingPreset
  state?: BreathingState
  intensity?: number // 0-1, system activity level
  syncGroup?: string // Synchronize with other modules
  disabled?: boolean
  customConfig?: Partial<BreathingConfig>
}

// Global sync state for breathing groups
const breathingGroups = new Map<string, { phase: number; timestamp: number }>()

const BREATHING_PRESETS: Record<BreathingPreset, BreathingConfig> = {
  idle: {
    scale: { min: 1, max: 1.02 },
    opacity: { min: 0.9, max: 1 },
    duration: 4,
    easing: 'easeInOut',
    glowIntensity: 20,
    glowColor: 'rgba(147, 51, 234, 0.3)'
  },
  active: {
    scale: { min: 0.98, max: 1.04 },
    opacity: { min: 0.85, max: 1 },
    duration: 2,
    easing: 'easeInOut',
    glowIntensity: 40,
    glowColor: 'rgba(147, 51, 234, 0.5)'
  },
  processing: {
    scale: { min: 0.95, max: 1.05 },
    opacity: { min: 0.8, max: 1 },
    duration: 1.2,
    easing: 'easeInOut',
    glowIntensity: 60,
    glowColor: 'rgba(236, 72, 153, 0.6)'
  },
  calm: {
    scale: { min: 1, max: 1.02 },
    opacity: { min: 0.9, max: 1 },
    duration: 4,
    easing: 'easeInOut',
    glowIntensity: 20,
    glowColor: 'rgba(147, 51, 234, 0.3)'
  },
  critical: {
    scale: { min: 0.95, max: 1.05 },
    opacity: { min: 0.8, max: 1 },
    duration: 1,
    easing: 'easeInOut',
    glowIntensity: 60,
    glowColor: 'rgba(236, 72, 153, 0.6)'
  },
  quantum: {
    scale: { min: 0.97, max: 1.03 },
    opacity: { min: 0.92, max: 1 },
    duration: 3,
    easing: 'circInOut',
    glowIntensity: 50,
    glowColor: 'rgba(34, 211, 238, 0.4)'
  },
  heartbeat: {
    scale: { min: 0.98, max: 1.06 },
    opacity: { min: 0.9, max: 1 },
    duration: 0.8,
    easing: 'backOut',
    glowIntensity: 80,
    glowColor: 'rgba(239, 68, 68, 0.7)'
  }
}

/**
 * useBreathing - Framer Motion breathing animation hook
 * @param options UseBreathingOptions
 * @returns { controls, variants, glow, glowColor }
 */
export function useBreathing(options: UseBreathingOptions = {}) {
  const {
    preset = 'idle',
    state = 'idle',
    intensity = 0,
    disabled = false,
    customConfig
  } = options

  const controls = useAnimation()
  const scale = useMotionValue(1)
  const opacity = useMotionValue(1)

  // Merge config
  const config = useMemo(() => {
    const base = { ...BREATHING_PRESETS[preset], ...customConfig }
    if (intensity > 0) {
      const multiplier = 1 + intensity * 0.5
      base.duration = base.duration / multiplier
      base.scale.max = base.scale.max + intensity * 0.02
      base.glowIntensity = base.glowIntensity * (1 + intensity)
    }
    return base
  }, [preset, intensity, customConfig])

  // Animation loop
  useEffect(() => {
    if (disabled) return
    let frame = 0
    let running = true
    const animate = async () => {
      while (running) {
        await controls.start({
          scale: config.scale.max,
          opacity: config.opacity.max,
          transition: { duration: config.duration / 2, ease: config.easing }
        })
        await controls.start({
          scale: config.scale.min,
          opacity: config.opacity.min,
          transition: { duration: config.duration / 2, ease: config.easing }
        })
        frame++
      }
    }
    animate()
    return () => { running = false }
  }, [controls, config, disabled])

  // Variants for framer-motion
  const variants = useMemo(() => {
    return {
      idle: {
        scale: [config.scale.min, config.scale.max, config.scale.min],
        opacity: [config.opacity.min, config.opacity.max, config.opacity.min],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: config.easing
        }
      },
      active: {
        scale: [config.scale.min, config.scale.max, config.scale.min],
        opacity: [config.opacity.min, config.opacity.max, config.opacity.min],
        transition: {
          duration: config.duration * 0.7,
          repeat: Infinity,
          ease: config.easing
        }
      },
      processing: {
        scale: [config.scale.min, config.scale.max, config.scale.min],
        opacity: [config.opacity.min, config.opacity.max, config.opacity.min],
        transition: {
          duration: config.duration * 0.5,
          repeat: Infinity,
          ease: config.easing
        }
      },
      breathe: {
        scale: [config.scale.min, config.scale.max, config.scale.min],
        opacity: [config.opacity.min, config.opacity.max, config.opacity.min],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: config.easing
        }
      }
    }
  }, [config])

  // Optionally, auto-start animation
  useEffect(() => {
    if (!disabled) controls.start(state)
  }, [controls, state, disabled])

  return {
    controls,
    scale,
    opacity,
    variants,
    glow: config.glowIntensity,
    glowColor: config.glowColor
  }
}

export type UseBreathingReturn = ReturnType<typeof useBreathing>

// Animation frame loop
useAnimationFrame((timestamp) => {
  if (PERFORMANCE_MODE && timestamp % 2 !== 0) return // Skip every other frame
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

const DEFAULT_CONFIG: Record<BreathingState, BreathingConfig> = {
  idle: { scale: 0.02, duration: 4, opacity: 0.95, glowIntensity: 0.3 },
  active: { scale: 0.03, duration: 2, opacity: 1, glowIntensity: 0.6 },
  processing: { scale: 0.04, duration: 1.5, opacity: 1, glowIntensity: 0.8 },
  error: { scale: 0.05, duration: 1, opacity: 1, glowIntensity: 1 }
}

export const useBreathing = (
  intensity: number = 0.5,
  state: BreathingState = 'idle',
  customConfig?: Partial<BreathingConfig>
): UseBreathingReturn => {
  const controls = useAnimation()
  
  const config = useMemo(() => ({
    ...DEFAULT_CONFIG[state],
    ...customConfig
  }), [state, customConfig])
  
  const variants = useMemo(() => {
    const baseScale = 1
    const scaleAmount = config.scale! * intensity
    
    return {
      idle: {
        scale: [baseScale, baseScale + scaleAmount, baseScale],
        opacity: [config.opacity, 1, config.opacity],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }
      },
      active: {
        scale: [baseScale, baseScale + scaleAmount, baseScale],
        opacity: [0.9, 1, 0.9],
        filter: ['brightness(1)', 'brightness(1.2)', 'brightness(1)'],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }
      },
      processing: {
        scale: [baseScale, baseScale + scaleAmount, baseScale + scaleAmount * 0.5, baseScale],
        opacity: [0.8, 1, 0.95, 0.8],
        filter: ['brightness(1)', 'brightness(1.3)', 'brightness(1.1)', 'brightness(1)'],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }
      },
      error: {
        scale: [baseScale, baseScale + scaleAmount, baseScale],
        opacity: [0.7, 1, 0.7],
        filter: ['brightness(1) hue-rotate(0deg)', 'brightness(1.4) hue-rotate(10deg)', 'brightness(1) hue-rotate(0deg)'],
        transition: {
          duration: config.duration,
          repeat: Infinity,
          ease: "easeInOut"
        }
      }
    }
  }, [config, intensity])
  
  useEffect(() => {
    controls.start(state)
  }, [controls, state])
  
  return {
    controls,
    variants,
    motionProps: {
      animate: controls,
      variants
    }
  }
}

// Export a simplified version for components that just need the motion props
export const useBreathingMotion = (
  intensity: number = 0.5,
  state: BreathingState = 'idle'
) => {
  const { motionProps } = useBreathing(intensity, state)
  return motionProps
} 