// src/components/ReflectionLogPanel.tsx
//! Tick Echo Display - DAWN's Introspective Reflection Stream
//! Real-time display of consciousness self-reflection and meta-cognitive analysis

import { useState, useRef, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './ReflectionLogPanel.css'

// Reflection entry structure
interface ReflectionEntry {
  timestamp: string
  tick_number?: number
  entropy?: number
  mood?: string
  scup?: number
  heat?: number
  zone?: string
  reflection: string
  priority?: 'low' | 'normal' | 'high' | 'critical'
  source?: string
}

/**
 * DAWN Reflection Log Panel
 * 
 * Displays the last 10 introspective reflections from auto_reflect.py,
 * showing DAWN's internal narrative as consciousness unfolds moment by moment.
 */
export function ReflectionLogPanel() {
  const [reflections, setReflections] = useState<ReflectionEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isPaused, setIsPaused] = useState(false)
  const [newEntryCount, setNewEntryCount] = useState(0)
  const [debugInfo, setDebugInfo] = useState<string>('')
  
  const containerRef = useRef<HTMLDivElement>(null)
  const lastReflectionCount = useRef<number>(0)
  const pollIntervalRef = useRef<number>()

  // Add some test data as fallback
  const createTestReflections = (): ReflectionEntry[] => {
    return [
      {
        timestamp: new Date().toISOString(),
        tick_number: 1001,
        entropy: 0.456,
        mood: 'contemplative',
        scup: 42.3,
        reflection: '[TEST] This is a test reflection to verify the UI is working',
        source: 'test_fallback'
      },
      {
        timestamp: new Date(Date.now() - 5000).toISOString(),
        tick_number: 1000,
        entropy: 0.391,
        mood: 'analytical',
        scup: 38.7,
        reflection: '[TEST] Previous test reflection showing historical data',
        source: 'test_fallback'
      }
    ]
  }

  // Load reflections from log file
  const loadReflections = useCallback(async (): Promise<ReflectionEntry[]> => {
    try {
      setDebugInfo('Attempting to read reflection log...')
      
      // Read the reflection log file using Tauri
      const fileContent = await invoke<string>('read_reflection_log', {
        path: 'runtime/logs/reflection.log'
      })
      
      setDebugInfo(`Read ${fileContent.length} bytes from log file`)
      
      if (!fileContent.trim()) {
        setDebugInfo('File was empty, using test data')
        return createTestReflections()
      }
      
      // Parse log entries - expect JSON Lines format or structured text
      const lines = fileContent.trim().split('\n')
      const entries: ReflectionEntry[] = []
      
      setDebugInfo(`Processing ${lines.length} lines from log file`)
      
      for (const line of lines) {
        try {
          // Try parsing as JSON first
          if (line.trim().startsWith('{')) {
            const entry = JSON.parse(line) as ReflectionEntry
            entries.push(entry)
          } else {
            // Fallback: parse structured text format
            // Format: [TIMESTAMP] [ENTROPY:X.XXX] [MOOD:VALUE] REFLECTION_TEXT
            const match = line.match(/^\[([^\]]+)\]\s*(?:\[ENTROPY:([\d.]+)\])?\s*(?:\[MOOD:([^\]]+)\])?\s*(?:\[SCUP:([\d.]+)\])?\s*(.+)$/)
            if (match) {
              const [, timestamp, entropy, mood, scup, reflection] = match
              entries.push({
                timestamp,
                entropy: entropy ? parseFloat(entropy) : undefined,
                mood: mood || undefined,
                scup: scup ? parseFloat(scup) : undefined,
                reflection: reflection.trim(),
                source: 'auto_reflect'
              })
            } else if (line.trim()) {
              // Simple fallback: treat as plain reflection with current timestamp
              entries.push({
                timestamp: new Date().toISOString(),
                reflection: line.trim(),
                source: 'unknown'
              })
            }
          }
        } catch (e) {
          console.warn('Failed to parse reflection entry:', line, e)
        }
      }
      
      setDebugInfo(`Successfully parsed ${entries.length} entries`)
      
      // Return last 10 entries in reverse chronological order (newest first)
      const result = entries.slice(-10).reverse()
      
      // If no entries found, return test data
      if (result.length === 0) {
        setDebugInfo('No valid entries found, using test data')
        return createTestReflections()
      }
      
      return result
    } catch (e) {
      console.error('Failed to load reflections:', e)
      setDebugInfo(`Error loading reflections: ${e instanceof Error ? e.message : 'Unknown error'}`)
      
      // Return test data on error
      return createTestReflections()
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

  // Refresh reflections data
  const refreshData = useCallback(async () => {
    if (isPaused) return
    
    try {
      setError(null)
      const newReflections = await loadReflections()
      setReflections(newReflections)
      
      // Check if new entries arrived
      if (newReflections.length > lastReflectionCount.current) {
        setNewEntryCount(newReflections.length - lastReflectionCount.current)
        lastReflectionCount.current = newReflections.length
        
        // Auto-scroll if there are new entries
        setTimeout(() => {
          if (containerRef.current) {
            containerRef.current.scrollTop = 0 // Scroll to top since newest is first
          }
        }, 100)
      }
    } catch (e) {
      console.error('Failed to refresh reflections:', e)
      setError(e instanceof Error ? e.message : 'Failed to load reflection data')
    }
  }, [isPaused, loadReflections])

  // Initial load
  useEffect(() => {
    const initialLoad = async () => {
      setIsLoading(true)
      await refreshData()
      setIsLoading(false)
    }
    
    initialLoad()
  }, [refreshData])

  // Setup polling
  useEffect(() => {
    if (isPaused) return
    
    pollIntervalRef.current = window.setInterval(refreshData, 3000) // Poll every 3 seconds
    
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
    }
  }, [refreshData, isPaused])

  // Toggle pause
  const togglePause = () => {
    setIsPaused(!isPaused)
    setNewEntryCount(0) // Clear new entry indicator when pausing/unpausing
  }

  if (isLoading) {
    return (
      <div className="reflection-log-panel loading">
        <div className="panel-header">
          <h3>🔁 Reflection Echo</h3>
        </div>
        <div className="loading-indicator">
          <div className="pulse-dot"></div>
          <span>Loading reflections...</span>
          <div className="debug-info">Debug: {debugInfo}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="reflection-log-panel">
      <div className="panel-header">
        <div className="header-left">
          <h3>🔁 Reflection Echo</h3>
          {newEntryCount > 0 && (
            <span className="new-badge">+{newEntryCount}</span>
          )}
        </div>
        
        <div className="panel-controls">
          <button 
            onClick={togglePause}
            className={`control-btn ${isPaused ? 'paused' : 'live'}`}
            title={isPaused ? 'Resume' : 'Pause'}
          >
            {isPaused ? '▶️' : '⏸️'}
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
          <button onClick={refreshData} className="retry-btn">Retry</button>
        </div>
      )}

      <div className="debug-panel">
        <small>Debug: {debugInfo}</small>
      </div>

      <div className="reflections-container" ref={containerRef}>
        {reflections.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤔</div>
            <div className="empty-text">No reflections yet</div>
            <div className="empty-subtext">Waiting for DAWN's introspection...</div>
          </div>
        ) : (
          <div className="reflection-entries">
            {reflections.map((reflection, index) => (
              <div 
                key={`reflection_${index}_${reflection.timestamp}`}
                className={`reflection-entry ${reflection.source === 'test_fallback' ? 'test-entry' : ''}`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="reflection-header">
                  <span className="reflection-time">
                    {formatTimestamp(reflection.timestamp)}
                  </span>
                  {reflection.tick_number && (
                    <span className="reflection-tick">
                      Tick #{reflection.tick_number}
                    </span>
                  )}
                  {reflection.source === 'test_fallback' && (
                    <span className="test-badge">TEST</span>
                  )}
                </div>
                
                <div className="reflection-content">
                  {reflection.reflection}
                </div>
                
                {(reflection.entropy !== undefined || reflection.mood || reflection.scup !== undefined) && (
                  <div className="reflection-metadata">
                    {reflection.entropy !== undefined && (
                      <span className="meta-tag entropy">
                        E: {reflection.entropy.toFixed(3)}
                      </span>
                    )}
                    {reflection.mood && (
                      <span className="meta-tag mood">
                        {reflection.mood}
                      </span>
                    )}
                    {reflection.scup !== undefined && (
                      <span className="meta-tag scup">
                        SCUP: {reflection.scup.toFixed(1)}
                      </span>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel-footer">
        <div className="status-info">
          <span className={`status-dot ${isPaused ? 'paused' : 'live'}`}></span>
          <span className="status-text">
            {isPaused ? 'Paused' : 'Live'} • {reflections.length} reflections
          </span>
        </div>
      </div>
    </div>
  )
} 