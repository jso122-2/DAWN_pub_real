import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LivingModuleWrapper } from '../consciousness/LivingModuleWrapper';
import { useRealTimeConsciousness } from '../../../dawn-desktop/src/hooks/useRealTimeConsciousness';
import { useModuleCommunication } from '../../hooks/useModuleCommunication';

interface Node {
  id: string;
  x: number;
  y: number;
  value: number;
  label: string;
  color: string;
}

export function TestModule({ 
  moduleId = "test-neural-1",
  onNodeActivated 
}: {
  moduleId?: string;
  onNodeActivated?: (nodeId: string, value: number) => void;
}) {
  const consciousness = useRealTimeConsciousness();
  const { sendMessage, messages } = useModuleCommunication(
    moduleId, 
    'neural-cluster', 
    ['neural_processing', 'node_activation']
  );

  // Create nodes that respond to consciousness
  const [nodes, setNodes] = useState<Node[]>([]);
  const [connections, setConnections] = useState<Array<{ from: string; to: string; active: boolean }>>([]);

  // Initialize nodes based on consciousness data
  useEffect(() => {
    const newNodes: Node[] = [
      { 
        id: 'consciousness-core', 
        x: 50, 
        y: 30,
        value: consciousness.scup / 100,
        label: 'Consciousness Core',
        color: consciousness.scup > 70 ? '#4CAF50' : consciousness.scup > 40 ? '#FF9800' : '#F44336'
      },
      { 
        id: 'entropy-node', 
        x: 150, 
        y: 80,
        value: consciousness.entropy,
        label: 'Entropy Field',
        color: `hsl(${consciousness.entropy * 60}, 70%, 50%)`
      },
      { 
        id: 'neural-activity', 
        x: 120, 
        y: 150,
        value: consciousness.neuralActivity,
        label: 'Neural Activity',
        color: `rgba(156, 39, 176, ${0.3 + consciousness.neuralActivity * 0.7})`
      },
      {
        id: 'mood-state',
        x: 200,
        y: 120,
        value: consciousness.mood === 'critical' ? 1 : consciousness.mood === 'excited' ? 0.8 : 0.5,
        label: 'Mood State',
        color: consciousness.mood === 'critical' ? '#F44336' : 
               consciousness.mood === 'excited' ? '#FF9800' : 
               consciousness.mood === 'active' ? '#2196F3' : '#4CAF50'
      }
    ];
    
    setNodes(newNodes);
    
    // Create connections between nodes
    setConnections([
      { from: 'consciousness-core', to: 'entropy-node', active: consciousness.scup > 50 },
      { from: 'entropy-node', to: 'neural-activity', active: consciousness.entropy > 0.5 },
      { from: 'neural-activity', to: 'mood-state', active: consciousness.neuralActivity > 0.6 },
      { from: 'consciousness-core', to: 'mood-state', active: consciousness.scup > 70 }
    ]);
  }, [consciousness]);

  // Handle node clicks
  const handleNodeClick = (nodeId: string, value: number) => {
    onNodeActivated?.(nodeId, value);
    
    // Send neural spike message
    sendMessage('neural_spike', {
      nodeId,
      value,
      clusterId: moduleId,
      timestamp: Date.now()
    }, undefined, value > 0.8 ? 'high' : 'normal');
  };

  // Listen for incoming messages
  useEffect(() => {
    const consciousnessMessages = messages.filter(msg => msg.type === 'consciousness_update');
    if (consciousnessMessages.length > 0) {
      // React to consciousness updates from other modules
      console.log(`${moduleId} received consciousness update:`, consciousnessMessages[consciousnessMessages.length - 1]);
    }
  }, [messages, moduleId]);

  return (
    <LivingModuleWrapper moduleId={moduleId} className="h-full" data-module-id={moduleId}>
      <div className="p-4 h-full">
        <h3 className="text-white/80 text-sm mb-4 font-mono">Neural Cluster: {moduleId}</h3>
        
        <div className="relative h-48 bg-black/20 rounded-lg overflow-hidden">
          <svg className="w-full h-full">
            {/* Connections */}
            {connections.map((conn, i) => {
              const fromNode = nodes.find(n => n.id === conn.from);
              const toNode = nodes.find(n => n.id === conn.to);
              if (!fromNode || !toNode) return null;
              
              return (
                <motion.line
                  key={`${conn.from}-${conn.to}`}
                  x1={fromNode.x}
                  y1={fromNode.y}
                  x2={toNode.x}
                  y2={toNode.y}
                  stroke={conn.active ? '#4FC3F7' : 'rgba(255,255,255,0.2)'}
                  strokeWidth={conn.active ? 2 : 1}
                  animate={{
                    opacity: conn.active ? [0.5, 1, 0.5] : 0.3,
                    strokeWidth: conn.active ? [1, 3, 1] : 1
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    delay: i * 0.2
                  }}
                />
              );
            })}
            
            {/* Nodes */}
            {nodes.map((node) => (
              <g key={node.id}>
                <motion.circle
                  cx={node.x}
                  cy={node.y}
                  r={8 + node.value * 12}
                  fill={node.color}
                  stroke="rgba(255,255,255,0.5)"
                  strokeWidth={1}
                  style={{ cursor: 'pointer' }}
                  onClick={() => handleNodeClick(node.id, node.value)}
                  animate={{
                    r: [8 + node.value * 12, 12 + node.value * 16, 8 + node.value * 12],
                    opacity: [0.7, 1, 0.7]
                  }}
                  transition={{
                    duration: 1.5 + node.value,
                    repeat: Infinity,
                    delay: node.x * 0.01
                  }}
                  whileHover={{ scale: 1.2 }}
                  whileTap={{ scale: 0.9 }}
                />
                
                <text
                  x={node.x}
                  y={node.y + 30}
                  textAnchor="middle"
                  className="text-xs fill-white/60 font-mono"
                  style={{ pointerEvents: 'none' }}
                >
                  {node.label}
                </text>
                
                <text
                  x={node.x}
                  y={node.y + 42}
                  textAnchor="middle"
                  className="text-xs fill-white/80 font-mono"
                  style={{ pointerEvents: 'none' }}
                >
                  {(node.value * 100).toFixed(0)}%
                </text>
              </g>
            ))}
          </svg>
        </div>

        <div className="mt-4 space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Active Connections</span>
            <span className="text-xs text-white font-mono">{connections.filter(c => c.active).length}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Messages Received</span>
            <span className="text-xs text-white font-mono">{messages.length}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-xs text-white/60">Cluster State</span>
            <span className={`text-xs font-mono px-2 py-1 rounded ${
              consciousness.mood === 'critical' ? 'bg-red-500/20 text-red-300' :
              consciousness.mood === 'excited' ? 'bg-yellow-500/20 text-yellow-300' :
              'bg-green-500/20 text-green-300'
            }`}>
              {consciousness.mood.toUpperCase()}
            </span>
          </div>
        </div>
      </div>
    </LivingModuleWrapper>
  );
} 