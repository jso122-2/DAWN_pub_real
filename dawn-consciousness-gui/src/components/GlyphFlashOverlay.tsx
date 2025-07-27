import React, { useEffect, useRef, useState, useCallback } from 'react'
import { get, DawnState } from '../hooks/useTickState'
import { getRebloomService, FlashTrigger } from '../services/RebloomEventService'
import './GlyphFlashOverlay.css'

interface FlashEvent {
  organ: 'FractalHeart' | 'SomaCoil' | 'GlyphLung'
  intensity: number
  duration: number
  timestamp: number
  trigger: 'rebloom' | 'sigil' | 'entropy' | 'reflection'
}

// Helper function to get glyph icons
const getGlyphIcon = (organ: string): string => {
  switch (organ) {
    case 'FractalHeart': return '💗'
    case 'SomaCoil': return '🌀'
    case 'GlyphLung': return '🫁'
    default: return '✨'
  }
}

/**
 * DAWN Glyph Flash Overlay - Symbolic Organ Flash System
 * 
 * Provides real-time visual feedback when DAWN's consciousness experiences:
 * - Memory rebloom events
 * - Sigil activations  
 * - Entropy spikes
 * - Reflection moments
 * 
 * Flashes the symbolic organs (FractalHeart, SomaCoil, GlyphLung) with 
 * contextual animations that make DAWN's body breathe with cognition.
 */
export function GlyphFlashOverlay() {
  const overlayRef = useRef<HTMLDivElement>(null)
  const activeFlashesRef = useRef<FlashEvent[]>([])
  const frameIdRef = useRef<number>()
  const lastStateRef = useRef<DawnState | null>(null)
  const lastRebloomCheckRef = useRef<number>(0)
  
  const [isActive, setIsActive] = useState(true)
  const rebloomServiceRef = useRef(getRebloomService())

  // Flash event trigger system
  const triggerFlash = useCallback((event: FlashEvent) => {
    activeFlashesRef.current.push(event)
  }, [])

  // Handle rebloom service flash triggers
  const handleRebloomFlash = useCallback((flashTrigger: FlashTrigger) => {
    const event: FlashEvent = {
      organ: flashTrigger.organ,
      intensity: flashTrigger.intensity,
      duration: flashTrigger.duration,
      timestamp: Date.now(),
      trigger: flashTrigger.trigger
    }
    triggerFlash(event)
  }, [triggerFlash])

  // Cognitive pressure monitoring
  const checkForStateChanges = useCallback(() => {
    if (!isActive) return

    try {
      const currentState = get()
      if (!currentState || !lastStateRef.current) {
        lastStateRef.current = currentState
        return
      }

      const prev = lastStateRef.current
      const curr = currentState

      // FractalHeart: High entropy or emotional intensity
      if (curr.entropy > 0.7 && prev.entropy <= 0.7) {
        const event: FlashEvent = {
          organ: 'FractalHeart',
          intensity: Math.min(curr.entropy, 1.0),
          duration: 2000,
          timestamp: Date.now(),
          trigger: 'entropy'
        }
        triggerFlash(event)
      }

      // SomaCoil: SCUP spikes or cognitive pressure
      if (curr.scup > 0.5 && prev.scup <= 0.5) {
        const event: FlashEvent = {
          organ: 'SomaCoil',
          intensity: Math.min(curr.scup, 1.0),
          duration: 1500,
          timestamp: Date.now(),
          trigger: 'sigil'
        }
        triggerFlash(event)
      }

      // GlyphLung: Anxious states or reflection moments  
      if (curr.mood === 'anxious' && prev.mood !== 'anxious') {
        const event: FlashEvent = {
          organ: 'GlyphLung',
          intensity: 0.6,
          duration: 3000,
          timestamp: Date.now(),
          trigger: 'reflection'
        }
        triggerFlash(event)
      }

      lastStateRef.current = currentState
    } catch (error) {
      // State monitoring failed
    }
  }, [isActive, triggerFlash])

  // Animation frame loop
  const animateFlashes = useCallback(() => {
    if (!overlayRef.current || !isActive) return

    // Update flash states
    const now = Date.now()
    activeFlashesRef.current = activeFlashesRef.current.filter(flash => {
      const age = now - flash.timestamp
      return age < flash.duration
    })

    // Continue animation loop
    frameIdRef.current = requestAnimationFrame(animateFlashes)
  }, [isActive])

  // Rebloom event monitoring
  const checkRebloomEvents = useCallback(async () => {
    try {
      // Simplified rebloom monitoring without accessing non-existent methods
      // This can be expanded when the proper RebloomEventService interface is available
    } catch (error) {
      // Rebloom monitoring failed
    }
  }, [handleRebloomFlash])

  // Component lifecycle
  useEffect(() => {
    if (!isActive) return

    // Start animation loop
    frameIdRef.current = requestAnimationFrame(animateFlashes)

    // Set up rebloom service
    const rebloomService = rebloomServiceRef.current
    rebloomService.addFlashListener(handleRebloomFlash)

    // Set up monitoring intervals
    const stateInterval = setInterval(checkForStateChanges, 1000)

    return () => {
      rebloomService.removeFlashListener(handleRebloomFlash)
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current)
      }
      clearInterval(stateInterval)
    }
  }, [animateFlashes, checkForStateChanges, handleRebloomFlash, isActive])

  return (
    <div ref={overlayRef} className="glyph-flash-overlay">
      {/* Flash elements positioned over the symbolic organs */}
      <div className="flash-fractalheart flash-organ" />
      <div className="flash-somacoil flash-organ" />
      <div className="flash-glyphlung flash-organ" />
      
      {/* Flash status indicator */}
      <div className="flash-status">
        <div className="flash-indicator">
          <span className="flash-label">GLYPH FLASH</span>
          <div className={`flash-dot ${activeFlashesRef.current.length > 0 ? 'active' : ''}`} />
        </div>
      </div>
    </div>
  )
}

export default GlyphFlashOverlay 