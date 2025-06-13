import React, { createContext, useContext, useState, useEffect } from 'react'
import dawnConfig from '../config/dawn.config.json'

interface ConfigContextType {
  config: typeof dawnConfig
  updateConfig: (path: string, value: any) => void
  getModuleType: (typeName: string) => any
}

const ConfigContext = createContext<ConfigContextType | null>(null)

export const ConfigProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [config, setConfig] = useState(dawnConfig)
  
  useEffect(() => {
    // Initialize breathing groups from config
    Object.entries(config.modules.breathingGroups).forEach(([groupId, groupConfig]) => {
      console.log(`[DAWN] Initializing breathing group: ${groupId}`)
    })
  }, [])
  
  const updateConfig = (path: string, value: any) => {
    // Deep update config by path (e.g., "system.consciousness.enabled")
    setConfig(prev => {
      const newConfig = { ...prev }
      const keys = path.split('.')
      let current = newConfig
      
      for (let i = 0; i < keys.length - 1; i++) {
        current = current[keys[i]]
      }
      
      current[keys[keys.length - 1]] = value
      return newConfig
    })
  }
  
  const getModuleType = (typeName: string) => {
    return config.modules.types[typeName]
  }
  
  return (
    <ConfigContext.Provider value={{ config, updateConfig, getModuleType }}>
      {children}
    </ConfigContext.Provider>
  )
}

export const useDAWNConfig = () => {
  const context = useContext(ConfigContext)
  if (!context) {
    throw new Error('useDAWNConfig must be used within ConfigProvider')
  }
  return context
}