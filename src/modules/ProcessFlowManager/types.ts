// src/modules/ProcessFlowManager/types.ts
export interface PythonProcess {
  id: string;
  name: string;
  script: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'paused';
  category: 'neural' | 'consciousness' | 'analysis' | 'synthesis' | 'memory';
  
  // Performance metrics
  cpuUsage: number;
  memoryUsage: number;
  executionTime: number;
  lastTick: number;
  
  // I/O configuration
  inputs: ProcessPort[];
  outputs: ProcessPort[];
  
  // Process metadata
  description: string;
  author: string;
  version: string;
  dependencies: string[];
  
  // Runtime data
  logs: ProcessLog[];
  errors: ProcessError[];
  outputData: any;
  
  // Visual positioning
  position: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
}

export interface ProcessPort {
  id: string;
  name: string;
  type: 'data' | 'trigger' | 'config' | 'stream';
  dataType: 'json' | 'tensor' | 'signal' | 'binary';
  connected: boolean;
  connectionId?: string;
}

export interface DataFlow {
  id: string;
  sourceProcessId: string;
  sourcePortId: string;
  targetProcessId: string;
  targetPortId: string;
  
  // Flow characteristics
  flowRate: number; // Data per second
  latency: number;  // ms
  dataType: string;
  
  // Visual properties
  particles: FlowParticle[];
  color: string;
  intensity: number;
}

export interface FlowParticle {
  position: { x: number; y: number; z: number };
  velocity: { x: number; y: number; z: number };
  life: number;
  data?: any;
}

export interface ProcessLog {
  timestamp: number;
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  data?: any;
}

export interface ProcessError {
  timestamp: number;
  type: string;
  message: string;
  stack?: string;
  recoverable: boolean;
}

export interface FlowState {
  processes: Map<string, PythonProcess>;
  flows: Map<string, DataFlow>;
  selectedProcessId: string | null;
  viewMode: '2d' | '3d';
  autoArrange: boolean;
  showMetrics: boolean;
  flowSpeed: number;
} 