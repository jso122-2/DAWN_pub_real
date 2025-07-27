// src/components/ThoughtTracePanel.tsx
//! Thought Trace Panel - DAWN's Forecast & Action Intent Log
//! Real-time display of predictive reasoning and resulting interventions

import { useState, useRef, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './ThoughtTracePanel.css'

// Thought trace entry structure
interface ThoughtEntry {
  id: string
  tick_number: number
  timestamp: string
  forecast_value?: number
  confidence?: number
  entropy?: number
  entropy_delta?: number
  scup?: number
  zone?: string
  action_taken: string
  risk_level: 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL'
  action_icon: string
  entry_type: 'FORECAST' | 'MEMORY' | 'REFLECTION' | 'REBLOOM'
  content: string
}

// Action type mappings
const ACTION_MAPPING = {
  'STABILIZE_PROTOCOL': { icon: '📈', risk: 'HIGH' as const },
  'REBLOOM_MEMORY': { icon: '🌸', risk: 'NORMAL' as const },
  'SIGIL_TRIGGER': { icon: '⚡', risk: 'HIGH' as const },
  'NO_ACTION': { icon: '⚖️', risk: 'LOW' as const },
  'DRIFT_DETECTED': { icon: '📉', risk: 'HIGH' as const },
  'DRIFT_COMPENSATE': { icon: '🎯', risk: 'NORMAL' as const },
  'ENTROPY_SPIKE_DETECTED': { icon: '💥', risk: 'CRITICAL' as const },
  'SCUP_PROCESSING': { icon: '🧬', risk: 'NORMAL' as const },
  'THERMAL_WARNING': { icon: '🔥', risk: 'HIGH' as const },
  'STABLE_UNITY_ACHIEVED': { icon: '✨', risk: 'LOW' as const },
  'MONITORING': { icon: '👁️', risk: 'LOW' as const }
}

/**
 * DAWN Thought Trace Panel
 * 
 * Displays a real-time log of DAWN's forecasting and decision-making process,
 * showing the last 10 predictive assessments and their resulting actions.
 */
export function ThoughtTracePanel() {
  const [thoughtEntries, setThoughtEntries] = useState<ThoughtEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isPaused, setIsPaused] = useState(false)
  const [autoScroll, setAutoScroll] = useState(true)
  const [debugInfo, setDebugInfo] = useState<string>('')
  
  const containerRef = useRef<HTMLDivElement>(null)
  const pollIntervalRef = useRef<number>()
  const lastFileSize = useRef<number>(0)

  // Create test data as fallback
  const createTestEntries = (): ThoughtEntry[] => {
    const now = Date.now()
    return [
      {
        id: 'test_1',
        tick_number: 1005,
        timestamp: new Date(now).toISOString(),
        forecast_value: 0.742,
        action_taken: 'STABILIZE_PROTOCOL',
        risk_level: 'HIGH',
        action_icon: '📈',
        entry_type: 'FORECAST',
        content: '[TEST] Forecast: 0.742 → STABILIZE_PROTOCOL'
      },
      {
        id: 'test_2',
        tick_number: 1004,
        timestamp: new Date(now - 3000).toISOString(),
        action_taken: 'MONITORING',
        risk_level: 'LOW',
        action_icon: '👁️',
        entry_type: 'MEMORY',
        content: '[TEST] The watcher observes the patterns within patterns'
      },
      {
        id: 'test_3',
        tick_number: 1003,
        timestamp: new Date(now - 6000).toISOString(),
        forecast_value: 0.456,
        action_taken: 'DRIFT_COMPENSATE',
        risk_level: 'NORMAL',
        action_icon: '🎯',
        entry_type: 'FORECAST',
        content: '[TEST] Forecast: 0.456 → DRIFT_COMPENSATE'
      }
    ]
  }

  // Load thought entries from log file
  const loadThoughtEntries = useCallback(async (): Promise<ThoughtEntry[]> => {
    try {
      setDebugInfo('Attempting to invoke read_thought_trace_log...')
      
      // Check if invoke function exists
      if (typeof invoke !== 'function') {
        setDebugInfo('ERROR: invoke function not available')
        return createTestEntries()
      }

      // Read the thought trace log file using Tauri
      const fileContent = await invoke<string>('read_thought_trace_log', {
        path: 'runtime/logs/thought_trace.log'
      })
      
      setDebugInfo(`Successfully read ${fileContent.length} bytes from thought trace log`)
      
      if (!fileContent.trim()) {
        setDebugInfo('File was empty, using test data')
        return createTestEntries()
      }
      
      // Parse log entries
      const lines = fileContent.trim().split('\n')
      const entries: ThoughtEntry[] = []
      
      setDebugInfo(`Processing ${lines.length} lines from thought trace log`)
      
      for (const line of lines) {
        try {
          // Parse format: [Tick 000003] FORECAST: 0.72 -> STABILIZE_PROTOCOL
          // Parse format: [Tick 000004] MEMORY: "The first threshold was crossed in silence."
          // Parse format: [Tick 000005] REFLECTION: "I became aware of the watcher."
          // Parse format: [Tick 000009] REBLOOM: origin->drift (method:sigil)
          
          const tickMatch = line.match(/^\[Tick (\d+)\]\s+(\w+):\s*(.+)$/)
          if (tickMatch) {
            const [, tickStr, entryType, content] = tickMatch
            const tickNumber = parseInt(tickStr, 10)
            
            let actionTaken = 'MONITORING'
            let forecastValue: number | undefined
            let actualContent = content
            
            if (entryType === 'FORECAST') {
              // Format: 0.72 -> STABILIZE_PROTOCOL
              const forecastMatch = content.match(/^([\d.]+)\s*->\s*(.+)$/)
              if (forecastMatch) {
                forecastValue = parseFloat(forecastMatch[1])
                actionTaken = forecastMatch[2]
                actualContent = `Forecast: ${forecastValue} → ${actionTaken}`
              }
            } else if (entryType === 'REBLOOM') {
              // Format: origin->drift (method:sigil)
              actionTaken = 'REBLOOM_MEMORY'
              actualContent = content
            } else if (entryType === 'MEMORY' || entryType === 'REFLECTION') {
              // Strip quotes and use content as-is
              actualContent = content.replace(/^"(.*)"$/, '$1')
            }
            
            const mapping = ACTION_MAPPING[actionTaken as keyof typeof ACTION_MAPPING] || ACTION_MAPPING.MONITORING
            
            entries.push({
              id: `thought_${tickNumber}_${entryType}`,
              tick_number: tickNumber,
              timestamp: new Date().toISOString(),
              forecast_value: forecastValue,
              action_taken: actionTaken,
              risk_level: mapping.risk,
              action_icon: mapping.icon,
              entry_type: entryType as any,
              content: actualContent
            })
          }
        } catch (e) {
          console.warn('Failed to parse thought entry:', line, e)
        }
      }
      
      setDebugInfo(`Successfully parsed ${entries.length} thought entries`)
      
      // Return last 10 entries in reverse chronological order (newest first)
      const result = entries.slice(-10).reverse()
      
      if (result.length === 0) {
        setDebugInfo('No valid entries found, using test data')
        return createTestEntries()
      }
      
      return result
    } catch (e) {
      console.error('Failed to load thought entries:', e)
      setDebugInfo(`Error loading thought entries: ${e instanceof Error ? e.message : 'Unknown error'}`)
      
      // Return test data on error
      return createTestEntries()
    }
  }, [])

  // Format timestamp for display
  const formatTimestamp = (timestamp: string): string => {
    try {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
      })
    } catch {
      return 'Unknown'
    }
  }

  // Refresh data from log file
  const refreshData = useCallback(async () => {
    if (isPaused) return
    
    try {
      const newEntries = await loadThoughtEntries()
      setThoughtEntries(newEntries)
      setError(null)
      
      // Auto-scroll to top if enabled (since newest entries are first)
      if (autoScroll && containerRef.current) {
        setTimeout(() => {
          if (containerRef.current) {
            containerRef.current.scrollTop = 0
          }
        }, 100)
      }
    } catch (e) {
      console.error('Failed to refresh thought data:', e)
      setError(e instanceof Error ? e.message : 'Failed to load thought trace data')
    }
  }, [isPaused, autoScroll, loadThoughtEntries])

  // Initial data load
  useEffect(() => {
    const initialLoad = async () => {
      setIsLoading(true)
      await refreshData()
      setIsLoading(false)
    }
    
    initialLoad()
  }, [refreshData])

  // Setup polling for new data
  useEffect(() => {
    if (isPaused) return
    
    pollIntervalRef.current = window.setInterval(refreshData, 2000) // Poll every 2 seconds
    
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
    }
  }, [refreshData, isPaused])

  // Format forecast display
  const formatForecast = (forecast?: number): string => {
    return forecast ? forecast.toFixed(3) : '---'
  }

  // Get risk level styling
  const getRiskLevelClass = (riskLevel: string): string => {
    return `risk-${riskLevel.toLowerCase()}`
  }

  // Get entry type styling
  const getEntryTypeClass = (entryType: string): string => {
    return `entry-type-${entryType.toLowerCase()}`
  }

  // Clear all entries (for manual refresh)
  const clearEntries = () => {
    setThoughtEntries([])
  }

  // Toggle pause
  const togglePause = () => {
    setIsPaused(!isPaused)
  }

  // Toggle auto-scroll
  const toggleAutoScroll = () => {
    setAutoScroll(!autoScroll)
  }

  if (isLoading) {
    return (
      <div className="thought-trace-panel loading">
        <div className="panel-header">
          <h3>🧠 Thought Trace</h3>
        </div>
        <div className="loading-indicator">
          Loading thought trace data...
          <div className="debug-info">Debug: {debugInfo}</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="thought-trace-panel error">
        <div className="panel-header">
          <h3>🧠 Thought Trace</h3>
        </div>
        <div className="error-message">
          <strong>Error:</strong> {error}
          <button onClick={refreshData} className="retry-btn">
            Retry
          </button>
        </div>
        <div className="debug-info">Debug: {debugInfo}</div>
      </div>
    )
  }

  return (
    <div className="thought-trace-panel">
      <div className="trace-header">
        <div className="trace-title">
          <span className="title-icon">🧭</span>
          <span className="title-text">THOUGHT TRACE</span>
          <span className="entry-count">{thoughtEntries.length}/10</span>
        </div>
        
        <div className="trace-controls">
          <button 
            onClick={toggleAutoScroll}
            className={`control-btn scroll-btn ${autoScroll ? 'active' : ''}`}
            title={autoScroll ? 'Disable auto-scroll' : 'Enable auto-scroll'}
          >
            📜
          </button>
          
          <button 
            onClick={togglePause}
            className={`control-btn pause-btn ${isPaused ? 'paused' : 'live'}`}
            title={isPaused ? 'Resume monitoring' : 'Pause monitoring'}
          >
            {isPaused ? '▶️' : '⏸️'}
          </button>
          
          <button 
            onClick={clearEntries}
            className="control-btn clear-btn"
            title="Clear all entries"
          >
            🗑️
          </button>
        </div>
      </div>

      <div className="debug-panel">
        <small>Debug: {debugInfo}</small>
      </div>

      <div className="trace-container" ref={containerRef}>
        {thoughtEntries.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤔</div>
            <div className="empty-text">No thought traces yet</div>
            <div className="empty-subtext">Monitoring DAWN's decision process...</div>
          </div>
        ) : (
          <div className="trace-entries">
            {thoughtEntries.map((entry, index) => (
              <div 
                key={entry.id}
                className={`trace-entry ${getRiskLevelClass(entry.risk_level)} ${getEntryTypeClass(entry.entry_type)} ${entry.id.startsWith('test_') ? 'test-entry' : ''}`}
                style={{ animationDelay: `${index * 0.05}s` }}
              >
                <div className="entry-line">
                  <span className="entry-tick">[Tick #{entry.tick_number}]</span>
                  <span className="entry-time">{formatTimestamp(entry.timestamp)}</span>
                  <span className="entry-action-icon">{entry.action_icon}</span>
                  <span className="entry-type">{entry.entry_type}</span>
                  {entry.forecast_value !== undefined && (
                    <>
                      <span className="entry-forecast">
                        {formatForecast(entry.forecast_value)}
                      </span>
                      <span className="entry-arrow">→</span>
                      <span className="entry-action">{entry.action_taken}</span>
                    </>
                  )}
                  {entry.id.startsWith('test_') && (
                    <span className="test-badge">TEST</span>
                  )}
                </div>
                
                <div className="entry-metadata">
                  <span className="meta-item content">{entry.content}</span>
                  {entry.confidence !== undefined && (
                    <span className="meta-item confidence">
                      Conf: {(entry.confidence * 100).toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="trace-footer">
        <div className="status-info">
          <div className="status-item">
            <span className={`status-dot ${isPaused ? 'paused' : 'live'}`}></span>
            <span>{isPaused ? 'Paused' : 'Live'}</span>
          </div>
          
          <div className="status-item">
            <span className="poll-rate">2s polling</span>
          </div>
          
          <div className="status-item">
            <span className={`auto-scroll ${autoScroll ? 'enabled' : 'disabled'}`}>
              Auto-scroll: {autoScroll ? 'ON' : 'OFF'}
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ThoughtTracePanel 