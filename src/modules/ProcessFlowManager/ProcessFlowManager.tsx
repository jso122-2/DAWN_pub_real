import React, { useEffect, useRef, useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Stars } from '@react-three/drei';
import { ProcessNode } from './ProcessNode';
import { DataFlow } from './DataFlow';
import { ProcessControls } from './ProcessControls';
import { ProcessMonitor } from './ProcessMonitor';
import { useProcessFlowStore } from '../../store/processFlowStore';
import { ProcessUtils } from '../../services/processManager';
import './ProcessFlowManager.css';

// Mock WebSocket context for now - will be replaced with actual context
const mockWebSocketContext = {
  lastTick: {
    tick_number: Math.floor(Date.now() / 1000),
    scup: Math.random() * 100,
    timestamp: Date.now()
  }
};

export const ProcessFlowManager: React.FC = () => {
  const {
    processes,
    flows,
    selectedProcessId,
    viewMode,
    showMetrics,
    autoArrange,
    flowSpeed,
    addProcess,
    autoArrangeProcesses,
    updateProcess
  } = useProcessFlowStore();
  
  const { lastTick } = mockWebSocketContext; // Replace with actual useWebSocket hook
  const canvasRef = useRef<HTMLDivElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  
  // Initialize with default processes
  useEffect(() => {
    if (processes.size === 0) {
      const defaultProcesses = [
        {
          id: 'neural-processor',
          name: 'Neural Processor',
          script: 'neural_process.py',
          status: 'idle' as const,
          category: 'neural' as const,
          cpuUsage: 0,
          memoryUsage: 0,
          executionTime: 0,
          lastTick: 0,
          inputs: [{ 
            id: 'in1', 
            name: 'Raw Data', 
            type: 'data' as const, 
            dataType: 'json' as const, 
            connected: false 
          }],
          outputs: [{ 
            id: 'out1', 
            name: 'Processed', 
            type: 'data' as const, 
            dataType: 'tensor' as const, 
            connected: false 
          }],
          description: 'Processes raw consciousness data through neural networks',
          author: 'DAWN',
          version: '1.0.0',
          dependencies: ['tensorflow', 'numpy'],
          logs: [],
          errors: [],
          outputData: null,
          position: { x: -200, y: 0, z: 0 },
          velocity: { x: 0, y: 0, z: 0 }
        },
        {
          id: 'consciousness-analyzer',
          name: 'Consciousness Analyzer',
          script: 'consciousness_analysis.py',
          status: 'idle' as const,
          category: 'consciousness' as const,
          cpuUsage: 0,
          memoryUsage: 0,
          executionTime: 0,
          lastTick: 0,
          inputs: [{ 
            id: 'in1', 
            name: 'Neural Output', 
            type: 'data' as const, 
            dataType: 'tensor' as const, 
            connected: false 
          }],
          outputs: [{ 
            id: 'out1', 
            name: 'Consciousness State', 
            type: 'stream' as const, 
            dataType: 'signal' as const, 
            connected: false 
          }],
          description: 'Analyzes neural patterns for consciousness unity',
          author: 'DAWN',
          version: '1.0.0',
          dependencies: ['qiskit', 'numpy'],
          logs: [],
          errors: [],
          outputData: null,
          position: { x: 200, y: 0, z: 0 },
          velocity: { x: 0, y: 0, z: 0 }
        },
        {
          id: 'memory-consolidator',
          name: 'Memory Consolidator',
          script: 'memory_consolidate.py',
          status: 'idle' as const,
          category: 'memory' as const,
          cpuUsage: 0,
          memoryUsage: 0,
          executionTime: 0,
          lastTick: 0,
          inputs: [{ 
            id: 'in1', 
            name: 'Memory Data', 
            type: 'data' as const, 
            dataType: 'json' as const, 
            connected: false 
          }],
          outputs: [{ 
            id: 'out1', 
            name: 'Consolidated', 
            type: 'data' as const, 
            dataType: 'json' as const, 
            connected: false 
          }],
          description: 'Consolidates scattered memories into coherent patterns',
          author: 'DAWN',
          version: '1.0.0',
          dependencies: ['numpy', 'sklearn'],
          logs: [],
          errors: [],
          outputData: null,
          position: { x: 0, y: 200, z: 0 },
          velocity: { x: 0, y: 0, z: 0 }
        }
      ];
      
      defaultProcesses.forEach(process => addProcess(process));
      setIsLoading(false);
    }
  }, [processes.size, addProcess]);
  
  // Auto-arrange on mount if enabled
  useEffect(() => {
    if (autoArrange && processes.size > 0) {
      autoArrangeProcesses();
    }
  }, [autoArrange, processes.size, autoArrangeProcesses]);
  
  // Update process metrics based on tick data
  useEffect(() => {
    if (lastTick && processes.size > 0) {
      processes.forEach((process) => {
        if (process.status === 'running') {
          updateProcess(process.id, {
            cpuUsage: Math.random() * 50 + lastTick.scup / 2,
            memoryUsage: Math.random() * 100,
            lastTick: lastTick.tick_number
          });
        }
      });
    }
  }, [lastTick, processes, updateProcess]);
  
  if (isLoading) {
    return (
      <div className="process-flow-manager loading">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <p>Initializing Process Flow Manager...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="process-flow-manager">
      <div className="flow-header">
        <h2>🌊 Process Flow Manager</h2>
        <div className="flow-stats">
          <span className="stat-item">
            <span className="stat-label">Active:</span>
            <span className="stat-value running">
              {Array.from(processes.values()).filter(p => p.status === 'running').length}
            </span>
          </span>
          <span className="stat-item">
            <span className="stat-label">Flows:</span>
            <span className="stat-value">{flows.size}</span>
          </span>
          <span className="stat-item">
            <span className="stat-label">Speed:</span>
            <span className="stat-value">{flowSpeed.toFixed(1)}x</span>
          </span>
        </div>
      </div>
      
      <div className="flow-container">
        <ProcessControls />
        
        <div className="flow-canvas" ref={canvasRef}>
          {viewMode === '3d' ? (
            <Canvas>
              <Suspense fallback={<div>Loading 3D Scene...</div>}>
                <PerspectiveCamera makeDefault position={[0, 0, 500]} />
                <OrbitControls 
                  enablePan={true} 
                  enableZoom={true} 
                  enableRotate={true}
                  maxDistance={1000}
                  minDistance={100}
                />
                
                <ambientLight intensity={0.2} />
                <pointLight position={[10, 10, 10]} intensity={0.8} />
                <pointLight position={[-10, -10, -10]} intensity={0.4} color="#00ff88" />
                
                <Stars 
                  radius={500} 
                  depth={50} 
                  count={3000} 
                  factor={4} 
                  saturation={0.2} 
                  fade 
                />
                
                {/* Render process nodes */}
                {Array.from(processes.values()).map((process) => (
                  <ProcessNode key={process.id} process={process} />
                ))}
                
                {/* Render data flows */}
                {Array.from(flows.values()).map((flow) => (
                  <DataFlow key={flow.id} flow={flow} processes={processes} />
                ))}
              </Suspense>
            </Canvas>
          ) : (
            <div className="flow-2d-view">
              <svg width="100%" height="100%" viewBox="-400 -300 800 600">
                <defs>
                  <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge> 
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                </defs>
                
                {/* Render flows as paths */}
                {Array.from(flows.values()).map((flow) => {
                  const source = processes.get(flow.sourceProcessId);
                  const target = processes.get(flow.targetProcessId);
                  if (!source || !target) return null;
                  
                  const midX = (source.position.x + target.position.x) / 2;
                  const midY = (source.position.y + target.position.y) / 2 - 50;
                  
                  return (
                    <path
                      key={flow.id}
                      d={`M ${source.position.x} ${source.position.y} Q ${midX} ${midY} ${target.position.x} ${target.position.y}`}
                      stroke={flow.color}
                      strokeWidth="3"
                      fill="none"
                      opacity={flow.intensity}
                      filter="url(#glow)"
                    />
                  );
                })}
                
                {/* Render process nodes */}
                {Array.from(processes.values()).map((process) => (
                  <g key={process.id} transform={`translate(${process.position.x}, ${process.position.y})`}>
                    <rect
                      x="-60"
                      y="-35"
                      width="120"
                      height="70"
                      rx="15"
                      fill={`var(--category-${process.category})`}
                      stroke="#00ff88"
                      strokeWidth={selectedProcessId === process.id ? 3 : 1}
                      opacity="0.8"
                      filter="url(#glow)"
                    />
                    <text 
                      textAnchor="middle" 
                      y="-10" 
                      fill="white" 
                      fontSize="14"
                      fontWeight="600"
                    >
                      {process.name}
                    </text>
                    <text 
                      textAnchor="middle" 
                      y="10" 
                      fill="rgba(255,255,255,0.7)" 
                      fontSize="12"
                    >
                      {process.status.toUpperCase()}
                    </text>
                    <circle
                      cx="45"
                      cy="-25"
                      r="8"
                      fill={ProcessUtils.getStatusColor(process.status)}
                      className={process.status === 'running' ? 'pulse' : ''}
                    />
                  </g>
                ))}
              </svg>
            </div>
          )}
        </div>
        
        {showMetrics && selectedProcessId && (
          <ProcessMonitor processId={selectedProcessId} />
        )}
      </div>
    </div>
  );
}; 