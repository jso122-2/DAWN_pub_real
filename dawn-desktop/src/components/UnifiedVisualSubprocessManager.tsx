import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  Play, Pause, Square, Settings, Eye, EyeOff, Cpu, MemoryStick, Activity, 
  Gauge, Clock, GitBranch, AlertTriangle, BarChart3, Zap, Calendar, 
  ArrowRight, Layers, Database, Timer, Workflow, Brain, Terminal,
  CheckCircle, Loader2, Hash, TrendingUp, Smile, ChevronRight, ChevronDown
} from 'lucide-react';

// Unified process interface combining all existing types
interface UnifiedProcess {
  id: string;
  name: string;
  script?: string;
  component?: string;
  category: 'neural' | 'consciousness' | 'system' | 'memory' | 'quantum' | 'processing';
  status: 'idle' | 'running' | 'stopped' | 'error' | 'completed' | 'queued';
  enabled: boolean;
  visible: boolean;
  
  // Performance metrics
  cpu: number;
  memory: number;
  fps: number;
  
  // Process details
  description: string;
  author?: string;
  version?: string;
  dependencies?: string[];
  
  // Tick awareness
  triggers?: {
    onTick?: number;
    onSCUP?: { operator: '>' | '<' | '=' | '>=' | '<=', value: number };
    onEntropy?: { operator: '>' | '<' | '=' | '>=' | '<=', value: number };
    onMood?: string[];
    onSignal?: string;
  };
  
  // Process state
  output?: string[];
  logs?: string[];
  errors?: string[];
  startTime?: Date;
  endTime?: Date;
  exitCode?: number;
  
  // Visual properties
  position?: { x: number; y: number; z: number };
  color?: string;
  
  // Module configuration (for React components)
  modules?: { name: string; enabled: boolean }[];
  parameters?: Record<string, any>;
}

// WebSocket connection for port 3000
interface WebSocketManager {
  connected: boolean;
  tickData: any;
  subprocesses: UnifiedProcess[];
  connect: () => void;
  disconnect: () => void;
  toggleProcess: (id: string) => void;
  executeProcess: (id: string, params?: any) => void;
  killProcess: (id: string) => void;
}

const useWebSocketConnection = (port: number = 8001): WebSocketManager => {
  const [connected, setConnected] = useState(false);
  const [tickData, setTickData] = useState(null);
  const [subprocesses, setSubprocesses] = useState<UnifiedProcess[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  
  // Helper function to get category colors
  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      neural: '#00ff88',
      consciousness: '#ff6b6b',
      system: '#4ecdc4',
      memory: '#45b7d1',
      quantum: '#96ceb4',
      processing: '#feca57'
    };
    return colors[category] || '#ffffff';
  };
  
  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`ws://localhost:${port}`);
      
      ws.onopen = () => {
        console.log(`Connected to DAWN consciousness engine on port ${port}`);
        setConnected(true);
        
        // Initialize with default processes if none exist
        if (subprocesses.length === 0) {
          setSubprocesses([
            {
              id: 'neural_activity',
              name: 'Neural Activity Visualizer',
              category: 'neural',
              status: 'idle',
              enabled: true,
              visible: true,
              cpu: 0,
              memory: 0,
              fps: 0,
              description: 'Real-time neural activity visualization',
              color: getCategoryColor('neural'),
              position: { x: 0, y: 0, z: 0 }
            },
            {
              id: 'consciousness_analyzer',
              name: 'Consciousness Analyzer',
              category: 'consciousness',
              status: 'idle',
              enabled: true,
              visible: true,
              cpu: 0,
              memory: 0,
              fps: 0,
              description: 'Consciousness pattern analysis',
              color: getCategoryColor('consciousness'),
              position: { x: 0, y: 0, z: 0 }
            },
            {
              id: 'memory_consolidator',
              name: 'Memory Consolidator',
              category: 'memory',
              status: 'idle',
              enabled: true,
              visible: true,
              cpu: 0,
              memory: 0,
              fps: 0,
              description: 'Memory consolidation and optimization',
              color: getCategoryColor('memory'),
              position: { x: 0, y: 0, z: 0 }
            },
            {
              id: 'entropy_reducer',
              name: 'Entropy Reducer',
              category: 'system',
              status: 'idle',
              enabled: true,
              visible: true,
              cpu: 0,
              memory: 0,
              fps: 0,
              description: 'System entropy reduction',
              color: getCategoryColor('system'),
              position: { x: 0, y: 0, z: 0 }
            },
            {
              id: 'quantum_processor',
              name: 'Quantum State Processor',
              category: 'quantum',
              status: 'idle',
              enabled: true,
              visible: true,
              cpu: 0,
              memory: 0,
              fps: 0,
              description: 'Quantum state processing and coherence',
              color: getCategoryColor('quantum'),
              position: { x: 0, y: 0, z: 0 }
            }
          ]);
        }
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch (data.type) {
          case 'tick':
            setTickData(data.data);
            // Update subprocess metrics based on tick data
            if (data.data && data.data.subprocesses) {
              setSubprocesses(prev => {
                const serverProcesses = data.data.subprocesses;
                return prev.map(localProcess => {
                  const serverProcess = serverProcesses.find((sp: any) => sp.id === localProcess.id);
                  if (serverProcess) {
                    return {
                      ...localProcess,
                      cpu: serverProcess.metrics?.cpu || localProcess.cpu,
                      memory: serverProcess.metrics?.memory || localProcess.memory,
                      fps: serverProcess.metrics?.fps || localProcess.fps,
                      enabled: serverProcess.enabled,
                      visible: serverProcess.visible,
                      status: serverProcess.enabled ? 'running' : 'idle'
                    };
                  }
                  return localProcess;
                });
              });
            }
            break;
          case 'subprocess_list':
            // Convert server format to our format
            if (data.data && Array.isArray(data.data)) {
              const convertedProcesses = data.data.map((serverProcess: any) => ({
                id: serverProcess.id,
                name: serverProcess.name,
                category: serverProcess.category,
                status: serverProcess.enabled ? 'running' : 'idle',
                enabled: serverProcess.enabled,
                visible: serverProcess.visible,
                cpu: serverProcess.metrics?.cpu || 0,
                memory: serverProcess.metrics?.memory || 0,
                fps: serverProcess.metrics?.fps || 0,
                description: `${serverProcess.name} subprocess`,
                color: getCategoryColor(serverProcess.category),
                position: { x: 0, y: 0, z: 0 }
              }));
              setSubprocesses(convertedProcesses);
            }
            break;
          case 'subprocess_update':
            if (data.data) {
              setSubprocesses(prev => prev.map(p => 
                p.id === data.data.id 
                  ? { 
                      ...p, 
                      enabled: data.data.enabled,
                      visible: data.data.visible,
                      cpu: data.data.metrics?.cpu || p.cpu,
                      memory: data.data.metrics?.memory || p.memory,
                      fps: data.data.metrics?.fps || p.fps,
                      status: data.data.enabled ? 'running' : 'idle'
                    }
                  : p
              ));
            }
            break;
          case 'connection':
            // Initial connection message
            console.log('WebSocket connection established:', data.data);
            break;
        }
      };
      
      ws.onclose = () => {
        setConnected(false);
        setTimeout(connect, 3000); // Auto-reconnect
      };
      
      wsRef.current = ws;
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      setTimeout(connect, 3000);
    }
  }, [port, subprocesses]);
  
  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnected(false);
  }, []);
  
  const toggleProcess = useCallback((id: string) => {
    if (wsRef.current && connected) {
      wsRef.current.send(JSON.stringify({
        action: 'toggle_process',
        processId: id
      }));
    }
  }, [connected]);
  
  const executeProcess = useCallback((id: string, params?: any) => {
    if (wsRef.current && connected) {
      wsRef.current.send(JSON.stringify({
        action: 'execute_process',
        processId: id,
        parameters: params
      }));
    }
  }, [connected]);
  
  const killProcess = useCallback((id: string) => {
    if (wsRef.current && connected) {
      wsRef.current.send(JSON.stringify({
        action: 'kill_process',
        processId: id
      }));
    }
  }, [connected]);
  
  useEffect(() => {
    connect();
    return disconnect;
  }, [connect, disconnect]);
  
  return {
    connected,
    tickData,
    subprocesses,
    connect,
    disconnect,
    toggleProcess,
    executeProcess,
    killProcess
  };
};

// Sample processes combining all existing categories
const defaultProcesses: UnifiedProcess[] = [
  // Neural processes
  {
    id: 'neural-processor',
    name: 'Neural Activity Visualizer',
    script: 'neural_activity.py',
    component: 'NeuralActivityVisualizer',
    category: 'neural',
    status: 'running',
    enabled: true,
    visible: true,
    cpu: 12.3,
    memory: 45.2,
    fps: 60,
    description: 'Real-time EEG brainwave visualization',
    color: '#00ff88',
    position: { x: -200, y: 0, z: 0 }
  },
  {
    id: 'consciousness-analyzer',
    name: 'Consciousness Analyzer',
    script: 'consciousness_analyzer.py',
    category: 'consciousness',
    status: 'idle',
    enabled: false,
    visible: true,
    cpu: 0,
    memory: 0,
    fps: 0,
    description: 'Analyzes consciousness patterns and correlations',
    triggers: { onTick: 100 },
    parameters: { analysis_depth: 5, pattern_threshold: 0.7 },
    color: '#8b5cf6',
    position: { x: 200, y: 0, z: 0 }
  },
  {
    id: 'memory-consolidator',
    name: 'Memory Consolidator',
    script: 'memory_consolidate.py',
    category: 'memory',
    status: 'queued',
    enabled: true,
    visible: true,
    cpu: 0,
    memory: 0,
    fps: 0,
    description: 'Consolidates scattered memories into coherent patterns',
    triggers: { onEntropy: { operator: '>', value: 0.6 } },
    color: '#06b6d4',
    position: { x: 0, y: 200, z: 0 }
  },
  {
    id: 'entropy-reducer',
    name: 'Entropy Reducer',
    script: 'entropy_reducer.py',
    category: 'system',
    status: 'stopped',
    enabled: false,
    visible: true,
    cpu: 0,
    memory: 0,
    fps: 0,
    description: 'Reduces system entropy through memory consolidation',
    triggers: { onEntropy: { operator: '>', value: 0.6 } },
    color: '#f59e0b',
    position: { x: -200, y: -200, z: 0 }
  },
  {
    id: 'quantum-processor',
    name: 'Quantum State Processor',
    script: 'quantum_processor.py',
    category: 'quantum',
    status: 'idle',
    enabled: true,
    visible: false,
    cpu: 0,
    memory: 0,
    fps: 0,
    description: 'Processes quantum consciousness states',
    color: '#ec4899',
    position: { x: 200, y: -200, z: 0 }
  }
];

interface UnifiedVisualSubprocessManagerProps {
  port?: number;
  onProcessToggle?: (processId: string, enabled: boolean) => void;
  globalEntropy?: number;
}

export const UnifiedVisualSubprocessManager: React.FC<UnifiedVisualSubprocessManagerProps> = ({
  port = 8001,
  onProcessToggle,
  globalEntropy = 0.5
}) => {
  const {
    connected,
    tickData,
    subprocesses,
    toggleProcess,
    executeProcess,
    killProcess
  } = useWebSocketConnection(port);
  
  const [processes, setProcesses] = useState<UnifiedProcess[]>(defaultProcesses);
  const [viewMode, setViewMode] = useState<'grid' | 'list' | '3d'>('grid');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showOnlyEnabled, setShowOnlyEnabled] = useState(false);
  const [showOnlyVisible, setShowOnlyVisible] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState(new Set(['neural', 'consciousness']));
  const [selectedProcess, setSelectedProcess] = useState<UnifiedProcess | null>(null);
  
  // Merge WebSocket processes with local processes
  useEffect(() => {
    if (subprocesses.length > 0) {
      setProcesses(prev => {
        const merged = [...prev];
        subprocesses.forEach(wsProc => {
          const index = merged.findIndex(p => p.id === wsProc.id);
          if (index >= 0) {
            merged[index] = { ...merged[index], ...wsProc };
          } else {
            merged.push(wsProc);
          }
        });
        return merged;
      });
    }
  }, [subprocesses]);
  
  // Process toggle handler
  const handleToggleProcess = useCallback((processId: string) => {
    const process = processes.find(p => p.id === processId);
    if (!process) return;
    
    const newEnabled = !process.enabled;
    
    // Update local state
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { 
            ...p, 
            enabled: newEnabled,
            status: newEnabled ? 'running' : 'stopped',
            cpu: newEnabled ? Math.random() * 50 : 0,
            memory: newEnabled ? Math.random() * 100 : 0,
            fps: newEnabled ? Math.random() * 60 : 0
          }
        : p
    ));
    
    // Send to WebSocket
    if (connected) {
      toggleProcess(processId);
    }
    
    // Notify parent component
    onProcessToggle?.(processId, newEnabled);
  }, [processes, connected, toggleProcess, onProcessToggle]);
  
  // Process visibility toggle
  const handleToggleVisibility = useCallback((processId: string) => {
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { ...p, visible: !p.visible }
        : p
    ));
  }, []);
  
  // Process execution
  const handleExecuteProcess = useCallback((processId: string) => {
    const process = processes.find(p => p.id === processId);
    if (!process) return;
    
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { 
            ...p, 
            status: 'running',
            startTime: new Date(),
            cpu: Math.random() * 80 + 10,
            memory: Math.random() * 70 + 20
          }
        : p
    ));
    
    if (connected) {
      executeProcess(processId, process.parameters);
    }
  }, [processes, connected, executeProcess]);
  
  // Process termination
  const handleKillProcess = useCallback((processId: string) => {
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { 
            ...p, 
            status: 'stopped',
            endTime: new Date(),
            cpu: 0,
            memory: 0,
            fps: 0
          }
        : p
    ));
    
    if (connected) {
      killProcess(processId);
    }
  }, [connected, killProcess]);
  
  // Use WebSocket subprocesses if available, otherwise fall back to default processes
  const activeProcesses = subprocesses.length > 0 ? subprocesses : processes;
  
  // Filter processes
  const filteredProcesses = activeProcesses.filter(process => {
    if (selectedCategory !== 'all' && process.category !== selectedCategory) return false;
    if (showOnlyEnabled && !process.enabled) return false;
    if (showOnlyVisible && !process.visible) return false;
    return true;
  });
  
  // Group processes by category
  const processCategories = filteredProcesses.reduce((acc, process) => {
    if (!acc[process.category]) {
      acc[process.category] = [];
    }
    acc[process.category].push(process);
    return acc;
  }, {} as Record<string, UnifiedProcess[]>);
  
  // Category icons
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'neural': return <Brain className="w-4 h-4" />;
      case 'consciousness': return <Zap className="w-4 h-4" />;
      case 'system': return <Cpu className="w-4 h-4" />;
      case 'memory': return <Database className="w-4 h-4" />;
      case 'quantum': return <Activity className="w-4 h-4" />;
      case 'processing': return <Workflow className="w-4 h-4" />;
      default: return <Settings className="w-4 h-4" />;
    }
  };
  
  // Status color and icon
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-green-400 bg-green-500/20';
      case 'idle': return 'text-blue-400 bg-blue-500/20';
      case 'stopped': return 'text-gray-400 bg-gray-500/20';
      case 'error': return 'text-red-400 bg-red-500/20';
      case 'completed': return 'text-emerald-400 bg-emerald-500/20';
      case 'queued': return 'text-yellow-400 bg-yellow-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };
  
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Play className="w-3 h-3" />;
      case 'idle': return <Clock className="w-3 h-3" />;
      case 'stopped': return <Square className="w-3 h-3" />;
      case 'error': return <AlertTriangle className="w-3 h-3" />;
      case 'completed': return <CheckCircle className="w-3 h-3" />;
      case 'queued': return <Loader2 className="w-3 h-3 animate-spin" />;
      default: return <Settings className="w-3 h-3" />;
    }
  };
  
  const toggleCategory = (category: string) => {
    setExpandedCategories(prev => {
      const newSet = new Set(prev);
      if (newSet.has(category)) {
        newSet.delete(category);
      } else {
        newSet.add(category);
      }
      return newSet;
    });
  };
  
  return (
    <div className="w-full h-full flex flex-col bg-black/90 backdrop-blur-sm border border-purple-500/30 rounded-xl overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-purple-500/30 bg-gradient-to-r from-purple-900/50 to-blue-900/50">
        <div className="flex items-center space-x-3">
          <motion.div
            animate={{ 
              boxShadow: connected 
                ? '0 0 20px #00ff88' 
                : '0 0 20px #ff0000',
              backgroundColor: connected ? '#00ff88' : '#ff0000'
            }}
            className="w-3 h-3 rounded-full"
          />
          <h2 className="text-xl font-bold text-white">
            Visual Subprocess Manager
          </h2>
          <span className="text-sm text-gray-400">
            Port {port} • {filteredProcesses.length} processes
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
            className="px-3 py-1 rounded bg-purple-600/50 hover:bg-purple-600/70 text-white text-sm transition-colors"
          >
            {viewMode === 'grid' ? <Layers className="w-4 h-4" /> : <BarChart3 className="w-4 h-4" />}
          </button>
          
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-2 py-1 rounded bg-gray-800 text-white text-sm border border-gray-600"
          >
            <option value="all">All Categories</option>
            <option value="neural">Neural</option>
            <option value="consciousness">Consciousness</option>
            <option value="system">System</option>
            <option value="memory">Memory</option>
            <option value="quantum">Quantum</option>
            <option value="processing">Processing</option>
          </select>
          
          <label className="flex items-center space-x-2 text-sm text-gray-300">
            <input
              type="checkbox"
              checked={showOnlyEnabled}
              onChange={(e) => setShowOnlyEnabled(e.target.checked)}
              className="rounded"
            />
            <span>Enabled Only</span>
          </label>
          
          <label className="flex items-center space-x-2 text-sm text-gray-300">
            <input
              type="checkbox"
              checked={showOnlyVisible}
              onChange={(e) => setShowOnlyVisible(e.target.checked)}
              className="rounded"
            />
            <span>Visible Only</span>
          </label>
        </div>
      </div>
      
      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {viewMode === 'grid' ? (
          // Grid view
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredProcesses.map((process) => (
              <motion.div
                key={process.id}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                  process.enabled 
                    ? 'border-green-500/50 bg-gradient-to-br from-green-900/20 to-blue-900/20' 
                    : 'border-gray-600/50 bg-gray-900/50'
                } hover:border-purple-400/70 hover:shadow-lg hover:shadow-purple-500/25`}
              >
                {/* Process header */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    {getCategoryIcon(process.category)}
                    <h3 className="font-semibold text-white text-sm">{process.name}</h3>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <div className={`px-2 py-1 rounded-full text-xs flex items-center space-x-1 ${getStatusColor(process.status)}`}>
                      {getStatusIcon(process.status)}
                      <span>{process.status}</span>
                    </div>
                  </div>
                </div>
                
                {/* Process description */}
                <p className="text-gray-300 text-xs mb-3 line-clamp-2">
                  {process.description}
                </p>
                
                {/* Metrics */}
                <div className="grid grid-cols-3 gap-2 mb-3 text-xs">
                  <div className="bg-gray-800/50 rounded p-2 text-center">
                    <Cpu className="w-3 h-3 mx-auto mb-1 text-blue-400" />
                    <div className="text-white">{process.cpu.toFixed(1)}%</div>
                  </div>
                  <div className="bg-gray-800/50 rounded p-2 text-center">
                    <MemoryStick className="w-3 h-3 mx-auto mb-1 text-green-400" />
                    <div className="text-white">{process.memory.toFixed(1)}%</div>
                  </div>
                  <div className="bg-gray-800/50 rounded p-2 text-center">
                    <Activity className="w-3 h-3 mx-auto mb-1 text-purple-400" />
                    <div className="text-white">{process.fps}</div>
                  </div>
                </div>
                
                {/* Controls */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-1">
                    <button
                      onClick={() => handleToggleProcess(process.id)}
                      className={`p-1.5 rounded text-xs transition-colors ${
                        process.enabled
                          ? 'bg-red-600/20 text-red-400 hover:bg-red-600/30'
                          : 'bg-green-600/20 text-green-400 hover:bg-green-600/30'
                      }`}
                      title={process.enabled ? 'Disable' : 'Enable'}
                    >
                      {process.enabled ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
                    </button>
                    
                    <button
                      onClick={() => handleToggleVisibility(process.id)}
                      className={`p-1.5 rounded text-xs transition-colors ${
                        process.visible
                          ? 'bg-blue-600/20 text-blue-400 hover:bg-blue-600/30'
                          : 'bg-gray-600/20 text-gray-400 hover:bg-gray-600/30'
                      }`}
                      title={process.visible ? 'Hide' : 'Show'}
                    >
                      {process.visible ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                    </button>
                    
                    {process.status === 'running' && (
                      <button
                        onClick={() => handleKillProcess(process.id)}
                        className="p-1.5 rounded text-xs bg-red-600/20 text-red-400 hover:bg-red-600/30 transition-colors"
                        title="Kill Process"
                      >
                        <Square className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                  
                  <button
                    onClick={() => setSelectedProcess(process)}
                    className="p-1.5 rounded text-xs bg-purple-600/20 text-purple-400 hover:bg-purple-600/30 transition-colors"
                    title="Process Details"
                  >
                    <Settings className="w-3 h-3" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          // List view by category
          <div className="space-y-4">
            {Object.entries(processCategories).map(([category, categoryProcesses]) => (
              <div key={category} className="bg-gray-900/50 rounded-lg border border-gray-700/50">
                <button
                  onClick={() => toggleCategory(category)}
                  className="w-full flex items-center justify-between p-4 hover:bg-gray-800/50 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    {getCategoryIcon(category)}
                    <h3 className="font-semibold text-white capitalize">{category}</h3>
                    <span className="text-sm text-gray-400">({categoryProcesses.length})</span>
                  </div>
                  {expandedCategories.has(category) ? 
                    <ChevronDown className="w-4 h-4 text-gray-400" /> : 
                    <ChevronRight className="w-4 h-4 text-gray-400" />
                  }
                </button>
                
                <AnimatePresence>
                  {expandedCategories.has(category) && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="border-t border-gray-700/50"
                    >
                      {categoryProcesses.map((process) => (
                        <div
                          key={process.id}
                          className="flex items-center justify-between p-4 border-b border-gray-700/30 last:border-b-0"
                        >
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h4 className="font-medium text-white">{process.name}</h4>
                              <div className={`px-2 py-1 rounded-full text-xs flex items-center space-x-1 ${getStatusColor(process.status)}`}>
                                {getStatusIcon(process.status)}
                                <span>{process.status}</span>
                              </div>
                            </div>
                            <p className="text-gray-400 text-sm">{process.description}</p>
                            <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                              <span>CPU: {process.cpu.toFixed(1)}%</span>
                              <span>Memory: {process.memory.toFixed(1)}%</span>
                              <span>FPS: {process.fps}</span>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleToggleProcess(process.id)}
                              className={`px-3 py-1 rounded text-sm transition-colors ${
                                process.enabled
                                  ? 'bg-red-600/20 text-red-400 hover:bg-red-600/30'
                                  : 'bg-green-600/20 text-green-400 hover:bg-green-600/30'
                              }`}
                            >
                              {process.enabled ? 'Disable' : 'Enable'}
                            </button>
                            
                            <button
                              onClick={() => handleToggleVisibility(process.id)}
                              className={`p-2 rounded transition-colors ${
                                process.visible
                                  ? 'bg-blue-600/20 text-blue-400 hover:bg-blue-600/30'
                                  : 'bg-gray-600/20 text-gray-400 hover:bg-gray-600/30'
                              }`}
                            >
                              {process.visible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                            </button>
                          </div>
                        </div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {/* Process Detail Modal */}
      <AnimatePresence>
        {selectedProcess && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            onClick={() => setSelectedProcess(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-gray-900 rounded-xl border border-purple-500/30 p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-white">{selectedProcess.name}</h3>
                <button
                  onClick={() => setSelectedProcess(null)}
                  className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
                >
                  <span className="text-gray-400 text-xl">&times;</span>
                </button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <h4 className="text-white font-semibold mb-2">Description</h4>
                  <p className="text-gray-300">{selectedProcess.description}</p>
                </div>
                
                {selectedProcess.script && (
                  <div>
                    <h4 className="text-white font-semibold mb-2">Script</h4>
                    <code className="bg-gray-800 px-3 py-1 rounded text-green-400">{selectedProcess.script}</code>
                  </div>
                )}
                
                {selectedProcess.triggers && (
                  <div>
                    <h4 className="text-white font-semibold mb-2">Triggers</h4>
                    <div className="bg-gray-800 p-3 rounded">
                      <pre className="text-sm text-gray-300">
                        {JSON.stringify(selectedProcess.triggers, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
                
                {selectedProcess.parameters && (
                  <div>
                    <h4 className="text-white font-semibold mb-2">Parameters</h4>
                    <div className="bg-gray-800 p-3 rounded">
                      <pre className="text-sm text-gray-300">
                        {JSON.stringify(selectedProcess.parameters, null, 2)}
                      </pre>
                    </div>
                  </div>
                )}
                
                <div className="flex space-x-3">
                  <button
                    onClick={() => handleExecuteProcess(selectedProcess.id)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors flex items-center space-x-2"
                  >
                    <Play className="w-4 h-4" />
                    <span>Execute</span>
                  </button>
                  
                  <button
                    onClick={() => handleToggleProcess(selectedProcess.id)}
                    className={`px-4 py-2 rounded-lg transition-colors flex items-center space-x-2 ${
                      selectedProcess.enabled
                        ? 'bg-red-600 hover:bg-red-700 text-white'
                        : 'bg-blue-600 hover:bg-blue-700 text-white'
                    }`}
                  >
                    {selectedProcess.enabled ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                    <span>{selectedProcess.enabled ? 'Disable' : 'Enable'}</span>
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UnifiedVisualSubprocessManager; 