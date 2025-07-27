// Clean Event Logger - Reduced Visual Noise with Hover Tooltips
// Displays essential event information with detailed metadata available on hover

import { useState, useRef, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'

interface CleanEvent {
  id: string
  timestamp: string
  tick?: number
  type: 'reflection' | 'rebloom' | 'sigil' | 'heat' | 'scup' | 'entropy' | 'system'
  priority: 'low' | 'normal' | 'high' | 'critical'
  title: string
  summary: string
  details?: {
    entropy?: number
    scup?: number
    heat?: number
    zone?: string
    mood?: string
    source_id?: string
    [key: string]: any
  }
}

const EVENT_STYLES = {
  reflection: { color: '#9b59b6', symbol: '🧠' },
  rebloom: { color: '#4ecdc4', symbol: '🌸' },
  sigil: { color: '#f39c12', symbol: '⚡' },
  heat: { color: '#e74c3c', symbol: '🔥' },
  scup: { color: '#3498db', symbol: '🧬' },
  entropy: { color: '#ff6b6b', symbol: '💥' },
  system: { color: '#95a5a6', symbol: '⚙️' }
}

const PRIORITY_STYLES = {
  low: { opacity: 0.7 },
  normal: { opacity: 0.9 },
  high: { opacity: 1, fontWeight: '600' },
  critical: { opacity: 1, fontWeight: '700', filter: 'brightness(1.2)' }
}

export function CleanEventLogger() {
  const [events, setEvents] = useState<CleanEvent[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [maxEvents] = useState(15)
  
  const containerRef = useRef<HTMLDivElement>(null)
  const pollIntervalRef = useRef<number>()

  // Load and parse events into clean format
  const loadEvents = useCallback(async (): Promise<CleanEvent[]> => {
    try {
      const reflectionContent = await invoke<string>('read_reflection_log', {
        path: 'gui-runtime/logs/reflection.log'
      }).catch(() => '')
      
      const events: CleanEvent[] = []
      
      // Parse reflection events
      if (reflectionContent.trim()) {
        const lines = reflectionContent.trim().split('\n').slice(-10)
        
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
              } else continue
            }
            
            const priority = entropy && parseFloat(entropy) > 0.8 ? 'critical' : 
                           entropy && parseFloat(entropy) > 0.6 ? 'high' : 'normal'
            
            events.push({
              id: `refl_${Date.now()}_${Math.random()}`,
              timestamp: new Date(timestamp).toLocaleTimeString(),
              tick: tick ? parseInt(tick) : undefined,
              type: 'reflection',
              priority: priority as any,
              title: 'Introspective Reflection',
              summary: reflection.length > 50 ? reflection.substring(0, 47) + '...' : reflection,
              details: {
                full_reflection: reflection,
                entropy: entropy ? parseFloat(entropy) : undefined,
                mood,
                scup: scup ? parseFloat(scup) : undefined,
                tick_number: tick ? parseInt(tick) : undefined
              }
            })
          } catch (e) {
            console.warn('Failed to parse reflection line:', line)
          }
        }
      }
      
      // Add simulated system events for demo
      const systemEvents: CleanEvent[] = [
        {
          id: 'sys_1',
          timestamp: new Date().toLocaleTimeString(),
          type: 'system',
          priority: 'normal',
          title: 'Memory Consolidation',
          summary: 'Background memory consolidation completed',
          details: { processed_memories: 42, duration: '1.2s' }
        },
        {
          id: 'sys_2',
          timestamp: new Date(Date.now() - 30000).toLocaleTimeString(),
          type: 'entropy',
          priority: 'high',
          title: 'Entropy Spike',
          summary: 'Cognitive entropy elevated to 0.847',
          details: { entropy: 0.847, trigger: 'complex reasoning', duration: '3.4s' }
        }
      ]
      
      return [...systemEvents, ...events]
        .sort((a, b) => new Date(`1970-01-01 ${b.timestamp}`).getTime() - new Date(`1970-01-01 ${a.timestamp}`).getTime())
        .slice(0, maxEvents)
        
    } catch (error) {
      console.error('Failed to load events:', error)
      return []
    }
  }, [maxEvents])

  useEffect(() => {
    const loadAndSetEvents = async () => {
      setIsLoading(true)
      try {
        const loadedEvents = await loadEvents()
        setEvents(loadedEvents)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load events')
      } finally {
        setIsLoading(false)
      }
    }

    loadAndSetEvents()

    // Refresh every 5 seconds
    pollIntervalRef.current = window.setInterval(loadAndSetEvents, 5000)

    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
    }
  }, [loadEvents])

  const formatTooltipContent = (event: CleanEvent): string => {
    const details = event.details || {}
    const parts = [
      `Type: ${event.type.toUpperCase()}`,
      `Priority: ${event.priority.toUpperCase()}`,
      `Time: ${event.timestamp}`,
      event.tick ? `Tick: ${event.tick}` : null,
    ].filter(Boolean)
    
    if (details.entropy !== undefined) parts.push(`Entropy: ${details.entropy.toFixed(3)}`)
    if (details.scup !== undefined) parts.push(`SCUP: ${details.scup.toFixed(3)}`)
    if (details.mood) parts.push(`Mood: ${details.mood}`)
    if (details.full_reflection) parts.push(`\nReflection: ${details.full_reflection}`)
    if (details.processed_memories) parts.push(`Processed: ${details.processed_memories} memories`)
    if (details.trigger) parts.push(`Trigger: ${details.trigger}`)
    if (details.duration) parts.push(`Duration: ${details.duration}`)
    
    return parts.join('\n')
  }

  if (isLoading) {
    return (
      <div className="loading">
        <div>Loading event stream...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="no-data">
        <div>Failed to load events: {error}</div>
      </div>
    )
  }

  if (events.length === 0) {
    return (
      <div className="no-data">
        <div>No recent events</div>
      </div>
    )
  }

  return (
    <div ref={containerRef} className="clean-event-stream">
      {events.map((event, index) => {
        const eventStyle = EVENT_STYLES[event.type]
        const priorityStyle = PRIORITY_STYLES[event.priority]
        
        return (
          <div
            key={event.id}
            className="event-item"
            style={{ 
              ...priorityStyle,
              borderLeftColor: eventStyle.color,
              animationDelay: `${index * 0.1}s`
            }}
            title={formatTooltipContent(event)}
          >
            <div className="event-header">
              <span 
                className="event-symbol" 
                style={{ color: eventStyle.color }}
              >
                {eventStyle.symbol}
              </span>
              <span className="event-title">{event.title}</span>
              <span className="event-time">{event.timestamp}</span>
            </div>
            <div className="event-summary">{event.summary}</div>
          </div>
        )
      })}
      
      <style>{`
        .clean-event-stream {
          display: flex;
          flex-direction: column;
          gap: var(--spacing-sm);
          max-height: 100%;
          overflow-y: auto;
        }
        
        .event-item {
          background: var(--color-overlay);
          border: 1px solid var(--color-border);
          border-left: 3px solid var(--color-border);
          border-radius: calc(var(--border-radius) - 2px);
          padding: var(--spacing-sm) var(--spacing-md);
          transition: all var(--animation-normal);
          animation: fadeInUp 0.3s ease forwards;
          opacity: 0;
          transform: translateY(10px);
          cursor: pointer;
        }
        
        .event-item:hover {
          background: var(--color-overlay-hover);
          border-color: var(--color-border-hover);
          transform: translateY(-1px);
        }
        
        .event-header {
          display: flex;
          align-items: center;
          gap: var(--spacing-sm);
          margin-bottom: var(--spacing-xs);
        }
        
        .event-symbol {
          font-size: 14px;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 20px;
          flex-shrink: 0;
        }
        
        .event-title {
          font-size: var(--font-size-label);
          font-weight: 600;
          color: var(--color-text-primary);
          text-transform: uppercase;
          letter-spacing: 0.3px;
          flex: 1;
        }
        
        .event-time {
          font-size: var(--font-size-micro);
          color: var(--color-text-muted);
          font-weight: 500;
        }
        
        .event-summary {
          font-size: var(--font-size-small);
          color: var(--color-text-secondary);
          line-height: 1.3;
          margin-left: 28px;
        }
        
        @keyframes fadeInUp {
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .loading, .no-data {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: var(--spacing-xxl);
          color: var(--color-text-tertiary);
          font-size: var(--font-size-label);
          text-align: center;
        }
      `}</style>
    </div>
  )
} 