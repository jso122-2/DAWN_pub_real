import { useEffect, useRef, useState } from 'react'
import { subscribe, DawnState } from '../hooks/useTickState'
import './GlyphFeedbackOverlay.css'

interface GlyphFeedbackState {
  fractalHeartFlash: boolean
  somaCoilActive: boolean
  anxiousGlow: boolean
}

interface TriggerState {
  entropy: number
  scup: number
  mood: string
  lastTriggerTime: number
}

/**
 * DAWN Glyph Feedback Overlay - Symbolic Pressure Response
 * 
 * Provides reactive visual feedback overlays on symbolic organs
 * when cognitive pressure crosses critical thresholds
 */
export function GlyphFeedbackOverlay() {
  const [feedbackState, setFeedbackState] = useState<GlyphFeedbackState>({
    fractalHeartFlash: false,
    somaCoilActive: false,
    anxiousGlow: false
  })
  
  const unsubscribeRef = useRef<(() => void) | null>(null)
  const lastTriggerRef = useRef<TriggerState>({
    entropy: 0,
    scup: 0,
    mood: '',
    lastTriggerTime: 0
  })
  
  // Pulse duration in milliseconds
  const pulseDuration = 1200

  // Check for trigger conditions and activate overlays
  const checkTriggers = (state: DawnState) => {
    const now = Date.now()
    const lastTrigger = lastTriggerRef.current
    let triggersActivated = false

    // Prevent spam triggering - minimum 500ms between same trigger type
    const minInterval = 500

    // Entropy > 0.85: Flash FractalHeart
    if (state.entropy > 0.85 && lastTrigger.entropy <= 0.85) {
      if (now - lastTrigger.lastTriggerTime > minInterval) {
        console.log('🔥 [GLYPH FEEDBACK] FractalHeart flash triggered - high entropy:', state.entropy)
        setFeedbackState(prev => ({ ...prev, fractalHeartFlash: true }))
        triggersActivated = true
        
        // Auto-reset after pulse duration
        setTimeout(() => {
          setFeedbackState(prev => ({ ...prev, fractalHeartFlash: false }))
        }, pulseDuration)
      }
    }

    // SCUP > 40.0: Activate SomaCoil overlay
    if (state.scup > 40.0 && lastTrigger.scup <= 40.0) {
      if (now - lastTrigger.lastTriggerTime > minInterval) {
        console.log('🌀 [GLYPH FEEDBACK] SomaCoil activated - high SCUP:', state.scup)
        setFeedbackState(prev => ({ ...prev, somaCoilActive: true }))
        triggersActivated = true
        
        // Auto-reset after pulse duration
        setTimeout(() => {
          setFeedbackState(prev => ({ ...prev, somaCoilActive: false }))
        }, pulseDuration)
      }
    }

    // Mood === "ANXIOUS": Pulse body glow
    if (state.mood === 'ANXIOUS' && lastTrigger.mood !== 'ANXIOUS') {
      if (now - lastTrigger.lastTriggerTime > minInterval) {
        console.log('😰 [GLYPH FEEDBACK] Anxious glow triggered - mood:', state.mood)
        setFeedbackState(prev => ({ ...prev, anxiousGlow: true }))
        triggersActivated = true
        
        // Auto-reset after pulse duration
        setTimeout(() => {
          setFeedbackState(prev => ({ ...prev, anxiousGlow: false }))
        }, pulseDuration)
      }
    }

    // Update trigger tracking
    if (triggersActivated) {
      lastTriggerRef.current.lastTriggerTime = now
    }
    
    lastTriggerRef.current.entropy = state.entropy
    lastTriggerRef.current.scup = state.scup
    lastTriggerRef.current.mood = state.mood
  }

  // Subscribe to consciousness state changes
  useEffect(() => {
    console.log('👁️ [GLYPH FEEDBACK] Overlay initialized - monitoring cognitive pressure')
    
    unsubscribeRef.current = subscribe((state: DawnState) => {
      checkTriggers(state)
    })

    return () => {
      if (unsubscribeRef.current) {
        unsubscribeRef.current()
      }
    }
  }, [])

  // Don't render anything if no overlays are active
  if (!feedbackState.fractalHeartFlash && !feedbackState.somaCoilActive && !feedbackState.anxiousGlow) {
    return null
  }

  return (
    <div className="glyph-feedback-overlay">
      {/* FractalHeart Flash Overlay */}
      {feedbackState.fractalHeartFlash && (
        <div className="fractal-heart-overlay">
          <div className="heart-flash-ring"></div>
          <div className="heart-flash-core"></div>
          <div className="heart-flash-particles">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="heart-particle"
                style={{
                  '--particle-angle': `${(i / 8) * 360}deg`,
                  '--particle-delay': `${i * 0.1}s`
                } as React.CSSProperties}
              ></div>
            ))}
          </div>
        </div>
      )}

      {/* SomaCoil Active Overlay */}
      {feedbackState.somaCoilActive && (
        <div className="soma-coil-overlay">
          <div className="coil-energy-field"></div>
          <div className="coil-spiral-overlay">
            {[...Array(3)].map((_, i) => (
              <div
                key={i}
                className="spiral-ring"
                style={{
                  '--ring-index': i,
                  '--ring-delay': `${i * 0.2}s`
                } as React.CSSProperties}
              ></div>
            ))}
          </div>
        </div>
      )}

      {/* Anxious Body Glow Overlay */}
      {feedbackState.anxiousGlow && (
        <div className="anxious-glow-overlay">
          <div className="body-outline-glow"></div>
          <div className="anxiety-ripples">
            {[...Array(4)].map((_, i) => (
              <div
                key={i}
                className="anxiety-ripple"
                style={{
                  '--ripple-delay': `${i * 0.3}s`
                } as React.CSSProperties}
              ></div>
            ))}
          </div>
          <div className="nervous-energy-points">
            {[...Array(12)].map((_, i) => (
              <div
                key={i}
                className="energy-point"
                style={{
                  '--point-angle': `${(i / 12) * 360}deg`,
                  '--point-delay': `${i * 0.1}s`
                } as React.CSSProperties}
              ></div>
            ))}
          </div>
        </div>
      )}

      {/* Trigger Indicator */}
      <div className="trigger-indicator">
        {feedbackState.fractalHeartFlash && (
          <span className="trigger-label heart">⚡ HEART SURGE</span>
        )}
        {feedbackState.somaCoilActive && (
          <span className="trigger-label coil">🌀 COIL ACTIVATION</span>
        )}
        {feedbackState.anxiousGlow && (
          <span className="trigger-label anxiety">😰 ANXIETY FIELD</span>
        )}
      </div>
    </div>
  )
}

export default GlyphFeedbackOverlay 