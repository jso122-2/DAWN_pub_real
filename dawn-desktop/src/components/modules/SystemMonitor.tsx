import { ConsciousModule } from './ConsciousModule'
import { useState, useEffect } from 'react'
import { cn } from '../../lib/utils'

interface SystemMonitorProps {
  metrics: {
    cpu: number
    memory: number
  }
}

export function SystemMonitor({ metrics }: SystemMonitorProps) {
  const [entropy, setEntropy] = useState(0)
  const [isCritical, setIsCritical] = useState(false)

  useEffect(() => {
    // Calculate system entropy from metrics
    const cpuLoad = metrics.cpu / 100
    const memoryPressure = metrics.memory / 100
    const newEntropy = (cpuLoad + memoryPressure) / 2
    
    setEntropy(newEntropy)
    setIsCritical(newEntropy > 0.8)
  }, [metrics])

  return (
    <ConsciousModule
      moduleId="system-monitor"
      breathingPreset={isCritical ? 'heartbeat' : 'calm'}
      floatingPreset="magnetic"
      entropy={entropy}
      isCritical={isCritical}
    >
      <div className={cn(
        "rounded-2xl p-organ transition-all",
        isCritical ? "glass-critical" : "glass-base"
      )}>
        <h3 className="text-lg font-bold mb-cell">System Status</h3>
        <div className="space-y-molecule">
          <div>CPU: {metrics.cpu}%</div>
          <div>Memory: {metrics.memory}%</div>
          <div>Entropy: {(entropy * 100).toFixed(1)}%</div>
        </div>
      </div>
    </ConsciousModule>
  )
} 