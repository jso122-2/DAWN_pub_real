import { ConsciousModule } from './ConsciousModule'
import { cn } from '../../lib/utils'
import { ReactNode } from 'react'

interface BaseModuleProps {
  id: string
  title: string
  children: ReactNode
  isActive?: boolean
  isCritical?: boolean
  [key: string]: any
}

export function BaseModule({ 
  id, 
  title, 
  children, 
  isActive = false,
  isCritical = false,
  ...props 
}: BaseModuleProps) {
  return (
    <ConsciousModule
      moduleId={id}
      breathingPreset={isCritical ? 'critical' : 'calm'}
      floatingPreset="gentle"
      syncGroup="main-modules"
      isActive={isActive}
      isCritical={isCritical}
      entropy={0.3} // Base entropy level
    >
      <div className={cn(
        "glass-base rounded-2xl p-organ",
        isActive && "glass-active",
        isCritical && "glass-critical"
      )}>
        <div className="mb-molecule">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
        {children}
      </div>
    </ConsciousModule>
  )
} 