import { useState, useEffect } from 'react'
import { get, subscribe, DawnState } from '../hooks/useTickState'

/**
 * Example component showing how to use the shared tick state hook
 * This pattern can be used for TickMonitorPanel, DriftGraphPanel, etc.
 */
export function ExampleTickPanel() {
  const [tickData, setTickData] = useState<DawnState | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    // Get initial state if available
    const initialState = get()
    if (initialState) {
      setTickData(initialState)
      setIsConnected(true)
    }

    // Subscribe to live updates
    const unsubscribe = subscribe((newState: DawnState) => {
      setTickData(newState)
      setIsConnected(true)
    })

    // Cleanup subscription on unmount
    return () => {
      unsubscribe()
    }
  }, [])

  if (!isConnected || !tickData) {
    return (
      <div className="tick-panel disconnected">
        <h3>🔄 DAWN Tick Monitor</h3>
        <p>Waiting for consciousness data...</p>
      </div>
    )
  }

  return (
    <div className="tick-panel connected">
      <h3>🧠 DAWN Consciousness Monitor</h3>
      
      <div className="metrics-grid">
        <div className="metric">
          <label>Tick #</label>
          <span className="value">{tickData.tick_number}</span>
        </div>
        
        <div className="metric">
          <label>Mood</label>
          <span className="value mood">{tickData.mood}</span>
        </div>
        
        <div className="metric">
          <label>Entropy</label>
          <span className="value entropy">
            {(tickData.entropy * 100).toFixed(1)}%
          </span>
        </div>
        
        <div className="metric">
          <label>SCUP</label>
          <span className="value scup">{tickData.scup.toFixed(1)}</span>
        </div>
      </div>
      
      <div className="status-indicator">
        <span className="dot active"></span>
        Live Feed Active
      </div>
    </div>
  )
}

export default ExampleTickPanel 