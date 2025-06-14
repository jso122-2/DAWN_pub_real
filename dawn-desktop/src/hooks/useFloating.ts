// Add performance monitoring
const PERFORMANCE_MODE = (import.meta as any).env?.VITE_PERFORMANCE_MODE === 'true'

import { useEffect, useRef, useMemo, useState } from 'react'
import { useAnimation, useMotionValue } from 'framer-motion'
import { useAnimationFrame } from './useAnimationFrame'

export type FloatingPreset = 'gentle' | 'active' | 'orbital' | 'magnetic'

export interface UseFloatingOptions {
  preset?: FloatingPreset
  intensity?: number // 0-1, system activity level
  disabled?: boolean
  customConfig?: Partial<FloatingConfig>
}

interface FloatingConfig {
  amplitude: number
  speed: number
  pattern: 'lissajous' | 'orbital' | 'random' | 'magnetic'
}

const FLOATING_PRESETS: Record<FloatingPreset, FloatingConfig> = {
  gentle: {
    amplitude: 10,
    speed: 0.0005,
    pattern: 'lissajous'
  },
  active: {
    amplitude: 20,
    speed: 0.001,
    pattern: 'lissajous'
  },
  orbital: {
    amplitude: 5,
    speed: 0.0003,
    pattern: 'orbital'
  },
  magnetic: {
    amplitude: 15,
    speed: 0.0008,
    pattern: 'magnetic'
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
      base.amplitude = base.amplitude * (1 + intensity)
      base.speed = base.speed * (1 + intensity * 0.5)
    }
    return base
  }, [preset, intensity, customConfig])

  useAnimationFrame((time: number) => {
    if (disabled) return
    const t = time * 0.001 * config.speed
    
    let x = 0, y = 0, rotate = 0
    
    switch (config.pattern) {
      case 'lissajous':
        x = config.amplitude * Math.sin(t * 1.3)
        y = config.amplitude * Math.sin(t * 2.1)
        rotate = Math.sin(t * 0.5) * 5
        break
        
      case 'orbital':
        x = config.amplitude * Math.cos(t)
        y = config.amplitude * Math.sin(t)
        rotate = t * 10 % 360
        break
        
      case 'random':
        x = config.amplitude * (Math.sin(t * 1.3) + Math.sin(t * 2.7) * 0.5)
        y = config.amplitude * (Math.sin(t * 2.1) + Math.sin(t * 3.2) * 0.5)
        rotate = Math.sin(t * 0.7) * 10
        break
        
      case 'magnetic':
        x = config.amplitude * Math.sin(t) * Math.cos(t * 0.7)
        y = config.amplitude * Math.cos(t) * Math.sin(t * 0.7)
        rotate = Math.sin(t * 0.3) * 3
        break
    }
    
    x.set(x)
    y.set(y)
    rotate.set(rotate)
    controls.start({
      x: x,
      y: y,
      rotate: rotate,
      transition: { duration: 0.1, ease: 'linear' }
    })
  })

  // Variants for framer-motion
  const variants = useMemo(() => ({
    float: {
      x: [0, config.amplitude, 0, -config.amplitude, 0],
      y: [0, config.amplitude, 0, -config.amplitude, 0],
      rotate: [0, 5, 0, -5, 0],
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