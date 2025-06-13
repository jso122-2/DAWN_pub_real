import React from 'react'
import { useConfig } from '../hooks/useConfig'

// Define a local ModuleConfig type matching the config
export interface ModuleConfig {
  id: string
  name: string
  category: string
  position: { x: number; y: number }
  size: { width: number; height: number }
  glowIntensity: number
  state?: 'active' | 'idle' | 'processing' | 'error'
}

// Dynamic imports for module components (must have default export)
const moduleComponents: Record<string, React.LazyExoticComponent<React.ComponentType<any>>> = {
  NeuralProcessor: React.lazy(() => import('../components/modules/NeuralProcessor').then(m => ({ default: m.default }))),
  QuantumCore: React.lazy(() => import('../components/modules/QuantumCore').then(m => ({ default: m.default }))),
  SystemMonitor: React.lazy(() => import('../components/modules/SystemMonitor').then(m => ({ default: m.default })))
}

export const createModuleFromConfig = (
  moduleType: keyof typeof import('../config/modules.config.json').moduleTypes,
  position: { x: number; y: number }
): ModuleConfig | null => {
  const { getModuleConfig } = useConfig()
  const config = getModuleConfig(moduleType)
  
  if (!config) return null
  
  return {
    id: `${config.id}-${Date.now()}`,
    name: config.name,
    category: config.category,
    position,
    size: config.defaultSize,
    glowIntensity: config.behavior.breathingIntensity,
    state: 'idle'
  }
}

export const ModuleFactory: React.FC<{ config: ModuleConfig }> = ({ config }) => {
  const { getModuleConfig } = useConfig()
  // Use config.id as the type key for lookup
  const moduleConfig = getModuleConfig(config.id.split('-')[0] as keyof typeof import('../config/modules.config.json').moduleTypes)

  if (!moduleConfig || !moduleConfig.component) {
    return <div>Unknown module type</div>
  }

  const Component = moduleComponents[moduleConfig.component]

  if (!Component) {
    return <div>Component not found: {moduleConfig.component}</div>
  }

  return (
    <React.Suspense fallback={<div>Loading consciousness...</div>}>
      <Component config={config} />
    </React.Suspense>
  )
}