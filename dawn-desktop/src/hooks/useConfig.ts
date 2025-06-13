import { useState, useEffect } from 'react'
import systemConfig from '../config/system.config.json'
import modulesConfig from '../config/modules.config.json'

export interface DAWNConfig {
  system: typeof systemConfig
  modules: typeof modulesConfig
}

export const useConfig = () => {
  const [config, setConfig] = useState<DAWNConfig>({
    system: systemConfig,
    modules: modulesConfig
  })
  
  const [isLoading, setIsLoading] = useState(true)
  
  useEffect(() => {
    // In the future, this could load from a backend or allow runtime updates
    setIsLoading(false)
  }, [])
  
  const updateSystemConfig = (updates: Partial<typeof systemConfig>) => {
    setConfig(prev => ({
      ...prev,
      system: { ...prev.system, ...updates }
    }))
  }
  
  const getModuleConfig = (moduleType: keyof typeof modulesConfig.moduleTypes) => {
    return config.modules.moduleTypes[moduleType]
  }
  
  return {
    config,
    isLoading,
    updateSystemConfig,
    getModuleConfig
  }
}