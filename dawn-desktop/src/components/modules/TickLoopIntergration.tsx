import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  GitBranch, 
  Activity, 
  Zap, 
  Database, 
  Radio,
  AlertTriangle,
  TrendingUp,
  Cpu,
  MemoryStick,
  Network
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';
import { getPythonExecutor, ProcessHandle, OutputChunk, ResourceMetrics } from '@/services/PythonExecutor';

// Data transformation types
interface TickData {
  id: string;
  timestamp: number;
  type: 'neural' | 'consciousness' | 'genomic' | 'system';
  value: number;
  metadata?: Record<string, any>;
}

interface DataBuffer {
  processId: string;
  buffer: TickData[];
  lastFlush: number;
  flushInterval: number;
}

interface BridgeMetrics {
  dataRate: number; // Data points per second
  latency: number; // Average latency in ms
  bufferedData: number; // Number of buffered items
  activeConnections: number;
}

interface PythonBridgeProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
  tickRate?: number; // Tick loop frequency in Hz
  onTickData?: (data: TickData[]) => void;
}

const PythonBridge: React.FC<PythonBridgeProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0,
  tickRate = 60,
  onTickData
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [activeProcesses, setActiveProcesses] = useState<ProcessHandle[]>([]);
  const [bridgeMetrics, setBridgeMetrics] = useState<BridgeMetrics>({
    dataRate: 0,
    latency: 0,
    bufferedData: 0,
    activeConnections: 0
  });
  const [dataFlow, setDataFlow] = useState<Record<string, number>>({});
  const [wsConnections, setWsConnections] = useState<Map<string, WebSocket>>(new Map());
  
  // Refs for performance optimization
  const dataBuffers = useRef<Map<string, DataBuffer>>(new Map());
  const metricsInterval = useRef<number | null>(null);
  const tickInterval = useRef<number | null>(null);
  const dataRateCounter = useRef(0);
  const executor = useRef(getPythonExecutor());
  
  // API configuration
  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';
  
  // Initialize bridge
  useEffect(() => {
    initializeBridge();
    
    return () => {
      cleanup();
    };
  }, []);
  
  // Initialize bridge connections and monitoring
  const initializeBridge = async () => {
    try {
      // Set up executor event listeners
      executor.current.on('connected', handleExecutorConnected);
      executor.current.on('disconnected', handleExecutorDisconnected);
      executor.current.on('process-started', handleProcessStarted);
      executor.current.on('process-completed', handleProcessCompleted);
      executor.current.on('process-error', handleProcessError);
      executor.current.on('output', handleProcessOutput);
      executor.current.on('metrics', handleResourceUpdate);
      
      // Start tick loop integration
      startTickLoop();
      
      // Start metrics monitoring
      startMetricsMonitoring();
      
      // Check connection status
      const status = await checkConnectionStatus();
      setIsConnected(status);
      
    } catch (error) {
      console.error('[PythonBridge] Initialization failed:', error);
      emitter.emit('bridge:error', { error });
    }
  };
  
  // Check API connection status
  const checkConnectionStatus = async (): Promise<boolean> => {
    try {
      const response = await fetch(`${API_BASE}/api/python/status`);
      return response.ok;
    } catch {
      return false;
    }
  };
  
  // Handle executor connection
  const handleExecutorConnected = () => {
    setIsConnected(true);
    emitter.emit('bridge:connected');
  };
  
  // Handle executor disconnection
  const handleExecutorDisconnected = () => {
    setIsConnected(false);
    emitter.emit('bridge:disconnected');
  };
  
  // Handle process started
  const handleProcessStarted = (handle: ProcessHandle) => {
    setActiveProcesses(prev => [...prev, handle]);
    
    // Initialize data buffer for this process
    dataBuffers.current.set(handle.id, {
      processId: handle.id,
      buffer: [],
      lastFlush: Date.now(),
      flushInterval: 1000 / tickRate // Flush at tick rate
    });
    
    // Create WebSocket for output streaming
    createOutputWebSocket(handle.id);
    
    // Emit to tick loop
    emitter.emit('tick:process-started', {
      processId: handle.id,
      script: handle.script,
      timestamp: Date.now()
    });
  };
  
  // Handle process completed
  const handleProcessCompleted = (handle: ProcessHandle) => {
    setActiveProcesses(prev => prev.filter(p => p.id !== handle.id));
    
    // Flush remaining buffer data
    flushBuffer(handle.id);
    
    // Clean up resources
    dataBuffers.current.delete(handle.id);
    closeOutputWebSocket(handle.id);
    
    // Emit to tick loop
    emitter.emit('tick:process-completed', {
      processId: handle.id,
      exitCode: handle.exitCode,
      timestamp: Date.now()
    });
  };
  
  // Handle process error
  const handleProcessError = (handle: ProcessHandle) => {
    console.error(`[PythonBridge] Process error: ${handle.id}`, handle.error);
    
    // Clean up
    setActiveProcesses(prev => prev.filter(p => p.id !== handle.id));
    dataBuffers.current.delete(handle.id);
    closeOutputWebSocket(handle.id);
    
    // Emit error to tick loop
    emitter.emit('tick:process-error', {
      processId: handle.id,
      error: handle.error,
      timestamp: Date.now()
    });
  };
  
  // Handle process output
  const handleProcessOutput = (chunk: OutputChunk) => {
    // Parse output for tick data
    const tickData = parseOutputToTickData(chunk);
    
    if (tickData) {
      // Add to buffer
      const buffer = dataBuffers.current.get(chunk.processId);
      if (buffer) {
        buffer.buffer.push(tickData);
        dataRateCounter.current++;
        
        // Check if buffer needs flushing
        if (Date.now() - buffer.lastFlush >= buffer.flushInterval) {
          flushBuffer(chunk.processId);
        }
      }
    }
    
    // Update data flow visualization
    setDataFlow(prev => ({
      ...prev,
      [chunk.processId]: (prev[chunk.processId] || 0) + 1
    }));
  };
  
  // Handle resource metrics update
  const handleResourceUpdate = (metrics: ResourceMetrics) => {
    // Emit metrics to tick loop for visualization
    emitter.emit('tick:resource-update', {
      processId: metrics.processId,
      cpu: metrics.cpu,
      memory: metrics.memory,
      timestamp: Date.now()
    });
  };
  
  // Parse output to tick data
  const parseOutputToTickData = (chunk: OutputChunk): TickData | null => {
    try {
      // Look for JSON data in output
      const jsonMatch = chunk.data.match(/\{.*\}/);
      if (jsonMatch) {
        const data = JSON.parse(jsonMatch[0]);
        
        // Transform to tick data format
        return {
          id: `${chunk.processId}-${Date.now()}`,
          timestamp: chunk.timestamp,
          type: detectDataType(data),
          value: extractValue(data),
          metadata: data
        };
      }
      
      // Look for progress indicators
      const progressMatch = chunk.data.match(/progress:\s*(\d+(?:\.\d+)?)/i);
      if (progressMatch) {
        return {
          id: `${chunk.processId}-progress-${Date.now()}`,
          timestamp: chunk.timestamp,
          type: 'system',
          value: parseFloat(progressMatch[1]),
          metadata: { type: 'progress' }
        };
      }
      
      return null;
    } catch (error) {
      console.warn('[PythonBridge] Failed to parse output:', error);
      return null;
    }
  };
  
  // Detect data type from parsed data
  const detectDataType = (data: any): TickData['type'] => {
    if (data.type) return data.type;
    if (data.neural || data.neurons) return 'neural';
    if (data.consciousness || data.qubits) return 'consciousness';
    if (data.sequence || data.genome) return 'genomic';
    return 'system';
  };
  
  // Extract numerical value from data
  const extractValue = (data: any): number => {
    if (typeof data.value === 'number') return data.value;
    if (typeof data.score === 'number') return data.score;
    if (typeof data.probability === 'number') return data.probability;
    if (typeof data.fitness === 'number') return data.fitness;
    return 0;
  };
  
  // Flush buffer to tick loop
  const flushBuffer = (processId: string) => {
    const buffer = dataBuffers.current.get(processId);
    if (!buffer || buffer.buffer.length === 0) return;
    
    // Send to tick loop
    if (onTickData) {
      onTickData(buffer.buffer);
    }
    
    // Emit to event system
    emitter.emit('tick:data-batch', {
      processId,
      data: buffer.buffer,
      count: buffer.buffer.length,
      timestamp: Date.now()
    });
    
    // Update metrics
    setBridgeMetrics(prev => ({
      ...prev,
      bufferedData: prev.bufferedData - buffer.buffer.length
    }));
    
    // Clear buffer
    buffer.buffer = [];
    buffer.lastFlush = Date.now();
  };
  
  // Create WebSocket for output streaming
  const createOutputWebSocket = (processId: string) => {
    const ws = new WebSocket(`ws://localhost:8001/api/python/output/${processId}/stream`);
    
    ws.onopen = () => {
      console.log(`[PythonBridge] Output WebSocket connected for ${processId}`);
      setWsConnections(prev => new Map(prev).set(processId, ws));
      setBridgeMetrics(prev => ({
        ...prev,
        activeConnections: prev.activeConnections + 1
      }));
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleProcessOutput({
          stream: data.type || 'stdout',
          data: data.content,
          timestamp: data.timestamp || Date.now(),
          processId
        });
      } catch (error) {
        console.error('[PythonBridge] WebSocket message parse error:', error);
      }
    };
    
    ws.onerror = (error) => {
      console.error(`[PythonBridge] WebSocket error for ${processId}:`, error);
    };
    
    ws.onclose = () => {
      console.log(`[PythonBridge] Output WebSocket closed for ${processId}`);
      setWsConnections(prev => {
        const newMap = new Map(prev);
        newMap.delete(processId);
        return newMap;
      });
      setBridgeMetrics(prev => ({
        ...prev,
        activeConnections: Math.max(0, prev.activeConnections - 1)
      }));
    };
  };
  
  // Close output WebSocket
  const closeOutputWebSocket = (processId: string) => {
    const ws = wsConnections.get(processId);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.close();
    }
  };
  
  // Start tick loop integration
  const startTickLoop = () => {
    tickInterval.current = setInterval(() => {
      // Flush all buffers at tick rate
      dataBuffers.current.forEach((buffer, processId) => {
        if (buffer.buffer.length > 0) {
          flushBuffer(processId);
        }
      });
    }, 1000 / tickRate) as any;
  };
  
  // Start metrics monitoring
  const startMetricsMonitoring = () => {
    metricsInterval.current = setInterval(() => {
      // Calculate data rate
      const dataRate = dataRateCounter.current;
      dataRateCounter.current = 0;
      
      // Calculate total buffered data
      let bufferedData = 0;
      dataBuffers.current.forEach(buffer => {
        bufferedData += buffer.buffer.length;
      });
      
      // Update metrics
      setBridgeMetrics(prev => ({
        ...prev,
        dataRate,
        bufferedData,
        latency: calculateAverageLatency()
      }));
    }, 1000) as any;
  };
  
  // Calculate average latency
  const calculateAverageLatency = (): number => {
    // Simple estimation based on buffer sizes
    let totalLatency = 0;
    let count = 0;
    
    dataBuffers.current.forEach(buffer => {
      if (buffer.buffer.length > 0) {
        const oldestData = buffer.buffer[0];
        totalLatency += Date.now() - oldestData.timestamp;
        count++;
      }
    });
    
    return count > 0 ? Math.round(totalLatency / count) : 0;
  };
  
  // Execute Python script via API
  const executePythonScript = async (script: string, args: Record<string, any>) => {
    try {
      const response = await fetch(`${API_BASE}/api/python/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ script, args })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      return result.processId;
    } catch (error) {
      console.error('[PythonBridge] Failed to execute script:', error);
      throw error;
    }
  };
  
  // Kill process via API
  const killPythonProcess = async (processId: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/python/kill/${processId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('[PythonBridge] Failed to kill process:', error);
      throw error;
    }
  };
  
  // Cleanup
  const cleanup = () => {
    // Clear intervals
    if (tickInterval.current) clearInterval(tickInterval.current);
    if (metricsInterval.current) clearInterval(metricsInterval.current);
    
    // Close all WebSocket connections
    wsConnections.forEach(ws => ws.close());
    
    // Remove event listeners
    executor.current.off('connected', handleExecutorConnected);
    executor.current.off('disconnected', handleExecutorDisconnected);
    executor.current.off('process-started', handleProcessStarted);
    executor.current.off('process-completed', handleProcessCompleted);
    executor.current.off('process-error', handleProcessError);
    executor.current.off('output', handleProcessOutput);
    executor.current.off('metrics', handleResourceUpdate);
  };
  
  // Get connection status color
  const getConnectionColor = () => {
    if (!isConnected) return 'text-red-400';
    if (activeProcesses.length === 0) return 'text-yellow-400';
    return 'text-green-400';
  };
  
  return (
    <div className="w-full h-full flex flex-col p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-purple-400" />
          <h3 className="text-white font-semibold">Python Bridge</h3>
          <div className={`flex items-center gap-1 ${getConnectionColor()}`}>
            <Radio className="w-4 h-4" />
            <span className="text-xs">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
        <div className="text-xs text-white/50">
          Tick Rate: {tickRate}Hz
        </div>
      </div>
      
      {/* Connection Status */}
      <div className="grid grid-cols-4 gap-2">
        {/* Data Rate */}
        <motion.div 
          className="glass-panel glass-depth-1 p-3 rounded-lg"
          animate={{ 
            boxShadow: bridgeMetrics.dataRate > 0 
              ? '0 0 20px rgba(34, 211, 238, 0.3)' 
              : undefined 
          }}
        >
          <div className="flex items-center justify-between">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            <span className="text-xs text-white/50">Data Rate</span>
          </div>
          <div className="text-lg font-mono text-white mt-1">
            {bridgeMetrics.dataRate}
            <span className="text-xs text-white/50 ml-1">pts/s</span>
          </div>
        </motion.div>
        
        {/* Latency */}
        <div className="glass-panel glass-depth-1 p-3 rounded-lg">
          <div className="flex items-center justify-between">
            <Activity className="w-4 h-4 text-yellow-400" />
            <span className="text-xs text-white/50">Latency</span>
          </div>
          <div className="text-lg font-mono text-white mt-1">
            {bridgeMetrics.latency}
            <span className="text-xs text-white/50 ml-1">ms</span>
          </div>
        </div>
        
        {/* Buffer */}
        <div className="glass-panel glass-depth-1 p-3 rounded-lg">
          <div className="flex items-center justify-between">
            <Database className="w-4 h-4 text-purple-400" />
            <span className="text-xs text-white/50">Buffered</span>
          </div>
          <div className="text-lg font-mono text-white mt-1">
            {bridgeMetrics.bufferedData}
            <span className="text-xs text-white/50 ml-1">items</span>
          </div>
        </div>
        
        {/* Connections */}
        <div className="glass-panel glass-depth-1 p-3 rounded-lg">
          <div className="flex items-center justify-between">
            <Network className="w-4 h-4 text-green-400" />
            <span className="text-xs text-white/50">Active</span>
          </div>
          <div className="text-lg font-mono text-white mt-1">
            {bridgeMetrics.activeConnections}
            <span className="text-xs text-white/50 ml-1">ws</span>
          </div>
        </div>
      </div>
      
      {/* Active Processes */}
      <div className="flex-1 overflow-y-auto space-y-2">
        <h4 className="text-sm text-white/70 mb-2">Active Processes</h4>
        
        <AnimatePresence>
          {activeProcesses.map((process) => (
            <motion.div
              key={process.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="glass-panel glass-depth-1 p-3 rounded-lg"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-purple-400" />
                  <span className="text-sm text-white">{process.script}</span>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                  >
                    <Zap className="w-3 h-3 text-green-400" />
                  </motion.div>
                </div>
                
                {/* Data flow indicator */}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-white/50">
                    {dataFlow[process.id] || 0} events
                  </span>
                  <motion.div
                    className="w-16 h-1 bg-white/10 rounded-full overflow-hidden"
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <motion.div
                      className="h-full bg-gradient-to-r from-purple-500 to-cyan-500"
                      animate={{ x: ['-100%', '100%'] }}
                      transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                    />
                  </motion.div>
                </div>
              </div>
              
              {/* Process metadata */}
              <div className="mt-2 text-xs text-white/50">
                PID: {process.pid || 'N/A'} | 
                Started: {new Date(process.startTime).toLocaleTimeString()}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {activeProcesses.length === 0 && (
          <div className="text-center text-white/30 py-8">
            No active Python processes
          </div>
        )}
      </div>
      
      {/* Visual Data Flow */}
      <div className="h-16 relative overflow-hidden rounded-lg bg-black/30">
        {/* Flowing particles to represent data */}
        <AnimatePresence>
          {activeProcesses.map((process, index) => (
            <motion.div
              key={`flow-${process.id}`}
              className="absolute h-full w-full"
              style={{ top: `${(index / activeProcesses.length) * 100}%` }}
            >
              {[...Array(5)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-2 h-2 rounded-full"
                  style={{
                    backgroundColor: index % 2 === 0 ? '#a855f7' : '#06b6d4',
                    left: `${i * 20}%`
                  }}
                  animate={{
                    x: ['0%', '100%'],
                    opacity: [0, 1, 1, 0]
                  }}
                  transition={{
                    duration: 2,
                    delay: i * 0.4,
                    repeat: Infinity,
                    ease: 'linear'
                  }}
                />
              ))}
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Labels */}
        <div className="absolute inset-0 flex items-center justify-between px-4 pointer-events-none">
          <span className="text-xs text-white/50">Python</span>
          <span className="text-xs text-white/50">→</span>
          <span className="text-xs text-white/50">Tick Loop</span>
        </div>
      </div>
      
      {/* Status Footer */}
      <div className="flex items-center justify-between text-xs text-white/50">
        <span>Entropy: {(globalEntropy * 100).toFixed(0)}%</span>
        <span>Bridge v1.0.0</span>
      </div>
    </div>
  );
};

export default PythonBridge;