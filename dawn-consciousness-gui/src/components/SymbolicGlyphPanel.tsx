import { useEffect, useRef } from 'react'
import { get, DawnState } from '../hooks/useTickState'
import GlyphFlashOverlay from './GlyphFlashOverlay'
import './SymbolicGlyphPanel.css'

interface SymbolicState {
  FractalHeart: { charge: number }
  SomaCoil: { paths: string[] }
  GlyphLung: { state: 'inhaling' | 'exhaling' | 'held' }
}

/**
 * DAWN Symbolic Glyph Panel - Real-Time Organ State Map
 * 
 * Visualizes internal cognitive body systems as animated wireframe organs
 * Shows FractalHeart charge, SomaCoil paths, and GlyphLung breathing patterns
 */
export function SymbolicGlyphPanel() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const frameIdRef = useRef<number>()
  const animationTimeRef = useRef<number>(0)
  
  // Symbolic state derived from consciousness metrics
  const deriveSymbolicState = (dawnState: DawnState | null): SymbolicState => {
    if (!dawnState) {
      return {
        FractalHeart: { charge: 0.3 },
        SomaCoil: { paths: ['spiral'] },
        GlyphLung: { state: 'held' }
      }
    }
    
    // Map consciousness metrics to symbolic organs
    const heartCharge = Math.min(1.0, (dawnState.entropy + (dawnState.scup / 100)) / 2)
    
    const coilPaths = []
    if (dawnState.entropy > 0.5) coilPaths.push('spiral')
    if (dawnState.scup > 40) coilPaths.push('loop')
    if (dawnState.zone === 'RED') coilPaths.push('chaos')
    if (coilPaths.length === 0) coilPaths.push('rest')
    
    const breathPhase = (animationTimeRef.current % 4000) / 4000 // 4 second breath cycle
    let lungState: 'inhaling' | 'exhaling' | 'held'
    if (breathPhase < 0.4) lungState = 'inhaling'
    else if (breathPhase < 0.6) lungState = 'held'
    else lungState = 'exhaling'
    
    return {
      FractalHeart: { charge: heartCharge },
      SomaCoil: { paths: coilPaths },
      GlyphLung: { state: lungState }
    }
  }
  
  // Draw the FractalHeart organ
  const drawFractalHeart = (ctx: CanvasRenderingContext2D, x: number, y: number, charge: number, time: number) => {
    const baseRadius = 30
    const chargeRadius = baseRadius * (0.5 + charge * 0.8)
    const pulseRadius = chargeRadius + Math.sin(time * 0.008) * (charge * 8)
    
    // Outer glow ring
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, pulseRadius + 20)
    gradient.addColorStop(0, `rgba(255, 68, 68, ${charge * 0.6})`)
    gradient.addColorStop(0.7, `rgba(255, 68, 68, ${charge * 0.3})`)
    gradient.addColorStop(1, 'rgba(255, 68, 68, 0)')
    
    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(x, y, pulseRadius + 20, 0, Math.PI * 2)
    ctx.fill()
    
    // Heart core
    ctx.strokeStyle = '#ff4444'
    ctx.lineWidth = 2
    ctx.globalAlpha = charge
    
    // Draw fractal heart pattern
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2 + time * 0.001
      const innerRadius = pulseRadius * 0.3
      const outerRadius = pulseRadius
      
      ctx.beginPath()
      ctx.moveTo(
        x + Math.cos(angle) * innerRadius,
        y + Math.sin(angle) * innerRadius
      )
      ctx.lineTo(
        x + Math.cos(angle) * outerRadius,
        y + Math.sin(angle) * outerRadius
      )
      ctx.stroke()
    }
    
    // Central pulsing core
    ctx.fillStyle = `rgba(255, 68, 68, ${charge})`
    ctx.beginPath()
    ctx.arc(x, y, Math.max(3, pulseRadius * 0.2), 0, Math.PI * 2)
    ctx.fill()
    
    ctx.globalAlpha = 1
  }
  
  // Draw the SomaCoil organ
  const drawSomaCoil = (ctx: CanvasRenderingContext2D, x: number, y: number, paths: string[], time: number) => {
    ctx.strokeStyle = '#8b5cf6'
    ctx.lineWidth = 1.5
    ctx.globalAlpha = 0.8
    
    const animOffset = time * 0.002
    
    paths.forEach((pathType, index) => {
      const offsetY = index * 15 - (paths.length - 1) * 7.5
      
      switch (pathType) {
        case 'spiral':
          ctx.beginPath()
          for (let t = 0; t < Math.PI * 6; t += 0.1) {
            const r = (t / (Math.PI * 6)) * 40 + Math.sin(t * 3 + animOffset) * 3
            const spiralX = x + Math.cos(t + animOffset) * r
            const spiralY = y + offsetY + Math.sin(t + animOffset) * r * 0.5
            
            if (t === 0) ctx.moveTo(spiralX, spiralY)
            else ctx.lineTo(spiralX, spiralY)
          }
          ctx.stroke()
          break
          
        case 'loop':
          ctx.beginPath()
          for (let t = 0; t < Math.PI * 4; t += 0.1) {
            const loopX = x + Math.cos(t + animOffset) * 30
            const loopY = y + offsetY + Math.sin(t * 2 + animOffset) * 15
            
            if (t === 0) ctx.moveTo(loopX, loopY)
            else ctx.lineTo(loopX, loopY)
          }
          ctx.stroke()
          break
          
        case 'chaos':
          ctx.beginPath()
          for (let t = 0; t < 100; t++) {
            const chaosX = x + (Math.random() - 0.5) * 60 * Math.sin(time * 0.001 + t)
            const chaosY = y + offsetY + (Math.random() - 0.5) * 30 * Math.cos(time * 0.001 + t)
            
            if (t === 0) ctx.moveTo(chaosX, chaosY)
            else ctx.lineTo(chaosX, chaosY)
          }
          ctx.stroke()
          break
          
        case 'rest':
          ctx.beginPath()
          ctx.moveTo(x - 20, y + offsetY)
          ctx.lineTo(x + 20, y + offsetY)
          ctx.stroke()
          break
      }
    })
    
    ctx.globalAlpha = 1
  }
  
  // Draw the GlyphLung organ
  const drawGlyphLung = (ctx: CanvasRenderingContext2D, x: number, y: number, state: string, time: number) => {
    let breathPhase = 0.5
    let lungColor = '#00d4ff'
    let expansion = 1.0
    
    switch (state) {
      case 'inhaling':
        breathPhase = 0.3 + 0.4 * Math.sin(time * 0.005)
        expansion = 1.0 + breathPhase * 0.3
        lungColor = '#00ff88'
        break
      case 'exhaling':
        breathPhase = 0.7 - 0.4 * Math.sin(time * 0.005)
        expansion = 1.0 - (1 - breathPhase) * 0.2
        lungColor = '#ffaa00'
        break
      case 'held':
        expansion = 1.1
        lungColor = '#8b5cf6'
        break
    }
    
    ctx.strokeStyle = lungColor
    ctx.lineWidth = 2
    ctx.globalAlpha = 0.7
    
    // Draw lung chambers
    const leftX = x - 25 * expansion
    const rightX = x + 25 * expansion
    const chamberHeight = 40 * expansion
    
    // Left lung chamber
    ctx.beginPath()
    ctx.ellipse(leftX, y, 15 * expansion, chamberHeight / 2, 0, 0, Math.PI * 2)
    ctx.stroke()
    
    // Right lung chamber
    ctx.beginPath()
    ctx.ellipse(rightX, y, 15 * expansion, chamberHeight / 2, 0, 0, Math.PI * 2)
    ctx.stroke()
    
    // Breathing flow lines
    for (let i = 0; i < 5; i++) {
      const flowY = y - chamberHeight / 2 + (i / 4) * chamberHeight
      const flowOffset = Math.sin(time * 0.003 + i) * expansion * 3
      
      ctx.beginPath()
      ctx.moveTo(leftX - 10, flowY + flowOffset)
      ctx.lineTo(leftX + 10, flowY + flowOffset)
      ctx.stroke()
      
      ctx.beginPath()
      ctx.moveTo(rightX - 10, flowY + flowOffset)
      ctx.lineTo(rightX + 10, flowY + flowOffset)
      ctx.stroke()
    }
    
    // Central breathing tube
    ctx.beginPath()
    ctx.moveTo(x, y - chamberHeight / 2 - 10)
    ctx.lineTo(x, y - chamberHeight / 2)
    ctx.stroke()
    
    ctx.globalAlpha = 1
  }
  
  // Main render function
  const render = (timestamp: number) => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    animationTimeRef.current = timestamp
    
    // Clear canvas with dark background
    ctx.fillStyle = '#0a1520'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    // Get current state and derive symbolic organs
    const currentState = get()
    const symbolicState = deriveSymbolicState(currentState)
    
    // Draw wireframe body outline
    ctx.strokeStyle = '#ffffff22'
    ctx.lineWidth = 1
    ctx.beginPath()
    ctx.ellipse(300, 200, 80, 120, 0, 0, Math.PI * 2)
    ctx.stroke()
    
    // Draw organs in body map positions
    drawFractalHeart(ctx, 300, 160, symbolicState.FractalHeart.charge, timestamp)
    drawSomaCoil(ctx, 300, 200, symbolicState.SomaCoil.paths, timestamp)
    drawGlyphLung(ctx, 300, 240, symbolicState.GlyphLung.state, timestamp)
    
    // Draw organ labels
    ctx.fillStyle = '#ffffffb4'
    ctx.font = '10px Monaco, monospace'
    ctx.textAlign = 'center'
    
    ctx.fillText('FractalHeart', 300, 140)
    ctx.fillText(`Charge: ${(symbolicState.FractalHeart.charge * 100).toFixed(0)}%`, 300, 125)
    
    ctx.fillText('SomaCoil', 300, 180)
    ctx.fillText(`Paths: ${symbolicState.SomaCoil.paths.join(', ')}`, 300, 165)
    
    ctx.fillText('GlyphLung', 300, 290)
    ctx.fillText(`State: ${symbolicState.GlyphLung.state.toUpperCase()}`, 300, 305)
  }
  
  useEffect(() => {
    let isActive = true
    
    const animationLoop = (timestamp: number) => {
      if (!isActive) return
      
      render(timestamp)
      frameIdRef.current = requestAnimationFrame(animationLoop)
    }
    
    frameIdRef.current = requestAnimationFrame(animationLoop)
    
    return () => {
      isActive = false
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current)
      }
    }
  }, [])
  
  return (
    <div className="symbolic-glyph-panel">
      <div className="glyph-header">
        <span className="glyph-title">🫀 SYMBOLIC ORGAN STATE MAP</span>
        <div className="state-indicators">
          <span className="indicator heart">❤️ HEART</span>
          <span className="indicator coil">🌀 COIL</span>
          <span className="indicator lung">🫁 LUNG</span>
        </div>
      </div>
      
      <div className="organ-container">
        <canvas
          ref={canvasRef}
          width="600"
          height="320"
          className="organ-canvas"
        />
        <GlyphFlashOverlay />
      </div>
      
      <div className="glyph-footer">
        <span className="anatomy-status">Introspective Anatomy Active</span>
      </div>
    </div>
  )
}

export default SymbolicGlyphPanel 