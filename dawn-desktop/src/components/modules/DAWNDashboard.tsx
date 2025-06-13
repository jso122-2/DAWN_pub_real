import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity,
  Brain,
  Terminal,
  AlertTriangle,
  Download,
  Upload,
  Pause,
  Play,
  RotateCcw,
  Zap,
  Shield,
  Settings,
  Gauge,
  Wifi,
  Database,
  Clock,
  Volume2,
  VolumeX
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';

// Import our modules (these would be actual imports in production)
// import TickLoopMonitor from './TickLoopMonitor';
// import ConsciousnessVisualizer from './ConsciousnessVisualizer';
// import PythonProcessManager from './PythonProcessManager';

// System state interface
interface SystemState {
  tickPaused: boolean;
  fps: number;
  wsLatency: number;
  processQueueDepth: number;
  memoryUsage: number;
  tickLag: number;
  soundEnabled: boolean;
}

// Log entry interface
interface LogEntry {
  id: string;
  timestamp: Date;
  level: 'info' | 'warning' | 'error' | 'success';
  module: string;
  message: string;
}

// Connection line data
interface DataStream {
  from: { x: number; y: number };
  to: { x: number; y: number };
  active: boolean;
  particles: number;
}

interface DAWNDashboardProps {
  emitter?: EventEmitter;
}

const DAWNDashboard: React.FC<DAWNDashboardProps> = ({ 
  emitter = new EventEmitter() 
}) => {
  const [systemState, setSystemState] = useState<SystemState>({
    tickPaused: false,
    fps: 60,
    wsLatency: 0,
    processQueueDepth: 0,
    memoryUsage: 0,
    tickLag: 0,
    soundEnabled: false
  });
  
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [activeProcesses, setActiveProcesses] = useState<any[]>([]);
  const [dataStreams, setDataStreams] = useState<DataStream[]>([]);
  const [systemMood, setSystemMood] = useState<'calm' | 'active' | 'excited' | 'critical'>('calm');
  const [emergencyMode, setEmergencyMode] = useState(false);
  
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fpsRef = useRef<number[]>([]);
  const lastFrameTime = useRef(performance.now());
  
  // Module refs for positioning
  const tickMonitorRef = useRef<HTMLDivElement>(null);
  const consciousnessRef = useRef<HTMLDivElement>(null);
  const pythonManagerRef = useRef<HTMLDivElement>(null);
  
  // Initialize data streams between modules
  useEffect(() => {
    const streams: DataStream[] = [
      {
        from: { x: 300, y: 300 }, // Tick monitor
        to: { x: 600, y: 200 }, // Consciousness
        active: true,
        particles: 5
      },
      {
        from: { x: 100, y: 300 }, // Python manager
        to: { x: 300, y: 300 }, // Tick monitor
        active: true,
        particles: 3
      },
      {
        from: { x: 600, y: 200 }, // Consciousness
        to: { x: 100, y: 300 }, // Python manager
        active: true,
        particles: 4
      }
    ];
    
    setDataStreams(streams);
  }, []);
  
  // FPS monitoring
  useEffect(() => {
    const updateFPS = () => {
      const now = performance.now();
      const delta = now - lastFrameTime.current;
      lastFrameTime.current = now;
      
      const fps = 1000 / delta;
      fpsRef.current.push(fps);
      if (fpsRef.current.length > 60) fpsRef.current.shift();
      
      const avgFPS = fpsRef.current.reduce((a, b) => a + b, 0) / fpsRef.current.length;
      setSystemState(prev => ({ ...prev, fps: Math.round(avgFPS) }));
      
      requestAnimationFrame(updateFPS);
    };
    
    const animationId = requestAnimationFrame(updateFPS);
    return () => cancelAnimationFrame(animationId);
  }, []);
  
  // Listen to system events
  useEffect(() => {
    // Tick events
    const handleTick = (data: any) => {
      addLog('info', 'TickLoop', `Tick #${data.tick_number} - SCUP: ${data.scup}%`);
      
      // Update system mood based on metrics
      if (data.entropy > 0.8) {
        setSystemMood('critical');
      } else if (data.scup > 70) {
        setSystemMood('excited');
      } else if (data.scup > 40) {
        setSystemMood('active');
      } else {
        setSystemMood('calm');
      }
    };
    
    // Process events
    const handleProcessOutput = (data: any) => {
      addLog('info', 'Process', data.output);
      setActiveProcesses(prev => [...prev.slice(-10), data]);
    };
    
    // Consciousness events
    const handleConsciousnessUpdate = (data: any) => {
      if (data.scup < 20) {
        addLog('warning', 'Consciousness', 'Low consciousness detected!');
      }
    };
    
    // Performance events
    const handlePerformanceUpdate = (data: any) => {
      setSystemState(prev => ({
        ...prev,
        wsLatency: data.latency || prev.wsLatency,
        memoryUsage: data.memoryUsage || prev.memoryUsage,
        tickLag: data.tickLag || prev.tickLag
      }));
    };
    
    emitter.on('tick:complete', handleTick);
    emitter.on('process:output', handleProcessOutput);
    emitter.on('consciousness:update', handleConsciousnessUpdate);
    emitter.on('performance:update', handlePerformanceUpdate);
    
    return () => {
      emitter.off('tick:complete', handleTick);
      emitter.off('process:output', handleProcessOutput);
      emitter.off('consciousness:update', handleConsciousnessUpdate);
      emitter.off('performance:update', handlePerformanceUpdate);
    };
  }, [emitter]);
  
  // Draw data streams
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const particles: any[] = [];
    
    // Initialize particles for each stream
    dataStreams.forEach((stream, streamIndex) => {
      for (let i = 0; i < stream.particles; i++) {
        particles.push({
          streamIndex,
          progress: i / stream.particles,
          speed: 0.005 + Math.random() * 0.005
        });
      }
    });
    
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw connection lines
      dataStreams.forEach((stream, index) => {
        if (!stream.active) return;
        
        ctx.beginPath();
        ctx.moveTo(stream.from.x, stream.from.y);
        ctx.lineTo(stream.to.x, stream.to.y);
        
        const gradient = ctx.createLinearGradient(
          stream.from.x, stream.from.y,
          stream.to.x, stream.to.y
        );
        
        const color = systemMood === 'critical' ? '#ef4444' :
                     systemMood === 'excited' ? '#f59e0b' :
                     systemMood === 'active' ? '#a855f7' : '#22d3ee';
        
        gradient.addColorStop(0, color + '40');
        gradient.addColorStop(0.5, color + '80');
        gradient.addColorStop(1, color + '40');
        
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 2;
        ctx.stroke();
      });
      
      // Draw particles
      particles.forEach(particle => {
        const stream = dataStreams[particle.streamIndex];
        if (!stream.active) return;
        
        particle.progress += particle.speed;
        if (particle.progress > 1) particle.progress = 0;
        
        const x = stream.from.x + (stream.to.x - stream.from.x) * particle.progress;
        const y = stream.from.y + (stream.to.y - stream.from.y) * particle.progress;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        
        const color = systemMood === 'critical' ? '#ef4444' :
                     systemMood === 'excited' ? '#f59e0b' :
                     systemMood === 'active' ? '#a855f7' : '#22d3ee';
        
        ctx.fillStyle = color;
        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
        ctx.fill();
      });
      
      requestAnimationFrame(draw);
    };
    
    draw();
  }, [dataStreams, systemMood]);
  
  // Add log entry
  const addLog = (level: LogEntry['level'], module: string, message: string) => {
    const entry: LogEntry = {
      id: Date.now().toString(),
      timestamp: new Date(),
      level,
      module,
      message
    };
    
    setLogs(prev => [...prev.slice(-100), entry]);
  };
  
  // Master control functions
  const toggleTickLoop = () => {
    setSystemState(prev => ({ ...prev, tickPaused: !prev.tickPaused }));
    emitter.emit('tick:toggle', { paused: !systemState.tickPaused });
    addLog('info', 'System', `Tick loop ${systemState.tickPaused ? 'resumed' : 'paused'}`);
  };
  
  const resetConsciousness = () => {
    emitter.emit('consciousness:reset');
    addLog('warning', 'System', 'Consciousness reset initiated');
  };
  
  const emergencyStop = () => {
    setEmergencyMode(true);
    emitter.emit('emergency:stop');
    addLog('error', 'System', 'EMERGENCY STOP ACTIVATED');
    
    // Auto-recover after 3 seconds
    setTimeout(() => {
      setEmergencyMode(false);
      addLog('success', 'System', 'Emergency mode cleared');
    }, 3000);
  };
  
  const exportState = () => {
    const state = {
      timestamp: new Date().toISOString(),
      systemState,
      logs: logs.slice(-50),
      activeProcesses
    };
    
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn-state-${Date.now()}.json`;
    a.click();
    
    addLog('success', 'System', 'State exported successfully');
  };
  
  // Get log color
  const getLogColor = (level: LogEntry['level']) => {
    switch (level) {
      case 'info': return 'text-blue-400';
      case 'warning': return 'text-yellow-400';
      case 'error': return 'text-red-400';
      case 'success': return 'text-green-400';
    }
  };
  
  return (
    <div className="w-full h-full bg-black relative overflow-hidden">
      {/* Background particle system */}
      <div className="absolute inset-0 opacity-30">
        {[...Array(30)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white rounded-full"
            initial={{ 
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight
            }}
            animate={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight
            }}
            transition={{
              duration: 20 + Math.random() * 10,
              repeat: Infinity,
              ease: 'linear'
            }}
          />
        ))}
      </div>
      
      {/* Data stream canvas */}
      <canvas
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight}
        className="absolute inset-0 pointer-events-none"
        style={{ opacity: 0.6 }}
      />
      
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 h-16 glass-panel glass-depth-2 flex items-center justify-between px-6 z-50">
        <div className="flex items-center gap-4">
          <Brain className="w-8 h-8 text-purple-400" />
          <h1 className="text-2xl font-bold text-white">DAWN Command Center</h1>
          <div className={`px-3 py-1 rounded-full text-xs ${
            emergencyMode ? 'bg-red-500/30 text-red-400' :
            systemMood === 'critical' ? 'bg-red-500/20 text-red-400' :
            systemMood === 'excited' ? 'bg-orange-500/20 text-orange-400' :
            systemMood === 'active' ? 'bg-purple-500/20 text-purple-400' :
            'bg-cyan-500/20 text-cyan-400'
          }`}>
            {emergencyMode ? 'EMERGENCY' : systemMood.toUpperCase()}
          </div>
        </div>
        
        {/* Master Controls */}
        <div className="flex items-center gap-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTickLoop}
            className="p-2 glass-panel glass-depth-1 rounded-lg hover:bg-white/10 transition-all"
            title="Toggle Tick Loop"
          >
            {systemState.tickPaused ? <Play className="w-5 h-5 text-green-400" /> : <Pause className="w-5 h-5 text-yellow-400" />}
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={resetConsciousness}
            className="p-2 glass-panel glass-depth-1 rounded-lg hover:bg-white/10 transition-all"
            title="Reset Consciousness"
          >
            <RotateCcw className="w-5 h-5 text-cyan-400" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={emergencyStop}
            className="p-2 glass-panel glass-depth-1 rounded-lg hover:bg-white/10 transition-all bg-red-500/20"
            title="Emergency Stop"
            disabled={emergencyMode}
          >
            <Shield className="w-5 h-5 text-red-400" />
          </motion.button>
          
          <div className="w-px h-8 bg-white/20" />
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={exportState}
            className="p-2 glass-panel glass-depth-1 rounded-lg hover:bg-white/10 transition-all"
            title="Export State"
          >
            <Download className="w-5 h-5 text-white/70" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setSystemState(prev => ({ ...prev, soundEnabled: !prev.soundEnabled }))}
            className="p-2 glass-panel glass-depth-1 rounded-lg hover:bg-white/10 transition-all"
            title="Toggle Sound"
          >
            {systemState.soundEnabled ? <Volume2 className="w-5 h-5 text-white/70" /> : <VolumeX className="w-5 h-5 text-white/70" />}
          </motion.button>
        </div>
      </div>
      
      {/* Main Layout */}
      <div className="absolute inset-0 top-16 p-4 grid grid-cols-12 gap-4">
        {/* Left Panel - Python Process Manager */}
        <div ref={pythonManagerRef} className="col-span-3 glass-panel glass-depth-2 rounded-xl p-4 overflow-hidden">
          <div className="h-full flex flex-col">
            <div className="flex items-center gap-2 mb-4">
              <Terminal className="w-5 h-5 text-green-400" />
              <h2 className="text-white font-semibold">Process Manager</h2>
            </div>
            {/* Placeholder for PythonProcessManager */}
            <div className="flex-1 bg-black/30 rounded-lg p-4 overflow-y-auto">
              <div className="text-white/50 text-sm">Python processes will appear here...</div>
            </div>
          </div>
        </div>
        
        {/* Center - Tick Loop Monitor */}
        <div ref={tickMonitorRef} className="col-span-6">
          <div className="glass-panel glass-depth-3 rounded-xl p-4 h-96">
            <div className="h-full flex items-center justify-center">
              {/* Placeholder for TickLoopMonitor */}
              <div className="text-center">
                <div className="w-48 h-48 rounded-full bg-purple-500/20 border-2 border-purple-400 flex items-center justify-center animate-pulse">
                  <div>
                    <div className="text-4xl font-bold text-white">0</div>
                    <div className="text-sm text-white/70">TICK</div>
                  </div>
                </div>
                <div className="mt-4 text-white/50">TickLoopMonitor</div>
              </div>
            </div>
          </div>
          
          {/* Bottom - Active Process Outputs */}
          <div className="mt-4 glass-panel glass-depth-2 rounded-xl p-4 h-48">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-cyan-400" />
              <h3 className="text-white font-medium text-sm">Active Process Outputs</h3>
            </div>
            <div className="h-32 bg-black/50 rounded-lg p-2 font-mono text-xs overflow-y-auto">
              {activeProcesses.length === 0 ? (
                <div className="text-white/30">No active processes...</div>
              ) : (
                activeProcesses.map((process, i) => (
                  <div key={i} className="text-green-400 mb-1">
                    [{new Date(process.timestamp).toLocaleTimeString()}] {process.output}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
        
        {/* Right Panel */}
        <div className="col-span-3 space-y-4">
          {/* Consciousness Visualizer */}
          <div ref={consciousnessRef} className="glass-panel glass-depth-2 rounded-xl p-4 h-64">
            <div className="h-full flex items-center justify-center">
              {/* Placeholder for ConsciousnessVisualizer */}
              <div className="text-center">
                <div className="w-32 h-32 rounded-full bg-gradient-to-br from-purple-400 to-cyan-400 animate-pulse" />
                <div className="mt-2 text-white/50 text-sm">Consciousness</div>
              </div>
            </div>
          </div>
          
          {/* System Logs */}
          <div className="glass-panel glass-depth-2 rounded-xl p-4 flex-1">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-yellow-400" />
              <h3 className="text-white font-medium text-sm">System Logs</h3>
            </div>
            <div className="h-64 bg-black/50 rounded-lg p-2 font-mono text-xs overflow-y-auto">
              {logs.length === 0 ? (
                <div className="text-white/30">System starting up...</div>
              ) : (
                logs.map(log => (
                  <div key={log.id} className={`mb-1 ${getLogColor(log.level)}`}>
                    [{log.timestamp.toLocaleTimeString()}] [{log.module}] {log.message}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* Performance Metrics Bar */}
      <div className="absolute bottom-0 left-0 right-0 h-12 glass-panel glass-depth-1 flex items-center justify-around px-6 text-xs">
        <div className="flex items-center gap-2">
          <Gauge className="w-4 h-4 text-green-400" />
          <span className="text-white/70">FPS:</span>
          <span className={`font-mono ${systemState.fps < 30 ? 'text-red-400' : 'text-green-400'}`}>
            {systemState.fps}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <Wifi className="w-4 h-4 text-cyan-400" />
          <span className="text-white/70">Latency:</span>
          <span className={`font-mono ${systemState.wsLatency > 100 ? 'text-yellow-400' : 'text-cyan-400'}`}>
            {systemState.wsLatency}ms
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-purple-400" />
          <span className="text-white/70">Queue:</span>
          <span className="font-mono text-purple-400">{systemState.processQueueDepth}</span>
        </div>
        
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-orange-400" />
          <span className="text-white/70">Memory:</span>
          <span className={`font-mono ${systemState.memoryUsage > 80 ? 'text-red-400' : 'text-orange-400'}`}>
            {systemState.memoryUsage}%
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-yellow-400" />
          <span className="text-white/70">Tick Lag:</span>
          <span className={`font-mono ${systemState.tickLag > 50 ? 'text-red-400' : 'text-yellow-400'}`}>
            {systemState.tickLag}ms
          </span>
        </div>
      </div>
      
      {/* Emergency Mode Overlay */}
      <AnimatePresence>
        {emergencyMode && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-red-500/20 backdrop-blur-sm flex items-center justify-center z-[100]"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0 }}
              className="glass-panel glass-depth-3 rounded-xl p-8 text-center"
            >
              <Shield className="w-16 h-16 text-red-400 mx-auto mb-4 animate-pulse" />
              <h2 className="text-2xl font-bold text-red-400 mb-2">EMERGENCY STOP ACTIVE</h2>
              <p className="text-white/70">All processes halted. System will recover in 3 seconds...</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default DAWNDashboard; 