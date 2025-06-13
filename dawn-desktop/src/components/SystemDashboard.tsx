import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import CognitiveLoadRadar from './CognitiveLoadRadar'
import EventStream from './EventStream'
import MetricsPanel from './MetricsPanel'
import { useCosmicStore } from '../store/cosmic.store'
import { TestModule } from './modules/TestModule'

// Event type for EventStream
interface Event {
  id: string;
  type: string;
  timestamp: Date;
  description: string;
  source: string;
  details?: string;
  causedBy?: string;
  metrics?: Record<string, number>;
  impact?: { level: string; description?: string };
}

export function SystemDashboard() {
  const { entropy, neuralActivity, quantumCoherence, systemLoad } = useCosmicStore()
  
  // Generate mock events for EventStream
  const [events, setEvents] = useState<Event[]>([])
  const [metrics, setMetrics] = useState({
    entropy: entropy,
    heat: systemLoad,
    scup: neuralActivity,
    tickRate: quantumCoherence
  })
  
  const [history, setHistory] = useState({
    entropy: [] as number[],
    heat: [] as number[],
    scup: [] as number[],
    tickRate: [] as number[]
  })

  // Update metrics when store changes
  useEffect(() => {
    setMetrics({
      entropy: entropy,
      heat: systemLoad,
      scup: neuralActivity,
      tickRate: quantumCoherence
    })
    
    // Update history
    setHistory(prev => ({
      entropy: [...prev.entropy.slice(-50), entropy],
      heat: [...prev.heat.slice(-50), systemLoad],
      scup: [...prev.scup.slice(-50), neuralActivity],
      tickRate: [...prev.tickRate.slice(-50), quantumCoherence]
    }))
  }, [entropy, systemLoad, neuralActivity, quantumCoherence])

  return (
    <div className="relative w-full h-screen">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="w-full h-full p-8 overflow-y-auto"
      >
        <div className="max-w-7xl mx-auto space-y-6">
          <h2 className="text-3xl font-bold text-center text-purple-300 mb-8">System Monitor</h2>
          
          {/* Cognitive Load Radar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <CognitiveLoadRadar metrics={{
              scup: metrics.scup,
              entropy: metrics.entropy,
              heat: metrics.heat,
              mood: 'stable', // You can wire this to a real value if available
              focus: 0.7,     // You can wire this to a real value if available
              stress: 0.3     // You can wire this to a real value if available
            }} />
          </motion.div>
          
          {/* Metrics Panel */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <MetricsPanel 
              metrics={metrics}
              history={history}
              isConnected={true}
              lastUpdate={Date.now()}
            />
          </motion.div>
          
          {/* Event Stream */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <EventStream 
              events={events}
              onEventSelect={(event) => console.log('Selected event:', event)}
            />
          </motion.div>
        </div>
      </motion.div>
      {/* Floating TestModule */}
      <TestModule 
        moduleId="dashboard-neural-1"
        onNodeActivated={(nodeId, value) => {
          // Handle node activation
        }}
      />
    </div>
  )
}

export default SystemDashboard 