import React, { useEffect } from 'react'
import { cleanupBreathingGroup } from '../hooks/useBreathing'

interface ModuleOrchestraProps {
  children: React.ReactElement[] | React.ReactElement
}

export function ModuleOrchestra({ children }: ModuleOrchestraProps) {
  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupBreathingGroup('main-modules')
      cleanupBreathingGroup('neural-network')
      cleanupBreathingGroup('consciousness-systems')
    }
  }, [])

  return (
    <div className="relative w-full h-full overflow-hidden">
      {/* Render children as-is without passing additional props */}
      {/* The children already receive necessary props from their parent components */}
      {children}
    </div>
  )
} 