import React, { useState, useEffect, useRef, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Terminal, Play, Square, CheckCircle, AlertCircle, Clock, Loader2,
  Hash, TrendingUp, Activity, Smile, ChevronRight, Zap, Cpu, Brain
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';
import { useDAWNApi } from '@/services/DAWNApiClient';
import type { TickData, PythonProcess } from '@/services/DAWNApiClient';

/**
 * Python Process Manager - Scientific Computing Control Center
 * 
 * A comprehensive visual interface for managing and monitoring Python executable processes
 * organized by scientific computing domains. Features real-time terminal output, 
 * parameter management, and process lifecycle tracking.
 * 
 * @example
 * ```tsx
 * // Basic usage
 * <PythonProcessManager 
 *   globalEntropy={0.5}
 *   emitter={eventEmitter}
 * />
 * 
 * // In a glass container
 * <div className="glass-base h-full rounded-xl overflow-hidden">
 *   <PythonProcessManager globalEntropy={systemConsciousness} />
 * </div>
 * ```
 * 
 * ## Features:
 * - 🧬 **5 Scientific Categories**: Genomic Processing, Neural Networks, Quantum Simulations, Data Analysis, System Diagnostics
 * - 🎮 **Interactive Controls**: Play, stop, parameter input, real-time monitoring
 * - 📺 **Live Terminal**: Real-time output with syntax highlighting and auto-scroll
 * - 📊 **Process Tracking**: Status indicators, progress bars, execution history
 * - ✨ **Visual Effects**: Particle systems, glass morphism, breathing animations
 * - 🔗 **Event Integration**: Emits process lifecycle events for system-wide awareness
 * 
 * ## Process Categories:
 * - **Genomic Processing**: DNA/RNA analysis, protein synthesis, RNA folding
 * - **Neural Networks**: Consciousness mapping, neural evolution, dream generation
 * - **Quantum Simulations**: Quantum entanglement, superposition visualization
 * - **Data Analysis**: Pattern recognition, chaos analysis, statistical functions
 * - **System Diagnostics**: Health monitoring, memory analysis, performance tracking
 * 
 * ## Production Integration:
 * To connect to real Python processes:
 * 1. Replace WebSocket simulation with actual WebSocket connection
 * 2. Connect to Python backend that executes scripts
 * 3. Stream real output from Python processes
 * 4. Handle file exports and result visualization
 * 
 * @param props.emitter - EventEmitter for system-wide event communication
 * @param props.globalEntropy - System entropy level (0-1) affecting visual intensity
 */

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

// Extended process instance with tick data
interface TickProcessInstance {
  process_id: string;
  id: string;
  script: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'queued';
  output: string[];
  exit_code?: number;
  started_at?: number;
  completed_at?: number;
  tick_started?: number;
  tick_completed?: number;
  tickTriggered?: boolean;
  tickStarted: number;
  tickCompleted?: number;
  scupBefore?: number;
  scupAfter?: number;
  entropyBefore?: number;
  entropyAfter?: number;
}

// Tick-aware Python scripts
const tickProcesses: TickAwareProcess[] = [
  {
    script: "consciousness_analyzer.py",
    description: "Analyzes consciousness patterns and correlations",
    category: "Consciousness Analysis",
    triggers: { onTick: 100 },
    params: { analysis_depth: 5, pattern_threshold: 0.7 },
    impact: { scup: 0.05, entropy: -0.02 }
  },
  {
    script: "entropy_reducer.py", 
    description: "Reduces system entropy through memory consolidation",
    category: "System Optimization",
    triggers: { onEntropy: { operator: '>', value: 0.6 } },
    params: { consolidation_rate: 0.3, preserve_recent: true },
    impact: { entropy: -0.15, scup: 0.03 }
  },
  {
    script: "mood_stabilizer.py",
    description: "Stabilizes mood during chaotic states",
    category: "Mood Management", 
    triggers: { onMood: ['chaotic', 'unstable'] },
    params: { stabilization_strength: 0.8, transition_speed: 0.5 },
    impact: { mood: 'calm', scup: 0.08 }
  },
  {
    script: "memory_defrag.py",
    description: "Defragments and optimizes memory structures",
    category: "System Optimization",
    triggers: { 
      onEntropy: { operator: '>', value: 0.7 },
      onSignal: 'memory_fragmentation'
    },
    params: { defrag_method: 'smart', preserve_associations: true },
    impact: { entropy: -0.2, scup: 0.1 }
  },
  {
    script: "neural_optimizer.py",
    description: "Optimizes neural pathways for efficiency",
    category: "Consciousness Analysis",
    triggers: { onSCUP: { operator: '<', value: 0.3 } },
    params: { optimization_level: 3, learning_rate: 0.01 },
    impact: { scup: 0.15, entropy: -0.05 }
  },
  {
    script: "quantum_entangler.py",
    description: "Creates quantum entanglements for coherence",
    category: "Quantum Operations",
    triggers: { onSCUP: { operator: '>', value: 0.8 } },
    params: { entanglement_strength: 0.9, coherence_target: 0.95 },
    impact: { scup: 0.1, entropy: 0.05 }
  },
  {
    script: "signal_injector.py",
    description: "Injects harmonic signals for synchronization",
    category: "Signal Processing",
    triggers: { onTick: 50 },
    params: { signal_type: 'harmonic', frequency: 432, amplitude: 0.6 },
    impact: { scup: 0.02, entropy: -0.01 }
  }
];

// Group processes by category
const tickProcessCategories = useMemo(() => {
  return tickProcesses.reduce((acc, process) => {
    if (!acc[process.category]) {
      acc[process.category] = [];
    }
    acc[process.category].push(process);
    return acc;
  }, {} as Record<string, TickAwareProcess[]>);
}, []);

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
  globalEntropy = 0.5,
  currentTick
}) => {
  const { isConnected, currentTick: apiTick, executeProcess, killProcess: apiKillProcess, apiClient } = useDAWNApi();
  
  // Use API tick or fallback to prop
  const tickState = apiTick || currentTick || {
    tick_number: 0,
    scup: 0.5,
    entropy: 0.5,
    mood: 'calm' as const,
    timestamp: Date.now(),
    neural_activity: 0.5,
    coherence_level: 0.5,
    memory_fragments: 0
  };

  // State management
  const [processes, setProcesses] = useState<TickProcessInstance[]>([]);
  const [autoExecute, setAutoExecute] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState(new Set(['Consciousness Analysis']));
  const [selectedProcess, setSelectedProcess] = useState<TickAwareProcess | null>(null);
  const [paramValues, setParamValues] = useState<Record<string, any>>({});
  
  const terminalRef = useRef<HTMLDivElement>(null);

  // Event handlers
  useEffect(() => {
    const handleTickUpdate = (tick: TickData) => {
      if (autoExecute) {
        checkTickTriggers(tick);
      }
    };

    const handlePythonOutput = ({ processId, chunk }: any) => {
      updateProcessOutput(processId, chunk);
      checkForSignalInjection(processId, chunk);
    };

    const handlePythonStatus = ({ processId, status }: any) => {
      updateProcessStatus(processId, status);
    };

    // Set up event listeners
    emitter.on('tick_update', handleTickUpdate);
    emitter.on('python_output', handlePythonOutput);
    emitter.on('python_status', handlePythonStatus);

    if (apiClient) {
      apiClient.on('tick_update', handleTickUpdate);
      apiClient.on('python_output', handlePythonOutput);
      apiClient.on('python_status', handlePythonStatus);
    }

    return () => {
      emitter.off('tick_update', handleTickUpdate);
      emitter.off('python_output', handlePythonOutput);
      emitter.off('python_status', handlePythonStatus);
      
      if (apiClient) {
        apiClient.off('tick_update', handleTickUpdate);
        apiClient.off('python_output', handlePythonOutput);
        apiClient.off('python_status', handlePythonStatus);
      }
    };
  }, [emitter, apiClient, autoExecute]);

  const checkTickTriggers = (tick: TickData) => {
    tickProcesses.forEach(process => {
      if (shouldTriggerProcess(process, tick)) {
        executeTickTriggeredProcess(process, tick);
      }
    });
  };

  const shouldTriggerProcess = (process: TickAwareProcess, tick: TickData): boolean => {
    const { triggers } = process;
    
    // Check tick trigger
    if (triggers.onTick && tick.tick_number % triggers.onTick === 0) {
      return true;
    }
    
    // Check SCUP trigger  
    if (triggers.onSCUP) {
      const condition = triggers.onSCUP;
      if (evaluateCondition(tick.scup, condition.operator, condition.value)) {
        return true;
      }
    }
    
    // Check entropy trigger
    if (triggers.onEntropy) {
      const condition = triggers.onEntropy;
      if (evaluateCondition(tick.entropy, condition.operator, condition.value)) {
        return true;
      }
    }
    
    // Check mood trigger
    if (triggers.onMood && triggers.onMood.includes(tick.mood)) {
      return true;
    }
    
    return false;
  };

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
      // Execute with tick context
      const result = await executeProcess({
        script: process.script,
        params: {
          ...process.params,
          tick_number: tick.tick_number,
          scup: tick.scup,
          entropy: tick.entropy,
          mood: tick.mood,
          trigger_type: 'automatic'
        }
      });
      
      const newProcess: TickProcessInstance = {
        process_id: result.process_id,
        id: result.process_id,
        script: process.script,
        status: 'running',
        output: [`[Tick ${tick.tick_number}] Auto-triggered by: ${JSON.stringify(process.triggers)}`],
        tickTriggered: true,
        tickStarted: tick.tick_number,
        scupBefore: tick.scup,
        entropyBefore: tick.entropy
      };
      
      setProcesses(prev => [...prev, newProcess]);
      
    } catch (error) {
      console.error(`Failed to execute ${process.script}:`, error);
    }
  };

  const startProcess = async (tickProcess: TickAwareProcess) => {
    try {
      const processParams = {
        ...tickProcess.params,
        ...paramValues,
        tick_number: tickState.tick_number,
        scup: tickState.scup,
        entropy: tickState.entropy,
        mood: tickState.mood,
        trigger_type: 'manual'
      };
      
      const result = await executeProcess({
        script: tickProcess.script,
        params: processParams
      });
      
      const newProcess: TickProcessInstance = {
        process_id: result.process_id,
        id: result.process_id,
        script: tickProcess.script,
        status: 'running',
        output: [`[Tick ${tickState.tick_number}] Manually started`],
        tickTriggered: false,
        tickStarted: tickState.tick_number,
        scupBefore: tickState.scup,
        entropyBefore: tickState.entropy
      };
      
      setProcesses(prev => [...prev, newProcess]);
      
    } catch (error) {
      console.error(`Failed to start ${tickProcess.script}:`, error);
    }
  };

  const updateProcessOutput = (processId: string, output: string) => {
    setProcesses(prev => prev.map(p => 
      p.id === processId 
        ? { ...p, output: [...p.output, output] }
        : p
    ));
  };

  const updateProcessStatus = (processId: string, status: string) => {
    setProcesses(prev => prev.map(p => {
      if (p.id === processId) {
        const updated = { ...p, status: status as any };
        
        if (status === 'completed' || status === 'error') {
          // Mark completion tick
          updated.tickCompleted = tickState.tick_number;
          updated.scupAfter = tickState.scup;
          updated.entropyAfter = tickState.entropy;
          
          // Calculate impact
          const tickDuration = (updated.tickCompleted || tickState.tick_number) - updated.tickStarted;
          const scupChange = (updated.scupAfter || 0) - (updated.scupBefore || 0);
          const entropyChange = (updated.entropyAfter || 0) - (updated.entropyBefore || 0);
          
          updated.output.push(
            `[Tick ${updated.tickCompleted || tickState.tick_number}] Process completed`,
            `Duration: ${tickDuration} ticks`,
            `SCUP impact: ${scupChange > 0 ? '+' : ''}${scupChange.toFixed(3)}`,
            `Entropy impact: ${entropyChange > 0 ? '+' : ''}${entropyChange.toFixed(3)}`
          );
          
          // Emit impact metrics
          emitter.emit('process_impact', {
            script: updated.script,
            duration: tickDuration,
            scupChange,
            entropyChange
          });
        }
        
        return updated;
      }
      return p;
    }));
  };

  // Scroll terminal to bottom when new output arrives
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [processes]);

  const checkForSignalInjection = (processId: string, output: string) => {
    // Parse signals from Python output
    if (output.includes('SIGNAL_INJECT:')) {
      const signal = output.split('SIGNAL_INJECT:')[1]?.trim();
      if (signal) {
        emitter.emit('signal_injection', { signal, processId });
        
        // Trigger processes listening for this signal
        tickProcesses.forEach(process => {
          if (process.triggers.onSignal === signal && autoExecute) {
            executeTickTriggeredProcess(process, tickState);
          }
        });
      }
    }
    
    // Parse consciousness updates
    if (output.includes('CONSCIOUSNESS_UPDATE:')) {
      try {
        const updateStr = output.split('CONSCIOUSNESS_UPDATE:')[1]?.trim();
        const update = JSON.parse(updateStr);
        emitter.emit('consciousness_update', update);
      } catch (error) {
        console.error('Failed to parse consciousness update:', error);
      }
    }
  };

  const killProcess = async (processId: string) => {
    try {
      await apiKillProcess(processId);
      setProcesses(prev => prev.filter(p => p.id !== processId));
    } catch (error) {
      console.error(`Failed to kill process ${processId}:`, error);
    }
  };

  const getTriggerDescription = (triggers: TickAwareProcess['triggers']): string => {
    const descriptions = [];
    
    if (triggers.onTick) {
      descriptions.push(`Every ${triggers.onTick} ticks`);
    }
    if (triggers.onSCUP) {
      descriptions.push(`SCUP ${triggers.onSCUP.operator} ${triggers.onSCUP.value}`);
    }
    if (triggers.onEntropy) {
      descriptions.push(`Entropy ${triggers.onEntropy.operator} ${triggers.onEntropy.value}`);
    }
    if (triggers.onMood) {
      descriptions.push(`Mood: ${triggers.onMood.join(', ')}`);
    }
    if (triggers.onSignal) {
      descriptions.push(`Signal: ${triggers.onSignal}`);
    }
    
    return descriptions.join(' | ') || 'No triggers';
  };

  const getImpactDescription = (impact?: TickAwareProcess['impact']): string => {
    if (!impact) return 'No expected impact';
    
    const impacts = [];
    if (impact.scup) impacts.push(`SCUP: ${impact.scup > 0 ? '+' : ''}${impact.scup}`);
    if (impact.entropy) impacts.push(`Entropy: ${impact.entropy > 0 ? '+' : ''}${impact.entropy}`);
    if (impact.mood) impacts.push(`Mood: ${impact.mood}`);
    
    return impacts.join(', ') || 'No expected impact';
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

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-green-400';
      case 'completed': return 'text-blue-400';
      case 'error': return 'text-red-400';
      default: return 'text-white/50';
    }
  };

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
              T{process.tickStarted}
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