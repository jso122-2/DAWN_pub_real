import { useAnimation } from 'framer-motion'
import { useEffect, useMemo } from 'react'

export type BreathingState = 'idle' | 'active' | 'processing' | 'error'

// Store for breathing groups - modules that breathe in sync
const breathingGroups = new Map<string, {
  modules: Set<string>
  state: BreathingState
  intensity: number
}>()

export const useBreathing = (
  intensity: number = 0.5,
  state: BreathingState = 'idle'
) => {
  const controls = useAnimation()
  
  const variants = useMemo(() => ({
    idle: {
      scale: [1, 1.02, 1],
      opacity: [0.95, 1, 0.95],
      transition: {
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    active: {
      scale: [1, 1.03, 1],
      opacity: [0.9, 1, 0.9],
      filter: ['brightness(1)', 'brightness(1.2)', 'brightness(1)'],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    processing: {
      scale: [1, 1.04, 1.02, 1],
      opacity: [0.8, 1, 0.95, 0.8],
      filter: ['brightness(1)', 'brightness(1.3)', 'brightness(1.1)', 'brightness(1)'],
      transition: {
        duration: 1.5,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    error: {
      scale: [1, 1.05, 1],
      opacity: [0.7, 1, 0.7],
      filter: ['brightness(1)', 'brightness(1.4)', 'brightness(1)'],
      transition: {
        duration: 1,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }), [intensity])
  
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

// Breathing group management
export const cleanupBreathingGroup = (groupId: string) => {
  console.log(`[DAWN] Cleaning up breathing group: ${groupId}`)
  breathingGroups.delete(groupId)
}

export const createBreathingGroup = (groupId: string, moduleIds: string[], state: BreathingState = 'idle') => {
  breathingGroups.set(groupId, {
    modules: new Set(moduleIds),
    state,
    intensity: 0.5
  })
}

export const addToBreathingGroup = (groupId: string, moduleId: string) => {
  const group = breathingGroups.get(groupId)
  if (group) {
    group.modules.add(moduleId)
  }
}

export const useBreathingSync = (moduleId: string, groupId: string) => {
  const group = breathingGroups.get(groupId)
  const state = group?.state || 'idle'
  const intensity = group?.intensity || 0.5
  
  return useBreathing(intensity, state)
}

export const syncBreathingGroup = (groupId: string) => {
  // Stub implementation
  console.log(`Syncing breathing group: ${groupId}`)
}
