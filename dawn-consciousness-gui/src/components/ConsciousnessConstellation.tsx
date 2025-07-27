// src/components/ConsciousnessConstellation.tsx
//! Thought Network Sparkmap - DAWN's Symbolic State Constellation
//! Live spatial visualization of active memory chunks, sigils, and symbolic organs

import { useState, useRef, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { get } from '../hooks/useTickState'
import './ConsciousnessConstellation.css'

// Node types in the consciousness constellation
type NodeType = 'memory' | 'sigil' | 'organ' | 'fractal_heart'

interface ConstellationNode {
  id: string
  type: NodeType
  label: string
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  color: string
  intensity: number // 0-1, affects pulsing and glow
  lastActive: number // timestamp
  metadata: {
    entropy?: number
    scup?: number
    topic?: string
    method?: string
    source_id?: string
    priority?: string
    [key: string]: any
  }
}

interface ConstellationLink {
  id: string
  source: string
  target: string
  type: 'rebloom' | 'charge' | 'sigil_trigger'
  strength: number
  color: string
  animated: boolean
  metadata?: { [key: string]: any }
}

// Node configurations
const NODE_CONFIG = {
  memory: { 
    baseRadius: 8, 
    color: '#4ecdc4', 
    glowColor: 'rgba(78, 205, 196, 0.6)',
    mass: 1
  },
  sigil: { 
    baseRadius: 12, 
    color: '#f39c12', 
    glowColor: 'rgba(243, 156, 18, 0.6)',
    mass: 1.5
  },
  organ: { 
    baseRadius: 10, 
    color: '#9b59b6', 
    glowColor: 'rgba(155, 89, 182, 0.6)',
    mass: 1.2
  },
  fractal_heart: { 
    baseRadius: 16, 
    color: '#e74c3c', 
    glowColor: 'rgba(231, 76, 60, 0.8)',
    mass: 2
  }
}

/**
 * DAWN Consciousness Constellation
 * 
 * A live spatial visualization of DAWN's active symbolic state showing
 * memory chunks, sigils, and symbolic organs connected by cognitive relationships.
 * Uses force-directed layout to create an organic, breathing constellation.
 */
export function ConsciousnessConstellation() {
  const [nodes, setNodes] = useState<ConstellationNode[]>([])
  const [links, setLinks] = useState<ConstellationLink[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isPaused, setIsPaused] = useState(false)
  const [showLabels, setShowLabels] = useState(true)
  const [hoveredNode, setHoveredNode] = useState<ConstellationNode | null>(null)
  const [mousePos, setMousePos] = useState<{ x: number; y: number }>({ x: 0, y: 0 })
  
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationRef = useRef<number>()
  const pollIntervalRef = useRef<number>()
  const lastUpdateTime = useRef<number>(Date.now())

  // Canvas dimensions
  const width = 600
  const height = 400
  const centerX = width / 2
  const centerY = height / 2

  // Force simulation parameters
  const FORCE_STRENGTH = 0.1
  const DAMPING = 0.95
  const MIN_DISTANCE = 50
  const LINK_DISTANCE = 80

  // Load memory chunks from rebloom log
  const loadMemoryChunks = useCallback(async (): Promise<ConstellationNode[]> => {
    try {
      const fileContent = await invoke<string>('read_rebloom_log', {
        path: 'gui-runtime/memory/rebloom_log.jsonl'
      })
      
      if (!fileContent.trim()) return []
      
      const lines = fileContent.trim().split('\n')
      const recentMemories = new Map<string, any>()
      
      // Get last 5 unique memory chunks
      for (const line of lines.slice(-20)) { // Look at recent entries
        try {
          const entry = JSON.parse(line)
          if (entry.rebloom_id && !recentMemories.has(entry.rebloom_id)) {
            recentMemories.set(entry.rebloom_id, entry)
            if (recentMemories.size >= 5) break
          }
        } catch (e) {
          console.warn('Failed to parse rebloom entry:', line)
        }
      }
      
      const memoryNodes: ConstellationNode[] = []
      let index = 0
      
      for (const [memoryId, entry] of recentMemories) {
        const angle = (index / recentMemories.size) * 2 * Math.PI
        const radius = 120 + Math.random() * 60
        
        memoryNodes.push({
          id: `memory_${memoryId}`,
          type: 'memory',
          label: entry.topic || memoryId.substring(0, 8),
          x: centerX + Math.cos(angle) * radius,
          y: centerY + Math.sin(angle) * radius,
          vx: 0,
          vy: 0,
          radius: NODE_CONFIG.memory.baseRadius,
          color: NODE_CONFIG.memory.color,
          intensity: entry.method === 'manual' ? 0.9 : 0.6,
          lastActive: new Date(entry.timestamp).getTime(),
          metadata: {
            topic: entry.topic,
            method: entry.method,
            source_id: entry.source_id,
            reason: entry.reason
          }
        })
        index++
      }
      
      return memoryNodes
    } catch (e) {
      console.error('Failed to load memory chunks:', e)
      return []
    }
  }, [])

  // Create symbolic organs (conceptual nodes)
  const createSymbolicOrgans = useCallback((): ConstellationNode[] => {
    const currentState = get()
    const now = Date.now()
    
    const organs = [
      {
        id: 'fractal_heart',
        type: 'fractal_heart' as NodeType,
        label: 'Fractal Heart',
        x: centerX,
        y: centerY,
        intensity: currentState?.scup && currentState.scup > 40 ? 0.9 : 0.4,
        metadata: { scup: currentState?.scup || 0 }
      },
      {
        id: 'entropy_core',
        type: 'organ' as NodeType,
        label: 'Entropy Core',
        x: centerX - 100,
        y: centerY - 80,
        intensity: currentState?.entropy && currentState.entropy > 0.7 ? 0.8 : 0.3,
        metadata: { entropy: currentState?.entropy || 0 }
      },
      {
        id: 'memory_nexus',
        type: 'organ' as NodeType,
        label: 'Memory Nexus',
        x: centerX + 100,
        y: centerY - 80,
        intensity: 0.5,
        metadata: { type: 'memory_processing' }
      },
      {
        id: 'drift_monitor',
        type: 'organ' as NodeType,
        label: 'Drift Monitor',
        x: centerX,
        y: centerY + 100,
        intensity: currentState?.zone === 'RED' ? 0.9 : 0.4,
        metadata: { zone: currentState?.zone || 'UNKNOWN' }
      }
    ]
    
    return organs.map(organ => ({
      ...organ,
      vx: 0,
      vy: 0,
      radius: NODE_CONFIG[organ.type].baseRadius,
      color: NODE_CONFIG[organ.type].color,
      lastActive: now
    }))
  }, [])

  // Create sigil nodes (active interventions)
  const createSigilNodes = useCallback((): ConstellationNode[] => {
    const currentState = get()
    if (!currentState?.sigils || currentState.sigils === 0) return []
    
    const now = Date.now()
    const sigilNodes: ConstellationNode[] = []
    
    // Create sigil nodes based on active count
    for (let i = 0; i < Math.min(currentState.sigils, 3); i++) {
      const angle = (i / 3) * 2 * Math.PI + Math.PI / 4
      const radius = 180
      
      sigilNodes.push({
        id: `sigil_${i}`,
        type: 'sigil',
        label: `Sigil ${i + 1}`,
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        vx: 0,
        vy: 0,
        radius: NODE_CONFIG.sigil.baseRadius,
        color: NODE_CONFIG.sigil.color,
        intensity: 0.8,
        lastActive: now,
        metadata: {
          priority: 'active',
          type: 'intervention'
        }
      })
    }
    
    return sigilNodes
  }, [])

  // Generate links between nodes
  const generateLinks = useCallback((allNodes: ConstellationNode[]): ConstellationLink[] => {
    const currentState = get()
    const links: ConstellationLink[] = []
    
    // Find key nodes
    const fractalHeart = allNodes.find(n => n.id === 'fractal_heart')
    const memoryNodes = allNodes.filter(n => n.type === 'memory')
    const sigilNodes = allNodes.filter(n => n.type === 'sigil')
    const entropyCore = allNodes.find(n => n.id === 'entropy_core')
    
    // SCUP charge arcs to Fractal Heart
    if (fractalHeart && currentState?.scup && currentState.scup > 40) {
      memoryNodes.forEach(memory => {
        if (memory.metadata.method === 'auto') {
          links.push({
            id: `charge_${memory.id}_to_heart`,
            source: memory.id,
            target: fractalHeart.id,
            type: 'charge',
            strength: 0.3,
            color: 'rgba(231, 76, 60, 0.6)',
            animated: true,
            metadata: { scup: currentState.scup }
          })
        }
      })
    }
    
    // Entropy surge links
    if (entropyCore && currentState?.entropy && currentState.entropy > 0.8) {
      sigilNodes.forEach(sigil => {
        links.push({
          id: `entropy_${entropyCore.id}_to_${sigil.id}`,
          source: entropyCore.id,
          target: sigil.id,
          type: 'sigil_trigger',
          strength: 0.4,
          color: 'rgba(255, 107, 107, 0.7)',
          animated: true,
          metadata: { entropy: currentState.entropy }
        })
      })
    }
    
    // Memory rebloom connections
    for (let i = 0; i < memoryNodes.length - 1; i++) {
      const source = memoryNodes[i]
      const target = memoryNodes[i + 1]
      
      if (source.metadata.source_id === target.id.replace('memory_', '')) {
        links.push({
          id: `rebloom_${source.id}_to_${target.id}`,
          source: source.id,
          target: target.id,
          type: 'rebloom',
          strength: 0.2,
          color: 'rgba(78, 205, 196, 0.5)',
          animated: false,
          metadata: { type: 'memory_connection' }
        })
      }
    }
    
    return links
  }, [])

  // Force simulation step
  const simulateForces = useCallback((nodes: ConstellationNode[], links: ConstellationLink[]) => {
    const nodeMap = new Map(nodes.map(n => [n.id, n]))
    
    // Reset forces
    nodes.forEach(node => {
      node.vx *= DAMPING
      node.vy *= DAMPING
    })
    
    // Repulsion between nodes
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const nodeA = nodes[i]
        const nodeB = nodes[j]
        
        const dx = nodeB.x - nodeA.x
        const dy = nodeB.y - nodeA.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        
        if (distance < MIN_DISTANCE) {
          const force = (MIN_DISTANCE - distance) * FORCE_STRENGTH
          const fx = (dx / distance) * force
          const fy = (dy / distance) * force
          
          nodeA.vx -= fx / NODE_CONFIG[nodeA.type].mass
          nodeA.vy -= fy / NODE_CONFIG[nodeA.type].mass
          nodeB.vx += fx / NODE_CONFIG[nodeB.type].mass
          nodeB.vy += fy / NODE_CONFIG[nodeB.type].mass
        }
      }
    }
    
    // Link forces
    links.forEach(link => {
      const source = nodeMap.get(link.source)
      const target = nodeMap.get(link.target)
      
      if (source && target) {
        const dx = target.x - source.x
        const dy = target.y - source.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        
        if (distance > 0) {
          const force = (distance - LINK_DISTANCE) * link.strength * FORCE_STRENGTH
          const fx = (dx / distance) * force
          const fy = (dy / distance) * force
          
          source.vx += fx / NODE_CONFIG[source.type].mass
          source.vy += fy / NODE_CONFIG[source.type].mass
          target.vx -= fx / NODE_CONFIG[target.type].mass
          target.vy -= fy / NODE_CONFIG[target.type].mass
        }
      }
    })
    
    // Apply velocities and boundary constraints
    nodes.forEach(node => {
      node.x += node.vx
      node.y += node.vy
      
      // Boundary constraints
      const margin = node.radius + 10
      if (node.x < margin) {
        node.x = margin
        node.vx = 0
      }
      if (node.x > width - margin) {
        node.x = width - margin
        node.vx = 0
      }
      if (node.y < margin) {
        node.y = margin
        node.vy = 0
      }
      if (node.y > height - margin) {
        node.y = height - margin
        node.vy = 0
      }
    })
  }, [width, height])

  // Render the constellation
  const render = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    
    // Clear canvas
    ctx.fillStyle = 'rgba(13, 27, 42, 0.8)'
    ctx.fillRect(0, 0, width, height)
    
    const time = Date.now()
    const now = Date.now()
    
    // Draw links
    links.forEach(link => {
      const sourceNode = nodes.find(n => n.id === link.source)
      const targetNode = nodes.find(n => n.id === link.target)
      
      if (sourceNode && targetNode) {
        ctx.strokeStyle = link.color
        ctx.lineWidth = link.animated ? 2 + Math.sin(time * 0.005) * 0.5 : 1.5
        ctx.globalAlpha = link.animated ? 0.7 + Math.sin(time * 0.008) * 0.2 : 0.6
        
        ctx.beginPath()
        ctx.moveTo(sourceNode.x, sourceNode.y)
        ctx.lineTo(targetNode.x, targetNode.y)
        ctx.stroke()
        
        // Animated particles on active links
        if (link.animated) {
          const progress = (time * 0.003) % 1
          const particleX = sourceNode.x + (targetNode.x - sourceNode.x) * progress
          const particleY = sourceNode.y + (targetNode.y - sourceNode.y) * progress
          
          ctx.fillStyle = link.color
          ctx.globalAlpha = 0.8
          ctx.beginPath()
          ctx.arc(particleX, particleY, 2, 0, 2 * Math.PI)
          ctx.fill()
        }
      }
    })
    
    // Draw nodes
    nodes.forEach(node => {
      const age = now - node.lastActive
      const dimming = age > 30000 ? 0.3 : 1 // Dim after 30 seconds
      const pulse = node.intensity * (0.8 + 0.2 * Math.sin(time * 0.01))
      
      // Glow effect
      ctx.globalAlpha = pulse * dimming * 0.3
      ctx.fillStyle = NODE_CONFIG[node.type].glowColor
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.radius * 2, 0, 2 * Math.PI)
      ctx.fill()
      
      // Main node
      ctx.globalAlpha = dimming
      ctx.fillStyle = node.color
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI)
      ctx.fill()
      
      // Pulsing border for active nodes
      if (node.intensity > 0.7) {
        ctx.strokeStyle = node.color
        ctx.lineWidth = 2 + pulse * 2
        ctx.globalAlpha = pulse * dimming * 0.5
        ctx.beginPath()
        ctx.arc(node.x, node.y, node.radius + 4, 0, 2 * Math.PI)
        ctx.stroke()
      }
      
      // Node labels
      if (showLabels) {
        ctx.fillStyle = '#ffffff'
        ctx.font = '10px Monaco, monospace'
        ctx.textAlign = 'center'
        ctx.globalAlpha = dimming * 0.8
        ctx.fillText(node.label, node.x, node.y + node.radius + 15)
      }
    })
    
    ctx.globalAlpha = 1
  }, [nodes, links, showLabels])

  // Animation loop
  const animate = useCallback(() => {
    if (!isPaused) {
      simulateForces(nodes, links)
    }
    render()
    animationRef.current = requestAnimationFrame(animate)
  }, [nodes, links, isPaused, simulateForces, render])

  // Load constellation data
  const loadConstellationData = useCallback(async () => {
    try {
      const [memoryNodes, organNodes, sigilNodes] = await Promise.all([
        loadMemoryChunks(),
        Promise.resolve(createSymbolicOrgans()),
        Promise.resolve(createSigilNodes())
      ])
      
      const allNodes = [...memoryNodes, ...organNodes, ...sigilNodes]
      const allLinks = generateLinks(allNodes)
      
      setNodes(allNodes)
      setLinks(allLinks)
      setError(null)
    } catch (e) {
      setError(`Failed to load constellation: ${e}`)
    }
  }, [loadMemoryChunks, createSymbolicOrgans, createSigilNodes, generateLinks])

  // Handle canvas mouse events
  const handleCanvasMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    
    setMousePos({ x, y })
    
    // Find hovered node
    const hovered = nodes.find(node => {
      const dx = x - node.x
      const dy = y - node.y
      return Math.sqrt(dx * dx + dy * dy) <= node.radius + 5
    })
    
    setHoveredNode(hovered || null)
  }

  // Export constellation as SVG
  const exportConstellation = () => {
    // Create SVG content
    let svgContent = `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">`
    svgContent += `<rect width="${width}" height="${height}" fill="#0d1b2a"/>`
    
    // Add links
    links.forEach(link => {
      const sourceNode = nodes.find(n => n.id === link.source)
      const targetNode = nodes.find(n => n.id === link.target)
      
      if (sourceNode && targetNode) {
        svgContent += `<line x1="${sourceNode.x}" y1="${sourceNode.y}" x2="${targetNode.x}" y2="${targetNode.y}" stroke="${link.color}" stroke-width="1.5" opacity="0.6"/>`
      }
    })
    
    // Add nodes
    nodes.forEach(node => {
      svgContent += `<circle cx="${node.x}" cy="${node.y}" r="${node.radius}" fill="${node.color}" opacity="0.8"/>`
      if (showLabels) {
        svgContent += `<text x="${node.x}" y="${node.y + node.radius + 15}" text-anchor="middle" fill="white" font-family="Monaco" font-size="10">${node.label}</text>`
      }
    })
    
    svgContent += '</svg>'
    
    // Download SVG
    const blob = new Blob([svgContent], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `dawn_constellation_${Date.now()}.svg`
    a.click()
    URL.revokeObjectURL(url)
  }

  // Set up polling and animation
  useEffect(() => {
    // Initial load
    loadConstellationData().then(() => setIsLoading(false))
    
    // Set up polling
    pollIntervalRef.current = window.setInterval(loadConstellationData, 3000)
    
    // Start animation
    animationRef.current = requestAnimationFrame(animate)
    
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [loadConstellationData, animate])

  if (isLoading) {
    return (
      <div className="constellation-panel loading">
        <div className="loading-indicator">
          <div className="pulse-dot"></div>
          <span>Mapping consciousness constellation...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="constellation-panel error">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="constellation-panel">
      <div className="constellation-header">
        <div className="constellation-title">
          <span className="title-icon">🌌</span>
          <span className="title-text">THOUGHT CONSTELLATION</span>
          <span className="node-count">{nodes.length} nodes</span>
        </div>
        
        <div className="constellation-controls">
          <button 
            onClick={() => setShowLabels(!showLabels)}
            className={`control-btn labels-btn ${showLabels ? 'active' : ''}`}
          >
            🏷️
          </button>
          
          <button 
            onClick={() => setIsPaused(!isPaused)}
            className={`control-btn pause-btn ${isPaused ? 'paused' : 'live'}`}
          >
            {isPaused ? '▶️' : '⏸️'}
          </button>
          
          <button 
            onClick={exportConstellation}
            className="control-btn export-btn"
          >
            💾
          </button>
        </div>
      </div>

      <div className="constellation-container">
        <canvas
          ref={canvasRef}
          width={width}
          height={height}
          onMouseMove={handleCanvasMouseMove}
          onMouseLeave={() => setHoveredNode(null)}
        />
        
        {/* Tooltip */}
        {hoveredNode && (
          <div 
            className="constellation-tooltip"
            style={{
              left: mousePos.x + 10,
              top: mousePos.y - 10
            }}
          >
            <div className="tooltip-title">{hoveredNode.label}</div>
            <div className="tooltip-type">{hoveredNode.type.toUpperCase()}</div>
            {Object.entries(hoveredNode.metadata).map(([key, value]) => (
              value !== undefined && (
                <div key={key} className="tooltip-meta">
                  {key}: {typeof value === 'number' ? value.toFixed(3) : String(value)}
                </div>
              )
            ))}
            <div className="tooltip-activity">
              Last active: {Math.round((Date.now() - hoveredNode.lastActive) / 1000)}s ago
            </div>
          </div>
        )}
      </div>
      
      {/* Status Footer */}
      <div className="constellation-footer">
        <div className="status-info">
          <div className="status-item">
            <span className={`status-dot ${isPaused ? 'paused' : 'live'}`}></span>
            <span>{isPaused ? 'Paused' : 'Live'}</span>
          </div>
          
          <div className="status-item">
            <span>🧠 {nodes.filter(n => n.type === 'memory').length} memories</span>
          </div>
          
          <div className="status-item">
            <span>⚡ {nodes.filter(n => n.type === 'sigil').length} sigils</span>
          </div>
          
          <div className="status-item">
            <span>🔗 {links.length} connections</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ConsciousnessConstellation 