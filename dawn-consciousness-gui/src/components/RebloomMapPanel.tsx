// src/components/RebloomMapPanel.tsx
//! Memory Lineage Visualization - DAWN's Semantic Ancestry Map
//! Real-time visualization of memory rebloom chains and cognitive recursion

import { useEffect, useRef, useState, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './RebloomMapPanel.css'

// Memory rebloom event structure
interface RebloomEvent {
  timestamp: string
  source_id: string
  rebloom_id: string
  method: 'auto' | 'manual'
  topic: string
  reason: string
}

// Memory node for visualization
interface MemoryNode {
  id: string
  topic: string
  timestamp: string
  method: 'auto' | 'manual'
  reason: string
  x: number
  y: number
  children: MemoryNode[]
  isActive: boolean
  depth: number
}

// Ancestry chain for rendering
interface AncestryChain {
  id: string
  root: MemoryNode
  lastUpdate: number
  nodeCount: number
}

/**
 * DAWN Memory Lineage Visualization
 * 
 * Renders real-time ancestry trees of rebloomed memories, showing how
 * consciousness recursively accesses past experiences for cognitive stability.
 */
export function RebloomMapPanel() {
  const [ancestryChains, setAncestryChains] = useState<AncestryChain[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [zoomLevel, setZoomLevel] = useState(1.0)
  const [showTooltip, setShowTooltip] = useState(false)
  const [tooltipData, setTooltipData] = useState<{ node: MemoryNode; x: number; y: number } | null>(null)
  
  const svgRef = useRef<SVGSVGElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const animationRef = useRef<number>()
  const lastFileSize = useRef<number>(0)
  
  // Panel dimensions
  const panelWidth = 600
  const panelHeight = 400
  const nodeRadius = 15
  const levelHeight = 60

  // Load rebloom events from log file
  const loadRebloomEvents = useCallback(async (): Promise<RebloomEvent[]> => {
    try {
      // Read the jsonl file using Tauri
      const fileContent = await invoke<string>('read_rebloom_log', {
        path: 'runtime/memory/rebloom_log.jsonl'
      })
      
      if (!fileContent.trim()) return []
      
      // Parse JSON Lines format
      const lines = fileContent.trim().split('\n')
      const events: RebloomEvent[] = []
      
      for (const line of lines) {
        try {
          const event = JSON.parse(line) as RebloomEvent
          events.push(event)
        } catch (e) {
          console.warn('Failed to parse rebloom event:', line)
        }
      }
      
      return events.reverse() // Most recent first
    } catch (e) {
      console.error('Failed to load rebloom events:', e)
      return []
    }
  }, [])

  // Build ancestry chains from rebloom events
  const buildAncestryChains = useCallback((events: RebloomEvent[]): AncestryChain[] => {
    if (events.length === 0) return []
    
    const nodeMap = new Map<string, MemoryNode>()
    const parentChildMap = new Map<string, string[]>() // source_id -> [rebloom_ids]
    const allNodeIds = new Set<string>()
    
    // First pass: create all nodes and track relationships
    events.forEach(event => {
      const now = Date.now()
      const eventTime = new Date(event.timestamp).getTime()
      const isActive = (now - eventTime) < 10000 // Active if within 10 seconds
      
      allNodeIds.add(event.source_id)
      allNodeIds.add(event.rebloom_id)
      
      // Create source node if not exists
      if (!nodeMap.has(event.source_id)) {
        nodeMap.set(event.source_id, {
          id: event.source_id,
          topic: event.topic,
          timestamp: event.timestamp,
          method: event.method,
          reason: event.reason,
          x: 0,
          y: 0,
          children: [],
          isActive,
          depth: 0
        })
      }
      
      // Create rebloom node if not exists
      if (!nodeMap.has(event.rebloom_id)) {
        nodeMap.set(event.rebloom_id, {
          id: event.rebloom_id,
          topic: event.topic,
          timestamp: event.timestamp,
          method: event.method,
          reason: event.reason,
          x: 0,
          y: 0,
          children: [],
          isActive,
          depth: 0
        })
      }
      
      // Track parent-child relationships
      if (!parentChildMap.has(event.source_id)) {
        parentChildMap.set(event.source_id, [])
      }
      const children = parentChildMap.get(event.source_id)!
      if (!children.includes(event.rebloom_id)) {
        children.push(event.rebloom_id)
      }
    })
    
    // Second pass: build actual tree structures (avoiding cycles)
    parentChildMap.forEach((childIds, parentId) => {
      const parentNode = nodeMap.get(parentId)
      if (parentNode) {
        // Only add children that don't create cycles
        parentNode.children = childIds
          .map(childId => nodeMap.get(childId)!)
          .filter(child => child && child.id !== parentId) // Avoid self-reference
      }
    })
    
    // Find interesting root nodes (nodes with multiple connections or recent activity)
    const candidateRoots = Array.from(allNodeIds)
      .map(nodeId => {
        const node = nodeMap.get(nodeId)!
        const childCount = parentChildMap.get(nodeId)?.length || 0
        const isRecent = (Date.now() - new Date(node.timestamp).getTime()) < 30000 // 30 seconds
        return {
          node,
          score: childCount * 2 + (isRecent ? 3 : 0) + (node.isActive ? 5 : 0)
        }
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 5) // Top 5 most interesting roots
    
    // Build chains from selected roots - center them in the viewport
    const chains: AncestryChain[] = []
    const numChains = Math.min(candidateRoots.length, 5)
    const totalWidth = numChains * 90 // 90px per chain
    const startX = (panelWidth - totalWidth) / 2 + 45 // Center horizontally
    
    candidateRoots.forEach((candidate, chainIndex) => {
      // Calculate centered positions for this chain
      const chainX = startX + (chainIndex * 90)
      const chainY = 100 // Start 100px from top for better centering
      positionNodes(candidate.node, chainX, chainY, 0)
      
      chains.push({
        id: candidate.node.id,
        root: candidate.node,
        lastUpdate: Date.now(),
        nodeCount: countNodes(candidate.node)
      })
    })
    
    console.log('🌸 [DEBUG] Final chains built:', chains.length)
    
    // Fallback: if no chains found, create simple flat visualization
    if (chains.length === 0 && events.length > 0) {
      console.log('🌸 [DEBUG] No ancestry chains found, creating flat visualization...')
      
      // Create unique nodes from recent events (flat, no hierarchy)
      const recentEvents = events.slice(0, 15) // Last 15 events
      const uniqueNodes = new Map<string, MemoryNode>()
      
      recentEvents.forEach(event => {
        if (!uniqueNodes.has(event.source_id)) {
          uniqueNodes.set(event.source_id, {
            id: event.source_id,
            topic: event.topic,
            timestamp: event.timestamp,
            method: event.method,
            reason: event.reason,
            x: 0,
            y: 0,
            children: [], // No children - flat visualization
            isActive: (Date.now() - new Date(event.timestamp).getTime()) < 10000,
            depth: 0
          })
        }
        
        if (!uniqueNodes.has(event.rebloom_id)) {
          uniqueNodes.set(event.rebloom_id, {
            id: event.rebloom_id,
            topic: event.topic,
            timestamp: event.timestamp,
            method: event.method,
            reason: event.reason,
            x: 0,
            y: 0,
            children: [], // No children - flat visualization
            isActive: (Date.now() - new Date(event.timestamp).getTime()) < 10000,
            depth: 0
          })
        }
      })
      
             // Position nodes in a centered grid
       const nodeArray = Array.from(uniqueNodes.values())
       const simpleChains: AncestryChain[] = []
       const maxNodes = 12
       const cols = 6
       const rows = Math.ceil(Math.min(nodeArray.length, maxNodes) / cols)
       
       // Center the grid
       const gridWidth = (cols - 1) * 85
       const gridHeight = (rows - 1) * 70
       const startX = (panelWidth - gridWidth) / 2
       const startY = (panelHeight - gridHeight) / 2
       
       nodeArray.slice(0, maxNodes).forEach((node, index) => {
         node.x = startX + (index % cols) * 85
         node.y = startY + Math.floor(index / cols) * 70
         
         simpleChains.push({
           id: `flat_${index}`,
           root: node,
           lastUpdate: Date.now(),
           nodeCount: 1
         })
       })
      
      console.log('🌸 [DEBUG] Created flat visualization:', simpleChains.length, 'nodes')
      return simpleChains
    }
    
    return chains
  }, [panelWidth])

  // Recursively position nodes in a chain with cycle detection
  const positionNodes = (node: MemoryNode, x: number, y: number, depth: number, visited = new Set<string>()) => {
    // Prevent infinite recursion from circular references
    if (visited.has(node.id) || depth > 5 || y > panelHeight - 50) {
      return
    }
    
    visited.add(node.id)
    // Ensure nodes stay within viewport bounds
    node.x = Math.max(nodeRadius + 10, Math.min(panelWidth - nodeRadius - 10, x))
    node.y = Math.max(nodeRadius + 10, Math.min(panelHeight - nodeRadius - 10, y))
    node.depth = depth
    
    if (node.children.length > 0) {
      const maxChildSpacing = 90
      const minChildSpacing = 40
      const availableWidth = panelWidth - (nodeRadius * 4) // Account for node size
      const idealSpacing = Math.min(maxChildSpacing, availableWidth / Math.max(1, node.children.length))
      const childSpacing = Math.max(minChildSpacing, idealSpacing)
      
      const totalWidth = (node.children.length - 1) * childSpacing
      const startX = node.x - (totalWidth / 2)
      
      node.children.forEach((child, index) => {
        if (!visited.has(child.id)) {
          const childX = startX + (index * childSpacing)
          const childY = node.y + levelHeight
          positionNodes(child, childX, childY, depth + 1, new Set(visited))
        }
      })
    }
  }

  // Count total nodes in a tree with cycle detection
  const countNodes = (node: MemoryNode, visited = new Set<string>()): number => {
    if (visited.has(node.id)) {
      return 0 // Don't count nodes we've already seen
    }
    
    visited.add(node.id)
    return 1 + node.children.reduce((sum, child) => sum + countNodes(child, new Set(visited)), 0)
  }

  // Render a memory node
  const renderNode = (node: MemoryNode, chainId: string) => {
    const isAutoMethod = node.method === 'auto'
    const pulseClass = isAutoMethod ? 'auto-pulse' : ''
    const activeClass = node.isActive ? 'active-node' : ''
    
    return (
      <g key={`${chainId}-${node.id}`} className={`memory-node ${pulseClass} ${activeClass}`}>
        <circle
          cx={node.x}
          cy={node.y}
          r={nodeRadius}
          className="node-circle"
          onMouseEnter={(e) => {
            setTooltipData({
              node,
              x: e.clientX,
              y: e.clientY
            })
            setShowTooltip(true)
          }}
          onMouseLeave={() => {
            setShowTooltip(false)
            setTooltipData(null)
          }}
        />
        <text
          x={node.x}
          y={node.y + 5}
          className="node-label"
          textAnchor="middle"
        >
          {node.topic.substring(0, 8)}
        </text>
        <text
          x={node.x}
          y={node.y - nodeRadius - 5}
          className="node-id"
          textAnchor="middle"
        >
          {node.id.split('_').pop()}
        </text>
      </g>
    )
  }

  // Render connections between nodes with cycle detection
  const renderConnections = (node: MemoryNode, chainId: string, visited = new Set<string>()): JSX.Element[] => {
    if (visited.has(node.id)) {
      return [] // Avoid infinite recursion
    }
    
    visited.add(node.id)
    const connections: JSX.Element[] = []
    
    node.children.forEach((child, index) => {
      // Draw line from parent to child
      connections.push(
        <line
          key={`${chainId}-connection-${node.id}-${child.id}`}
          x1={node.x}
          y1={node.y + nodeRadius}
          x2={child.x}
          y2={child.y - nodeRadius}
          className="ancestry-line"
          strokeDasharray={child.isActive ? '5,5' : 'none'}
        />
      )
      
      // Recursively render child connections (only if not already visited)
      if (!visited.has(child.id)) {
        connections.push(...renderConnections(child, chainId, new Set(visited)))
      }
    })
    
    return connections
  }

  // Render all nodes in a chain with cycle detection
  const renderChainNodes = (node: MemoryNode, chainId: string, visited = new Set<string>()): JSX.Element[] => {
    if (visited.has(node.id)) {
      return [] // Avoid infinite recursion
    }
    
    visited.add(node.id)
    const nodes: JSX.Element[] = [renderNode(node, chainId)]
    
    node.children.forEach(child => {
      if (!visited.has(child.id)) {
        nodes.push(...renderChainNodes(child, chainId, new Set(visited)))
      }
    })
    
    return nodes
  }

  // Zoom controls
  const handleZoomIn = () => setZoomLevel(prev => Math.min(prev + 0.2, 2.0))
  const handleZoomOut = () => setZoomLevel(prev => Math.max(prev - 0.2, 0.5))
  const handleZoomFit = () => {
    // Auto-fit based on content size
    if (ancestryChains.length === 0) {
      setZoomLevel(1.0)
      return
    }
    
    // Find the bounds of all nodes
    let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity
    
    const checkNodeBounds = (node: MemoryNode, visited = new Set<string>()) => {
      if (visited.has(node.id)) return
      visited.add(node.id)
      
      minX = Math.min(minX, node.x - nodeRadius)
      maxX = Math.max(maxX, node.x + nodeRadius)
      minY = Math.min(minY, node.y - nodeRadius)
      maxY = Math.max(maxY, node.y + nodeRadius)
      
      node.children.forEach(child => {
        if (!visited.has(child.id)) {
          checkNodeBounds(child, new Set(visited))
        }
      })
    }
    
    ancestryChains.forEach(chain => checkNodeBounds(chain.root))
    
    if (minX !== Infinity) {
      const contentWidth = maxX - minX
      const contentHeight = maxY - minY
      const scaleX = (panelWidth - 40) / contentWidth
      const scaleY = (panelHeight - 40) / contentHeight
      const optimalScale = Math.min(scaleX, scaleY, 1.5) // Cap at 1.5x
      setZoomLevel(Math.max(0.5, optimalScale))
    } else {
      setZoomLevel(1.0)
    }
  }

  // Poll for updates
  useEffect(() => {
    const pollInterval = setInterval(async () => {
      try {
        const events = await loadRebloomEvents()
        console.log('🌸 [DEBUG] Loaded events:', events.length)
        const chains = buildAncestryChains(events)
        console.log('🌸 [DEBUG] Built chains:', chains.length, chains.map(c => `${c.id} (${c.nodeCount} nodes)`))
        setAncestryChains(chains)
        setError(null)
      } catch (e) {
        console.error('🌸 [DEBUG] Error:', e)
        setError(`Failed to load rebloom data: ${e}`)
      }
    }, 3000) // Poll every 3 seconds

    // Initial load
    loadRebloomEvents()
      .then(events => {
        console.log('🌸 [DEBUG] Initial load - events:', events.length)
        if (events.length > 0) {
          console.log('🌸 [DEBUG] Sample event:', events[0])
        }
        const chains = buildAncestryChains(events)
        console.log('🌸 [DEBUG] Initial chains:', chains.length, chains.map(c => `${c.id} (${c.nodeCount} nodes)`))
        setAncestryChains(chains)
        setIsLoading(false)
      })
      .catch(e => {
        console.error('🌸 [DEBUG] Initial load error:', e)
        setError(`Failed to load initial data: ${e}`)
        setIsLoading(false)
      })

    return () => clearInterval(pollInterval)
  }, [loadRebloomEvents, buildAncestryChains])

  if (isLoading) {
    return (
      <div className="rebloom-panel loading">
        <div className="loading-indicator">
          <div className="pulse-dot"></div>
          <span>Loading memory lineage...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="rebloom-panel error">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      </div>
    )
  }

  return (
    <div className="rebloom-panel" ref={containerRef}>
      <div className="panel-header">
        <div className="panel-title">
          <span className="title-icon">🌸</span>
          <span className="title-text">MEMORY LINEAGE</span>
          <span className="chain-count">{ancestryChains.length} chains</span>
        </div>
        
        <div className="zoom-controls">
          <button onClick={handleZoomOut} className="zoom-btn">−</button>
          <span className="zoom-display">{Math.round(zoomLevel * 100)}%</span>
          <button onClick={handleZoomIn} className="zoom-btn">+</button>
          <button onClick={handleZoomFit} className="zoom-btn fit">⊡</button>
        </div>
      </div>

      <div className="ancestry-container">
        <svg 
          ref={svgRef}
          width={panelWidth}
          height={panelHeight}
          className="ancestry-svg"
          style={{ transform: `scale(${zoomLevel})` }}
        >
          {/* Render all chains */}
          {ancestryChains.map(chain => (
            <g key={chain.id} className="ancestry-chain">
              {/* Render connections first (behind nodes) */}
              {renderConnections(chain.root, chain.id)}
              
              {/* Render nodes */}
              {renderChainNodes(chain.root, chain.id)}
            </g>
          ))}
          
          {/* Background grid */}
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      {/* Tooltip */}
      {showTooltip && tooltipData && (
        <div 
          className="rebloom-tooltip"
          style={{
            position: 'fixed',
            left: tooltipData.x + 10,
            top: tooltipData.y - 10,
            zIndex: 1000
          }}
        >
          <div className="tooltip-content">
            <div className="tooltip-header">
              <span className="tooltip-id">{tooltipData.node.id}</span>
              <span className={`tooltip-method ${tooltipData.node.method}`}>
                {tooltipData.node.method}
              </span>
            </div>
            <div className="tooltip-topic">{tooltipData.node.topic}</div>
            <div className="tooltip-reason">{tooltipData.node.reason}</div>
            <div className="tooltip-time">
              {new Date(tooltipData.node.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
      )}

      {/* Status indicators */}
      <div className="panel-footer">
        <div className="legend">
          <div className="legend-item">
            <div className="legend-dot auto"></div>
            <span>Auto Rebloom</span>
          </div>
          <div className="legend-item">
            <div className="legend-dot manual"></div>
            <span>Manual</span>
          </div>
          <div className="legend-item">
            <div className="legend-dot active"></div>
            <span>Active (10s)</span>
          </div>
        </div>
        
        <div className="update-status">
          Last update: {new Date().toLocaleTimeString()}
        </div>
      </div>
    </div>
  )
}

export default RebloomMapPanel 