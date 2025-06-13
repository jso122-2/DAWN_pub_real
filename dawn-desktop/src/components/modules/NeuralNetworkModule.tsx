import React, { useState, useEffect, useRef } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { Brain, Zap } from 'lucide-react';

// Simple EventEmitter implementation for the module
class EventEmitter {
  private events: { [key: string]: Array<(...args: any[]) => void> } = {};

  on(event: string, listener: (...args: any[]) => void): this {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
    return this;
  }

  off(event: string, listenerToRemove: (...args: any[]) => void): this {
    if (!this.events[event]) return this;
    this.events[event] = this.events[event].filter(listener => listener !== listenerToRemove);
    return this;
  }

  emit(event: string, ...args: any[]): boolean {
    if (!this.events[event]) return false;
    this.events[event].forEach(listener => listener(...args));
    return true;
  }
}

interface Node {
  id: string;
  x: number;
  y: number;
  layer: number;
  active: boolean;
  value: number;
}

interface Connection {
  from: string;
  to: string;
  weight: number;
  active: boolean;
}

interface NeuralNetworkModuleProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
}

const NeuralNetworkModule: React.FC<NeuralNetworkModuleProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0 
}) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [processing, setProcessing] = useState(false);
  const [dataFlow, setDataFlow] = useState<number[]>([]);
  const svgRef = useRef<SVGSVGElement>(null);
  const controls = useAnimation();
  
  // Initialize neural network structure
  useEffect(() => {
    const networkNodes: Node[] = [];
    const networkConnections: Connection[] = [];
    
    // Create 3 layers: input (3), hidden (4), output (3)
    const layers = [3, 4, 3];
    const layerSpacing = 120;
    const nodeSpacing = 60;
    
    let nodeId = 0;
    
    // Create nodes
    layers.forEach((nodeCount, layerIndex) => {
      const startY = (300 - (nodeCount * nodeSpacing)) / 2;
      
      for (let i = 0; i < nodeCount; i++) {
        networkNodes.push({
          id: `node-${nodeId}`,
          x: layerIndex * layerSpacing + 50,
          y: startY + i * nodeSpacing + 30,
          layer: layerIndex,
          active: false,
          value: Math.random()
        });
        nodeId++;
      }
    });
    
    // Create connections between layers
    for (let l = 0; l < layers.length - 1; l++) {
      const currentLayerNodes = networkNodes.filter(n => n.layer === l);
      const nextLayerNodes = networkNodes.filter(n => n.layer === l + 1);
      
      currentLayerNodes.forEach(fromNode => {
        nextLayerNodes.forEach(toNode => {
          networkConnections.push({
            from: fromNode.id,
            to: toNode.id,
            weight: Math.random(),
            active: false
          });
        });
      });
    }
    
    setNodes(networkNodes);
    setConnections(networkConnections);
  }, []);
  
  // Simulate data processing
  const processData = async () => {
    if (processing) return;
    
    setProcessing(true);
    emitter.emit('module:processing', { 
      moduleId: 'neural-network',
      type: 'neural-processing',
      timestamp: Date.now()
    });
    
    // Activate input layer
    const inputNodes = nodes.filter(n => n.layer === 0);
    for (const node of inputNodes) {
      await activateNode(node.id);
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    
    // Process through hidden layer
    const hiddenNodes = nodes.filter(n => n.layer === 1);
    for (const node of hiddenNodes) {
      await activateNode(node.id);
      await new Promise(resolve => setTimeout(resolve, 80));
    }
    
    // Activate output layer
    const outputNodes = nodes.filter(n => n.layer === 2);
    for (const node of outputNodes) {
      await activateNode(node.id);
      await new Promise(resolve => setTimeout(resolve, 120));
    }
    
    // Emit processed data
    emitter.emit('module:data', {
      moduleId: 'neural-network',
      data: {
        inputs: inputNodes.map(n => n.value),
        outputs: outputNodes.map(n => n.value),
        processingTime: Date.now()
      }
    });
    
    // Reset after processing
    setTimeout(() => {
      setNodes(prev => prev.map(n => ({ ...n, active: false })));
      setConnections(prev => prev.map(c => ({ ...c, active: false })));
      setProcessing(false);
    }, 1000);
  };
  
  // Activate a node and its connections
  const activateNode = async (nodeId: string) => {
    // Activate the node
    setNodes(prev => prev.map(n => 
      n.id === nodeId ? { ...n, active: true, value: Math.random() } : n
    ));
    
    // Activate connections from this node
    setConnections(prev => prev.map(c => 
      c.from === nodeId ? { ...c, active: true } : c
    ));
    
    // Create particle flow
    const newFlow = Array(3).fill(0).map(() => Math.random() * 100);
    setDataFlow(newFlow);
  };
  
  // Auto-process based on entropy
  useEffect(() => {
    if (globalEntropy > 0.7 && !processing) {
      processData();
    }
  }, [globalEntropy, processing]);
  
  // Listen for external data events
  useEffect(() => {
    const handleExternalData = (data: any) => {
      if (data.targetId === 'neural-network' && !processing) {
        processData();
      }
    };
    
    emitter.on('module:connection', handleExternalData);
    return () => {
      emitter.off('module:connection', handleExternalData);
    };
  }, [emitter, processing]);
  
  return (
    <div className="relative w-full h-full min-h-[300px] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <Brain className="w-5 h-5 text-purple-400" />
        <h3 className="text-white font-semibold">Neural Network</h3>
        {processing && (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <Zap className="w-4 h-4 text-cyan-400" />
          </motion.div>
        )}
      </div>
      
      {/* Neural Network Visualization */}
      <div className="flex-1 relative">
        <svg
          ref={svgRef}
          className="w-full h-full"
          viewBox="0 0 400 300"
          preserveAspectRatio="xMidYMid meet"
        >
          {/* Particle effects background */}
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
            
            <radialGradient id="nodeGradient">
              <stop offset="0%" stopColor="rgba(168, 85, 247, 0.8)" />
              <stop offset="100%" stopColor="rgba(168, 85, 247, 0.2)" />
            </radialGradient>
            
            <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="rgba(6, 182, 212, 0.2)" />
              <stop offset="50%" stopColor="rgba(168, 85, 247, 0.6)" />
              <stop offset="100%" stopColor="rgba(236, 72, 153, 0.2)" />
            </linearGradient>
          </defs>
          
          {/* Connections */}
          <g className="connections">
            {connections.map((connection, index) => {
              const fromNode = nodes.find(n => n.id === connection.from);
              const toNode = nodes.find(n => n.id === connection.to);
              
              if (!fromNode || !toNode) return null;
              
              return (
                <g key={`${connection.from}-${connection.to}`}>
                  {/* Connection line */}
                  <motion.line
                    x1={fromNode.x}
                    y1={fromNode.y}
                    x2={toNode.x}
                    y2={toNode.y}
                    stroke={connection.active ? "url(#connectionGradient)" : "rgba(255, 255, 255, 0.1)"}
                    strokeWidth={connection.active ? 2 : 1}
                    initial={{ pathLength: 0 }}
                    animate={{ 
                      pathLength: 1,
                      opacity: connection.active ? [0.3, 1, 0.3] : 0.2 
                    }}
                    transition={{ 
                      duration: 2,
                      repeat: connection.active ? Infinity : 0 
                    }}
                  />
                  
                  {/* Particle flow on active connections */}
                  {connection.active && dataFlow.map((offset, i) => (
                    <motion.circle
                      key={`particle-${i}`}
                      r="2"
                      fill="rgba(34, 211, 238, 0.8)"
                      filter="url(#glow)"
                      initial={{ 
                        x: fromNode.x,
                        y: fromNode.y 
                      }}
                      animate={{
                        x: [fromNode.x, toNode.x],
                        y: [fromNode.y, toNode.y],
                        opacity: [0, 1, 0]
                      }}
                      transition={{
                        duration: 1,
                        delay: i * 0.2,
                        repeat: Infinity,
                        ease: "easeInOut"
                      }}
                    />
                  ))}
                </g>
              );
            })}
          </g>
          
          {/* Nodes */}
          <g className="nodes">
            {nodes.map((node, index) => (
              <motion.g
                key={node.id}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                {/* Node glow effect */}
                {node.active && (
                  <motion.circle
                    cx={node.x}
                    cy={node.y}
                    r="25"
                    fill="none"
                    stroke="rgba(168, 85, 247, 0.4)"
                    strokeWidth="2"
                    initial={{ r: 15, opacity: 0 }}
                    animate={{ r: 25, opacity: [0, 0.6, 0] }}
                    transition={{ duration: 1, repeat: Infinity }}
                  />
                )}
                
                {/* Main node */}
                <motion.circle
                  cx={node.x}
                  cy={node.y}
                  r="15"
                  fill={node.active ? "url(#nodeGradient)" : "rgba(168, 85, 247, 0.3)"}
                  stroke={node.active ? "rgba(168, 85, 247, 0.8)" : "rgba(168, 85, 247, 0.4)"}
                  strokeWidth="2"
                  filter={node.active ? "url(#glow)" : undefined}
                  animate={{
                    scale: node.active ? [1, 1.2, 1] : 1,
                  }}
                  transition={{ duration: 0.5 }}
                  whileHover={{ scale: 1.1 }}
                  onClick={() => !processing && activateNode(node.id)}
                  className="cursor-pointer"
                />
                
                {/* Node value */}
                <text
                  x={node.x}
                  y={node.y}
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="white"
                  fontSize="10"
                  className="pointer-events-none"
                >
                  {(node.value * 100).toFixed(0)}
                </text>
              </motion.g>
            ))}
          </g>
        </svg>
      </div>
      
      {/* Control Button */}
      <motion.button
        onClick={processData}
        disabled={processing}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="mt-4 px-4 py-2 bg-purple-500/20 border border-purple-400/50 rounded-lg text-purple-300 disabled:opacity-50 transition-all"
      >
        {processing ? 'Processing...' : 'Process Data'}
      </motion.button>
      
      {/* Status */}
      <div className="mt-2 text-xs text-white/50">
        Nodes: {nodes.filter(n => n.active).length}/{nodes.length} active • 
        Entropy: {(globalEntropy * 100).toFixed(0)}%
      </div>
    </div>
  );
};

export default NeuralNetworkModule;