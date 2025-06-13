import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Play, 
  Square, 
  Wifi, 
  WifiOff, 
  Zap, 
  Monitor, 
  Settings,
  AlertTriangle,
  CheckCircle,
  Clock,
  Cpu
} from 'lucide-react';
import { ConsciousModule } from './ConsciousModule';

// Temporary mock types until FastAPIBackend is available
interface MockConnectionHealth {
  isConnected: boolean;
  latency: number;
  wsConnections: number;
  lastPing?: number;
}

interface MockBatchExecuteRequest {
  requests: Array<{
    script: string;
    args: Record<string, any>;
    priority: number;
  }>;
  sequential: boolean;
  onProgress?: (current: number, total: number) => void;
}

// Mock hook for demonstration
const useMockDAWNApi = () => ({
  client: {
    executePythonScript: async (params: any) => ({ process_id: `mock-${Date.now()}` }),
    killProcess: async (id: string) => ({ success: true }),
    on: (event: string, handler: Function) => {},
    off: (event: string, handler: Function) => {}
  },
  isConnected: true,
  healthMetrics: {
    isConnected: true,
    latency: 23,
    wsConnections: 1,
    lastPing: Date.now()
  } as MockConnectionHealth,
  executeBatch: async (request: MockBatchExecuteRequest) => ({
    processes: request.requests.map((_, i) => ({ process_id: `batch-${i}` })),
    failedRequests: []
  }),
  streamOutput: async (processId: string) => new ReadableStream(),
  checkHealth: async () => {}
});

// Example component demonstrating DAWN API integration
export function ApiIntegrationExample() {
  // Use mock hook temporarily
  const { 
    client, 
    isConnected, 
    healthMetrics, 
    executeBatch, 
    streamOutput, 
    checkHealth 
  } = useMockDAWNApi();

  const [processes, setProcesses] = useState<string[]>([]);
  const [batchProgress, setBatchProgress] = useState({ current: 0, total: 0 });
  const [tickData, setTickData] = useState<any>(null);
  const [consciousnessLevel, setConsciousnessLevel] = useState(0.75);
  const [outputStreams, setOutputStreams] = useState<Map<string, string>>(new Map());
  const [isExecutingBatch, setIsExecutingBatch] = useState(false);

  const outputRef = useRef<HTMLDivElement>(null);

  // ===== Event Handlers =====

  useEffect(() => {
    // Subscribe to real-time updates
    const handleTickUpdate = (data: any) => {
      setTickData(data);
      setConsciousnessLevel(data.scup / 100);
    };

    const handlePythonOutput = ({ processId, chunk }: any) => {
      setOutputStreams(prev => {
        const newStreams = new Map(prev);
        const existing = newStreams.get(processId) || '';
        newStreams.set(processId, existing + chunk.content + '\n');
        return newStreams;
      });
    };

    const handleProcessStatus = ({ processId, status }: any) => {
      if (status === 'completed') {
        setProcesses(prev => prev.filter(id => id !== processId));
      }
    };

    client.on('tick:update', handleTickUpdate);
    client.on('python:output', handlePythonOutput);
    client.on('python:status', handleProcessStatus);

    return () => {
      client.off('tick:update', handleTickUpdate);
      client.off('python:output', handlePythonOutput);
      client.off('python:status', handleProcessStatus);
    };
  }, [client]);

  // ===== API Operations =====

  const executeSingleScript = useCallback(async () => {
    try {
      const result = await client.executePythonScript({
        script: 'neural_analysis.py',
        args: { 
          mode: 'consciousness',
          iterations: 1000,
          entropy_threshold: consciousnessLevel 
        },
        priority: 5
      });
      
      setProcesses(prev => [...prev, result.process_id]);
      console.log('Started process:', result.process_id);
    } catch (error) {
      console.error('Failed to execute script:', error);
    }
  }, [client, consciousnessLevel]);

  const executeBatchScripts = useCallback(async () => {
    setIsExecutingBatch(true);
    setBatchProgress({ current: 0, total: 0 });

    const batchRequest: MockBatchExecuteRequest = {
      requests: [
        {
          script: 'neural_mapping.py',
          args: { depth: 'deep', resolution: 'high' },
          priority: 8
        },
        {
          script: 'quantum_coherence.py',
          args: { qubits: 16, entanglement_strength: 0.8 },
          priority: 7
        },
        {
          script: 'consciousness_metrics.py',
          args: { analysis_type: 'full', include_dreams: true },
          priority: 6
        },
        {
          script: 'system_diagnostics.py',
          args: { comprehensive: true, repair_mode: 'auto' },
          priority: 5
        }
      ],
      sequential: false, // Execute in parallel
      onProgress: (current: number, total: number) => {
        setBatchProgress({ current, total });
      }
    };

    try {
      const result = await executeBatch(batchRequest);
      
      setProcesses(prev => [
        ...prev, 
        ...result.processes.map((p: any) => p.process_id)
      ]);
      
      console.log('Batch executed:', result);
      
      if (result.failedRequests.length > 0) {
        console.warn('Some requests failed:', result.failedRequests);
      }
    } catch (error) {
      console.error('Batch execution failed:', error);
    } finally {
      setIsExecutingBatch(false);
    }
  }, [executeBatch]);

  const killAllProcesses = useCallback(async () => {
    const killPromises = processes.map(processId => 
      client.killProcess(processId).catch((err: any) => 
        console.warn(`Failed to kill process ${processId}:`, err)
      )
    );
    
    await Promise.allSettled(killPromises);
    setProcesses([]);
    setOutputStreams(new Map());
  }, [client, processes]);

  const streamProcessOutput = useCallback(async (processId: string) => {
    try {
      const stream = await streamOutput(processId);
      const reader = stream.getReader();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        setOutputStreams(prev => {
          const newStreams = new Map(prev);
          const existing = newStreams.get(processId) || '';
          newStreams.set(processId, existing + (value as any).content + '\n');
          return newStreams;
        });
      }
    } catch (error) {
      console.error('Stream error:', error);
    }
  }, [streamOutput]);

  // ===== Health Status Component =====

  const HealthStatus: React.FC<{ metrics: MockConnectionHealth }> = ({ metrics }) => (
    <motion.div 
      className="glass-base p-4 rounded-lg"
      animate={{
        scale: [1, 1.02, 1],
        opacity: [0.9, 1, 0.9]
      }}
      transition={{
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-white font-medium flex items-center gap-2">
          {metrics.isConnected ? (
            <><Wifi className="w-4 h-4 text-green-400" /> Connected</>
          ) : (
            <><WifiOff className="w-4 h-4 text-red-400" /> Disconnected</>
          )}
        </h3>
        <button
          onClick={checkHealth}
          className="p-1 rounded hover:bg-white/10 transition-colors"
        >
          <Settings className="w-4 h-4 text-white/70" />
        </button>
      </div>
      
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-white/70">Latency:</span>
          <span className="text-white">{metrics.latency}ms</span>
        </div>
        <div className="flex justify-between">
          <span className="text-white/70">WebSocket Connections:</span>
          <span className="text-white">{metrics.wsConnections}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-white/70">Last Ping:</span>
          <span className="text-white">
            {metrics.lastPing ? new Date(metrics.lastPing).toLocaleTimeString() : 'Never'}
          </span>
        </div>
      </div>
    </motion.div>
  );

  // ===== Render =====

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h2 className="text-2xl font-bold text-white mb-2">
          DAWN API Integration Demo
        </h2>
        <p className="text-white/70">
          Demonstrating consciousness-aware Python execution and real-time monitoring
        </p>
      </motion.div>

      {/* Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* Connection Health */}
        <HealthStatus metrics={healthMetrics} />

        {/* Tick Data */}
        <ConsciousModule
          moduleId="tick-monitor"
          mood={tickData?.mood === 'chaotic' ? 'critical' : 'calm'}
          consciousnessLevel={tickData?.scup || 50}
          entropyLevel={tickData?.entropy || 0.3}
          category="monitor"
        >
          <div className="glass-base p-4 rounded-lg space-y-3">
            <h3 className="text-white font-medium flex items-center gap-2">
              <Activity className="w-4 h-4" />
              Consciousness Monitor
            </h3>
            {tickData ? (
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-white/70">Tick:</span>
                  <span className="text-white">#{tickData.tick_number}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/70">SCUP:</span>
                  <span className="text-white">{tickData.scup}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/70">Entropy:</span>
                  <span className="text-white">{(tickData.entropy * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/70">Mood:</span>
                  <span className={`capitalize ${
                    tickData.mood === 'chaotic' ? 'text-red-400' :
                    tickData.mood === 'excited' ? 'text-orange-400' :
                    tickData.mood === 'active' ? 'text-blue-400' :
                    'text-green-400'
                  }`}>
                    {tickData.mood}
                  </span>
                </div>
              </div>
            ) : (
              <div className="text-white/50">Simulating consciousness data...</div>
            )}
          </div>
        </ConsciousModule>

        {/* Process Control */}
        <ConsciousModule
          moduleId="process-control"
          mood={processes.length > 0 ? 'active' : 'calm'}
          consciousnessLevel={50 + (processes.length * 10)}
          isActive={processes.length > 0}
          category="process"
        >
          <div className="glass-base p-4 rounded-lg space-y-3">
            <h3 className="text-white font-medium flex items-center gap-2">
              <Cpu className="w-4 h-4" />
              Process Manager
            </h3>
            <div className="text-sm text-white/70">
              Active: {processes.length} processes
            </div>
            <div className="flex gap-2">
              <button
                onClick={executeSingleScript}
                disabled={!isConnected}
                className="flex-1 p-2 bg-green-500/20 hover:bg-green-500/30 disabled:bg-gray-500/20 disabled:cursor-not-allowed rounded text-white text-xs flex items-center justify-center gap-1 transition-colors"
              >
                <Play className="w-3 h-3" />
                Single
              </button>
              <button
                onClick={executeBatchScripts}
                disabled={!isConnected || isExecutingBatch}
                className="flex-1 p-2 bg-blue-500/20 hover:bg-blue-500/30 disabled:bg-gray-500/20 disabled:cursor-not-allowed rounded text-white text-xs flex items-center justify-center gap-1 transition-colors"
              >
                <Zap className="w-3 h-3" />
                Batch
              </button>
              <button
                onClick={killAllProcesses}
                disabled={processes.length === 0}
                className="flex-1 p-2 bg-red-500/20 hover:bg-red-500/30 disabled:bg-gray-500/20 disabled:cursor-not-allowed rounded text-white text-xs flex items-center justify-center gap-1 transition-colors"
              >
                <Square className="w-3 h-3" />
                Kill All
              </button>
            </div>
            
            {/* Batch Progress */}
            {isExecutingBatch && (
              <div className="space-y-2">
                <div className="flex justify-between text-xs text-white/70">
                  <span>Batch Progress</span>
                  <span>{batchProgress.current}/{batchProgress.total}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <motion.div
                    className="bg-blue-500 h-2 rounded-full"
                    animate={{ 
                      width: `${(batchProgress.current / Math.max(batchProgress.total, 1)) * 100}%` 
                    }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>
            )}
          </div>
        </ConsciousModule>
      </div>

      {/* Process Output */}
      <AnimatePresence>
        {outputStreams.size > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="glass-base rounded-lg"
          >
            <div className="p-4 border-b border-white/10">
              <h3 className="text-white font-medium flex items-center gap-2">
                <Monitor className="w-4 h-4" />
                Process Output
              </h3>
            </div>
            <div 
              ref={outputRef}
              className="p-4 space-y-4 max-h-96 overflow-y-auto"
            >
              {Array.from(outputStreams.entries()).map(([processId, output]) => (
                <div key={processId} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-white/70 text-sm font-mono">
                      Process: {processId}
                    </span>
                    <button
                      onClick={() => streamProcessOutput(processId)}
                      className="text-xs text-blue-400 hover:text-blue-300"
                    >
                      Refresh Stream
                    </button>
                  </div>
                  <pre className="text-xs text-white/80 font-mono bg-black/20 p-3 rounded overflow-x-auto">
                    {output || 'No output yet...'}
                  </pre>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Connection Status Alerts */}
      <AnimatePresence>
        {!isConnected && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="glass-base p-4 rounded-lg border border-red-500/50"
          >
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-red-400" />
              <div>
                <h4 className="text-red-400 font-medium">Connection Simulated</h4>
                <p className="text-white/70 text-sm">
                  Using mock data for demonstration. Real DAWN backend integration coming soon.
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default ApiIntegrationExample; 