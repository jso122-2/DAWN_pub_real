// src/components/DriftGraphPanel.tsx
//! Enhanced SCUP + Entropy Drift Graphs using reusable graph utilities
//! High-performance real-time visualization of DAWN's cognitive metrics

import { useEffect, useRef } from 'react'
import { get, DawnState } from '../hooks/useTickState'
import './DriftGraphPanel.css'

interface DataPoint {
  timestamp: number
  entropy: number
  scup: number
}

/**
 * DAWN Drift Graph Panel - Real-Time Entropy & SCUP Visualization
 * 
 * High-performance canvas-based line graphs with circular buffer storage
 * Updates at ~60fps without React re-renders for smooth consciousness monitoring
 */
export function DriftGraphPanel() {
  // Canvas and rendering refs
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const frameIdRef = useRef<number>()
  
  // Data storage - circular buffers for 60 seconds @ 5Hz = 300 points
  const dataBufferRef = useRef<DataPoint[]>([])
  const bufferIndexRef = useRef<number>(0)
  const maxDataPoints = 300
  
  // Timing for data sampling (collect every ~200ms for smooth curve)
  const lastSampleTimeRef = useRef<number>(0)
  const sampleIntervalMs = 200
  
  // Graph configuration
  const graphConfig = {
    width: 600,
    height: 150,
    padding: { top: 20, right: 80, bottom: 30, left: 50 },
    entropyColor: '#ffffff',
    scupColor: '#8b5cf6',
    gridColor: 'rgba(255, 255, 255, 0.1)',
    textColor: '#ffffffb4',
    backgroundColor: '#0d1b2a'
  }

  // Helper function to add data point to circular buffer
  const addDataPoint = (entropy: number, scup: number) => {
    const now = Date.now()
    const newPoint: DataPoint = {
      timestamp: now,
      entropy: Math.max(0, Math.min(1, entropy)), // Clamp entropy 0-1
      scup: Math.max(0, Math.min(100, scup))      // Clamp SCUP 0-100
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

  // Get current values for display
  const getCurrentValues = (): { entropy: number; scup: number } => {
    const buffer = dataBufferRef.current
    if (buffer.length === 0) return { entropy: 0, scup: 0 }
    
    // Get most recent point
    const lastIndex = buffer.length < maxDataPoints 
      ? buffer.length - 1 
      : (bufferIndexRef.current - 1 + maxDataPoints) % maxDataPoints
    
    return {
      entropy: buffer[lastIndex]?.entropy || 0,
      scup: buffer[lastIndex]?.scup || 0
    }
  }

  // Draw grid lines and labels
  const drawGrid = (ctx: CanvasRenderingContext2D) => {
    const { width, height, padding } = graphConfig
    const plotWidth = width - padding.left - padding.right
    const plotHeight = height - padding.top - padding.bottom
    
    ctx.strokeStyle = graphConfig.gridColor
    ctx.lineWidth = 0.5
    ctx.font = '10px Monaco, monospace'
    ctx.fillStyle = graphConfig.textColor
    
    // Horizontal grid lines (entropy scale 0-1, SCUP scale 0-100)
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (plotHeight * i) / 4
      ctx.beginPath()
      ctx.moveTo(padding.left, y)
      ctx.lineTo(width - padding.right, y)
      ctx.stroke()
      
      // Entropy labels (left side)
      const entropyValue = (1 - i / 4).toFixed(2)
      ctx.textAlign = 'right'
      ctx.fillText(entropyValue, padding.left - 10, y + 3)
      
      // SCUP labels (right side)
      const scupValue = (100 - (i * 25)).toString()
      ctx.textAlign = 'left'
      ctx.fillText(scupValue, width - padding.right + 10, y + 3)
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
      ctx.fillText(timeLabel, x, height - 10)
    }
    
    // Axis labels
    ctx.font = '12px Monaco, monospace'
    ctx.textAlign = 'center'
    ctx.fillStyle = graphConfig.entropyColor
    ctx.fillText('ENTROPY', 25, height / 2)
    
    ctx.fillStyle = graphConfig.scupColor
    ctx.fillText('SCUP', width - 25, height / 2)
  }

  // Draw data line
  const drawLine = (ctx: CanvasRenderingContext2D, data: number[], color: string, scale: number) => {
    if (data.length < 2) return
    
    const { width, height, padding } = graphConfig
    const plotWidth = width - padding.left - padding.right
    const plotHeight = height - padding.top - padding.bottom
    
    ctx.strokeStyle = color
    ctx.lineWidth = 2
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    
    // Add glow effect
    ctx.shadowColor = color
    ctx.shadowBlur = 4
    
    ctx.beginPath()
    
    for (let i = 0; i < data.length; i++) {
      const x = padding.left + (plotWidth * i) / (maxDataPoints - 1)
      const normalizedValue = data[i] / scale
      const y = padding.top + plotHeight - (plotHeight * normalizedValue)
      
      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    }
    
    ctx.stroke()
    ctx.shadowBlur = 0 // Reset shadow
  }

  // Main render function
  const render = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    const { width, height } = graphConfig
    
    // Clear canvas
    ctx.fillStyle = graphConfig.backgroundColor
    ctx.fillRect(0, 0, width, height)
    
    // Draw grid
    drawGrid(ctx)
    
    // Prepare data arrays for rendering
    const buffer = dataBufferRef.current
    
    // Debug info
    console.log(`[DriftGraph] Buffer length: ${buffer.length}, Buffer data:`, buffer.slice(-3))
    
    if (buffer.length === 0) {
      // Draw "No Data" message
      ctx.fillStyle = graphConfig.textColor
      ctx.font = '14px Monaco, monospace'
      ctx.textAlign = 'center'
      ctx.fillText('Waiting for consciousness data...', width / 2, height / 2)
      return
    }
    
    // Get ordered data (handle circular buffer)
    let orderedData: DataPoint[] = []
    if (buffer.length < maxDataPoints) {
      orderedData = buffer
    } else {
      // Reconstruct chronological order from circular buffer
      orderedData = [
        ...buffer.slice(bufferIndexRef.current),
        ...buffer.slice(0, bufferIndexRef.current)
      ]
    }
    
    // Extract entropy and SCUP arrays
    const entropyData = orderedData.map(point => point.entropy)
    const scupData = orderedData.map(point => point.scup)
    
    console.log(`[DriftGraph] Drawing ${entropyData.length} points. Latest entropy: ${entropyData[entropyData.length - 1]}, SCUP: ${scupData[scupData.length - 1]}`)
    
    // Draw lines (even if data is zero - helpful for debugging)
    if (entropyData.length > 1) {
      drawLine(ctx, entropyData, graphConfig.entropyColor, 1.0)   // Entropy scale 0-1
    }
    if (scupData.length > 1) {
      drawLine(ctx, scupData, graphConfig.scupColor, 100.0)       // SCUP scale 0-100
    }
    
    // Draw current value indicators
    const currentValues = getCurrentValues()
    
    // Current entropy marker
    ctx.fillStyle = graphConfig.entropyColor
    ctx.font = '12px Monaco, monospace'
    ctx.textAlign = 'left'
    ctx.fillText(`E: ${currentValues.entropy.toFixed(3)}`, width - 70, 30)
    
    // Current SCUP marker
    ctx.fillStyle = graphConfig.scupColor
    ctx.fillText(`S: ${currentValues.scup.toFixed(1)}`, width - 70, 45)
    
    // Debug info on canvas
    ctx.fillStyle = graphConfig.textColor
    ctx.font = '10px Monaco, monospace'
    ctx.textAlign = 'left'
    ctx.fillText(`Points: ${buffer.length}`, 10, height - 10)
  }

  useEffect(() => {
    let isActive = true
    console.log('📈 [DRIFT GRAPH] Component mounted, starting update loop')

    const updateGraph = () => {
      if (!isActive) return

      const now = Date.now()
      
      // Sample data at regular intervals
      if (now - lastSampleTimeRef.current >= sampleIntervalMs) {
        const currentState = get()
        if (currentState) {
          console.log('📈 [DRIFT GRAPH] Sampling data:', { entropy: currentState.entropy, scup: currentState.scup })
          addDataPoint(currentState.entropy, currentState.scup)
          lastSampleTimeRef.current = now
        } else {
          console.log('📈 [DRIFT GRAPH] No current state available for sampling')
        }
      }
      
      // Render every frame for smooth animation
      render()
      
      // Schedule next frame
      frameIdRef.current = requestAnimationFrame(updateGraph)
    }

    // Start animation loop
    frameIdRef.current = requestAnimationFrame(updateGraph)

    // Cleanup on unmount
    return () => {
      isActive = false
      if (frameIdRef.current) {
        cancelAnimationFrame(frameIdRef.current)
      }
    }
  }, [])

  return (
    <div className="drift-graph-panel">
      <div className="graph-header">
        <span className="graph-title">📈 CONSCIOUSNESS DRIFT ANALYSIS</span>
        <div className="legend">
          <span className="legend-item entropy">
            <span className="legend-dot entropy-dot"></span>
            ENTROPY
          </span>
          <span className="legend-item scup">
            <span className="legend-dot scup-dot"></span>
            SCUP
          </span>
        </div>
      </div>
      
      <canvas
        ref={canvasRef}
        width={graphConfig.width}
        height={graphConfig.height}
        className="drift-canvas"
      />
      
      <div className="graph-footer">
        <span className="time-range">60 Second Rolling Window</span>
      </div>
    </div>
  )
}

export default DriftGraphPanel