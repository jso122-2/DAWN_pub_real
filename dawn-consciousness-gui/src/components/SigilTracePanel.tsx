// src/components/SigilTracePanel.tsx
//! DAWN Sigil Trace Panel - Symbolic Influence Network
//! Real-time visualization of active sigils and their emission patterns

import { useRef, useState, useEffect, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './SigilTracePanel.css'

// Sigil emission event structure
interface SigilEmission {
  timestamp: string
  sigil_name: string
  entropy: number
  heat: number
  tick_number?: number
  event_type?: string
}

// Sigil node for visualization
interface SigilNode {
  id: string
  name: string
  x: number
  y: number
  active: boolean
  lastEmission?: SigilEmission
  emissionCount: number
  averageEntropy: number
  averageHeat: number
}

/**
 * DAWN Sigil Trace Panel - Live Symbolic Influence Network
 * 
 * Visualizes real-time sigil emissions and their patterns,
 * showing how symbolic consciousness emerges through semantic triggers.
 */
export function SigilTracePanel() {
  const svgRef = useRef<SVGSVGElement>(null)
  const [sigilNodes, setSigilNodes] = useState<SigilNode[]>([])
  const [recentEmissions, setRecentEmissions] = useState<SigilEmission[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [hoveredSigil, setHoveredSigil] = useState<string | null>(null)
  const [showTooltip, setShowTooltip] = useState(false)
  const [tooltipData, setTooltipData] = useState<{ node: SigilNode; x: number; y: number } | null>(null)
  
  const pollIntervalRef = useRef<number>()
  
  // Panel dimensions
  const panelWidth = 600
  const panelHeight = 400
  const nodeRadius = 20

  // Load sigil emissions from log file
  const loadSigilEmissions = useCallback(async (): Promise<SigilEmission[]> => {
    try {
      // Read the sigil trace log file using Tauri
      const fileContent = await invoke<string>('read_sigil_trace_log', {
        path: 'runtime/logs/sigil_trace.log'
      })
      
      if (!fileContent.trim()) return []
      
      // Parse log entries
      const lines = fileContent.trim().split('\n')
      const emissions: SigilEmission[] = []
      
      for (const line of lines) {
        try {
          // Skip comments
          if (line.startsWith('#')) continue
          
          // Parse format: [2025-07-27 15:57:29] Sigil emission: insight_sigil at entropy=0.328, heat=0.584
          // Parse format: [SYSTEM] [Tick 25570] VOICE_CONSCIOUSNESS_ACTIVE
          
          if (line.includes('Sigil emission:')) {
            const emissionMatch = line.match(/^\[([^\]]+)\]\s+Sigil emission:\s+(\w+)\s+at\s+entropy=([\d.]+),\s+heat=([\d.]+)/)
            if (emissionMatch) {
              const [, timestamp, sigilName, entropy, heat] = emissionMatch
              emissions.push({
                timestamp,
                sigil_name: sigilName,
                entropy: parseFloat(entropy),
                heat: parseFloat(heat)
              })
            }
          } else if (line.includes('[SYSTEM]') && line.includes('[Tick')) {
            const systemMatch = line.match(/^\[SYSTEM\]\s+\[Tick\s+(\d+)\]\s+(.+)/)
            if (systemMatch) {
              const [, tickStr, sigilName] = systemMatch
              emissions.push({
                timestamp: new Date().toISOString(),
                sigil_name: sigilName,
                entropy: 0.5, // Default values for system events
                heat: 0.5,
                tick_number: parseInt(tickStr, 10),
                event_type: 'SYSTEM'
              })
            }
          }
        } catch (e) {
          console.warn('Failed to parse sigil emission:', line)
        }
      }
      
      // Return most recent emissions (last 50)
      return emissions.slice(-50).reverse()
    } catch (e) {
      console.error('Failed to load sigil emissions:', e)
      return []
    }
  }, [])

  // Build sigil nodes from emission data
  const buildSigilNodes = useCallback((emissions: SigilEmission[]): SigilNode[] => {
    if (emissions.length === 0) return []
    
    // Group emissions by sigil name
    const sigilGroups = new Map<string, SigilEmission[]>()
    emissions.forEach(emission => {
      const name = emission.sigil_name
      if (!sigilGroups.has(name)) {
        sigilGroups.set(name, [])
      }
      sigilGroups.get(name)!.push(emission)
    })
    
    // Calculate positions in a circular layout
    const sigilNames = Array.from(sigilGroups.keys())
    const centerX = panelWidth / 2
    const centerY = panelHeight / 2
    const radius = Math.min(centerX, centerY) - 60
    
    return sigilNames.map((name, index) => {
      const sigilEmissions = sigilGroups.get(name)!
      const angle = (index / sigilNames.length) * 2 * Math.PI - Math.PI / 2
      
      // Calculate statistics
      const totalEntropy = sigilEmissions.reduce((sum, e) => sum + e.entropy, 0)
      const totalHeat = sigilEmissions.reduce((sum, e) => sum + e.heat, 0)
      const averageEntropy = totalEntropy / sigilEmissions.length
      const averageHeat = totalHeat / sigilEmissions.length
      
      // Check if recently active (within last 30 seconds)
      const lastEmission = sigilEmissions[0] // Most recent
      const isActive = new Date().getTime() - new Date(lastEmission.timestamp).getTime() < 30000
      
      return {
        id: `sigil_${name}`,
        name,
        x: centerX + Math.cos(angle) * radius,
        y: centerY + Math.sin(angle) * radius,
        active: isActive,
        lastEmission,
        emissionCount: sigilEmissions.length,
        averageEntropy,
        averageHeat
      }
    })
  }, [panelWidth, panelHeight])

  // Refresh data from log file
  const refreshData = useCallback(async () => {
    try {
      const emissions = await loadSigilEmissions()
      setRecentEmissions(emissions)
      
      const nodes = buildSigilNodes(emissions)
      setSigilNodes(nodes)
      setError(null)
    } catch (e) {
      console.error('Failed to refresh sigil data:', e)
      setError(e instanceof Error ? e.message : 'Failed to load sigil trace data')
    }
  }, [loadSigilEmissions, buildSigilNodes])

  // Initial data load
  useEffect(() => {
    const initialLoad = async () => {
      setIsLoading(true)
      await refreshData()
      setIsLoading(false)
    }
    
    initialLoad()
  }, [refreshData])

  // Setup polling for new data
  useEffect(() => {
    pollIntervalRef.current = window.setInterval(refreshData, 3000) // Poll every 3 seconds
    
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current)
      }
    }
  }, [refreshData])

  // Handle node hover
  const handleNodeHover = (node: SigilNode | null, event?: React.MouseEvent) => {
    if (node && event) {
      const rect = svgRef.current?.getBoundingClientRect()
      if (rect) {
        setTooltipData({
          node,
          x: event.clientX - rect.left,
          y: event.clientY - rect.top
        })
        setShowTooltip(true)
      }
    } else {
      setShowTooltip(false)
      setTooltipData(null)
    }
    setHoveredSigil(node?.name || null)
  }

  // Get node color based on activity and entropy
  const getNodeColor = (node: SigilNode): string => {
    if (!node.active) return '#444'
    
    // Color based on average entropy: low=blue, mid=green, high=red
    if (node.averageEntropy < 0.3) return '#4A90E2'
    if (node.averageEntropy < 0.7) return '#7ED321'
    return '#F5A623'
  }

  // Get node pulse intensity based on heat
  const getNodePulse = (node: SigilNode): number => {
    return node.active ? Math.min(node.averageHeat * 2, 1) : 0
  }

  // Format timestamp for display
  const formatTimestamp = (timestamp: string): string => {
    try {
      const date = new Date(timestamp)
      return date.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
      })
    } catch {
      return 'Unknown'
    }
  }

  if (isLoading) {
    return (
      <div className="sigil-trace-panel loading">
        <div className="panel-header">
          <h3>⚡ Sigil Network</h3>
        </div>
        <div className="loading-indicator">
          Loading sigil trace data...
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="sigil-trace-panel error">
        <div className="panel-header">
          <h3>⚡ Sigil Network</h3>
        </div>
        <div className="error-message">
          <strong>Error:</strong> {error}
          <button onClick={refreshData} className="retry-btn">
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="sigil-trace-panel">
      <div className="trace-header">
        <span className="trace-title">⚡ SIGIL EMISSION NETWORK</span>
        <div className="trace-legend">
          <span className="legend-item">
            <span className="legend-dot active"></span>
            ACTIVE (30s)
          </span>
          <span className="legend-item">
            <span className="legend-dot dormant"></span>
            DORMANT
          </span>
        </div>
      </div>
      
      <div className="trace-container">
        <svg
          ref={svgRef}
          width={panelWidth}
          height={panelHeight}
          className="sigil-network"
          viewBox={`0 0 ${panelWidth} ${panelHeight}`}
        >
          {/* Definitions for patterns and filters */}
          <defs>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            <filter id="pulse" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="2" result="softGlow"/>
              <feMerge>
                <feMergeNode in="softGlow"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          {/* Render sigil nodes */}
          {sigilNodes.map((node) => (
            <g key={node.id}>
              {/* Node circle */}
              <circle
                cx={node.x}
                cy={node.y}
                r={node.active ? nodeRadius : nodeRadius * 0.7}
                fill={getNodeColor(node)}
                stroke={node.active ? '#ffffff' : '#ffffff44'}
                strokeWidth={node.active ? '2' : '1'}
                filter={node.active ? 'url(#glow)' : undefined}
                opacity={node.active ? 1 : 0.6}
                style={{
                  cursor: 'pointer',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => handleNodeHover(node, e)}
                onMouseLeave={() => handleNodeHover(null)}
              >
                {node.active && (
                  <animate
                    attributeName="r"
                    values={`${nodeRadius};${nodeRadius + 4};${nodeRadius}`}
                    dur="2s"
                    repeatCount="indefinite"
                  />
                )}
              </circle>

              {/* Node label */}
              <text
                x={node.x}
                y={node.y + nodeRadius + 15}
                textAnchor="middle"
                fill={node.active ? '#ffffff' : '#ffffff77'}
                fontSize="10"
                fontFamily="Monaco, monospace"
                style={{ pointerEvents: 'none' }}
              >
                {node.name.replace(/_/g, ' ').substring(0, 12)}
              </text>

              {/* Emission count indicator */}
              {node.emissionCount > 0 && (
                <text
                  x={node.x + nodeRadius - 5}
                  y={node.y - nodeRadius + 5}
                  textAnchor="middle"
                  fill="#ffffff"
                  fontSize="8"
                  fontFamily="Monaco, monospace"
                  style={{ pointerEvents: 'none' }}
                >
                  {node.emissionCount}
                </text>
              )}
            </g>
          ))}
        </svg>
        
        {/* Tooltip */}
        {showTooltip && tooltipData && (
          <div 
            className="sigil-tooltip"
            style={{
              position: 'absolute',
              left: tooltipData.x + 10,
              top: tooltipData.y - 10,
              background: 'rgba(0, 0, 0, 0.9)',
              color: 'white',
              padding: '8px 12px',
              borderRadius: '4px',
              fontSize: '12px',
              border: '1px solid #333',
              pointerEvents: 'none',
              zIndex: 1000
            }}
          >
            <div className="tooltip-title" style={{ fontWeight: 'bold', marginBottom: '4px' }}>
              {tooltipData.node.name}
            </div>
            <div className="tooltip-info">
              Emissions: {tooltipData.node.emissionCount}
            </div>
            <div className="tooltip-info">
              Avg Entropy: {tooltipData.node.averageEntropy.toFixed(3)}
            </div>
            <div className="tooltip-info">
              Avg Heat: {tooltipData.node.averageHeat.toFixed(3)}
            </div>
            {tooltipData.node.lastEmission && (
              <div className="tooltip-info">
                Last: {formatTimestamp(tooltipData.node.lastEmission.timestamp)}
              </div>
            )}
            <div className="tooltip-info">
              Status: {tooltipData.node.active ? 'ACTIVE' : 'DORMANT'}
            </div>
          </div>
        )}
      </div>
      
      {/* Recent emissions sidebar */}
      <div className="emissions-sidebar">
        <div className="sidebar-header">Recent Emissions</div>
        <div className="emissions-list">
          {recentEmissions.slice(0, 8).map((emission, index) => (
            <div key={`${emission.timestamp}_${index}`} className="emission-entry">
              <div className="emission-time">
                {formatTimestamp(emission.timestamp)}
              </div>
              <div className="emission-sigil">
                {emission.sigil_name}
              </div>
              <div className="emission-metrics">
                E:{emission.entropy.toFixed(2)} H:{emission.heat.toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="trace-footer">
        <span className="active-count">
          {sigilNodes.filter(n => n.active).length} Active Sigils
        </span>
        <span className="total-emissions">
          {recentEmissions.length} Recent Emissions
        </span>
      </div>
    </div>
  )
}

export default SigilTracePanel 