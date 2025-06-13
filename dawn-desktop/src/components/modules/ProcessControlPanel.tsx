import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { 
  Cpu,
  MemoryStick,
  Gauge,
  Clock,
  GitBranch,
  Play,
  Pause,
  AlertTriangle,
  BarChart3,
  Zap,
  Calendar,
  Settings,
  ArrowRight,
  Layers,
  Database,
  Activity,
  Timer,
  Workflow
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';

// Process types
interface ProcessNode {
  id: string;
  name: string;
  type: 'python' | 'system' | 'quantum' | 'neural';
  status: 'queued' | 'running' | 'completed' | 'error' | 'paused';
  dependencies: string[];
  resources: {
    cpu: number; // cores
    memory: number; // GB
    gpu?: number; // percentage
    priority: 'low' | 'normal' | 'high' | 'critical';
  };
  schedule?: {
    type: 'immediate' | 'scheduled' | 'triggered';
    cron?: string;
    trigger?: string;
  };
  metrics?: {
    startTime?: Date;
    duration?: number;
    cpuUsage?: number;
    memoryUsage?: number;
    errorRate?: number;
  };
}

// Pipeline branch
interface PipelineBranch {
  id: string;
  name: string;
  parallel: boolean;
  nodes: ProcessNode[];
}

interface ProcessControlPanelProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
}

const ProcessControlPanel: React.FC<ProcessControlPanelProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0 
}) => {
  const [processQueue, setProcessQueue] = useState<ProcessNode[]>([]);
  const [branches, setBranches] = useState<PipelineBranch[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<ProcessNode | null>(null);
  const [resourceUsage, setResourceUsage] = useState({
    cpu: 45,
    memory: 62,
    gpu: 30
  });
  const [activeView, setActiveView] = useState<'queue' | 'resources' | 'schedule' | 'metrics'>('queue');
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  // Initialize with sample processes
  useEffect(() => {
    const sampleProcesses: ProcessNode[] = [
      {
        id: 'proc-1',
        name: 'genome_analyzer.py',
        type: 'python',
        status: 'running',
        dependencies: [],
        resources: { cpu: 4, memory: 8, gpu: 20, priority: 'high' },
        schedule: { type: 'immediate' },
        metrics: { startTime: new Date(), cpuUsage: 75, memoryUsage: 60 }
      },
      {
        id: 'proc-2',
        name: 'neural_training.py',
        type: 'neural',
        status: 'queued',
        dependencies: ['proc-1'],
        resources: { cpu: 8, memory: 16, gpu: 80, priority: 'critical' },
        schedule: { type: 'triggered', trigger: 'proc-1:complete' }
      },
      {
        id: 'proc-3',
        name: 'quantum_simulation.py',
        type: 'quantum',
        status: 'queued',
        dependencies: [],
        resources: { cpu: 2, memory: 4, priority: 'normal' },
        schedule: { type: 'scheduled', cron: '0 */2 * * *' }
      }
    ];
    
    setProcessQueue(sampleProcesses);
    
    // Create pipeline branches
    setBranches([
      {
        id: 'branch-1',
        name: 'Main Pipeline',
        parallel: false,
        nodes: [sampleProcesses[0], sampleProcesses[1]]
      },
      {
        id: 'branch-2',
        name: 'Parallel Tasks',
        parallel: true,
        nodes: [sampleProcesses[2]]
      }
    ]);
  }, []);
  
  // Simulate resource usage updates
  useEffect(() => {
    const interval = setInterval(() => {
      setResourceUsage(prev => ({
        cpu: Math.min(100, Math.max(0, prev.cpu + (Math.random() - 0.5) * 10)),
        memory: Math.min(100, Math.max(0, prev.memory + (Math.random() - 0.5) * 5)),
        gpu: Math.min(100, Math.max(0, prev.gpu + (Math.random() - 0.5) * 15))
      }));
    }, 2000);
    
    return () => clearInterval(interval);
  }, []);
  
  // Draw holographic pipeline visualization
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const drawPipeline = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw connections
      branches.forEach((branch, branchIndex) => {
        const y = 50 + branchIndex * 100;
        
        branch.nodes.forEach((node, nodeIndex) => {
          const x = 50 + nodeIndex * 150;
          
          // Draw node
          ctx.beginPath();
          ctx.arc(x, y, 30, 0, Math.PI * 2);
          
          const gradient = ctx.createRadialGradient(x, y, 0, x, y, 30);
          if (node.status === 'running') {
            gradient.addColorStop(0, 'rgba(34, 197, 94, 0.8)');
            gradient.addColorStop(1, 'rgba(34, 197, 94, 0.2)');
          } else if (node.status === 'error') {
            gradient.addColorStop(0, 'rgba(239, 68, 68, 0.8)');
            gradient.addColorStop(1, 'rgba(239, 68, 68, 0.2)');
          } else {
            gradient.addColorStop(0, 'rgba(168, 85, 247, 0.8)');
            gradient.addColorStop(1, 'rgba(168, 85, 247, 0.2)');
          }
          
          ctx.fillStyle = gradient;
          ctx.fill();
          
          // Draw connection line
          if (nodeIndex < branch.nodes.length - 1) {
            ctx.beginPath();
            ctx.moveTo(x + 30, y);
            ctx.lineTo(x + 120, y);
            ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
            ctx.lineWidth = 2;
            ctx.stroke();
          }
          
          // Draw label
          ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
          ctx.font = '10px monospace';
          ctx.textAlign = 'center';
          ctx.fillText(node.name.slice(0, 10), x, y + 50);
        });
      });
    };
    
    drawPipeline();
    
    const animationFrame = requestAnimationFrame(function animate() {
      drawPipeline();
      requestAnimationFrame(animate);
    });
    
    return () => cancelAnimationFrame(animationFrame);
  }, [branches]);
  
  // Reorder processes in queue
  const handleReorder = (newOrder: ProcessNode[]) => {
    setProcessQueue(newOrder);
    emitter.emit('process:reorder', { order: newOrder.map(p => p.id) });
  };
  
  // Update process resources
  const updateProcessResources = (processId: string, resources: Partial<ProcessNode['resources']>) => {
    setProcessQueue(prev => prev.map(p => 
      p.id === processId 
        ? { ...p, resources: { ...p.resources, ...resources } }
        : p
    ));
  };
  
  // Get status color
  const getStatusColor = (status: ProcessNode['status']) => {
    switch (status) {
      case 'running': return 'bg-green-500';
      case 'completed': return 'bg-blue-500';
      case 'error': return 'bg-red-500';
      case 'paused': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };
  
  // Get priority color
  const getPriorityColor = (priority: ProcessNode['resources']['priority']) => {
    switch (priority) {
      case 'critical': return 'text-red-400';
      case 'high': return 'text-orange-400';
      case 'normal': return 'text-blue-400';
      case 'low': return 'text-gray-400';
    }
  };
  
  return (
    <div className="w-full h-full flex flex-col p-4 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Workflow className="w-6 h-6 text-purple-400" />
          <h3 className="text-white font-bold text-lg">Process Control Panel</h3>
        </div>
        
        {/* View Selector */}
        <div className="flex gap-2">
          {(['queue', 'resources', 'schedule', 'metrics'] as const).map(view => (
            <button
              key={view}
              onClick={() => setActiveView(view)}
              className={`px-3 py-1 rounded-lg text-sm transition-all ${
                activeView === view
                  ? 'bg-purple-500/30 text-purple-300 border border-purple-400/50'
                  : 'bg-white/5 text-white/60 hover:bg-white/10'
              }`}
            >
              {view.charAt(0).toUpperCase() + view.slice(1)}
            </button>
          ))}
        </div>
      </div>
      
      {/* Main Content Area */}
      <div className="flex-1 flex gap-4">
        {/* Left Panel - Queue/Pipeline */}
        <div className="flex-1 space-y-4">
          {activeView === 'queue' && (
            <>
              {/* Pipeline Visualization */}
              <div className="glass-panel glass-depth-2 rounded-xl p-4">
                <h4 className="text-white/80 font-medium mb-3 flex items-center gap-2">
                  <GitBranch className="w-4 h-4" />
                  Pipeline Flow
                </h4>
                <canvas
                  ref={canvasRef}
                  width={600}
                  height={200}
                  className="w-full h-48 rounded-lg bg-black/30"
                />
              </div>
              
              {/* Process Queue */}
              <div className="glass-panel glass-depth-2 rounded-xl p-4">
                <h4 className="text-white/80 font-medium mb-3 flex items-center gap-2">
                  <Layers className="w-4 h-4" />
                  Process Queue
                </h4>
                <Reorder.Group
                  axis="y"
                  values={processQueue}
                  onReorder={handleReorder}
                  className="space-y-2"
                >
                  {processQueue.map((process) => (
                    <Reorder.Item
                      key={process.id}
                      value={process}
                      className="glass-panel glass-depth-1 rounded-lg p-3 cursor-move"
                      whileHover={{ scale: 1.02 }}
                      whileDrag={{ scale: 1.05 }}
                      onClick={() => setSelectedProcess(process)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${getStatusColor(process.status)}`} />
                          <div>
                            <div className="text-white text-sm font-medium">{process.name}</div>
                            <div className="text-xs text-white/50">
                              {process.dependencies.length > 0 && `Depends on: ${process.dependencies.join(', ')}`}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`text-xs ${getPriorityColor(process.resources.priority)}`}>
                            {process.resources.priority}
                          </span>
                          {process.status === 'running' ? (
                            <Pause className="w-4 h-4 text-yellow-400" />
                          ) : (
                            <Play className="w-4 h-4 text-green-400" />
                          )}
                        </div>
                      </div>
                    </Reorder.Item>
                  ))}
                </Reorder.Group>
              </div>
            </>
          )}
          
          {activeView === 'resources' && (
            <div className="glass-panel glass-depth-2 rounded-xl p-4 space-y-4">
              <h4 className="text-white/80 font-medium mb-3 flex items-center gap-2">
                <Cpu className="w-4 h-4" />
                Resource Allocation
              </h4>
              
              {/* Resource Meters */}
              <div className="space-y-6">
                {/* CPU Meter */}
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-white/70">CPU Usage</span>
                    <span className="text-cyan-400">{resourceUsage.cpu.toFixed(0)}%</span>
                  </div>
                  <div className="h-3 bg-black/50 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                      animate={{ width: `${resourceUsage.cpu}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                  <div className="mt-2 grid grid-cols-8 gap-1">
                    {[...Array(8)].map((_, i) => (
                      <div
                        key={i}
                        className={`h-8 rounded ${
                          i < Math.floor(resourceUsage.cpu / 12.5)
                            ? 'bg-cyan-500/50'
                            : 'bg-white/5'
                        }`}
                      />
                    ))}
                  </div>
                </div>
                
                {/* Memory Meter */}
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-white/70">Memory Usage</span>
                    <span className="text-purple-400">{resourceUsage.memory.toFixed(0)}%</span>
                  </div>
                  <div className="h-3 bg-black/50 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                      animate={{ width: `${resourceUsage.memory}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>
                
                {/* GPU Meter */}
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-white/70">GPU Usage</span>
                    <span className="text-green-400">{resourceUsage.gpu.toFixed(0)}%</span>
                  </div>
                  <div className="h-3 bg-black/50 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                      animate={{ width: `${resourceUsage.gpu}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>
              </div>
              
              {/* Allocation Controls */}
              {selectedProcess && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6 p-4 bg-white/5 rounded-lg space-y-4"
                >
                  <h5 className="text-white/80 text-sm font-medium">
                    Allocate Resources: {selectedProcess.name}
                  </h5>
                  
                  {/* CPU Cores */}
                  <div>
                    <label className="text-xs text-white/60 block mb-1">CPU Cores</label>
                    <input
                      type="range"
                      min="1"
                      max="16"
                      value={selectedProcess.resources.cpu}
                      onChange={(e) => updateProcessResources(selectedProcess.id, { cpu: parseInt(e.target.value) })}
                      className="w-full accent-cyan-500"
                    />
                    <div className="flex justify-between text-xs text-white/40 mt-1">
                      <span>1 core</span>
                      <span>{selectedProcess.resources.cpu} cores</span>
                      <span>16 cores</span>
                    </div>
                  </div>
                  
                  {/* Memory */}
                  <div>
                    <label className="text-xs text-white/60 block mb-1">Memory (GB)</label>
                    <input
                      type="range"
                      min="1"
                      max="64"
                      value={selectedProcess.resources.memory}
                      onChange={(e) => updateProcessResources(selectedProcess.id, { memory: parseInt(e.target.value) })}
                      className="w-full accent-purple-500"
                    />
                    <div className="flex justify-between text-xs text-white/40 mt-1">
                      <span>1 GB</span>
                      <span>{selectedProcess.resources.memory} GB</span>
                      <span>64 GB</span>
                    </div>
                  </div>
                  
                  {/* Priority */}
                  <div>
                    <label className="text-xs text-white/60 block mb-2">Priority</label>
                    <div className="flex gap-2">
                      {(['low', 'normal', 'high', 'critical'] as const).map(priority => (
                        <button
                          key={priority}
                          onClick={() => updateProcessResources(selectedProcess.id, { priority })}
                          className={`px-3 py-1 rounded text-xs transition-all ${
                            selectedProcess.resources.priority === priority
                              ? 'bg-purple-500/30 text-purple-300 border border-purple-400/50'
                              : 'bg-white/5 text-white/60 hover:bg-white/10'
                          }`}
                        >
                          {priority}
                        </button>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
          )}
          
          {activeView === 'schedule' && (
            <div className="glass-panel glass-depth-2 rounded-xl p-4">
              <h4 className="text-white/80 font-medium mb-4 flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Process Scheduling
              </h4>
              
              <div className="space-y-4">
                {processQueue.map(process => (
                  <div key={process.id} className="p-3 bg-white/5 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-white text-sm font-medium">{process.name}</span>
                      <span className={`text-xs px-2 py-1 rounded ${
                        process.schedule?.type === 'immediate' ? 'bg-green-500/20 text-green-400' :
                        process.schedule?.type === 'scheduled' ? 'bg-blue-500/20 text-blue-400' :
                        'bg-yellow-500/20 text-yellow-400'
                      }`}>
                        {process.schedule?.type}
                      </span>
                    </div>
                    
                    {process.schedule?.type === 'scheduled' && (
                      <div className="flex items-center gap-2 text-xs text-white/60">
                        <Clock className="w-3 h-3" />
                        <span>Cron: {process.schedule.cron}</span>
                      </div>
                    )}
                    
                    {process.schedule?.type === 'triggered' && (
                      <div className="flex items-center gap-2 text-xs text-white/60">
                        <Zap className="w-3 h-3" />
                        <span>Trigger: {process.schedule.trigger}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {activeView === 'metrics' && (
            <div className="glass-panel glass-depth-2 rounded-xl p-4">
              <h4 className="text-white/80 font-medium mb-4 flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                Performance Metrics
              </h4>
              
              {/* Metrics Grid */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-2xl font-bold text-cyan-400">
                    {processQueue.filter(p => p.status === 'running').length}
                  </div>
                  <div className="text-xs text-white/60">Active Processes</div>
                </div>
                
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-2xl font-bold text-green-400">
                    {processQueue.filter(p => p.status === 'completed').length}
                  </div>
                  <div className="text-xs text-white/60">Completed</div>
                </div>
                
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-2xl font-bold text-red-400">
                    {processQueue.filter(p => p.status === 'error').length}
                  </div>
                  <div className="text-xs text-white/60">Errors</div>
                </div>
                
                <div className="p-4 bg-white/5 rounded-lg">
                  <div className="text-2xl font-bold text-purple-400">
                    {(globalEntropy * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-white/60">System Entropy</div>
                </div>
              </div>
              
              {/* Process Timeline */}
              <div className="mt-6">
                <h5 className="text-white/70 text-sm mb-3">Process Timeline</h5>
                <div className="space-y-2">
                  {processQueue.slice(0, 5).map((process, index) => (
                    <div key={process.id} className="flex items-center gap-3">
                      <div className="text-xs text-white/40 w-16">
                        {new Date().toLocaleTimeString().slice(0, 5)}
                      </div>
                      <div className="flex-1 h-6 bg-white/5 rounded overflow-hidden">
                        <motion.div
                          className={`h-full ${
                            process.status === 'running' ? 'bg-gradient-to-r from-green-500 to-emerald-500' :
                            process.status === 'completed' ? 'bg-gradient-to-r from-blue-500 to-cyan-500' :
                            'bg-gradient-to-r from-gray-500 to-gray-600'
                          }`}
                          initial={{ width: 0 }}
                          animate={{ width: `${Math.random() * 100}%` }}
                          transition={{ duration: 1, delay: index * 0.1 }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Right Panel - Selected Process Details */}
        {selectedProcess && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="w-80 glass-panel glass-depth-2 rounded-xl p-4"
          >
            <h4 className="text-white/80 font-medium mb-4">Process Details</h4>
            
            <div className="space-y-4">
              {/* Status */}
              <div>
                <label className="text-xs text-white/60">Status</label>
                <div className="flex items-center gap-2 mt-1">
                  <div className={`w-3 h-3 rounded-full ${getStatusColor(selectedProcess.status)}`} />
                  <span className="text-white text-sm">{selectedProcess.status}</span>
                </div>
              </div>
              
              {/* Type */}
              <div>
                <label className="text-xs text-white/60">Type</label>
                <div className="text-white text-sm mt-1">{selectedProcess.type}</div>
              </div>
              
              {/* Dependencies */}
              {selectedProcess.dependencies.length > 0 && (
                <div>
                  <label className="text-xs text-white/60">Dependencies</label>
                  <div className="mt-1 space-y-1">
                    {selectedProcess.dependencies.map(dep => (
                      <div key={dep} className="text-xs text-white/70 flex items-center gap-1">
                        <ArrowRight className="w-3 h-3" />
                        {dep}
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Metrics */}
              {selectedProcess.metrics && (
                <div>
                  <label className="text-xs text-white/60">Current Metrics</label>
                  <div className="mt-2 space-y-2">
                    {selectedProcess.metrics.cpuUsage && (
                      <div className="flex justify-between text-xs">
                        <span className="text-white/50">CPU Usage</span>
                        <span className="text-cyan-400">{selectedProcess.metrics.cpuUsage}%</span>
                      </div>
                    )}
                    {selectedProcess.metrics.memoryUsage && (
                      <div className="flex justify-between text-xs">
                        <span className="text-white/50">Memory Usage</span>
                        <span className="text-purple-400">{selectedProcess.metrics.memoryUsage}%</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Actions */}
              <div className="pt-4 space-y-2">
                <button className="w-full px-4 py-2 bg-green-500/20 hover:bg-green-500/30 border border-green-400/50 rounded-lg text-green-400 text-sm transition-all">
                  Start Process
                </button>
                <button className="w-full px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-400/50 rounded-lg text-red-400 text-sm transition-all">
                  Terminate
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </div>
      
      {/* Holographic Effects */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-500/50 to-transparent animate-pulse" />
        <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent animate-pulse" />
      </div>
    </div>
  );
};

export default ProcessControlPanel; 