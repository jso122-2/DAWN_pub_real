import { useEffect, useRef } from 'react'
import { get, DawnState } from '../hooks/useTickState'
import './ThoughtRateHeatmap.css'

interface ThoughtRateData {
  timestamp: number
  tickNumber: number
  hz: number
  entropy: number
}

/**
 * DAWN Thought Rate Heatmap - Temporal Cognition Map
 * 
 * Visualizes tick frequency and cognitive volatility over time
 * as a real-time heatmap with entropy spike overlays
 */
export function ThoughtRateHeatmap() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const frameIdRef = useRef<number>()
  
  // Data storage - circular buffer for 60 seconds of data
  const dataBufferRef = useRef<ThoughtRateData[]>([])
  const bufferIndexRef = useRef<number>(0)
  const maxDataPoints = 60 // 60 seconds @ 1Hz sampling
  
  // Tracking for Hz calculation
  const lastTickRef = useRef<number>(0)
  const lastSampleTimeRef = useRef<number>(0)
  const sampleInterval = 1000 // Sample every 1 second
  
  // Heatmap configuration
  const heatmapConfig = {
    width: 600,
    height: 200,
    padding: { top: 20, right: 40, bottom: 30, left: 40 },
    maxHz: 16,
    barWidth: 8,
    backgroundColor: '#0a1520'
  }
  
  // Color mapping for Hz values
  const getHzColor = (hz: number): string => {
    const normalizedHz = Math.max(0, Math.min(1, hz / heatmapConfig.maxHz))
    
    if (normalizedHz < 0.25) {
      // 0-4 Hz: Cool blue
      const intensity = normalizedHz * 4
      return `rgb(${Math.floor(100 * intensity)}, ${Math.floor(150 * intensity)}, ${Math.floor(255 * (0.6 + 0.4 * intensity))})`
    } else if (normalizedHz < 0.75) {
      // 4-12 Hz: Blue to white transition
      const intensity = (normalizedHz - 0.25) * 2
      const blue = Math.floor(255 * (1 - intensity * 0.5))
      const green = Math.floor(255 * intensity)
      const red = Math.floor(255 * intensity)
      return `rgb(${red}, ${green}, ${blue})`
    } else {
      // 12-16 Hz: White to orange/red
      const intensity = (normalizedHz - 0.75) * 4
      const red = 255
      const green = Math.floor(255 * (1 - intensity * 0.5))
      const blue = Math.floor(100 * (1 - intensity))
      return `rgb(${red}, ${green}, ${blue})`
    }
  }
  
  // Add data point to circular buffer
  const addDataPoint = (tickNumber: number, hz: number, entropy: number) => {
    const now = Date.now()
    const newPoint: ThoughtRateData = {
      timestamp: now,
      tickNumber,
      hz: Math.max(0, Math.min(heatmapConfig.maxHz, hz)), // Clamp to max
      entropy
    }
    
    const buffer = dataBufferRef.current
    
    if (buffer.length < maxDataPoints) {
      buffer.push(newPoint)
    } else {
      // Circular buffer - overwrite oldest point
      buffer[bufferIndexRef.current] = newPoint
      bufferIndexRef.current = (bufferIndexRef.current + 1) % maxDataPoints
    }
  }
  
  // Calculate Hz from tick deltas
  const calculateHz = (currentTick: number, deltaTime: number): number => {
    if (lastTickRef.current === 0) {
      lastTickRef.current = currentTick
      return 0
    }
    
    const tickDelta = currentTick - lastTickRef.current
    lastTickRef.current = currentTick
    
    // Convert to Hz (ticks per second)
    const hz = tickDelta / (deltaTime / 1000)
    return Math.max(0, hz) // Ensure non-negative
  }
  
  // Draw grid and labels
  const drawGrid = (ctx: CanvasRenderingContext2D) => {
    const { width, height, padding } = heatmapConfig
    const plotWidth = width - padding.left - padding.right
    const plotHeight = height - padding.top - padding.bottom
    
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)'
    ctx.lineWidth = 0.5
    ctx.font = '9px Monaco, monospace'
    ctx.fillStyle = '#ffffffb4'
    
    // Horizontal grid lines (Hz levels)
    for (let i = 0; i <= 4; i++) {
      const hz = (heatmapConfig.maxHz * i) / 4
      const y = padding.top + (plotHeight * (4 - i)) / 4
      
      ctx.beginPath()
      ctx.moveTo(padding.left, y)
      ctx.lineTo(width - padding.right, y)
      ctx.stroke()
      
      // Hz labels
      ctx.textAlign = 'right'
      ctx.fillText(`${hz.toFixed(0)}Hz`, padding.left - 5, y + 3)
    }
    
    // Vertical grid lines (time markers)
    for (let i = 0; i <= 6; i++) {
      const x = padding.left + (plotWidth * i) / 6
      ctx.beginPath()
      ctx.moveTo(x, padding.top)
      ctx.lineTo(x, height - padding.bottom)
      ctx.stroke()
      
      // Time labels
      const timeLabel = `${60 - (i * 10)}s`
      ctx.textAlign = 'center'
      ctx.fillText(timeLabel, x, height - 8)
    }
    
    // Axis labels
    ctx.font = '11px Monaco, monospace'
    ctx.textAlign = 'center'
    ctx.fillStyle = '#ffffff'
    ctx.fillText('THOUGHT RATE', width / 2, height - 8)
    
    // Y-axis label (rotated)
    ctx.save()
    ctx.translate(15, height / 2)
    ctx.rotate(-Math.PI / 2)
    ctx.fillText('Hz', 0, 0)
    ctx.restore()
  }
  
  // Draw heatmap bars
  const drawHeatmap = (ctx: CanvasRenderingContext2D) => {
    const { width, height, padding, barWidth } = heatmapConfig
    const plotWidth = width - padding.left - padding.right
    const plotHeight = height - padding.top - padding.bottom
    
    const buffer = dataBufferRef.current
    if (buffer.length === 0) return
    
    // Get ordered data (handle circular buffer)
    let orderedData: ThoughtRateData[] = []
    if (buffer.length < maxDataPoints) {
      orderedData = buffer
    } else {
      orderedData = [
        ...buffer.slice(bufferIndexRef.current),
        ...buffer.slice(0, bufferIndexRef.current)
      ]
    }
    
    // Draw bars
    orderedData.forEach((point, index) => {
      const x = padding.left + (plotWidth * index) / (maxDataPoints - 1) - barWidth / 2
      const barHeight = (plotHeight * point.hz) / heatmapConfig.maxHz
      const y = height - padding.bottom - barHeight
      
      // Get color based on Hz
      const color = getHzColor(point.hz)
      ctx.fillStyle = color
      
      // Add glow effect for high Hz
      if (point.hz > 8) {
        ctx.shadowColor = color
        ctx.shadowBlur = 4
      }
      
      ctx.fillRect(x, y, barWidth, barHeight)
      ctx.shadowBlur = 0 // Reset shadow
      
      // Entropy spike overlay
      if (point.entropy > 0.8) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)'
        ctx.beginPath()
        ctx.arc(x + barWidth / 2, y - 5, 3, 0, Math.PI * 2)
        ctx.fill()
      }
    })
  }
  
  // Main render function
  const render = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    const { width, height } = heatmapConfig
    
    // Clear canvas
    ctx.fillStyle = heatmapConfig.backgroundColor
    ctx.fillRect(0, 0, width, height)
    
    // Draw grid
    drawGrid(ctx)
    
    // Draw heatmap
    drawHeatmap(ctx)
    
    // Draw current Hz indicator
    const buffer = dataBufferRef.current
    if (buffer.length > 0) {
      const latestPoint = buffer[buffer.length - 1] || buffer[bufferIndexRef.current - 1]
      if (latestPoint) {
        ctx.fillStyle = '#00ff88'
        ctx.font = '11px Monaco, monospace'
        ctx.textAlign = 'left'
        ctx.fillText(`Current: ${latestPoint.hz.toFixed(1)} Hz`, heatmapConfig.padding.left, 15)
        
        // Show unexpected drop warning
        if (latestPoint.hz < 2 && buffer.length > 5) {
          const prevPoint = buffer[Math.max(0, buffer.length - 6)]
          if (prevPoint && prevPoint.hz > 6) {
            ctx.fillStyle = '#ff4444'
            ctx.fillText('⚠️ Thought rate drop detected', heatmapConfig.padding.left + 150, 15)
          }
        }
      }
    }
  }
  
  useEffect(() => {
    let isActive = true
    
    const updateLoop = () => {
      if (!isActive) return
      
      const now = Date.now()
      
      // Sample data at regular intervals
      if (now - lastSampleTimeRef.current >= sampleInterval) {
        const currentState = get()
        if (currentState && currentState.tick_number) {
          const deltaTime = now - lastSampleTimeRef.current
          const hz = calculateHz(currentState.tick_number, deltaTime)
          
          addDataPoint(currentState.tick_number, hz, currentState.entropy)
          lastSampleTimeRef.current = now
          
          console.log(`🧠 [THOUGHT RATE] ${hz.toFixed(1)} Hz (tick: ${currentState.tick_number})`)
        }
      }
      
      // Render every frame
      render()
      
      frameIdRef.current = requestAnimationFrame(updateLoop)
    }
    
    frameIdRef.current = requestAnimationFrame(updateLoop)
    
    return () => {
      isActive = false
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current)
      }
    }
  }, [])
  
  return (
    <div className="thought-rate-heatmap">
      <div className="heatmap-header">
        <span className="heatmap-title">🌀 TEMPORAL COGNITION MAP</span>
        <div className="rate-legend">
          <span className="legend-item low">
            <span className="legend-dot low-hz"></span>
            0-4 Hz
          </span>
          <span className="legend-item mid">
            <span className="legend-dot mid-hz"></span>
            4-12 Hz
          </span>
          <span className="legend-item high">
            <span className="legend-dot high-hz"></span>
            12+ Hz
          </span>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={heatmapConfig.width}
        height={heatmapConfig.height}
        className="heatmap-canvas"
      />
      
      <div className="heatmap-footer">
        <span className="volatility-info">
          White dots indicate entropy spikes (&gt;0.8)
        </span>
      </div>
    </div>
  )
}

export default ThoughtRateHeatmap 