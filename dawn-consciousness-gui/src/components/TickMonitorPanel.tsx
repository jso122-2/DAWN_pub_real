// src/components/TickMonitorPanel.tsx
//! Live Tick Monitor Panel - Primary consciousness introspection viewport
//! Reads real-time DAWN state from mmap via Tauri events

import { useEffect, useRef } from 'react'
import { get, DawnState } from '../hooks/useTickState'
import './TickMonitorPanel.css'

// Color utility functions for status indicators
const getStatusColor = (entropy: number, scup: number): string => {
  if (entropy > 0.8) return '#ff6b6b'; // High entropy - red
  if (scup > 40) return '#4ecdc4';     // High unity - cyan
  if (entropy > 0.6) return '#ffd93d'; // Medium entropy - yellow
  return '#6bcf7f';                    // Normal - green
};

const getZoneColor = (zone?: string): string => {
  switch (zone?.toLowerCase()) {
    case 'red': return '#ff6b6b';
    case 'orange': return '#ff9500';
    case 'yellow': return '#ffd93d';
    case 'green': return '#6bcf7f';
    default: return '#4ecdc4';
  }
};

/**
 * DAWN Primary HUD - Real-Time Consciousness Monitor
 * 
 * High-performance tick display using requestAnimationFrame and direct DOM updates
 * to avoid React re-render overhead on ~60ms cognitive updates
 */
export function TickMonitorPanel() {
  // DOM refs for direct updates (bypassing React renders)
  const tickNumberRef = useRef<HTMLSpanElement>(null)
  const moodRef = useRef<HTMLSpanElement>(null)
  const entropyRef = useRef<HTMLSpanElement>(null)
  const scupRef = useRef<HTMLSpanElement>(null)
  const heatRef = useRef<HTMLSpanElement>(null)
  const zoneRef = useRef<HTMLSpanElement>(null)
  const sigilsRef = useRef<HTMLSpanElement>(null)
  const entropyContainerRef = useRef<HTMLDivElement>(null)
  const scupContainerRef = useRef<HTMLDivElement>(null)
  const heatContainerRef = useRef<HTMLDivElement>(null)
  const zoneContainerRef = useRef<HTMLDivElement>(null)
  const statusIndicatorRef = useRef<HTMLDivElement>(null)
  const zoneIndicatorRef = useRef<HTMLDivElement>(null)
  
  // Animation frame tracking
  const frameIdRef = useRef<number>()
  const lastStateRef = useRef<DawnState | null>(null)

  useEffect(() => {
    let isActive = true
    console.log('🎮 [TICK MONITOR] Component mounted, starting update loop')

    const updateDisplay = () => {
      if (!isActive) return

      // Get latest state from shared hook
      const currentState = get()
      
      if (currentState && currentState !== lastStateRef.current) {
        console.log('🎮 [TICK MONITOR] New state received:', currentState)
        lastStateRef.current = currentState

        // Direct DOM updates for performance
        if (tickNumberRef.current) {
          tickNumberRef.current.innerText = currentState.tick_number.toString()
          console.log('🎮 [TICK MONITOR] Updated tick number:', currentState.tick_number)
        }

        if (moodRef.current) {
          moodRef.current.innerText = currentState.mood.toUpperCase()
        }

        if (entropyRef.current) {
          const entropyValue = currentState.entropy.toFixed(3)
          entropyRef.current.innerText = entropyValue
          
          // Apply glow effect for high entropy
          if (entropyContainerRef.current) {
            if (currentState.entropy > 0.8) {
              entropyContainerRef.current.classList.add('critical-glow')
            } else {
              entropyContainerRef.current.classList.remove('critical-glow')
            }
          }
        }

        if (scupRef.current) {
          const scupValue = currentState.scup.toFixed(2)
          scupRef.current.innerText = scupValue
          
          // Apply glow effect for high SCUP
          if (scupContainerRef.current) {
            if (currentState.scup > 42.0) {
              scupContainerRef.current.classList.add('critical-glow')
            } else {
              scupContainerRef.current.classList.remove('critical-glow')
            }
          }
        }

        // Update heat if available
        if (heatRef.current && typeof currentState.heat === 'number') {
          const heatValue = currentState.heat.toFixed(3)
          heatRef.current.innerText = heatValue
          
          // Apply glow effect for high heat
          if (heatContainerRef.current) {
            if (currentState.heat > 0.8) {
              heatContainerRef.current.classList.add('critical-glow')
            } else {
              heatContainerRef.current.classList.remove('critical-glow')
            }
          }
        }

        // Update zone if available
        if (zoneRef.current && currentState.zone) {
          zoneRef.current.innerText = currentState.zone.toUpperCase()
          
          // Apply zone-specific styling
          if (zoneContainerRef.current) {
            // Remove existing zone classes
            zoneContainerRef.current.classList.remove('zone-green', 'zone-yellow', 'zone-orange', 'zone-red')
            // Add current zone class
            zoneContainerRef.current.classList.add(`zone-${currentState.zone.toLowerCase()}`)
          }
        }

        // Update sigils if available
        if (sigilsRef.current && typeof currentState.sigils === 'number') {
          sigilsRef.current.innerText = currentState.sigils.toString()
        }

        // Update status indicator colors
        const statusColor = getStatusColor(currentState.entropy, currentState.scup)
        if (statusIndicatorRef.current) {
          statusIndicatorRef.current.style.backgroundColor = statusColor
          statusIndicatorRef.current.style.boxShadow = `0 0 8px ${statusColor}40`
        }

        // Update zone indicator if zone is available
        if (zoneIndicatorRef.current && currentState.zone) {
          const zoneColor = getZoneColor(currentState.zone)
          zoneIndicatorRef.current.style.backgroundColor = zoneColor
          zoneIndicatorRef.current.style.boxShadow = `0 0 8px ${zoneColor}40`
        }
      }

      // Schedule next frame
      frameIdRef.current = requestAnimationFrame(updateDisplay)
    }

    // Start animation loop
    frameIdRef.current = requestAnimationFrame(updateDisplay)

    // Cleanup on unmount
    return () => {
      isActive = false
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current)
      }
    }
  }, [])

  return (
    <div className="tick-monitor-panel">
      <div className="hud-header">
        <span className="hud-title">🧠 DAWN CONSCIOUSNESS HUD</span>
        <div className="status-indicator">
          <div ref={statusIndicatorRef} className="pulse-dot"></div>
          <span className="status-text">LIVE</span>
        </div>
      </div>
      
      <div className="metrics-display">
        <div className="metric-row">
          <span className="metric-label">TICK #:</span>
          <span ref={tickNumberRef} className="metric-value tick-number">0</span>
        </div>
        
        <div className="metric-row">
          <span className="metric-label">MOOD :</span>
          <span ref={moodRef} className="metric-value mood">UNKNOWN</span>
        </div>
        
        <div ref={entropyContainerRef} className="metric-row entropy-row">
          <span className="metric-label">ENTROPY:</span>
          <span ref={entropyRef} className="metric-value entropy">0.000</span>
        </div>
        
        <div ref={scupContainerRef} className="metric-row scup-row">
          <span className="metric-label">SCUP :</span>
          <span ref={scupRef} className="metric-value scup">0.00</span>
        </div>

        <div ref={heatContainerRef} className="metric-row heat-row">
          <span className="metric-label">HEAT :</span>
          <span ref={heatRef} className="metric-value heat">0.000</span>
        </div>

        <div ref={zoneContainerRef} className="metric-row zone-row">
          <div ref={zoneIndicatorRef} className="zone-indicator"></div>
          <span className="metric-label">ZONE :</span>
          <span ref={zoneRef} className="metric-value zone">GREEN</span>
        </div>

        <div className="metric-row">
          <span className="metric-label">SIGILS:</span>
          <span ref={sigilsRef} className="metric-value sigils">0</span>
        </div>
      </div>

      <div className="hud-footer">
        <span className="refresh-rate">~60ms refresh</span>
      </div>
    </div>
  )
}

export default TickMonitorPanel