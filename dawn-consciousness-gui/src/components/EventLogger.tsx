// src/components/EventLogger.tsx
//! Unified Cognition Event Feed - DAWN's Inner Dialogue Printout
//! Real-time streaming log of all consciousness events in chronological order

import { useState, useRef, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { get } from '../hooks/useTickState'
import './EventLogger.css'

// Event types for the unified feed
type EventType = 'reflection' | 'rebloom' | 'sigil' | 'heat_spike' | 'scup_spike' | 'entropy_spike' | 'system'

interface UnifiedEvent {
  id: string
  timestamp: string
  tick_number?: number
  type: EventType
  priority: 'low' | 'normal' | 'high' | 'critical'
  title: string
  description: string
  metadata?: {
    entropy?: number
    scup?: number
    heat?: number
    zone?: string
    mood?: string
    sigil_name?: string
    source_id?: string
    rebloom_id?: string
    [key: string]: any
  }
}

// Event type configurations
const EVENT_CONFIG = {
  reflection: { emoji: '🧠', label: 'REFLECTION', color: '#9b59b6' },
  rebloom: { emoji: '🌸', label: 'REBLOOM', color: '#4ecdc4' },
  sigil: { emoji: '⚡', label: 'SIGIL', color: '#f39c12' },
  heat_spike: { emoji: '🔥', label: 'HEAT', color: '#e74c3c' },
  scup_spike: { emoji: '🧬', label: 'SCUP', color: '#3498db' },
  entropy_spike: { emoji: '💥', label: 'ENTROPY', color: '#ff6b6b' },
  system: { emoji: '⚙️', label: 'SYSTEM', color: '#95a5a6' }
}

/**
 * DAWN Unified Event Logger
 * 
 * Displays a live, scrolling feed of all consciousness events including
 * reflections, memory reblooms, sigil triggers, and cognitive alerts.
 * This is DAWN's complete "inner dialogue printout" in chronological order.
 */
export function EventLogger() {
  const [events, setEvents] = useState<UnifiedEvent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [maxEvents] = useState(20) // Reduced default
  
  const containerRef = useRef<HTMLDivElement>(null)
  const pollIntervalRef = useRef<number>()
  const lastEventCount = useRef<number>(0)
  const lastMetrics = useRef<{ entropy: number; scup: number; heat: number; tick: number }>({ 
    entropy: 0, scup: 0, heat: 0, tick: 0 
  })

  // Load and parse reflection logs
  const loadReflectionEvents = useCallback(async (): Promise<UnifiedEvent[]> => {
    try {
      const fileContent = await invoke<string>('read_reflection_log', {
        path: 'gui-runtime/logs/reflection.log'
      })
      
      if (!fileContent.trim()) return []
      
      const lines = fileContent.trim().split('\n')
      const events: UnifiedEvent[] = []
      
      for (const line of lines) {
        try {
          let reflection, timestamp, entropy, mood, scup, tick
          
          if (line.trim().startsWith('{')) {
            const entry = JSON.parse(line)
            reflection = entry.reflection
            timestamp = entry.timestamp
            entropy = entry.entropy
            mood = entry.mood
            scup = entry.scup
            tick = entry.tick_number
          } else {
            const match = line.match(/^\[([^\]]+)\]\s*(?:\[ENTROPY:([\d.]+)\])?\s*(?:\[MOOD:([^\]]+)\])?\s*(?:\[SCUP:([\d.]+)\])?\s*(?:\[T:(\d+)\])?\s*(.+)$/)
            if (match) {
              [, timestamp, entropy, mood, scup, tick, reflection] = match
            } else {
              continue
            }
          }
          
          const priority = entropy && parseFloat(entropy) > 0.8 ? 'critical' : 
                         entropy && parseFloat(entropy) > 0.6 ? 'high' : 'normal'
          
          events.push({
            id: `reflection_${timestamp}_${events.length}`,
            timestamp,
            tick_number: tick ? parseInt(tick) : undefined,
            type: 'reflection',
            priority,
            title: `${mood || 'UNKNOWN'} Reflection`,
            description: reflection?.trim() || '',
            metadata: {
              entropy: entropy ? parseFloat(entropy) : undefined,
              mood: mood || undefined,
              scup: scup ? parseFloat(scup) : undefined
            }
          })
        } catch (e) {
          console.warn('Failed to parse reflection:', line)
        }
      }
      
      return events
    } catch (e) {
      console.error('Failed to load reflections:', e)
      return []
    }
  }, [])

  // Load and parse rebloom events
  const loadRebloomEvents = useCallback(async (): Promise<UnifiedEvent[]> => {
    try {
      const fileContent = await invoke<string>('read_rebloom_log', {
        path: 'gui-runtime/memory/rebloom_log.jsonl'
      })
      
      if (!fileContent.trim()) return []
      
      const lines = fileContent.trim().split('\n')
      const events: UnifiedEvent[] = []
      
      for (const line of lines) {
        try {
          const entry = JSON.parse(line)
          const isManual = entry.method === 'manual'
          
          events.push({
            id: `rebloom_${entry.timestamp}_${entry.rebloom_id}`,
            timestamp: entry.timestamp,
            type: 'rebloom',
            priority: isManual ? 'high' : 'normal',
            title: `${isManual ? 'Manual' : 'Auto'} Memory Rebloom`,
            description: `${entry.source_id} → ${entry.rebloom_id} | Topic: ${entry.topic} | ${entry.reason}`,
            metadata: {
              source_id: entry.source_id,
              rebloom_id: entry.rebloom_id,
              topic: entry.topic,
              method: entry.method,
              reason: entry.reason
            }
          })
        } catch (e) {
          console.warn('Failed to parse rebloom event:', line)
        }
      }
      
      return events
    } catch (e) {
      console.error('Failed to load rebloom events:', e)
      return []
    }
  }, [])

  // Monitor current consciousness state for spikes
  const monitorConsciousnessSpikes = useCallback((): UnifiedEvent[] => {
    try {
      const currentState = get()
      if (!currentState) return []
      
      const events: UnifiedEvent[] = []
      const now = new Date().toISOString()
      const current = {
        entropy: currentState.entropy || 0,
        scup: currentState.scup || 0,
        heat: 0, // Not available in current state
        tick: currentState.tick_number || 0
      }
      
      // Check for significant spikes
      const entropyDelta = current.entropy - lastMetrics.current.entropy
      const scupDelta = current.scup - lastMetrics.current.scup
      
      // Entropy spike detection
      if (entropyDelta > 0.2 && current.entropy > 0.7) {
        events.push({
          id: `entropy_spike_${current.tick}`,
          timestamp: now,
          tick_number: current.tick,
          type: 'entropy_spike',
          priority: current.entropy > 0.8 ? 'critical' : 'high',
          title: 'Entropy Spike Detected',
          description: `Entropy surged from ${lastMetrics.current.entropy.toFixed(3)} to ${current.entropy.toFixed(3)} (+${entropyDelta.toFixed(3)})`,
          metadata: {
            entropy: current.entropy,
            previous_entropy: lastMetrics.current.entropy,
            delta: entropyDelta
          }
        })
      }
      
      // SCUP spike detection
      if (scupDelta > 10 && current.scup > 35) {
        events.push({
          id: `scup_spike_${current.tick}`,
          timestamp: now,
          tick_number: current.tick,
          type: 'scup_spike',
          priority: current.scup > 50 ? 'critical' : 'high',
          title: 'SCUP Processing Surge',
          description: `SCUP increased from ${lastMetrics.current.scup.toFixed(1)} to ${current.scup.toFixed(1)} (+${scupDelta.toFixed(1)})`,
          metadata: {
            scup: current.scup,
            previous_scup: lastMetrics.current.scup,
            delta: scupDelta
          }
        })
      }
      
      // Update last metrics
      lastMetrics.current = current
      
      return events
    } catch (e) {
      console.error('Failed to monitor consciousness spikes:', e)
      return []
    }
  }, [])

  // Combine and sort all events
  const combineEvents = useCallback((reflectionEvents: UnifiedEvent[], rebloomEvents: UnifiedEvent[], spikeEvents: UnifiedEvent[]): UnifiedEvent[] => {
    const allEvents = [...reflectionEvents, ...rebloomEvents, ...spikeEvents]
    
    // Sort by timestamp (newest first)
    allEvents.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
    
    // Limit to maxEvents
    return allEvents.slice(0, maxEvents)
  }, [maxEvents])

  // Load all events
  const loadAllEvents = useCallback(async () => {
    try {
      const [reflectionEvents, rebloomEvents] = await Promise.all([
        loadReflectionEvents(),
        loadRebloomEvents()
      ])
      
      const spikeEvents = monitorConsciousnessSpikes()
      const combinedEvents = combineEvents(reflectionEvents, rebloomEvents, spikeEvents)
      
      setEvents(prevEvents => {
        // Check for new events
        if (combinedEvents.length > lastEventCount.current) {
          const newCount = combinedEvents.length - lastEventCount.current
          lastEventCount.current = combinedEvents.length
          
          // Auto-scroll if not paused
          setTimeout(scrollToBottom, 100)
        }
        
        return combinedEvents
      })
      
      setError(null)
    } catch (e) {
      setError(`Failed to load events: ${e}`)
    }
  }, [loadReflectionEvents, loadRebloomEvents, monitorConsciousnessSpikes, combineEvents])

  // Scroll to bottom
  const scrollToBottom = () => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight
    }
  }

  // Format timestamp
  const formatTimestamp = (timestamp: string, showDate = false): string => {
    try {
      const date = new Date(timestamp)
      if (showDate) {
        return date.toLocaleDateString('en-US', { 
          hour12: false, 
          hour: '2-digit', 
          minute: '2-digit', 
          second: '2-digit' 
        })
      }
      return date.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
      })
    } catch (e) {
      return timestamp.substring(11, 19) || timestamp.substring(0, 8)
    }
  }

  // Filter events
  const filteredEvents = events.filter(event => 
    true // No filter applied, all events are displayed
  )

  // Set up polling
  useEffect(() => {
    const pollEvents = () => {
      loadAllEvents()
    }

    // Initial load
    loadAllEvents().then(() => {
      setIsLoading(false)
      setTimeout(scrollToBottom, 100)
    })

    // Set up polling interval
    pollIntervalRef.current = window.setInterval(pollEvents, 2000) // Poll every 2 seconds

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
    }
  }, [loadAllEvents])

  if (isLoading) {
    return (
      <div className="event-logger loading">
        <div className="loading-indicator">
          <div className="pulse-dot"></div>
          <span>Loading events...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="event-logger error">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span>Error loading events</span>
        </div>
      </div>
    )
  }

  const recentEvents = events.slice(-maxEvents)

  return (
    <div className="event-logger">
      <div className="logger-header">
        <div className="logger-title">
          <span className="title-text">Recent Events</span>
          <span className="event-count">{events.length}</span>
        </div>
      </div>

      <div 
        ref={containerRef} 
        className="events-container"
      >
        {recentEvents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-text">No recent events</div>
          </div>
        ) : (
          <div className="events-feed">
            {recentEvents.map((event, index) => {
              const config = EVENT_CONFIG[event.type]
              return (
                <div 
                  key={event.id}
                  className={`event-entry ${event.type}`}
                  title={`${config.label}: ${event.description} (${formatTimestamp(event.timestamp)})`}
                >
                  <div className="event-content">
                    <span className="event-emoji">{config.emoji}</span>
                    <span className="event-text">{event.description}</span>
                    <span className="event-time">{formatTimestamp(event.timestamp, true)}</span>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default EventLogger 