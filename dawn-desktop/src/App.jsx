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
import ChatInterface from './components/ChatInterface.jsx'
import './App.css'

function App() {
  console.log('🧠 DAWN Neural Monitor Loading...')
  
  // Simplified state management
  const [backendOnline, setBackendOnline] = useState(false)
  const [connectionError, setConnectionError] = useState(null)
  const [connectionMode, setConnectionMode] = useState('checking') // 'checking', 'tauri', 'websocket', 'offline'
  const [isLoading, setIsLoading] = useState(true)
  
  const [metrics, setMetrics] = useState({
    scup: 0.000,
    entropy: 0.000,
    heat: 0.000,
    mood: "Initializing...",
    tick_count: 0
  })
  
  // Tick engine controls
  const [tickStatus, setTickStatus] = useState({
    isRunning: false,
    isPaused: false,
    tickCount: 0,
    intervalMs: 500
  })
  
  // UI state
  const [showConfigPanel, setShowConfigPanel] = useState(false)
  const [showChat, setShowChat] = useState(false)
  const [lastUpdateTime, setLastUpdateTime] = useState(null)
  const [updateCount, setUpdateCount] = useState(0)

  // Health check function
  const checkBackend = async () => {
    try {
      // Try Tauri first (preferred method)
      try {
        const tauriHealth = await invoke('health_check')
        if (tauriHealth) {
          setBackendOnline(true)
          setConnectionError(null)
          setConnectionMode('tauri')
          return true
        }
      } catch (tauriError) {
        console.log('🦀 Tauri not available, trying direct HTTP...')
      }

      // Fallback to direct HTTP health check
      await checkBackendHealth()
      setBackendOnline(true)
      setConnectionError(null)
      setConnectionMode('websocket')
      return true
      
    } catch (error) {
      console.error('❌ Backend health check failed:', error)
      setBackendOnline(false)
      setConnectionError(error.message || 'Backend connection failed')
      setConnectionMode('offline')
      return false
    }
  }

  // Initialize connection and set up monitoring
  useEffect(() => {
    let healthCheckInterval = null
    let unsubscribeFunctions = []

    const initializeApp = async () => {
      setIsLoading(true)
      
      // Initial health check
      const isHealthy = await checkBackend()
      
      if (isHealthy) {
        try {
          if (connectionMode === 'tauri') {
            // Set up Tauri event listeners with enhanced tracking
            const unlistenMetrics = await listen('metrics-update', (event) => {
              console.log('📨 Tauri live metrics received:', event.payload)
              const data = event.payload
              
              // Update metrics with validation
              const newMetrics = {
                scup: typeof data.scup === 'number' ? data.scup : 0,
                entropy: typeof data.entropy === 'number' ? data.entropy : 0,
                heat: typeof data.heat === 'number' ? data.heat : 0,
                mood: data.mood || 'Unknown',
                tick_count: data.tick_count || 0
              }
              
              setMetrics(newMetrics)
              setLastUpdateTime(new Date().toLocaleTimeString())
              setUpdateCount(prev => prev + 1)
              
              // Log live data values for debugging
              console.log(`🔥 Live update #${updateCount + 1}: SCUP=${newMetrics.scup.toFixed(3)}, Entropy=${newMetrics.entropy.toFixed(3)}, Heat=${newMetrics.heat.toFixed(3)}, Mood=${newMetrics.mood}`)
              
              setTickStatus(prev => ({
                ...prev,
                tickCount: data.tick_count || 0,
                isRunning: data.is_running !== undefined ? data.is_running : prev.isRunning,
                isPaused: data.is_paused !== undefined ? data.is_paused : prev.isPaused
              }))
            })
            
            unsubscribeFunctions.push(unlistenMetrics)
            
            // Get initial metrics via Tauri
            try {
              const initialMetrics = await invoke('get_current_metrics')
              setMetrics({
                scup: initialMetrics.scup || 0,
                entropy: initialMetrics.entropy || 0,
                heat: initialMetrics.heat || 0,
                mood: initialMetrics.mood || 'Unknown',
                tick_count: initialMetrics.tick_count || 0
              })
            } catch (err) {
              console.warn('⚠️ Failed to get initial Tauri metrics:', err)
            }
            
          } else {
            // Set up WebSocket connection
            await connectWebSocket()
            
            const unsubscribeMetrics = onMetricsUpdate((data) => {
              console.log('📨 WebSocket live metrics received:', data)
              const metricsData = data.metrics || data
              
              // Update metrics with validation and tracking
              const newMetrics = {
                scup: typeof metricsData.scup === 'number' ? metricsData.scup : 0,
                entropy: typeof metricsData.entropy === 'number' ? metricsData.entropy : 0,
                heat: typeof metricsData.heat === 'number' ? metricsData.heat : 0,
                mood: metricsData.mood || 'Unknown',
                tick_count: metricsData.tick_count || 0
              }
              
              setMetrics(newMetrics)
              setLastUpdateTime(new Date().toLocaleTimeString())
              setUpdateCount(prev => prev + 1)
              
              // Log live data values for debugging
              console.log(`🌐 WS Live update #${updateCount + 1}: SCUP=${newMetrics.scup.toFixed(3)}, Entropy=${newMetrics.entropy.toFixed(3)}, Heat=${newMetrics.heat.toFixed(3)}, Mood=${newMetrics.mood}`)
              
              setTickStatus(prev => ({
                ...prev,
                tickCount: metricsData.tick_count || 0,
                isRunning: data.controller_state ? data.controller_state === 'running' : prev.isRunning,
                isPaused: data.controller_state ? data.controller_state === 'paused' : prev.isPaused
              }))
            })
            
            const unsubscribeConnection = onConnectionChange((connected) => {
              console.log('🔗 Connection status changed:', connected)
              if (!connected) {
                setBackendOnline(false)
                setConnectionError('WebSocket connection lost')
                setConnectionMode('offline')
              }
            })
            
            const unsubscribeError = onError((errorMsg) => {
              console.error('❌ API Error:', errorMsg)
              setConnectionError(errorMsg)
              setBackendOnline(false)
              setConnectionMode('offline')
            })
            
            unsubscribeFunctions.push(unsubscribeMetrics, unsubscribeConnection, unsubscribeError)
            
            // Get initial metrics via HTTP
            try {
              const initialMetrics = await fetchMetrics()
              setMetrics({
                scup: initialMetrics.scup || 0,
                entropy: initialMetrics.entropy || 0,
                heat: initialMetrics.heat || 0,
                mood: initialMetrics.mood || 'Unknown',
                tick_count: initialMetrics.tick_count || 0
              })
            } catch (err) {
              console.warn('⚠️ Failed to get initial HTTP metrics:', err)
            }
          }
          
        } catch (setupError) {
          console.error('❌ Failed to set up connection:', setupError)
          setConnectionError('Failed to establish real-time connection')
        }
      }
      
      setIsLoading(false)
    }

    // Start initialization
    initializeApp()

    // Set up periodic health checks (every 5 seconds)
    healthCheckInterval = setInterval(checkBackend, 5000)

    // Cleanup function
    return () => {
      console.log('🧹 Cleaning up connections...')
      if (healthCheckInterval) clearInterval(healthCheckInterval)
      unsubscribeFunctions.forEach(unsub => {
        try {
          if (typeof unsub === 'function') unsub()
        } catch (err) {
          console.warn('Error during cleanup:', err)
        }
      })
    }
  }, []) // Run once on mount

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <h2 className="text-2xl font-bold mb-2">🧠 DAWN Neural Monitor</h2>
          <p className="text-gray-400">Initializing connection...</p>
        </div>
      </div>
    )
  }

  // Backend offline state
  if (!backendOnline) {
    return (
      <div className="min-h-screen bg-gray-900 text-white p-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-red-900/50 border border-red-500 rounded-xl p-8 backdrop-blur-sm">
            <h2 className="text-3xl font-bold mb-4 flex items-center">
              <span className="mr-3">⚠️</span>
              Backend Offline
            </h2>
            
            <div className="mb-6">
              <p className="text-xl mb-2">Connection Status: <span className="text-red-400 font-bold">{connectionError}</span></p>
              <p className="text-gray-300">The DAWN Neural System backend is not responding.</p>
            </div>

            <div className="bg-gray-800/80 rounded-lg p-6 mb-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center">
                <span className="mr-2">⚡</span>
                Quick Fix Instructions
              </h3>
              
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mt-0.5">1</span>
                  <div>
                    <p className="font-medium">Start the Python backend:</p>
                    <code className="bg-gray-900 text-yellow-400 px-3 py-2 rounded block mt-1 font-mono">
                      cd interface && python main.py
                    </code>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mt-0.5">2</span>
                  <div>
                    <p className="font-medium">Or use the startup script:</p>
                    <code className="bg-gray-900 text-yellow-400 px-3 py-2 rounded block mt-1 font-mono">
                      python start_dawn_api.py
                    </code>
                  </div>
                </div>
                
                <div className="flex items-start space-x-3">
                  <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mt-0.5">3</span>
                  <div>
                    <p className="font-medium">Verify backend is running:</p>
                    <code className="bg-gray-900 text-yellow-400 px-3 py-2 rounded block mt-1 font-mono">
                      curl http://localhost:8000/health
                    </code>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex space-x-4">
              <button 
                onClick={() => window.location.reload()}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
              >
                <span>🔄</span>
                <span>Retry Connection</span>
              </button>
              
              <button 
                onClick={checkBackend}
                className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors duration-200 flex items-center space-x-2"
              >
                <span>🏥</span>
                <span>Health Check</span>
              </button>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-600">
              <p className="text-sm text-gray-400">
                <strong>Connection Mode:</strong> {connectionMode} | 
                <strong className="ml-2">Last Error:</strong> {connectionError}
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Test live data function
  const handleTestLiveData = async () => {
    if (connectionMode === 'tauri') {
      try {
        console.log('🧪 Testing live data with force update...')
        const result = await invoke('test_force_metrics_update')
        console.log('✅ Force update result:', result)
        
        // Show success feedback
        setConnectionError(null)
        const tempMessage = `Live data test successful: ${result}`
        setConnectionError(tempMessage)
        setTimeout(() => setConnectionError(null), 3000)
        
      } catch (err) {
        console.error('❌ Live data test failed:', err)
        setConnectionError(`Live data test failed: ${err}`)
      }
    }
  }

  // Tick engine control handlers
  const handleStart = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('start_tick_engine')
        setTickStatus(prev => ({ ...prev, isRunning: true, isPaused: false }))
        console.log('✅ Tick engine started via Tauri')
      } catch (err) {
        console.error('❌ Failed to start tick engine:', err)
        setConnectionError(`Failed to start tick engine: ${err}`)
      }
    }
  }

  const handleStop = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('stop_tick_engine')
        setTickStatus(prev => ({ ...prev, isRunning: false, isPaused: false }))
        console.log('✅ Tick engine stopped via Tauri')
      } catch (err) {
        console.error('❌ Failed to stop tick engine:', err)
        setConnectionError(`Failed to stop tick engine: ${err}`)
      }
    }
  }

  const handlePause = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('pause_tick_engine')
        setTickStatus(prev => ({ ...prev, isPaused: true }))
        console.log('✅ Tick engine paused via Tauri')
      } catch (err) {
        console.error('❌ Failed to pause tick engine:', err)
        setConnectionError(`Failed to pause tick engine: ${err}`)
      }
    }
  }

  const handleResume = async () => {
    if (connectionMode === 'tauri') {
      try {
        await invoke('resume_tick_engine')
        setTickStatus(prev => ({ ...prev, isPaused: false }))
        console.log('✅ Tick engine resumed via Tauri')
      } catch (err) {
        console.error('❌ Failed to resume tick engine:', err)
        setConnectionError(`Failed to resume tick engine: ${err}`)
      }
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white flex">
      {/* Main dashboard */}
      <div className={`flex-1 p-6 transition-all duration-300 ${showChat ? 'mr-96' : ''}`}>
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
              
              {/* Live Data Test Button */}
              <button
                onClick={handleTestLiveData}
                className="px-4 py-2 rounded-lg font-medium transition-all duration-300 transform hover:scale-105 bg-yellow-600 hover:bg-yellow-700 text-white shadow-yellow-500/20 shadow-lg"
                title="Test live data updates"
              >
                <span className="flex items-center space-x-2">
                  <span>🧪</span>
                  <span>Test Live Data</span>
                </span>
              </button>

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
                connectionMode === 'websocket' ? 'bg-green-900/30 border-green-400/50 text-green-300 shadow-green-400/20 shadow-lg' :
                connectionMode === 'tauri' ? 'bg-cyan-900/30 border-cyan-400/50 text-cyan-300 shadow-cyan-400/20 shadow-lg' :
                connectionMode === 'checking' ? 'bg-yellow-900/30 border-yellow-400/50 text-yellow-300 shadow-yellow-400/20 shadow-lg' :
                'bg-red-900/30 border-red-400/50 text-red-300'
              }`}>
                <div className={`w-4 h-4 rounded-full transition-all duration-300 ${
                  connectionMode === 'websocket' ? 'bg-green-400 animate-pulse shadow-green-400/50 shadow-lg' :
                  connectionMode === 'tauri' ? 'bg-cyan-400 animate-pulse shadow-cyan-400/50 shadow-lg' :
                  connectionMode === 'checking' ? 'bg-yellow-400 animate-ping' :
                  'bg-red-400'
                }`} />
                <span className="font-semibold text-lg">
                  {connectionMode === 'websocket' ? '🟢 WebSocket Connected' :
                   connectionMode === 'tauri' ? '🦀 Tauri Connected' :
                   connectionMode === 'checking' ? '🟡 Checking Connection...' :
                   '🔴 Backend Offline'}
                </span>
                {connectionMode === 'tauri' && (
                  <span className="text-xs opacity-75 ml-2">(Native Integration)</span>
                )}
                {connectionMode === 'websocket' && (
                  <span className="text-xs opacity-75 ml-2">(HTTP + WebSocket)</span>
                )}
              </div>
            </div>
          </div>
          
          {/* Live Data Status */}
          <div className="mt-4 p-4 bg-cyan-900/20 border border-cyan-400/30 rounded-xl backdrop-blur-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-cyan-400 rounded-full animate-pulse"></div>
                  <span className="text-cyan-300 font-medium">Live Data Stream</span>
                </div>
                <div className="text-gray-400 text-sm">
                  Updates: <span className="text-cyan-300 font-mono">{updateCount}</span>
                </div>
                {lastUpdateTime && (
                  <div className="text-gray-400 text-sm">
                    Last: <span className="text-cyan-300 font-mono">{lastUpdateTime}</span>
                  </div>
                )}
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <span className="text-gray-400">Tick:</span>
                <span className="text-cyan-300 font-mono font-bold">#{metrics.tick_count.toLocaleString()}</span>
              </div>
            </div>
          </div>

          {/* Error Display */}
          {connectionError && (
            <div className={`mt-4 p-4 rounded-xl backdrop-blur-sm ${
              connectionError.includes('successful') || connectionError.includes('Live data test')
                ? 'bg-green-900/30 border border-green-500/50'
                : 'bg-red-900/30 border border-red-500/50'
            }`}>
              <div className="flex items-center justify-between">
                <p className={`flex items-center ${
                  connectionError.includes('successful') || connectionError.includes('Live data test')
                    ? 'text-green-300'
                    : 'text-red-300'
                }`}>
                  <span className="mr-2">
                    {connectionError.includes('successful') || connectionError.includes('Live data test') ? '✅' : '⚠️'}
                  </span>
                  {connectionError}
                </p>
                {!connectionError.includes('successful') && !connectionError.includes('Live data test') && (
                  <button 
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
                  >
                    🔄 Reconnect
                  </button>
                )}
              </div>
            </div>
           )}
         </header>

        {/* Comprehensive Tick Engine Control Panel */}
        <div className="max-w-7xl mx-auto mb-8">
          <TickControl 
            tickStatus={tickStatus}
            onTimingChange={(newInterval) => {
              console.log(`⏱️ Tick timing changed to ${newInterval}ms`)
              setTickStatus(prev => ({ ...prev, intervalMs: newInterval }))
            }}
            onStatusChange={(newStatus) => {
              setTickStatus(prev => ({ ...prev, ...newStatus }))
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
        <div className="max-w-7xl mx-auto mb-8">
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

        {/* Live Data Diagnostic Panel */}
        <div className="max-w-7xl mx-auto">
          <div className="bg-gradient-to-r from-cyan-900/20 via-blue-900/20 to-purple-900/20 backdrop-blur-sm rounded-2xl p-6 border border-cyan-400/30 shadow-2xl">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-cyan-300 flex items-center">
                <span className="mr-3">🔬</span>
                Live Data Diagnostic
              </h3>
              <button
                onClick={handleTestLiveData}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-lg transition-all duration-300 transform hover:scale-105 flex items-center space-x-2"
              >
                <span>🧪</span>
                <span>Force Update</span>
              </button>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600/50">
                <div className="text-gray-400 text-sm mb-1">Connection Mode</div>
                <div className={`font-bold text-lg ${
                  connectionMode === 'tauri' ? 'text-cyan-400' : 
                  connectionMode === 'websocket' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {connectionMode.toUpperCase()}
                </div>
              </div>
              
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600/50">
                <div className="text-gray-400 text-sm mb-1">Total Updates</div>
                <div className="text-cyan-400 font-bold text-lg font-mono">
                  {updateCount.toLocaleString()}
                </div>
              </div>
              
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600/50">
                <div className="text-gray-400 text-sm mb-1">Last Update</div>
                <div className="text-cyan-400 font-bold text-lg font-mono">
                  {lastUpdateTime || 'Waiting...'}
                </div>
              </div>
              
              <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-600/50">
                <div className="text-gray-400 text-sm mb-1">Data Status</div>
                <div className={`font-bold text-lg flex items-center space-x-2 ${
                  updateCount > 0 ? 'text-green-400' : 'text-yellow-400'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${
                    updateCount > 0 ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'
                  }`} />
                  <span>{updateCount > 0 ? 'LIVE' : 'STATIC'}</span>
                </div>
              </div>
            </div>
            
            {/* Quick metrics summary */}
            <div className="mt-4 p-4 bg-gray-900/50 rounded-lg border border-gray-600/30">
              <div className="text-gray-400 text-sm mb-2">Current Values (Live Preview)</div>
              <div className="font-mono text-sm space-y-1">
                <div className="flex justify-between">
                  <span className="text-blue-400">SCUP:</span>
                  <span className="text-white">{metrics.scup.toFixed(6)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-green-400">Entropy:</span>
                  <span className="text-white">{metrics.entropy.toFixed(6)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-orange-400">Heat:</span>
                  <span className="text-white">{metrics.heat.toFixed(6)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-purple-400">Mood:</span>
                  <span className="text-white">{metrics.mood}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Enhanced Status Indicator */}
        <div className="fixed bottom-6 left-6 bg-gray-800/90 backdrop-blur-sm rounded-lg px-4 py-3 border border-gray-600 shadow-lg">
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-gray-300">React Active</span>
            </div>
            {updateCount > 0 && (
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                <span className="text-cyan-300 font-mono">{updateCount} updates</span>
              </div>
            )}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                connectionMode === 'tauri' ? 'bg-cyan-400 animate-pulse' :
                connectionMode === 'websocket' ? 'bg-green-400 animate-pulse' :
                'bg-red-400'
              }`}></div>
              <span className="text-gray-300">{connectionMode}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Chat sidebar */}
      <div className={`fixed right-0 top-0 h-full w-96 bg-gray-800 shadow-xl transform transition-transform duration-300 ease-in-out z-50 ${
        showChat ? 'translate-x-0' : 'translate-x-full'
      }`}>
        <ChatInterface currentMood={metrics.mood} />
      </div>
      
      {/* Chat toggle button */}
      <button
        onClick={() => setShowChat(!showChat)}
        className={`fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg flex items-center justify-center transition-all duration-300 z-40 ${
          showChat 
            ? 'bg-purple-600 hover:bg-purple-700 shadow-purple-500/30' 
            : 'bg-blue-600 hover:bg-blue-700 shadow-blue-500/30'
        } hover:scale-110 active:scale-95`}
      >
        <span className="text-xl">
          {showChat ? '✕' : '💬'}
        </span>
      </button>
    </div>
  )
}

function MetricCard({ title, value, colorScheme, icon, subtitle, description }) {
  const [isUpdating, setIsUpdating] = useState(false)
  const [previousValue, setPreviousValue] = useState(value)
  const [changeDirection, setChangeDirection] = useState(null) // 'up', 'down', null
  const [updateFlash, setUpdateFlash] = useState(false)
  
  const colorSchemes = {
    blue: {
      primary: 'text-blue-400',
      secondary: 'text-blue-300',
      bg: 'bg-blue-400',
      border: 'border-blue-400/30',
      shadow: 'shadow-blue-400/20',
      glow: 'shadow-blue-400/30',
      ring: 'ring-blue-400/50'
    },
    green: {
      primary: 'text-green-400',
      secondary: 'text-green-300',
      bg: 'bg-green-400',
      border: 'border-green-400/30',
      shadow: 'shadow-green-400/20',
      glow: 'shadow-green-400/30',
      ring: 'ring-green-400/50'
    },
    orange: {
      primary: 'text-orange-400',
      secondary: 'text-orange-300',
      bg: 'bg-orange-400',
      border: 'border-orange-400/30',
      shadow: 'shadow-orange-400/20',
      glow: 'shadow-orange-400/30',
      ring: 'ring-orange-400/50'
    },
    purple: {
      primary: 'text-purple-400',
      secondary: 'text-purple-300',
      bg: 'bg-purple-400',
      border: 'border-purple-400/30',
      shadow: 'shadow-purple-400/20',
      glow: 'shadow-purple-400/30',
      ring: 'ring-purple-400/50'
    }
  }
  
  const colors = colorSchemes[colorScheme]
  
  useEffect(() => {
    if (value !== previousValue) {
      setIsUpdating(true)
      setUpdateFlash(true)
      
      // Determine change direction for numeric values
      if (typeof value === 'number' && typeof previousValue === 'number') {
        setChangeDirection(value > previousValue ? 'up' : 'down')
      } else {
        setChangeDirection(null)
      }
      
      setPreviousValue(value)
      
      // Reset update state
      const timer = setTimeout(() => {
        setIsUpdating(false)
        setUpdateFlash(false)
        setChangeDirection(null)
      }, 600)
      
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
      bg-gray-800/80 backdrop-blur-sm rounded-2xl p-6 border transition-all duration-500 ease-out transform relative overflow-hidden
      hover:bg-gray-700/80 hover:scale-105 hover:-translate-y-1
      ${isUpdating ? `ring-2 ${colors.ring} ${colors.glow} shadow-2xl brightness-110` : colors.border}
      ${updateFlash ? 'animate-pulse' : ''}
      ${colors.shadow} shadow-lg
    `}>
      {/* Flash overlay for updates */}
      {updateFlash && (
        <div className={`absolute inset-0 ${colors.bg} opacity-20 animate-ping`} />
      )}
      
      <div className="flex items-center justify-between mb-4 relative z-10">
        <div className="flex items-center space-x-3">
          <span className={`text-2xl transition-all duration-300 ${isUpdating ? 'animate-bounce' : ''}`}>
            {icon}
          </span>
          <div>
            <h3 className="text-sm text-gray-400 uppercase tracking-wider font-bold">
              {title}
            </h3>
            <p className="text-xs text-gray-500">{subtitle}</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {/* Change direction indicator */}
          {changeDirection && (
            <div className={`transition-all duration-300 ${
              changeDirection === 'up' ? 'text-green-400' : 'text-red-400'
            }`}>
              <span className={`text-lg ${isUpdating ? 'animate-bounce' : ''}`}>
                {changeDirection === 'up' ? '↗️' : '↘️'}
              </span>
            </div>
          )}
          
          {/* Update indicator */}
          <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
            isUpdating ? `${colors.bg} animate-ping scale-125` : `${colors.bg} opacity-60`
          }`} />
        </div>
      </div>
      
      <div className="relative mb-4 z-10">
        <p className={`
          text-4xl font-bold transition-all duration-500 ease-out transform
          ${isUpdating ? 'scale-110 brightness-125 drop-shadow-lg' : 'scale-100'}
          ${colors.primary}
        `}>
          {formatValue(value)}
        </p>
        
        {/* Floating sparkle effect for updates */}
        {isUpdating && (
          <>
            <div className={`
              absolute -top-2 -right-2 w-3 h-3 rounded-full ${colors.bg}
              animate-bounce opacity-80
            `} />
            <div className={`
              absolute -bottom-1 -left-1 w-2 h-2 rounded-full ${colors.bg}
              animate-ping opacity-60 delay-100
            `} />
          </>
        )}
      </div>
      
      {/* Enhanced progress bar for numeric values */}
      {typeof value === 'number' && (
        <div className="mb-3 h-3 bg-gray-700 rounded-full overflow-hidden relative z-10">
          <div 
            className={`
              h-full ${colors.bg} transition-all duration-700 ease-out transform origin-left relative
              ${isUpdating ? 'brightness-125 scale-y-110 animate-pulse' : 'brightness-100 scale-y-100'}
            `}
            style={{ 
              width: `${getProgressWidth()}%`,
              filter: isUpdating ? 'drop-shadow(0 0 8px currentColor)' : 'drop-shadow(0 0 4px currentColor)'
            }}
          >
            {/* Progress bar glow effect */}
            {isUpdating && (
              <div className={`absolute inset-0 ${colors.bg} opacity-50 animate-pulse`} />
            )}
          </div>
        </div>
      )}
      
      {/* Description with live update count */}
      <div className="flex justify-between items-center relative z-10">
        <p className="text-xs text-gray-500 italic">
          {description}
        </p>
        {isUpdating && (
          <span className="text-xs text-cyan-400 animate-pulse font-mono">
            LIVE
          </span>
        )}
      </div>
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