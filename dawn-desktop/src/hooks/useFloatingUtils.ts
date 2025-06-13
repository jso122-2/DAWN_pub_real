import { useCallback } from 'react'

interface ModulePosition {
  x: number
  y: number
  vx: number
  vy: number
  element?: HTMLElement
}

// Global registry for module positions (for magnetic repulsion)
const moduleRegistry = new Map<string, ModulePosition>()
const orbitalGroups = new Map<string, { center: { x: number; y: number }; modules: string[] }>()

// Utility hook to create orbital group center
export function useOrbitalCenter(groupId: string) {
  const setCenter = useCallback((x: number, y: number) => {
    const group = orbitalGroups.get(groupId) || { center: { x, y }, modules: [] }
    group.center = { x, y }
    orbitalGroups.set(groupId, group)
  }, [groupId])

  return { setCenter }
}

// Get all module positions for visualization
export function getModulePositions(): Map<string, ModulePosition> {
  return new Map(moduleRegistry)
}

// Force recalculation for specific module
export function applyImpulse(moduleId: string, impulseX: number, impulseY: number) {
  const module = moduleRegistry.get(moduleId)
  if (module) {
    module.vx += impulseX
    module.vy += impulseY
  }
} 