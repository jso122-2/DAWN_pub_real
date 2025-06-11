import { useState, useEffect } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'

export default function TickControl({ onTimingChange, className = "" }) {
  const [tickStatus, setTickStatus] = useState({
    tick_number: 0,
    is_running: false,
    is_paused: false,
    interval_ms: 500,
    uptime_seconds: 0,
    total_ticks: 0,
    avg_tick_duration_ms: 0,
    last_tick_timestamp: null
  })
  
  const [intervalInput, setIntervalInput] = useState(500)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdate, setLastUpdate] = useState(Date.now())

  // Fetch initial tick status
  useEffect(() => {
    const fetchTickStatus = async () => {
      try {
        console.log('🔄 Fetching initial tick status...')
        const status = await invoke('get_tick_status')
        setTickStatus(status)
        setIntervalInput(status.interval_ms)
        console.log('✅ Tick status loaded:', status)
      } catch (err) {
        console.error('❌ Failed to fetch tick status:', err)
        setError(`Failed to load tick status: ${err}`)
      }
    }

    fetchTickStatus()
  }, [])

  // Listen for real-time tick updates
  useEffect(() => {
    const setupListeners = async () => {
      try {
        // Listen for tick updates from WebSocket
        const unlistenTick = await listen('tick-update', (event) => {
          console.log('📨 Tick update received:', event.payload)
          if (event.payload && event.payload.tick_number !== undefined) {
            setTickStatus(prev => ({
              ...prev,
              tick_number: event.payload.tick_number,
              last_tick_timestamp: event.payload.timestamp
            }))
            setLastUpdate(Date.now())
          }
        })

        // Listen for metrics updates (fallback)
        const unlistenMetrics = await listen('metrics-update', (event) => {
          if (event.payload && event.payload.tick_count !== undefined) {
            setTickStatus(prev => ({
              ...prev,
              tick_number: event.payload.tick_count
            }))
            setLastUpdate(Date.now())
          }
        })

        return [unlistenTick, unlistenMetrics]
      } catch (err) {
        console.error('❌ Failed to setup listeners:', err)
        return []
      }
    }

    setupListeners().then(cleanupFunctions => {
      return () => {
        cleanupFunctions.forEach(cleanup => cleanup && cleanup())
      }
    })

    // Periodic status refresh
    const statusInterval = setInterval(async () => {
      try {
        const status = await invoke('get_tick_status')
        setTickStatus(status)
      } catch (err) {
        console.warn('⚠️ Failed to refresh tick status:', err)
      }
    }, 2000) // Refresh every 2 seconds

    return () => clearInterval(statusInterval)
  }, [])

  // Control functions
  const handleStart = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('🚀 Starting tick engine...')
      await invoke('start_tick_engine')
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      console.log('✅ Tick engine started')
    } catch (err) {
      console.error('❌ Failed to start tick engine:', err)
      setError(`Failed to start: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStop = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('🛑 Stopping tick engine...')
      await invoke('stop_tick_engine')
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      console.log('✅ Tick engine stopped')
    } catch (err) {
      console.error('❌ Failed to stop tick engine:', err)
      setError(`Failed to stop: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handlePause = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('⏸️ Pausing tick engine...')
      await invoke('pause_tick_engine')
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      console.log('✅ Tick engine paused')
    } catch (err) {
      console.error('❌ Failed to pause tick engine:', err)
      setError(`Failed to pause: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleResume = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('▶️ Resuming tick engine...')
      await invoke('resume_tick_engine')
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      console.log('✅ Tick engine resumed')
    } catch (err) {
      console.error('❌ Failed to resume tick engine:', err)
      setError(`Failed to resume: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleStep = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('👆 Executing single tick...')
      await invoke('execute_single_tick')
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      console.log('✅ Single tick executed')
    } catch (err) {
      console.error('❌ Failed to execute single tick:', err)
      setError(`Failed to step: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleTimingChange = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log(`⏱️ Setting tick timing to ${intervalInput}ms...`)
      await invoke('set_tick_timing', { intervalMs: parseInt(intervalInput) })
      const status = await invoke('get_tick_status')
      setTickStatus(status)
      if (onTimingChange) {
        onTimingChange(parseInt(intervalInput))
      }
      console.log(`✅ Tick timing set to ${intervalInput}ms`)
    } catch (err) {
      console.error('❌ Failed to set tick timing:', err)
      setError(`Failed to set timing: ${err}`)
    } finally {
      setIsLoading(false)
    }
  }

  // Helper functions
  const getStateColor = () => {
    if (!tickStatus.is_running) return 'text-gray-400'
    if (tickStatus.is_paused) return 'text-yellow-400'
    return 'text-green-400'
  }

  const getStateText = () => {
    if (!tickStatus.is_running) return 'Stopped'
    if (tickStatus.is_paused) return 'Paused'
    return 'Running'
  }

  const getTicksPerSecond = () => {
    return tickStatus.interval_ms > 0 ? (1000 / tickStatus.interval_ms).toFixed(1) : '0'
  }

  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const mins = Math.floor((seconds % 3600) / 60)
    const secs = Math.floor(seconds % 60)
    
    if (hours > 0) {
      return `${hours}h ${mins}m ${secs}s`
    } else if (mins > 0) {
      return `${mins}m ${secs}s`
    } else {
      return `${secs}s`
    }
  }

  return (
    <div className={`bg-gray-800/50 backdrop-blur-lg rounded-2xl p-6 border border-gray-700/50 shadow-2xl ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className={`w-4 h-4 rounded-full transition-all duration-300 ${
            tickStatus.is_running && !tickStatus.is_paused 
              ? 'bg-green-400 animate-pulse shadow-green-400/50 shadow-lg' 
              : tickStatus.is_paused 
                ? 'bg-yellow-400 animate-bounce' 
                : 'bg-gray-500'
          }`} />
          <h3 className="text-xl font-bold text-gray-200">
            ⚙️ Tick Engine Control
          </h3>
        </div>
        <div className={`text-sm font-semibold px-3 py-1 rounded-full ${
          tickStatus.is_running && !tickStatus.is_paused 
            ? 'bg-green-900/30 text-green-400 border border-green-500/30'
            : tickStatus.is_paused 
              ? 'bg-yellow-900/30 text-yellow-400 border border-yellow-500/30'
              : 'bg-gray-900/30 text-gray-400 border border-gray-500/30'
        }`}>
          {getStateText()}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
          <p className="text-red-300 text-sm flex items-center">
            <span className="mr-2">⚠️</span>
            {error}
          </p>
        </div>
      )}

      {/* Status Display */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-900/30 rounded-lg p-4 border border-gray-600/30">
          <div className="text-gray-400 text-xs mb-1">Tick Count</div>
          <div className={`text-xl font-bold font-mono transition-all duration-300 ${getStateColor()}`}>
            #{tickStatus.tick_number.toLocaleString()}
          </div>
        </div>
        
        <div className="bg-gray-900/30 rounded-lg p-4 border border-gray-600/30">
          <div className="text-gray-400 text-xs mb-1">Interval</div>
          <div className="text-xl font-bold font-mono text-blue-400">
            {tickStatus.interval_ms}ms
          </div>
        </div>
        
        <div className="bg-gray-900/30 rounded-lg p-4 border border-gray-600/30">
          <div className="text-gray-400 text-xs mb-1">Rate</div>
          <div className="text-xl font-bold font-mono text-purple-400">
            {getTicksPerSecond()} Hz
          </div>
        </div>
        
        <div className="bg-gray-900/30 rounded-lg p-4 border border-gray-600/30">
          <div className="text-gray-400 text-xs mb-1">Uptime</div>
          <div className="text-xl font-bold font-mono text-cyan-400">
            {formatUptime(tickStatus.uptime_seconds)}
          </div>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
        {/* Start/Stop Button */}
        <button
          onClick={tickStatus.is_running ? handleStop : handleStart}
          disabled={isLoading}
          className={`px-4 py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${
            tickStatus.is_running
              ? 'bg-red-600 hover:bg-red-700 text-white shadow-red-500/20 shadow-lg'
              : 'bg-green-600 hover:bg-green-700 text-white shadow-green-500/20 shadow-lg'
          }`}
        >
          {isLoading ? '⏳' : tickStatus.is_running ? '🛑 Stop' : '🚀 Start'}
        </button>

        {/* Pause/Resume Button */}
        <button
          onClick={tickStatus.is_paused ? handleResume : handlePause}
          disabled={!tickStatus.is_running || isLoading}
          className={`px-4 py-3 rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed ${
            tickStatus.is_paused
              ? 'bg-green-600 hover:bg-green-700 text-white shadow-green-500/20 shadow-lg'
              : 'bg-yellow-600 hover:bg-yellow-700 text-white shadow-yellow-500/20 shadow-lg'
          }`}
        >
          {isLoading ? '⏳' : tickStatus.is_paused ? '▶️ Resume' : '⏸️ Pause'}
        </button>

        {/* Step Button */}
        <button
          onClick={handleStep}
          disabled={tickStatus.is_running || isLoading}
          className="px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-blue-500/20 shadow-lg"
        >
          {isLoading ? '⏳' : '👆 Step'}
        </button>

        {/* Refresh Button */}
        <button
          onClick={async () => {
            try {
              const status = await invoke('get_tick_status')
              setTickStatus(status)
            } catch (err) {
              setError(`Failed to refresh: ${err}`)
            }
          }}
          disabled={isLoading}
          className="px-4 py-3 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all duration-300 transform hover:scale-105 shadow-purple-500/20 shadow-lg"
        >
          🔄 Refresh
        </button>
      </div>

      {/* Timing Control */}
      <div className="bg-gray-900/30 rounded-lg p-4 border border-gray-600/30">
        <h4 className="text-gray-300 font-semibold mb-3 flex items-center">
          <span className="mr-2">⏱️</span>
          Timing Control
        </h4>
        
        <div className="space-y-4">
          {/* Slider */}
          <div>
            <div className="flex justify-between text-sm text-gray-400 mb-2">
              <span>10ms</span>
              <span className="font-mono">{intervalInput}ms ({(1000/intervalInput).toFixed(1)} Hz)</span>
              <span>5000ms</span>
            </div>
            <input
              type="range"
              min="10"
              max="5000"
              value={intervalInput}
              onChange={(e) => setIntervalInput(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #3b82f6 0%, #3b82f6 ${((intervalInput - 10) / (5000 - 10)) * 100}%, #374151 ${((intervalInput - 10) / (5000 - 10)) * 100}%, #374151 100%)`
              }}
            />
          </div>

          {/* Input and Apply */}
          <div className="flex space-x-3">
            <input
              type="number"
              min="10"
              max="5000"
              value={intervalInput}
              onChange={(e) => setIntervalInput(parseInt(e.target.value) || 10)}
              className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Interval (ms)"
            />
            <button
              onClick={handleTimingChange}
              disabled={isLoading || intervalInput === tickStatus.interval_ms}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all duration-300 transform hover:scale-105"
            >
              Apply
            </button>
          </div>
        </div>
      </div>

      {/* Performance Stats */}
      {tickStatus.avg_tick_duration_ms > 0 && (
        <div className="mt-4 text-xs text-gray-500 text-center">
          Avg tick duration: {tickStatus.avg_tick_duration_ms.toFixed(1)}ms
          {tickStatus.last_tick_timestamp && (
            <span className="ml-3">
              Last update: {new Date(lastUpdate).toLocaleTimeString()}
            </span>
          )}
        </div>
      )}

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }

        .slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }
      `}</style>
    </div>
  )
} 