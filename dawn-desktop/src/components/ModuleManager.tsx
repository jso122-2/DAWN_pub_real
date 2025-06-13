import { TestModule } from './modules/TestModule'
import { useLocation } from 'react-router-dom'

export function ModuleManager() {
  const location = useLocation()

  // Define which modules appear on which routes
  const moduleConfig: Record<string, string[]> = {
    '/': ['test-neural', 'system-monitor'],
    '/dashboard': ['neural-network', 'data-flow'],
    '/terminal': ['terminal-main']
  }

  const currentModules = moduleConfig[location.pathname] || []

  return (
    <>
      {currentModules.includes('test-neural') && (
        <TestModule moduleId="test-neural-main" />
      )}
      {/* Add more module conditions here as you implement more modules */}
    </>
  )
} 