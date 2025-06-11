import { useState, useEffect } from 'react'
import { 
  fetchMetrics, 
  checkBackendHealth, 
  connectWebSocket, 
  onMetricsUpdate, 
  onConnectionChange, 
  onError,
  getConnectionStatus 
} from './lib/api.js'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'
import TickControl from './components/TickControl.jsx'
import ConfigPanel from './components/ConfigPanel.jsx'
import TickIndicator from './components/TickIndicator.jsx'
import './App.css'

function App() {
  console.log('🧠 DAWN Neural Monitor Loading...')
  
  const [metrics, setMetrics] = useState({
    scup: 0.000,
    entropy: 0.000,
    heat: 0.000,
    mood: "Initializing...",
    tick_count: 0
  })
  
  const [isConnected, setIsConnected] = useState(false)
  const [connectionMode, setConnectionMode] = useState('connecting') // 'connecting', 'connected', 'tauri', 'mock', 'error'
  const [error, setError] = useState(null)
  
  // Tick engine controls
  const [tickStatus, setTickStatus] = useState({
    isRunning: false,
    isPaused: false,
    tickCount: 0,
    intervalMs: 500
  })
  
  // Configuration panel state
  const [showConfigPanel, setShowConfigPanel] = useState(false)
  
  // Backend connection with fallback to mock data
  useEffect(() => {
    console.log('🎯 Initializing DAWN backend connection...')
    
    let mockInterval = null
    let connectionCheckInterval = null
    
    const initializeConnection = async () => {
      try {
        setConnectionMode('connecting')
        setError(null)
        
        // Try Tauri connection first
        try {
          console.log('🦀 Attempting Tauri connection...')
          
          // Set up Tauri event listener
          const unlistenTauri = await listen('metrics-update', (event) => {
            console.log('📨 Tauri metrics received:', event.payload)
            const metricsData = event.payload
            
            setMetrics({
              scup: metricsData.scup || 0,
              entropy: metricsData.entropy || 0,
              heat: metricsData.heat || 0,
              mood: metricsData.mood || 'Unknown',
              tick_count: metricsData.tick_count || 0
            })
            
            // Update tick status
            setTickStatus(prev => ({
              ...prev,
              tickCount: metricsData.tick_count || 0,
              isRunning: metricsData.is_running !== undefined ? metricsData.is_running : prev.isRunning,
              isPaused: metricsData.is_paused !== undefined ? metricsData.is_paused : prev.isPaused
            }))
            
            setIsConnected(true)
            setConnectionMode('tauri')
            setError(null)
          })
          
          // Try to get initial metrics via Tauri
          const initialTauriMetrics = await invoke('get_current_metrics')
          setMetrics({
            scup: initialTauriMetrics.scup || 0,
            entropy: initialTauriMetrics.entropy || 0,
            heat: initialTauriMetrics.heat || 0,
            mood: initialTauriMetrics.mood || 'Unknown',
            tick_count: initialTauriMetrics.tick_count || 0
          })
          setIsConnected(true)
          setConnectionMode('tauri')
          console.log('✅ Tauri connection successful!')
          
          return [unlistenTauri]
          
        } catch (tauriError) {
          console.log('⚠️ Tauri connection failed, falling back to WebSocket:', tauriError)
          
          // Fallback to WebSocket connection
          // Check backend health first
          console.log('🏥 Checking backend health...')
          await checkBackendHealth()
          console.log('✅ Backend is healthy')
          
          // Connect to WebSocket for real-time data
          console.log('🔌 Connecting to WebSocket...')
          await connectWebSocket()
        }
        
        // Set up event listeners for real-time updates
        const unsubscribeMetrics = onMetricsUpdate((data) => {
          console.log('📨 Real-time metrics received:', data)
          
          // Handle both direct metrics and tick update format
          const metricsData = data.metrics || data
          
          setMetrics({
            scup: metricsData.scup || 0,
            entropy: metricsData.entropy || 0,
            heat: metricsData.heat || 0,
            mood: metricsData.mood || 'Unknown',
            tick_count: metricsData.tick_count || 0
          })
          
          // Update tick status from WebSocket data
          setTickStatus(prev => ({
            ...prev,
            tickCount: metricsData.tick_count || 0,
            isRunning: data.controller_state ? data.controller_state === 'running' : prev.isRunning,
            isPaused: data.controller_state ? data.controller_state === 'paused' : prev.isPaused
          }))
          
          setIsConnected(true)
          setConnectionMode('connected')
          setError(null)
        })
        
        const unsubscribeConnection = onConnectionChange((connected) => {
          console.log('🔗 Connection status changed:', connected)
          setIsConnected(connected)
          if (!connected) {
            setConnectionMode('error')
            setError('WebSocket connection lost')
          }
        })
        
        const unsubscribeError = onError((errorMsg) => {
          console.error('❌ API Error:', errorMsg)
          setError(errorMsg)
          setConnectionMode('error')
        })
        
        // Fetch initial data
        try {
          const initialMetrics = await fetchMetrics()
          setMetrics({
            scup: initialMetrics.scup || 0,
            entropy: initialMetrics.entropy || 0,
            heat: initialMetrics.heat || 0,
            mood: initialMetrics.mood || 'Unknown',
            tick_count: initialMetrics.tick_count || 0
          })
          setIsConnected(true)
          setConnectionMode('connected')
          console.log('✅ Initial metrics loaded from backend')
        } catch (fetchError) {
          console.warn('⚠️ Failed to fetch initial metrics:', fetchError)
        }
        
        // Periodic connection health check
        connectionCheckInterval = setInterval(async () => {
          try {
            await checkBackendHealth()
            const status = getConnectionStatus()
            if (!status.websocket) {
              console.log('🔄 WebSocket disconnected, attempting reconnect...')
              await connectWebSocket()
            }
          } catch (healthError) {
            console.warn('⚠️ Health check failed:', healthError)
            setError('Backend connection lost')
            setConnectionMode('error')
          }
        }, 30000) // Check every 30 seconds
        
        return [unsubscribeMetrics, unsubscribeConnection, unsubscribeError]
        
      } catch (connectionError) {
        console.error('❌ Failed to connect to backend:', connectionError)
        setError(`Backend offline: ${connectionError.message}`)
        setConnectionMode('mock')
        
        // Fall back to beautiful mock data
        console.log('🎭 Falling back to mock data mode...')
        mockInterval = setInterval(() => {
          const time = Date.now() / 1000
          
          // Generate realistic neural metrics with smooth variations
          const newMetrics = {
            scup: Math.max(0.100, Math.min(0.900, 
              0.650 + 0.200 * Math.sin(time / 8) + (Math.random() - 0.5) * 0.080
            )),
            entropy: Math.max(0.050, Math.min(0.750, 
              0.400 + 0.150 * Math.cos(time / 12) + (Math.random() - 0.5) * 0.060
            )),
            heat: Math.max(0.100, Math.min(0.800, 
              0.350 + 0.180 * Math.sin(time / 15) + (Math.random() - 0.5) * 0.070
            )),
            mood: [
              'Focused', 'Analytical', 'Optimized', 'Processing', 
              'Reflective', 'Stable', 'Creative', 'Alert'
            ][Math.floor(Math.random() * 8)],
            tick_count: metrics.tick_count + 1
          }
          
          setMetrics(newMetrics)
          setIsConnected(false) // Mock mode shows as disconnected
          
          console.log(`🎭 Mock metrics updated - SCUP: ${newMetrics.scup.toFixed(3)}, Mood: ${newMetrics.mood}`)
        }, 500)
        
        return []
      }
    }
    
    initializeConnection().then((unsubscribeFunctions) => {
      // Store cleanup functions
      return () => {
        console.log('🧹 Cleaning up connections...')
        if (unsubscribeFunctions) {
          unsubscribeFunctions.forEach(unsubscribe => unsubscribe())
        }
        if (mockInterval) clearInterval(mockInterval)
        if (connectionCheckInterval) clearInterval(connectionCheckInterval)
      }
    })
    
    // Cleanup on unmount
    return () => {
      if (mockInterval) clearInterval(mockInterval)
      if (connectionCheckInterval) clearInterval(connectionCheckInterval)
    }
  }, []) // Empty dependency array - only run once on mount

  // Tick engine control handlers
  const handleStart = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('start_tick_engine')
        setTickStatus(prev => ({ ...prev, isRunning: true }))
        console.log('✅ Tick engine started via Tauri')
      } catch (err) {
        console.error('❌ Failed to start tick engine:', err)
        setError(`Failed to start tick engine: ${err}`)
      }
    }
  }

  const handleStop = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('stop_tick_engine')
        setTickStatus(prev => ({ ...prev, isRunning: false }))
        console.log('✅ Tick engine stopped via Tauri')
      } catch (err) {
        console.error('❌ Failed to stop tick engine:', err)
        setError(`Failed to stop tick engine: ${err}`)
      }
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <header className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 via-purple-500 to-cyan-400 bg-clip-text text-transparent">
              🧠 DAWN Neural Monitor
            </h1>
            <p className="text-gray-400 mt-2 text-lg">
              Deep Adaptive Wisdom Network - Real-time Cognitive Monitoring
            </p>
          </div>
          
          <div className="flex items-center space-x-6">
            {/* Tick Indicator */}
            <TickIndicator 
              tickCount={metrics.tick_count} 
              isRunning={tickStatus.isRunning} 
              isPaused={tickStatus.isPaused}
              intervalMs={tickStatus.intervalMs}
              className="flex-shrink-0"
            />
            
            {/* Config Panel Toggle Button */}
            <button
              onClick={() => setShowConfigPanel(!showConfigPanel)}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 transform hover:scale-105 ${
                showConfigPanel 
                  ? 'bg-purple-600 hover:bg-purple-700 text-white shadow-purple-500/20 shadow-lg' 
                  : 'bg-gray-700 hover:bg-gray-600 text-gray-300 border border-gray-600'
              }`}
            >
              <span className="flex items-center space-x-2">
                <span>⚙️</span>
                <span>{showConfigPanel ? 'Hide Config' : 'Configuration'}</span>
              </span>
            </button>
            
            {/* Connection Status Indicator */}
            <div className={`flex items-center space-x-3 px-6 py-3 rounded-xl border-2 transition-all duration-500 ${
              connectionMode === 'connected' ? 'bg-green-900/30 border-green-400/50 text-green-300 shadow-green-400/20 shadow-lg' :
              connectionMode === 'tauri' ? 'bg-cyan-900/30 border-cyan-400/50 text-cyan-300 shadow-cyan-400/20 shadow-lg' :
              connectionMode === 'connecting' ? 'bg-yellow-900/30 border-yellow-400/50 text-yellow-300 shadow-yellow-400/20 shadow-lg' :
              connectionMode === 'mock' ? 'bg-blue-900/30 border-blue-400/50 text-blue-300 shadow-blue-400/20 shadow-lg' :
              'bg-red-900/30 border-red-400/50 text-red-300'
            }`}>
              <div className={`w-4 h-4 rounded-full transition-all duration-300 ${
                connectionMode === 'connected' ? 'bg-green-400 animate-pulse shadow-green-400/50 shadow-lg' :
                connectionMode === 'tauri' ? 'bg-cyan-400 animate-pulse shadow-cyan-400/50 shadow-lg' :
                connectionMode === 'connecting' ? 'bg-yellow-400 animate-ping' :
                connectionMode === 'mock' ? 'bg-blue-400 animate-bounce' :
                'bg-red-400'
              }`} />
              <span className="font-semibold text-lg">
                {connectionMode === 'connected' ? '🟢 Backend Connected' :
                 connectionMode === 'tauri' ? '🦀 Tauri Connected' :
                 connectionMode === 'connecting' ? '🟡 Connecting...' :
                 connectionMode === 'mock' ? '🔵 Demo Mode' :
                 '🔴 Backend Offline'}
              </span>
              {connectionMode === 'mock' && (
                <span className="text-xs opacity-75 ml-2">(Live Simulation)</span>
              )}
              {connectionMode === 'tauri' && (
                <span className="text-xs opacity-75 ml-2">(Native Integration)</span>
              )}
            </div>
          </div>
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="mt-4 p-4 bg-red-900/30 border border-red-500/50 rounded-xl backdrop-blur-sm">
            <div className="flex items-center justify-between">
              <p className="text-red-300 flex items-center">
                <span className="mr-2">⚠️</span>
                {error}
              </p>
              {connectionMode === 'error' && (
                <button 
                  onClick={() => window.location.reload()}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
                >
                  🔄 Reconnect
                </button>
              )}
            </div>
            {connectionMode === 'mock' && (
              <p className="text-yellow-300 text-sm mt-2">
                💡 Start the Python backend: <code className="bg-gray-800 px-2 py-1 rounded">python main.py</code>
              </p>
            )}
                     </div>
         )}
       </header>

      {/* Comprehensive Tick Engine Control Panel */}
      <div className="max-w-7xl mx-auto mb-8">
        <TickControl 
          onTimingChange={(newInterval) => {
            console.log(`⏱️ Tick timing changed to ${newInterval}ms`)
            setTickStatus(prev => ({ ...prev, intervalMs: newInterval }))
          }}
        />
      </div>

      {/* Advanced Configuration Panel */}
      {showConfigPanel && (
        <div className="max-w-7xl mx-auto mb-8 transform transition-all duration-500 ease-out animate-in slide-in-from-top fade-in">
          <ConfigPanel currentMetrics={metrics} />
        </div>
      )}
      
      {/* Main Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 max-w-7xl mx-auto mb-8">
        <MetricCard
          title="SCUP"
          value={metrics.scup}
          colorScheme="blue"
          icon="🧠"
          subtitle="Cognitive Unity Potential"
          description="Neural coherence measurement"
        />
        
        <MetricCard
          title="Entropy"
          value={metrics.entropy}
          colorScheme="green"
          icon="🌀"
          subtitle="System Disorder"
          description="Information complexity index"
        />
        
        <MetricCard
          title="Heat"
          value={metrics.heat}
          colorScheme="orange"
          icon="🔥"
          subtitle="Processing Intensity"
          description="Neural activity temperature"
        />
        
        <MetricCard
          title="Mood"
          value={metrics.mood}
          colorScheme="purple"
          icon="💭"
          subtitle="System State"
          description="Current cognitive mode"
        />
      </div>

      {/* System Telemetry */}
      <div className="max-w-7xl mx-auto">
        <div className="bg-gray-800/60 backdrop-blur-sm rounded-2xl p-8 border border-gray-700/50 shadow-2xl">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-2xl font-bold text-gray-200 flex items-center">
              <span className="mr-3">📊</span>
              Neural Telemetry Dashboard
            </h3>
            <div className="text-gray-400 font-mono text-lg">
              Tick #{metrics.tick_count.toLocaleString()}
            </div>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <TelemetryItem 
              label="SCUP Level" 
              value={`${(metrics.scup * 100).toFixed(1)}%`}
              color="text-blue-400"
            />
            <TelemetryItem 
              label="Entropy Rate" 
              value={`${(metrics.entropy * 100).toFixed(1)}%`}
              color="text-green-400"
            />
            <TelemetryItem 
              label="Heat Index" 
              value={`${(metrics.heat * 100).toFixed(1)}%`}
              color="text-orange-400"
            />
            <TelemetryItem 
              label="Current Mood" 
              value={metrics.mood}
              color="text-purple-400"
            />
          </div>
        </div>
      </div>
      
      {/* Status Indicator */}
      <div className="fixed bottom-6 right-6 bg-gray-800/90 backdrop-blur-sm rounded-lg px-4 py-3 border border-gray-600 shadow-lg">
        <div className="flex items-center space-x-2 text-sm">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-gray-300">React App Active</span>
        </div>
      </div>
    </div>
  )
}

function MetricCard({ title, value, colorScheme, icon, subtitle, description }) {
  const [isUpdating, setIsUpdating] = useState(false)
  const [previousValue, setPreviousValue] = useState(value)
  
  const colorSchemes = {
    blue: {
      primary: 'text-blue-400',
      secondary: 'text-blue-300',
      bg: 'bg-blue-400',
      border: 'border-blue-400/30',
      shadow: 'shadow-blue-400/20',
      glow: 'shadow-blue-400/30'
    },
    green: {
      primary: 'text-green-400',
      secondary: 'text-green-300',
      bg: 'bg-green-400',
      border: 'border-green-400/30',
      shadow: 'shadow-green-400/20',
      glow: 'shadow-green-400/30'
    },
    orange: {
      primary: 'text-orange-400',
      secondary: 'text-orange-300',
      bg: 'bg-orange-400',
      border: 'border-orange-400/30',
      shadow: 'shadow-orange-400/20',
      glow: 'shadow-orange-400/30'
    },
    purple: {
      primary: 'text-purple-400',
      secondary: 'text-purple-300',
      bg: 'bg-purple-400',
      border: 'border-purple-400/30',
      shadow: 'shadow-purple-400/20',
      glow: 'shadow-purple-400/30'
    }
  }
  
  const colors = colorSchemes[colorScheme]
  
  useEffect(() => {
    if (value !== previousValue) {
      setIsUpdating(true)
      setPreviousValue(value)
      
      const timer = setTimeout(() => setIsUpdating(false), 400)
      return () => clearTimeout(timer)
    }
  }, [value, previousValue])
  
  const formatValue = (val) => {
    return typeof val === 'number' ? val.toFixed(3) : String(val)
  }
  
  const getProgressWidth = () => {
    return typeof value === 'number' ? Math.min(100, Math.max(0, value * 100)) : 0
  }

  return (
    <div className={`
      bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border transition-all duration-500 ease-out transform
      hover:bg-gray-700/80 hover:scale-105 hover:-translate-y-1
      ${isUpdating ? `animate-pulse ring-2 ring-opacity-60 ${colors.border} ${colors.glow} shadow-2xl` : colors.border}
      ${colors.shadow} shadow-lg
    `}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{icon}</span>
          <div>
            <h3 className="text-sm text-gray-400 uppercase tracking-wider font-bold">
              {title}
            </h3>
            <p className="text-xs text-gray-500">{subtitle}</p>
          </div>
        </div>
        <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
          isUpdating ? `${colors.bg} animate-ping` : `${colors.bg} opacity-60`
        }`} />
      </div>
      
      <div className="relative mb-4">
        <p className={`
          text-4xl font-bold transition-all duration-500 ease-out transform
          ${isUpdating ? 'scale-110 brightness-125' : 'scale-100'}
          ${colors.primary}
        `}>
          {formatValue(value)}
        </p>
        
        {/* Floating update indicator */}
        {isUpdating && (
          <div className={`
            absolute -top-2 -right-2 w-3 h-3 rounded-full ${colors.bg}
            animate-bounce opacity-80
          `} />
        )}
      </div>
      
      {/* Progress bar for numeric values */}
      {typeof value === 'number' && (
        <div className="mb-3 h-2 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className={`
              h-full ${colors.bg} transition-all duration-700 ease-out transform origin-left
              ${isUpdating ? 'brightness-125 scale-y-125' : 'brightness-100 scale-y-100'}
            `}
            style={{ 
              width: `${getProgressWidth()}%`,
              filter: 'drop-shadow(0 0 4px currentColor)'
            }}
          />
        </div>
      )}
      
      {/* Description */}
      <p className="text-xs text-gray-500 italic">
        {description}
      </p>
    </div>
  )
}

function TelemetryItem({ label, value, color }) {
  return (
    <div className="text-center p-4 bg-gray-900/50 rounded-xl border border-gray-700/50">
      <div className="text-gray-400 text-sm mb-2">{label}</div>
      <div className={`${color} font-bold text-xl font-mono`}>{value}</div>
    </div>
  )
}

export default App 