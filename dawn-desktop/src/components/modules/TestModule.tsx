import React, { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Activity, Zap, Brain } from 'lucide-react'

// Types
interface Node {
  id: string
  x: number
  y: number
  value: number
  label: string
}

interface Connection {
  from: string
  to: string
  active: boolean
  intensity: number
}

interface DataPacket {
  id: string
  from: string
  to: string
  progress: number
  value: number
}

// Module Container wrapper
function ModuleContainer({ 
  children, 
  title, 
  moduleId,
  className,
  onEvent,
  dataIntensity = 0
}: {
  children: React.ReactNode
  title: string
  moduleId: string
  className?: string
  onEvent?: (event: any) => void
  dataIntensity?: number
}) {
  const [isActive, setIsActive] = useState(false);

  // Use useEffect to update active state when dataIntensity changes
  useEffect(() => {
    setIsActive(dataIntensity > 0.7);
  }, [dataIntensity]);

  // Simple breathing and floating animation variants (inline)
  const breathingVariants = {
    calm: { 
      scale: [1, 1.02, 1], 
      opacity: [0.9, 1, 0.9], 
      y: [0, -10, 0],
      transition: { 
        duration: 4, 
        repeat: Infinity, 
        ease: 'easeInOut' 
      } 
    },
    active: { 
      scale: [1, 1.04, 1], 
      opacity: [0.85, 1, 0.85], 
      y: [0, -15, 0],
      transition: { 
        duration: 2, 
        repeat: Infinity, 
        ease: 'easeInOut' 
      } 
    }
  }

  return (
    <motion.div
      initial="calm"
      animate={isActive ? 'active' : 'calm'}
      variants={breathingVariants}
      style={{ position: 'absolute' }}
      className={
        `glass-neural rounded-2xl p-6 min-w-[400px] min-h-[300px] ${isActive ? 'glass-active' : ''} ${className || ''}`
      }
    >
      <div className="flex items-center gap-2 mb-4">
        <Brain className="w-5 h-5 text-neural-400" />
        <h3 className="text-lg font-semibold text-neural-300">{title}</h3>
      </div>
      {children}
    </motion.div>
  )
}

// Main TestModule component
export function TestModule({ 
  moduleId = "test-neural-1",
  onNodeActivated 
}: {
  moduleId?: string
  onNodeActivated?: (nodeId: string, value: number) => void
}) {
  // State
  const [nodes] = useState<Node[]>([
    { id: 'input-1', x: 50, y: 80, value: 0, label: 'Input' },
    { id: 'input-2', x: 50, y: 180, value: 0, label: 'Input' },
    { id: 'hidden-1', x: 200, y: 60, value: 0, label: 'Hidden' },
    { id: 'hidden-2', x: 200, y: 130, value: 0, label: 'Hidden' },
    { id: 'hidden-3', x: 200, y: 200, value: 0, label: 'Hidden' },
    { id: 'output', x: 350, y: 130, value: 0, label: 'Output' }
  ])

  const [connections] = useState<Connection[]>([
    { from: 'input-1', to: 'hidden-1', active: false, intensity: 0 },
    { from: 'input-1', to: 'hidden-2', active: false, intensity: 0 },
    { from: 'input-2', to: 'hidden-2', active: false, intensity: 0 },
    { from: 'input-2', to: 'hidden-3', active: false, intensity: 0 },
    { from: 'hidden-1', to: 'output', active: false, intensity: 0 },
    { from: 'hidden-2', to: 'output', active: false, intensity: 0 },
    { from: 'hidden-3', to: 'output', active: false, intensity: 0 }
  ])

  const [nodeValues, setNodeValues] = useState<Record<string, number>>({})
  const [dataPackets, setDataPackets] = useState<DataPacket[]>([])
  const [dataIntensity, setDataIntensity] = useState(0)
  const svgRef = useRef<SVGSVGElement>(null)

  // Simulate data flow
  useEffect(() => {
    const interval = setInterval(() => {
      // Generate random input values
      const input1Value = Math.random()
      const input2Value = Math.random()
      
      // Update node values with propagation
      setNodeValues(prev => ({
        ...prev,
        'input-1': input1Value,
        'input-2': input2Value
      }))

      // Create data packets for visualization
      const newPackets: DataPacket[] = []
      
      if (input1Value > 0.3) {
        newPackets.push(
          { id: `${Date.now()}-${Math.random()}-input1-hidden1`, from: 'input-1', to: 'hidden-1', progress: 0, value: input1Value },
          { id: `${Date.now()}-${Math.random()}-input1-hidden2`, from: 'input-1', to: 'hidden-2', progress: 0, value: input1Value }
        )
      }
      
      if (input2Value > 0.3) {
        newPackets.push(
          { id: `${Date.now()}-${Math.random()}-input2-hidden2`, from: 'input-2', to: 'hidden-2', progress: 0, value: input2Value },
          { id: `${Date.now()}-${Math.random()}-input2-hidden3`, from: 'input-2', to: 'hidden-3', progress: 0, value: input2Value }
        )
      }

      setDataPackets(prev => [...prev, ...newPackets])
      
      // Calculate data intensity
      const intensity = (input1Value + input2Value) / 2
      setDataIntensity(intensity)
    }, 2000)

    return () => clearInterval(interval)
  }, [])

  // Animate data packets
  useEffect(() => {
    const animationInterval = setInterval(() => {
      setDataPackets(prev => {
        const updated = prev.map(packet => ({
          ...packet,
          progress: packet.progress + 0.05
        })).filter(packet => packet.progress <= 1)

        // Trigger node activation when packet arrives
        updated.forEach(packet => {
          if (packet.progress > 0.95 && packet.progress <= 1) {
            const targetNode = nodes.find(n => n.id === packet.to)
            if (targetNode && onNodeActivated) {
              // Use setTimeout to avoid setState during render
              setTimeout(() => {
                onNodeActivated(packet.to, packet.value)
              }, 0)
            }

            // Propagate to next layer
            if (packet.to.startsWith('hidden')) {
              setTimeout(() => {
                setDataPackets(p => [...p, {
                  id: `${Date.now()}-${Math.random()}-${packet.to}-output`,
                  from: packet.to,
                  to: 'output',
                  progress: 0,
                  value: packet.value * 0.8
                }])
              }, 100)
            }
          }
        })

        return updated
      })
    }, 50)

    return () => clearInterval(animationInterval)
  }, [nodes, onNodeActivated])

  // Connection glow based on data flow
  const getConnectionGlow = useCallback((from: string, to: string) => {
    const activePackets = dataPackets.filter(
      p => p.from === from && p.to === to && p.progress < 1
    )
    if (activePackets.length === 0) return 0
    
    const maxIntensity = Math.max(...activePackets.map(p => p.value))
    return maxIntensity
  }, [dataPackets])

  return (
    <ModuleContainer
      title="Neural Network Test"
      moduleId={moduleId}
      dataIntensity={dataIntensity}
      className="left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
    >
      <div className="relative">
        <svg 
          ref={svgRef}
          width="400" 
          height="260" 
          className="absolute inset-0"
        >
          {/* Render connections */}
          {connections.map((conn, idx) => {
            const fromNode = nodes.find(n => n.id === conn.from)
            const toNode = nodes.find(n => n.id === conn.to)
            if (!fromNode || !toNode) return null

            const glowIntensity = getConnectionGlow(conn.from, conn.to)
            
            return (
              <g key={idx}>
                <line
                  x1={fromNode.x}
                  y1={fromNode.y}
                  x2={toNode.x}
                  y2={toNode.y}
                  stroke={glowIntensity > 0 ? "rgba(168, 85, 247, 0.8)" : "rgba(168, 85, 247, 0.2)"}
                  strokeWidth={glowIntensity > 0 ? 2 : 1}
                  className="transition-all duration-300"
                  filter={glowIntensity > 0 ? "url(#glow)" : ""}
                />
              </g>
            )
          })}

          {/* Define glow filter */}
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
        </svg>

        {/* Render nodes */}
        {nodes.map(node => (
          <motion.div
            key={node.id}
            className="absolute"
            style={{ left: node.x - 20, top: node.y - 20 }}
            animate={{
              scale: nodeValues[node.id] > 0.5 ? 1.2 : 1,
            }}
            transition={{ duration: 0.3 }}
          >
            <div 
              className={
                nodeValues[node.id] > 0.7 
                  ? "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold bg-neural-500 text-white shadow-[0_0_20px_rgba(168,85,247,0.8)]"
                  : nodeValues[node.id] > 0.3
                  ? "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold bg-neural-600/50 text-neural-200 shadow-[0_0_10px_rgba(168,85,247,0.4)]"
                  : "w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold bg-neural-800/30 text-neural-400 border border-neural-700"
              }
            >
              {node.label[0]}
            </div>
            <div className="absolute -bottom-5 left-1/2 -translate-x-1/2 text-[10px] text-neural-400 whitespace-nowrap">
              {node.label}
            </div>
          </motion.div>
        ))}

        {/* Render data packets */}
        <AnimatePresence>
          {dataPackets.map(packet => {
            const fromNode = nodes.find(n => n.id === packet.from)
            const toNode = nodes.find(n => n.id === packet.to)
            if (!fromNode || !toNode) return null

            const x = fromNode.x + (toNode.x - fromNode.x) * packet.progress
            const y = fromNode.y + (toNode.y - fromNode.y) * packet.progress

            return (
              <motion.div
                key={packet.id}
                className="absolute w-3 h-3 rounded-full"
                style={{
                  left: x - 6,
                  top: y - 6,
                  background: `radial-gradient(circle, rgba(34, 211, 238, ${packet.value}) 0%, transparent 70%)`,
                  boxShadow: `0 0 ${10 * packet.value}px rgba(34, 211, 238, ${packet.value})`
                }}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0, opacity: 0 }}
                transition={{ duration: 0.2 }}
              />
            )
          })}
        </AnimatePresence>

        {/* Status bar */}
        <div className="mt-8 pt-4 border-t border-neural-800/30">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-consciousness-400" />
              <span className="text-neural-400">Data Flow</span>
            </div>
            <div className="flex items-center gap-2">
              <div className={
                dataIntensity > 0.7 ? "w-2 h-2 rounded-full bg-consciousness-400 animate-pulse" : "w-2 h-2 rounded-full bg-neural-600"
              } />
              <span className="text-neural-300">
                {(dataIntensity * 100).toFixed(0)}% Active
              </span>
            </div>
          </div>
          
          {/* Intensity bar */}
          <div className="mt-2 h-1 bg-neural-900/50 rounded-full overflow-hidden">
            <motion.div 
              className="h-full bg-gradient-to-r from-neural-500 to-consciousness-400"
              animate={{ width: `${dataIntensity * 100}%` }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </div>
    </ModuleContainer>
  )
}