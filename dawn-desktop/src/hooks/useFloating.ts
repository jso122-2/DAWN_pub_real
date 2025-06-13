// Add performance monitoring
const PERFORMANCE_MODE = (import.meta as any).env?.VITE_PERFORMANCE_MODE === 'true'

import { useEffect, useRef, useMemo } from 'react'
import { useAnimation, useMotionValue } from 'framer-motion'

export type FloatingPreset = 'gentle' | 'active' | 'orbital' | 'magnetic'

export interface UseFloatingOptions {
  preset?: FloatingPreset
  intensity?: number // 0-1, system activity level
  disabled?: boolean
  customConfig?: Partial<FloatingConfig>
}

interface FloatingConfig {
  amplitude: { x: number; y: number }
  frequency: number
  rotationAmount: number
  magneticStrength: number
  orbitalRadius: number
  mouseInfluence: number
  dampening: number
}

const FLOATING_PRESETS: Record<FloatingPreset, FloatingConfig> = {
  gentle: {
    amplitude: { x: 10, y: 15 },
    frequency: 0.0005,
    rotationAmount: 2,
    magneticStrength: 50,
    orbitalRadius: 0,
    mouseInfluence: 0.1,
    dampening: 0.95
  },
  active: {
    amplitude: { x: 20, y: 25 },
    frequency: 0.001,
    rotationAmount: 5,
    magneticStrength: 80,
    orbitalRadius: 0,
    mouseInfluence: 0.2,
    dampening: 0.9
  },
  orbital: {
    amplitude: { x: 5, y: 5 },
    frequency: 0.0003,
    rotationAmount: 360,
    magneticStrength: 30,
    orbitalRadius: 150,
    mouseInfluence: 0.05,
    dampening: 0.98
  },
  magnetic: {
    amplitude: { x: 15, y: 20 },
    frequency: 0.0008,
    rotationAmount: 3,
    magneticStrength: 120,
    orbitalRadius: 0,
    mouseInfluence: 0.3,
    dampening: 0.85
  }
}

/**
 * useFloating - Framer Motion floating animation hook
 * @param options UseFloatingOptions
 * @returns { controls, x, y, rotate, variants }
 */
export function useFloating(options: UseFloatingOptions = {}) {
  const {
    preset = 'gentle',
    intensity = 0,
    disabled = false,
    customConfig
  } = options

  const controls = useAnimation()
  const x = useMotionValue(0)
  const y = useMotionValue(0)
  const rotate = useMotionValue(0)

  // Merge config
  const config = useMemo(() => {
    const base = { ...FLOATING_PRESETS[preset], ...customConfig }
    if (intensity > 0) {
      base.amplitude.x = base.amplitude.x * (1 + intensity)
      base.amplitude.y = base.amplitude.y * (1 + intensity)
      base.frequency = base.frequency * (1 + intensity * 0.5)
      base.rotationAmount = base.rotationAmount * (1 + intensity)
    }
    return base
  }, [preset, intensity, customConfig])

  // Animation loop
  useEffect(() => {
    if (disabled) return
    let running = true
    let start = performance.now()
    const animate = async () => {
      while (running) {
        const now = performance.now()
        const t = (now - start)
        const fx = Math.sin(t * config.frequency) * config.amplitude.x
        const fy = Math.cos(t * config.frequency * 0.7) * config.amplitude.y
        const rot = Math.sin(t * config.frequency * 0.5) * config.rotationAmount
        x.set(fx)
        y.set(fy)
        rotate.set(rot)
        await controls.start({
          x: fx,
          y: fy,
          rotate: rot,
          transition: { duration: 0.1, ease: 'linear' }
        })
        await new Promise(r => setTimeout(r, 16))
      }
    }
    animate()
    return () => { running = false }
  }, [controls, config, disabled, x, y, rotate])

  // Variants for framer-motion
  const variants = useMemo(() => ({
    float: {
      x: [0, config.amplitude.x, 0, -config.amplitude.x, 0],
      y: [0, config.amplitude.y, 0, -config.amplitude.y, 0],
      rotate: [0, config.rotationAmount, 0, -config.rotationAmount, 0],
      transition: {
        duration: 8 / (1 + intensity),
        repeat: Infinity,
        ease: 'easeInOut'
      }
    }
  }), [config, intensity])

  return {
    controls,
    x,
    y,
    rotate,
    variants
  }
}

export type UseFloatingReturn = ReturnType<typeof useFloating> 