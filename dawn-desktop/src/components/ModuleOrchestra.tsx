import React, { useEffect, useState } from 'react'
import { getModulePositions } from '../hooks/useFloatingUtils'
import { cleanupBreathingGroup } from '../hooks/useBreathing'
import { safePassPropsToChildren } from '../utils/propUtils'
import { usePropDebugger } from '../utils/propDebugger'

interface ModuleOrchestraProps {
  children: React.ReactElement[] | React.ReactElement
}

export function ModuleOrchestra({ children }: ModuleOrchestraProps) {
  const [globalEntropy, setGlobalEntropy] = useState(0)
  
  // Debug prop passing to identify issues
  usePropDebugger({ children }, {
    componentName: 'ModuleOrchestra',
    logLevel: 'warn',
    highlightDOMIssues: true
  })

  // Monitor system activity and adjust global entropy
  useEffect(() => {
    const interval = setInterval(() => {
      const positions = getModulePositions()
      
      // Calculate entropy based on module movement
      let totalVelocity = 0
      positions.forEach(module => {
        totalVelocity += Math.sqrt(module.vx ** 2 + module.vy ** 2)
      })
      
      const avgVelocity = totalVelocity / Math.max(positions.size, 1)
      setGlobalEntropy(Math.min(avgVelocity / 10, 1))
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupBreathingGroup('main-modules')
      cleanupBreathingGroup('neural-network')
      cleanupBreathingGroup('quantum-systems')
    }
  }, [])

  return (
    <div className="relative w-full h-full overflow-hidden">
      {/* Pass entropy to all children safely */}
      {safePassPropsToChildren(children, { globalEntropy })}
    </div>
  )
} 