import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Terminal, 
  Play, 
  Square, 
  RotateCcw, 
  ChevronDown, 
  ChevronRight,
  Cpu,
  Brain,
  Dna,
  BarChart,
  Activity,
  Download,
  Loader2,
  AlertCircle,
  CheckCircle,
  Clock,
  Zap,
  Hash,
  TrendingDown,
  TrendingUp,
  Smile
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';
import { useDAWNApi } from '@/services/DAWNApiClient';
import type { TickData, PythonProcess } from '@/services/DAWNApiClient';

// Tick-aware process definition
interface TickAwareProcess {
  script: string;
  description: string;
  category: string;
  triggers: {
    onTick?: number;
    onSCUP?: { operator: '>' | '<' | '=' | '>=' | '<=', value: number };
    onEntropy?: { operator: '>' | '<' | '=' | '>=' | '<=', value: number };
    onMood?: string[];
    onSignal?: string;
  };
  params: Record<string, any>;
  impact?: {
    scup?: number; // Expected SCUP change
    entropy?: number; // Expected entropy change
    mood?: string; // Expected mood change
  };
}

// Process instance with tick data
interface TickProcessInstance extends PythonProcess {
  id: string;
  script: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'queued';
  output: string[];
  
  tickTriggered?: boolean;
  tickStarted: number;
  tickCompleted?: number;
  scupBefore?: number;
  scupAfter?: number;
  entropyBefore?: number;
  entropyAfter?: number;
}

// Tick-aware process categories
const tickProcessCategories: Record<string, TickAwareProcess[]> = {
  "Consciousness Analysis": [
    {
      script: "consciousness_analyzer.py",
      description: "Analyzes consciousness patterns and coherence",
      category: "Consciousness Analysis",
      triggers: {
        onTick: 100, // Run every 100 ticks
        onSCUP: { operator: '>', value: 0.7 }
      },
      params: {
        depth: 5,
        resolution: "high",
        include_history: true
      },
      impact: {
        scup: 0.05,
        entropy: -0.02
      }
    },
    {
      script: "memory_defrag.py",
      description: "Defragments consciousness memory for optimal performance",
      category: "Consciousness Analysis",
      triggers: {
        onEntropy: { operator: '>', value: 0.8 },
        onSignal: "memory_fragmented"
      },
      params: {
        aggressive: false,
        preserve_recent: 1000
      },
      impact: {
        entropy: -0.15,
        scup: 0.1
      }
    }
  ],
  "System Optimization": [
    {
      script: "entropy_reducer.py",
      description: "Reduces system entropy through pattern consolidation",
      category: "System Optimization",
      triggers: {
        onEntropy: { operator: '>=', value: 0.6 }
      },
      params: {
        method: "consolidation",
        threshold: 0.1,
        iterations: 100
      },
      impact: {
        entropy: -0.3,
        scup: 0.05
      }
    },
    {
      script: "neural_optimizer.py",
      description: "Optimizes neural pathways for efficiency",
      category: "System Optimization",
      triggers: {
        onTick: 500,
        onSCUP: { operator: '<', value: 0.5 }
      },
      params: {
        optimization_level: 3,
        prune_threshold: 0.01
      },
      impact: {
        scup: 0.2,
        entropy: 0.05
      }
    }
  ],
  "Mood Management": [
    {
      script: "mood_stabilizer.py",
      description: "Stabilizes mood swings and emotional volatility",
      category: "Mood Management",
      triggers: {
        onMood: ["chaotic", "volatile", "unstable"],
        onEntropy: { operator: '>', value: 0.7 }
      },
      params: {
        target_mood: "balanced",
        smoothing_factor: 0.8,
        duration: 100
      },
      impact: {
        mood: "balanced",
        entropy: -0.1
      }
    }
  ],
  "Quantum Operations": [
    {
      script: "quantum_entangler.py",
      description: "Creates quantum entanglements between processes",
      category: "Quantum Operations",
      triggers: {
        onSignal: "quantum_ready",
        onSCUP: { operator: '>', value: 0.8 }
      },
      params: {
        qubits: 8,
        entanglement_strength: 0.9,
        coherence_time: 1000
      },
      impact: {
        scup: 0.15,
        entropy: 0.1
      }
    }
  ],
  "Signal Processing": [
    {
      script: "signal_injector.py",
      description: "Injects custom signals into the consciousness stream",
      category: "Signal Processing",
      triggers: {
        onTick: 50
      },
      params: {
        signal_type: "harmonic",
        frequency: 432,
        amplitude: 0.5
      },
      impact: {
        scup: 0.02,
        mood: "resonant"
      }
    }
  ]
};

// Category icons
const categoryIcons: Record<string, React.ReactNode> = {
  "Consciousness Analysis": <Brain className="w-4 h-4" />,
  "System Optimization": <Cpu className="w-4 h-4" />,
  "Mood Management": <Smile className="w-4 h-4" />,
  "Quantum Operations": <Zap className="w-4 h-4" />,
  "Signal Processing": <Activity className="w-4 h-4" />
};

interface PythonProcessManagerProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
  currentTick?: TickData;
}

const PythonProcessManager: React.FC<PythonProcessManagerProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0,
  currentTick
}) => {
  const { client, isConnected } = useDAWNApi();
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [processes, setProcesses] = useState<TickProcessInstance[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<TickAwareProcess | null>(null);
  const [paramValues, setParamValues] = useState<Record<string, any>>({});
  const [tickTriggers, setTickTriggers] = useState<Map<string, TickAwareProcess[]>>(new Map());
  const [autoExecute, setAutoExecute] = useState(true);
  const terminalRef = useRef<HTMLDivElement>(null);
  
  // Current tick state
  const tickState = currentTick || {
    tick_number: 0,
    scup: 0.5,
    entropy: 0.5,
    mood: "neutral",
    timestamp: Date.now(),
    signals: {}
  };
  
  // Subscribe to tick updates
  useEffect(() => {
    const handleTickUpdate = (tick: TickData) => {
      checkTickTriggers(tick);
    };
    
    const handlePythonOutput = ({ processId, chunk }: any) => {
      updateProcessOutput(processId, chunk.content);
      
      // Check for signal injections from Python
      checkForSignalInjection(processId, chunk.content);
    };
    
    const handlePythonStatus = ({ processId, status }: any) => {
      updateProcessStatus(processId, status);
    };
    
    client.on('tick:update', handleTickUpdate);
    client.on('python:output', handlePythonOutput);
    client.on('python:status', handlePythonStatus);
    
    return () => {
      client.off('tick:update', handleTickUpdate);
      client.off('python:output', handlePythonOutput);
      client.off('python:status', handlePythonStatus);
    };
  }, [client]);
  
  // Check tick triggers
  const checkTickTriggers = (tick: TickData) => {
    if (!autoExecute) return;
    
    Object.values(tickProcessCategories).forEach(category => {
      category.forEach(process => {
        if (shouldTriggerProcess(process, tick)) {
          executeTickTriggeredProcess(process, tick);
        }
      });
    });
  };
  
  // Check if process should be triggered
  const shouldTriggerProcess = (process: TickAwareProcess, tick: TickData): boolean => {
    const { triggers } = process;
    
    // Check tick number
    if (triggers.onTick && tick.tick_number % triggers.onTick === 0) {
      return true;
    }
    
    // Check SCUP condition
    if (triggers.onSCUP) {
      const { operator, value } = triggers.onSCUP;
      if (evaluateCondition(tick.scup, operator, value)) {
        return true;
      }
    }
    
    // Check entropy condition
    if (triggers.onEntropy) {
      const { operator, value } = triggers.onEntropy;
      if (evaluateCondition(tick.entropy, operator, value)) {
        return true;
      }
    }
    
    // Check mood condition
    if (triggers.onMood && triggers.onMood.includes(tick.mood)) {
      return true;
    }
    
    // Check signal condition
    if (triggers.onSignal && tick.signals[triggers.onSignal]) {
      return true;
    }
    
    return false;
  };
  
  // Evaluate numeric condition
  const evaluateCondition = (
    value: number, 
    operator: string, 
    threshold: number
  ): boolean => {
    switch (operator) {
      case '>': return value > threshold;
      case '<': return value < threshold;
      case '=': return Math.abs(value - threshold) < 0.01;
      case '>=': return value >= threshold;
      case '<=': return value <= threshold;
      default: return false;
    }
  };
  
  // Execute tick-triggered process
  const executeTickTriggeredProcess = async (
    process: TickAwareProcess, 
    tick: TickData
  ) => {
    // Check if already running
    const isRunning = processes.some(p => 
      p.script === process.script && p.status === 'running'
    );
    if (isRunning) return;
    
    try {
      const result = await client.executePythonScript({
        script: process.script,
        args: {
          ...process.params,
          tick_number: tick.tick_number,
          scup: tick.scup,
          entropy: tick.entropy,
          mood: tick.mood
        }
      });
      
      const newProcess: TickProcessInstance = {
        id: result.process_id,
        script: process.script,
        status: 'running',
        output: [`[Tick ${tick.tick_number}] Auto-triggered by: ${JSON.stringify(process.triggers)}`],
        started_at: Date.now(),
        tick_started: tick.tick_number,
        tickTriggered: true,
        scupBefore: tick.scup,
        entropyBefore: tick.entropy
      };
      
      setProcesses(prev => [...prev, newProcess]);
      
      // Emit tick event
      emitter.emit('tick:process-triggered', {
        process: process.script,
        tick: tick.tick_number,
        triggers: process.triggers
      });
      
    } catch (error) {
      console.error('[PythonProcessManager] Failed to execute tick-triggered process:', error);
    }
  };
  
  // Manual process start
  const startProcess = async (tickProcess: TickAwareProcess) => {
    try {
      const result = await client.executePythonScript({
        script: tickProcess.script,
        args: {
          ...paramValues,
          ...tickProcess.params,
          tick_number: tickState.tick_number,
          scup: tickState.scup,
          entropy: tickState.entropy,
          mood: tickState.mood
        }
      });
      
      const newProcess: TickProcessInstance = {
        id: result.process_id,
        script: tickProcess.script,
        status: 'running',
        output: [`[Tick ${tickState.tick_number}] Manually started`],
        started_at: Date.now(),
        tick_started: tickState.tick_number,
        tickTriggered: false,
        scupBefore: tickState.scup,
        entropyBefore: tickState.entropy
      };
      
      setProcesses(prev => [...prev, newProcess]);
      
      // Emit process start event
      emitter.emit('module:process-start', {
        moduleId: 'python-process-manager',
        processId: result.process_id,
        process: tickProcess
      });
      
    } catch (error) {
      console.error('[PythonProcessManager] Failed to start process:', error);
    }
  };
  
  // Update process output
  const updateProcessOutput = (processId: string, output: string) => {
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { ...p, output: [...p.output, output] }
        : p
    ));
  };
  
  // Update process status
  const updateProcessStatus = (processId: string, status: string) => {
    setProcesses(prev => prev.map(p => {
      if (p.id === processId) {
        const updated = { ...p, status: status as any };
        
        if (status === 'completed' || status === 'error') {
          updated.tickCompleted = tickState.tick_number;
          updated.scupAfter = tickState.scup;
          updated.entropyAfter = tickState.entropy;
          
          // Calculate impact
          const tickDuration = updated.tickCompleted - updated.tick_started;
          const scupChange = updated.scupAfter! - updated.scupBefore!;
          const entropyChange = updated.entropyAfter! - updated.entropyBefore!;
          
          updated.output.push(
            `[Tick ${updated.tickCompleted}] Process completed`,
            `Duration: ${tickDuration} ticks`,
            `SCUP impact: ${scupChange > 0 ? '+' : ''}${scupChange.toFixed(3)}`,
            `Entropy impact: ${entropyChange > 0 ? '+' : ''}${entropyChange.toFixed(3)}`
          );
          
          // Emit impact event
          emitter.emit('tick:process-impact', {
            processId,
            tickDuration,
            scupChange,
            entropyChange
          });
        }
        
        return updated;
      }
      return p;
    }));
  };
  
  // Check for signal injection from Python output
  const checkForSignalInjection = (processId: string, output: string) => {
    // Look for signal injection pattern
    const signalMatch = output.match(/SIGNAL_INJECT:\s*(\w+)(?:\s*=\s*(.+))?/);
    if (signalMatch) {
      const [, signal, value] = signalMatch;
      
      // Emit signal to tick loop
      emitter.emit('tick:signal-injection', {
        processId,
        signal,
        value: value || true,
        tick: tickState.tick_number
      });
    }
    
    // Look for consciousness state updates
    const consciousnessMatch = output.match(/CONSCIOUSNESS_UPDATE:\s*(.+)/);
    if (consciousnessMatch) {
      try {
        const update = JSON.parse(consciousnessMatch[1]);
        emitter.emit('tick:consciousness-update', update);
      } catch (error) {
        console.error('[PythonProcessManager] Failed to parse consciousness update:', error);
      }
    }
  };
  
  // Kill a process
  const killProcess = async (processId: string) => {
    try {
      await client.killProcess(processId);
      updateProcessStatus(processId, 'error');
    } catch (error) {
      console.error('[PythonProcessManager] Failed to kill process:', error);
    }
  };
  
  // Get trigger description
  const getTriggerDescription = (triggers: TickAwareProcess['triggers']): string => {
    const parts: string[] = [];
    
    if (triggers.onTick) {
      parts.push(`Every ${triggers.onTick} ticks`);
    }
    if (triggers.onSCUP) {
      parts.push(`SCUP ${triggers.onSCUP.operator} ${triggers.onSCUP.value}`);
    }
    if (triggers.onEntropy) {
      parts.push(`Entropy ${triggers.onEntropy.operator} ${triggers.onEntropy.value}`);
    }
    if (triggers.onMood) {
      parts.push(`Mood: ${triggers.onMood.join(', ')}`);
    }
    if (triggers.onSignal) {
      parts.push(`Signal: ${triggers.onSignal}`);
    }
    
    return parts.join(' | ');
  };
  
  // Get impact description
  const getImpactDescription = (impact?: TickAwareProcess['impact']): string => {
    if (!impact) return '';
    
    const parts: string[] = [];
    
    if (impact.scup !== undefined) {
      parts.push(`SCUP ${impact.scup > 0 ? '+' : ''}${impact.scup}`);
    }
    if (impact.entropy !== undefined) {
      parts.push(`Entropy ${impact.entropy > 0 ? '+' : ''}${impact.entropy}`);
    }
    if (impact.mood) {
      parts.push(`Mood → ${impact.mood}`);
    }
    
    return parts.join(' | ');
  };
  
  // Toggle category expansion
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
  
  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-green-400';
      case 'completed': return 'text-blue-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };
  
  // Get status icon
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Loader2 className="w-4 h-4 animate-spin" />;
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'error': return <AlertCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };
  
  return (
    <div className="w-full h-full flex flex-col p-4 space-y-4">
      {/* Header with Tick Info */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-purple-400" />
          <h3 className="text-white font-semibold">Tick-Aware Process Manager</h3>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
        </div>
        <div className="flex items-center gap-4 text-xs text-white/50">
          <div className="flex items-center gap-1">
            <Hash className="w-3 h-3" />
            <span>Tick: {tickState.tick_number}</span>
          </div>
          <div className="flex items-center gap-1">
            <TrendingUp className="w-3 h-3" />
            <span>SCUP: {tickState.scup.toFixed(2)}</span>
          </div>
          <div className="flex items-center gap-1">
            <Activity className="w-3 h-3" />
            <span>Entropy: {tickState.entropy.toFixed(2)}</span>
          </div>
          <div className="flex items-center gap-1">
            <Smile className="w-3 h-3" />
            <span>{tickState.mood}</span>
          </div>
        </div>
      </div>
      
      {/* Auto-execute Toggle */}
      <div className="flex items-center justify-between glass-panel glass-depth-1 p-3 rounded-lg">
        <span className="text-sm text-white/70">Auto-execute on triggers</span>
        <motion.button
          onClick={() => setAutoExecute(!autoExecute)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className={`px-3 py-1 rounded-full text-xs transition-all ${
            autoExecute 
              ? 'bg-green-500/20 text-green-400 border border-green-400/50' 
              : 'bg-red-500/20 text-red-400 border border-red-400/50'
          }`}
        >
          {autoExecute ? 'Enabled' : 'Disabled'}
        </motion.button>
      </div>
      
      {/* Process Categories */}
      <div className="flex-1 overflow-y-auto space-y-2">
        {Object.entries(tickProcessCategories).map(([category, categoryProcesses]) => (
          <motion.div
            key={category}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-panel glass-depth-1 rounded-lg overflow-hidden"
          >
            {/* Category Header */}
            <button
              onClick={() => toggleCategory(category)}
              className="w-full p-3 flex items-center justify-between hover:bg-white/5 transition-colors"
            >
              <div className="flex items-center gap-2">
                {categoryIcons[category]}
                <span className="text-white font-medium">{category}</span>
                <span className="text-xs text-white/50">({categoryProcesses.length})</span>
              </div>
              <motion.div
                animate={{ rotate: expandedCategories.has(category) ? 90 : 0 }}
                transition={{ duration: 0.2 }}
              >
                <ChevronRight className="w-4 h-4 text-white/50" />
              </motion.div>
            </button>
            
            {/* Category Processes */}
            <AnimatePresence>
              {expandedCategories.has(category) && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t border-white/10"
                >
                  {categoryProcesses.map((process, index) => (
                    <motion.div
                      key={process.script}
                      initial={{ x: -20, opacity: 0 }}
                      animate={{ x: 0, opacity: 1 }}
                      transition={{ delay: index * 0.05 }}
                      className="p-3 border-b border-white/5 hover:bg-white/5 transition-colors"
                    >
                      <div className="space-y-2">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="text-white text-sm font-medium">{process.script}</span>
                              {processes.some(p => p.script === process.script && p.status === 'running') && (
                                <Loader2 className="w-3 h-3 text-green-400 animate-spin" />
                              )}
                              {process.triggers.onTick && (
                                <Hash className="w-3 h-3 text-blue-400" title="Tick triggered" />
                              )}
                            </div>
                            <p className="text-xs text-white/60 mt-1">{process.description}</p>
                          </div>
                          
                          {/* Action Button */}
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            onClick={() => startProcess(process)}
                            className="p-1.5 rounded bg-green-500/20 hover:bg-green-500/30 transition-colors"
                          >
                            <Play className="w-4 h-4 text-green-400" />
                          </motion.button>
                        </div>
                        
                        {/* Triggers */}
                        <div className="flex items-center gap-2 text-xs">
                          <span className="text-white/40">Triggers:</span>
                          <span className="text-purple-400">{getTriggerDescription(process.triggers)}</span>
                        </div>
                        
                        {/* Expected Impact */}
                        {process.impact && (
                          <div className="flex items-center gap-2 text-xs">
                            <span className="text-white/40">Impact:</span>
                            <span className="text-cyan-400">{getImpactDescription(process.impact)}</span>
                          </div>
                        )}
                        
                        {/* Parameters */}
                        {selectedProcess?.script === process.script && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            className="mt-2 p-2 bg-black/20 rounded space-y-2"
                          >
                            {Object.entries(process.params).map(([param, defaultValue]) => (
                              <div key={param} className="flex items-center gap-2">
                                <label className="text-xs text-white/50 min-w-[100px]">{param}:</label>
                                <input
                                  type="text"
                                  value={paramValues[param] || defaultValue || ''}
                                  onChange={(e) => setParamValues(prev => ({
                                    ...prev,
                                    [param]: e.target.value
                                  }))}
                                  className="flex-1 px-2 py-1 bg-white/5 border border-white/10 rounded text-xs text-white"
                                  placeholder={`Default: ${defaultValue}`}
                                />
                              </div>
                            ))}
                          </motion.div>
                        )}
                        
                        <button
                          onClick={() => setSelectedProcess(
                            selectedProcess?.script === process.script ? null : process
                          )}
                          className="text-xs text-purple-400 hover:text-purple-300"
                        >
                          {selectedProcess?.script === process.script ? 'Hide' : 'Show'} parameters
                        </button>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        ))}
      </div>
      
      {/* Process Output Terminal */}
      <div className="h-48 glass-panel glass-depth-2 rounded-lg p-3">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Terminal className="w-4 h-4 text-white/50" />
            <span className="text-sm text-white/70">Process Output</span>
          </div>
          <div className="flex items-center gap-2">
            {processes.filter(p => p.status === 'running').map(p => (
              <motion.button
                key={p.id}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => killProcess(p.id)}
                className="p-1 rounded bg-red-500/20 hover:bg-red-500/30 transition-colors"
                title={`Kill ${p.script}`}
              >
                <Square className="w-3 h-3 text-red-400" />
              </motion.button>
            ))}
          </div>
        </div>
        
        <div
          ref={terminalRef}
          className="h-32 overflow-y-auto bg-black/50 rounded p-2 font-mono text-xs"
        >
          {processes.length === 0 ? (
            <div className="text-white/30">No processes running...</div>
          ) : (
            processes.flatMap((process, pIndex) => [
              <div key={`header-${pIndex}`} className="text-white/70 mb-1">
                === {process.script} [{process.id}] {process.tickTriggered && '⚡'} ===
              </div>,
              ...process.output.map((line, lIndex) => (
                <div
                  key={`${process.id}-${lIndex}`}
                  className={`${
                    line.includes('Error') ? 'text-red-400' :
                    line.includes('complete') ? 'text-green-400' :
                    line.includes('Tick') ? 'text-blue-400' :
                    line.includes('SCUP') || line.includes('Entropy') ? 'text-yellow-400' :
                    line.includes('SIGNAL_INJECT') ? 'text-purple-400' :
                    'text-white/60'
                  }`}
                >
                  {line}
                </div>
              ))
            ])
          )}
        </div>
      </div>
      
      {/* Active Processes with Tick Info */}
      <div className="flex gap-2 overflow-x-auto">
        {processes.filter(p => p.status === 'running').map(process => (
          <motion.div
            key={process.id}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="flex items-center gap-2 px-3 py-1 bg-white/5 rounded-full whitespace-nowrap"
          >
            <div className={getStatusColor(process.status)}>
              {getStatusIcon(process.status)}
            </div>
            <span className="text-xs text-white/70">{process.script}</span>
            <span className="text-xs text-white/40">
              T{process.tick_started}
            </span>
            {process.tickTriggered && (
              <Zap className="w-3 h-3 text-yellow-400" title="Tick triggered" />
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default PythonProcessManager;