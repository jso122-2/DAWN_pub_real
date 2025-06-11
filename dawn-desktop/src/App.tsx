import { useEffect } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'
import useMetricsStore from './store/metricsStore'
import MetricCard from './components/MetricCard'
import ConnectionStatus from './components/ConnectionStatus'
import './App.css'

function App() {
  const { 
    metrics, 
    subsystems,
    connectionStatus,
    error,
    isLoading,
    fetchMetrics,
    fetchSubsystems,
    checkBackendHealth,
    subscribeToMetrics,
    initializeEventListeners
  } = useMetricsStore()

  useEffect(() => {
    // Initialize event listeners for real-time updates
    const cleanup = initializeEventListeners()
    
    // Initialize the application
    const initialize = async () => {
      try {
        console.log('🚀 Initializing DAWN Desktop App with @tauri-apps/api')
        
        // Check backend health first
        await checkBackendHealth()
        
        // Subscribe to real-time metrics via WebSocket
        await subscribeToMetrics()
        
        // Fetch initial data via Rust commands
        await fetchMetrics()
        await fetchSubsystems()
        
        console.log('✅ DAWN app initialized successfully')
      } catch (error) {
        console.error('❌ Failed to initialize application:', error)
      }
    }
    
    initialize()
    
    // Periodic health checks every 30 seconds
    const healthCheckInterval = setInterval(() => {
      checkBackendHealth()
    }, 30000)
    
    // Manual metrics refresh every 10 seconds as fallback
    const metricsInterval = setInterval(() => {
      if (connectionStatus.backend === 'connected') {
        fetchMetrics()
      }
    }, 10000)
    
    return () => {
      cleanup()
      clearInterval(healthCheckInterval)
      clearInterval(metricsInterval)
    }
  }, [initializeEventListeners, checkBackendHealth, subscribeToMetrics, fetchMetrics, fetchSubsystems, connectionStatus.backend])

  // Test Tauri command function
  const testTauriConnection = async () => {
    try {
      console.log('🔍 Testing Tauri connection...')
      const health = await invoke('check_backend_health')
      console.log('✅ Backend health:', health)
      
      const currentMetrics = await invoke('get_current_metrics')
      console.log('📊 Current metrics:', currentMetrics)
    } catch (error) {
      console.error('❌ Tauri connection test failed:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      {/* Header with Connection Status */}
      <header className="mb-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-4xl font-bold">DAWN Neural Monitor</h1>
            <div className="text-sm text-gray-400">
              Real-time via @tauri-apps/api
            </div>
          </div>
          
          {/* Enhanced Connection Status */}
          <ConnectionStatus 
            backend={connectionStatus.backend}
            websocket={connectionStatus.websocket}
            lastUpdate={connectionStatus.lastUpdate}
          />
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="mt-4 p-4 bg-red-900/30 border border-red-500/50 rounded-lg backdrop-blur-sm">
            <div className="flex items-center justify-between">
              <p className="text-red-300 flex items-center">
                <span className="text-red-400 mr-2">⚠️</span>
                {error}
              </p>
              <button 
                onClick={testTauriConnection}
                className="text-xs text-red-400 hover:text-red-300 underline"
              >
                Test Connection
              </button>
            </div>
          </div>
        )}
        
        {/* Loading Indicator */}
        {isLoading && (
          <div className="mt-4 text-center">
            <div className="inline-flex items-center space-x-2 text-gray-400">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400"></div>
              <span className="animate-pulse">Loading metrics via Tauri...</span>
            </div>
          </div>
        )}
      </header>
      
      {/* Enhanced Metrics Grid with Real-time Animations */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto mb-8">
        <MetricCard
          title="SCUP"
          value={metrics.scup}
          colorScheme="blue"
          icon="🧠"
          subtitle={`Tick: ${metrics.tick_count}`}
          isConnected={connectionStatus.backend === 'connected' && connectionStatus.websocket}
          lastUpdate={connectionStatus.lastUpdate}
        />
        
        <MetricCard
          title="Entropy"
          value={metrics.entropy}
          colorScheme="green"
          icon="🌀"
          subtitle="Neural Coherence"
          isConnected={connectionStatus.backend === 'connected' && connectionStatus.websocket}
          lastUpdate={connectionStatus.lastUpdate}
        />
        
        <MetricCard
          title="Heat"
          value={metrics.heat}
          colorScheme="orange"
          icon="🔥"
          subtitle="System Temperature"
          isConnected={connectionStatus.backend === 'connected' && connectionStatus.websocket}
          lastUpdate={connectionStatus.lastUpdate}
        />
        
        <MetricCard
          title="Mood"
          value={metrics.mood}
          colorScheme="purple"
          icon="💭"
          subtitle="System State"
          isConnected={connectionStatus.backend === 'connected' && connectionStatus.websocket}
          lastUpdate={connectionStatus.lastUpdate}
        />
      </div>

      {/* Enhanced Subsystems Panel */}
      <div className="max-w-7xl mx-auto">
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-700/50">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-xl font-semibold text-gray-200 flex items-center">
              <span className="mr-2">🔧</span>
              Active Subsystems
            </h3>
            <div className="text-sm text-gray-400">
              {subsystems.length} active
            </div>
          </div>
          
          {subsystems.length === 0 ? (
            <div className="text-center text-gray-500 py-12">
              <div className="text-4xl mb-4">🤖</div>
              <p className="text-lg">No subsystems detected</p>
              <p className="text-sm mt-2">
                {connectionStatus.backend === 'connected' 
                  ? 'Waiting for neural engine initialization...' 
                  : 'Connect to backend to see subsystems'
                }
              </p>
              <button 
                onClick={fetchSubsystems}
                className="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm transition-colors"
              >
                Refresh Subsystems
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {subsystems.map((subsystem, index) => (
                <div 
                  key={subsystem.id} 
                  className="bg-gray-700/50 rounded-lg p-4 hover:bg-gray-600/50 transition-all duration-300 transform hover:scale-105 border border-gray-600/30"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="flex justify-between items-start mb-3">
                    <h4 className="font-medium text-gray-200 flex items-center">
                      <span className="mr-2">⚙️</span>
                      {subsystem.name}
                    </h4>
                    <span className={`text-xs px-2 py-1 rounded-full transition-all duration-300 ${
                      subsystem.status === 'active' 
                        ? 'bg-green-900/50 text-green-300 border border-green-500/30' 
                        : 'bg-gray-900/50 text-gray-400 border border-gray-500/30'
                    }`}>
                      {subsystem.status}
                    </span>
                  </div>
                  
                  <div className="text-sm text-gray-400 space-y-1">
                    <div className="flex items-center">
                      <span className="text-gray-500 mr-2">ID:</span>
                      <span className="text-gray-300 font-mono text-xs">{subsystem.id}</span>
                    </div>
                    
                    {Object.keys(subsystem.state).length > 0 && (
                      <div className="mt-3">
                        <details className="cursor-pointer group">
                          <summary className="text-gray-500 hover:text-gray-300 text-xs flex items-center transition-colors">
                            <span className="mr-1 transform group-open:rotate-90 transition-transform">▶</span>
                            State ({Object.keys(subsystem.state).length} properties)
                          </summary>
                          <div className="mt-2 ml-4 space-y-1 text-xs max-h-32 overflow-y-auto">
                            {Object.entries(subsystem.state).slice(0, 5).map(([key, value]) => (
                              <div key={key} className="flex justify-between truncate">
                                <span className="text-gray-500 mr-2">{key}:</span>
                                <span className="text-gray-300 font-mono">
                                  {typeof value === 'object' 
                                    ? `{${Object.keys(value as object).length} keys}` 
                                    : String(value).slice(0, 20)
                                  }
                                </span>
                              </div>
                            ))}
                            {Object.keys(subsystem.state).length > 5 && (
                              <div className="text-gray-600 text-center pt-1 border-t border-gray-700">
                                +{Object.keys(subsystem.state).length - 5} more properties...
                              </div>
                            )}
                          </div>
                        </details>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Enhanced Footer with Real-time System Info */}
      <footer className="mt-8 text-center">
        <div className="bg-gray-800/30 backdrop-blur-sm rounded-lg p-4 border border-gray-700/30">
          <div className="flex justify-center items-center space-x-8 text-sm">
            <div className="flex items-center space-x-2">
              <span className={`w-2 h-2 rounded-full ${
                connectionStatus.backend === 'connected' ? 'bg-green-400 animate-pulse' : 'bg-red-400'
              }`} />
              <span className="text-gray-400">Neural Engine:</span>
              <span className={connectionStatus.backend === 'connected' ? 'text-green-400' : 'text-red-400'}>
                {connectionStatus.backend === 'connected' ? 'Online' : 'Offline'}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className={`w-2 h-2 rounded-full ${
                connectionStatus.websocket ? 'bg-blue-400 animate-pulse' : 'bg-gray-400'
              }`} />
              <span className="text-gray-400">WebSocket:</span>
              <span className={connectionStatus.websocket ? 'text-blue-400' : 'text-gray-400'}>
                {connectionStatus.websocket ? 'Active' : 'Inactive'}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-gray-400">Subsystems:</span>
              <span className="text-purple-400 font-bold">{subsystems.length}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-gray-400">Tick:</span>
              <span className="text-cyan-400 font-mono">{metrics.tick_count}</span>
            </div>
          </div>
          
          {metrics.timestamp > 0 && (
            <div className="mt-2 text-xs text-gray-500">
              Last update: {new Date(metrics.timestamp * 1000).toLocaleString()}
            </div>
          )}
        </div>
      </footer>
    </div>
  )
}

export default App
