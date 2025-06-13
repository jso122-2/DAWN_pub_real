import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence, useMotionValue, useTransform } from 'framer-motion';
import { 
  Activity, 
  Zap, 
  Heart, 
  AlertTriangle, 
  TrendingUp,
  Waves,
  CircuitBoard,
  Sparkles
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';

// Tick data interface
interface TickData {
  tick_number: number;
  scup: number; // System Consciousness Unity Percentage (0-100)
  entropy: number; // 0-1
  mood: string; // 'calm' | 'active' | 'excited' | 'chaotic'
  timestamp: number;
  duration?: number; // ms
  lag?: number; // ms
}

// Mood color mapping
const moodColors: Record<string, string> = {
  calm: '#22c55e',
  active: '#3b82f6',
  excited: '#a855f7',
  chaotic: '#ef4444'
};

interface TickLoopMonitorProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
}

const TickLoopMonitor: React.FC<TickLoopMonitorProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0 
}) => {
  const [isConnected, setIsConnected] = useState(false);
  const [currentTick, setCurrentTick] = useState<TickData | null>(null);
  const [tickHistory, setTickHistory] = useState<TickData[]>([]);
  const [pulseScale, setPulseScale] = useState(1);
  const [tickRate, setTickRate] = useState(0);
  const [anomalies, setAnomalies] = useState<string[]>([]);
  
  const wsRef = useRef<WebSocket | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  const lastTickTimeRef = useRef<number>(Date.now());
  
  // Motion values for smooth animations
  const scupValue = useMotionValue(50);
  const entropyValue = useMotionValue(0.5);
  const orbGlow = useTransform(scupValue, [0, 100], ['rgba(168, 85, 247, 0.3)', 'rgba(168, 85, 247, 0.9)']);
  
  // Connect to WebSocket
  const connectWebSocket = useCallback(() => {
    try {
      // In production, use actual WebSocket URL
      // wsRef.current = new WebSocket('ws://localhost:8000/ws/tick');
      
      // For demo, simulate WebSocket connection
      setIsConnected(true);
      simulateTickData();
      
      /* Production WebSocket code:
      wsRef.current.onopen = () => {
        console.log('[TickLoop] WebSocket connected');
        setIsConnected(true);
      };
      
      wsRef.current.onmessage = (event) => {
        const data: TickData = JSON.parse(event.data);
        handleTickData(data);
      };
      
      wsRef.current.onerror = (error) => {
        console.error('[TickLoop] WebSocket error:', error);
      };
      
      wsRef.current.onclose = () => {
        console.log('[TickLoop] WebSocket disconnected');
        setIsConnected(false);
        // Reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
      };
      */
    } catch (error) {
      console.error('[TickLoop] Failed to connect:', error);
      setIsConnected(false);
    }
  }, []);
  
  // Simulate tick data for demo
  const simulateTickData = () => {
    let tickNumber = 1000;
    
    const sendTick = () => {
      const now = Date.now();
      const duration = now - lastTickTimeRef.current;
      lastTickTimeRef.current = now;
      
      const data: TickData = {
        tick_number: tickNumber++,
        scup: Math.min(100, Math.max(0, 50 + Math.sin(tickNumber * 0.1) * 30 + (Math.random() - 0.5) * 20)),
        entropy: Math.min(1, Math.max(0, 0.5 + Math.sin(tickNumber * 0.05) * 0.3 + (Math.random() - 0.5) * 0.2)),
        mood: ['calm', 'active', 'excited', 'chaotic'][Math.floor(Math.random() * 4)],
        timestamp: now,
        duration: duration,
        lag: Math.random() < 0.1 ? Math.random() * 50 : 0
      };
      
      handleTickData(data);
      
      // Variable tick rate based on entropy
      const nextTickDelay = 1000 - (data.entropy * 500) + Math.random() * 200;
      setTimeout(sendTick, nextTickDelay);
    };
    
    sendTick();
  };
  
  // Handle incoming tick data
  const handleTickData = (data: TickData) => {
    setCurrentTick(data);
    setPulseScale(1.2);
    setTimeout(() => setPulseScale(1), 300);
    
    // Update motion values smoothly
    scupValue.set(data.scup);
    entropyValue.set(data.entropy);
    
    // Update tick history (keep last 100)
    setTickHistory(prev => [...prev.slice(-99), data]);
    
    // Calculate tick rate
    if (data.duration) {
      setTickRate(1000 / data.duration);
    }
    
    // Check for anomalies
    if (data.lag && data.lag > 30) {
      setAnomalies(prev => [...prev.slice(-4), `High lag: ${data.lag.toFixed(0)}ms`]);
    }
    if (data.scup < 20) {
      setAnomalies(prev => [...prev.slice(-4), 'Low consciousness detected']);
    }
    if (data.entropy > 0.8) {
      setAnomalies(prev => [...prev.slice(-4), 'High entropy warning']);
    }
    
    // Emit tick event
    emitter.emit('tick:complete', data);
  };
  
  // Draw tick rate graph
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || tickHistory.length < 2) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const draw = () => {
      const width = canvas.width;
      const height = canvas.height;
      
      // Clear canvas
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, width, height);
      
      // Draw grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.lineWidth = 1;
      for (let i = 0; i < height; i += 20) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(width, i);
        ctx.stroke();
      }
      
      // Draw tick rate line
      ctx.strokeStyle = 'rgba(34, 211, 238, 0.8)';
      ctx.lineWidth = 2;
      ctx.beginPath();
      
      tickHistory.forEach((tick, index) => {
        const x = (index / (tickHistory.length - 1)) * width;
        const rate = tick.duration ? 1000 / tick.duration : 1;
        const y = height - (rate / 2) * height;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
      
      // Draw SCUP overlay
      ctx.strokeStyle = 'rgba(168, 85, 247, 0.6)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      
      tickHistory.forEach((tick, index) => {
        const x = (index / (tickHistory.length - 1)) * width;
        const y = height - (tick.scup / 100) * height;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      
      ctx.stroke();
    };
    
    draw();
  }, [tickHistory]);
  
  // Initialize WebSocket connection
  useEffect(() => {
    connectWebSocket();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connectWebSocket]);
  
  // Create particle effect
  const renderParticles = () => {
    if (!currentTick) return null;
    
    return [...Array(Math.floor(currentTick.entropy * 20))].map((_, i) => (
      <motion.div
        key={`particle-${i}`}
        className="absolute w-1 h-1 bg-purple-400 rounded-full"
        initial={{ 
          x: 0, 
          y: 0,
          opacity: 0.8 
        }}
        animate={{
          x: Math.cos(i * 0.5) * 100 * currentTick.entropy,
          y: Math.sin(i * 0.5) * 100 * currentTick.entropy,
          opacity: 0
        }}
        transition={{
          duration: 2,
          repeat: Infinity,
          delay: i * 0.1,
          ease: 'linear'
        }}
      />
    ));
  };
  
  return (
    <div className="w-full h-full flex flex-col p-4 relative overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Heart className="w-5 h-5 text-purple-400" />
          <h3 className="text-white font-semibold">Tick Loop Monitor</h3>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
        </div>
        <div className="text-xs text-white/50">
          Rate: {tickRate.toFixed(1)} Hz
        </div>
      </div>
      
      {/* Central Core Visualization */}
      <div className="flex-1 flex items-center justify-center relative">
        {/* Pulse Rings */}
        <AnimatePresence>
          {currentTick && (
            <motion.div
              key={currentTick.tick_number}
              className="absolute w-64 h-64 rounded-full border-2 border-purple-400/30"
              initial={{ scale: 0.8, opacity: 1 }}
              animate={{ scale: 2, opacity: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 1.5, ease: 'easeOut' }}
            />
          )}
        </AnimatePresence>
        
        {/* SCUP Orb */}
        <motion.div
          className="relative w-48 h-48 rounded-full flex items-center justify-center"
          animate={{ scale: pulseScale }}
          transition={{ type: 'spring', stiffness: 300 }}
          style={{
            background: orbGlow,
            boxShadow: `0 0 ${currentTick?.scup || 50}px ${moodColors[currentTick?.mood || 'calm']}`,
            filter: 'blur(0.5px)'
          }}
        >
          {/* Inner Core */}
          <motion.div
            className="absolute inset-4 rounded-full bg-gradient-to-br from-purple-400 to-cyan-400"
            animate={{ 
              rotate: currentTick ? currentTick.tick_number * 2 : 0,
              scale: [1, 1.1, 1]
            }}
            transition={{ 
              rotate: { duration: 20, ease: 'linear' },
              scale: { duration: 2, repeat: Infinity }
            }}
          />
          
          {/* Tick Number */}
          <div className="relative z-10 text-center">
            <motion.div
              key={currentTick?.tick_number}
              initial={{ scale: 1.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="text-3xl font-bold text-white"
            >
              {currentTick?.tick_number || 0}
            </motion.div>
            <div className="text-xs text-white/70">TICK</div>
          </div>
          
          {/* Energy Particles */}
          <div className="absolute inset-0 flex items-center justify-center">
            {renderParticles()}
          </div>
        </motion.div>
        
        {/* Orbiting Metrics */}
        <div className="absolute inset-0 flex items-center justify-center">
          {/* SCUP Indicator */}
          <motion.div
            className="absolute glass-panel glass-depth-1 rounded-lg p-3"
            animate={{
              x: Math.cos(Date.now() * 0.001) * 150,
              y: Math.sin(Date.now() * 0.001) * 150
            }}
          >
            <div className="flex items-center gap-2">
              <CircuitBoard className="w-4 h-4 text-purple-400" />
              <div>
                <div className="text-xs text-white/60">SCUP</div>
                <div className="text-lg font-bold text-purple-400">
                  {currentTick?.scup.toFixed(1)}%
                </div>
              </div>
            </div>
          </motion.div>
          
          {/* Entropy Indicator */}
          <motion.div
            className="absolute glass-panel glass-depth-1 rounded-lg p-3"
            animate={{
              x: Math.cos(Date.now() * 0.001 + Math.PI * 0.66) * 150,
              y: Math.sin(Date.now() * 0.001 + Math.PI * 0.66) * 150
            }}
          >
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <div>
                <div className="text-xs text-white/60">Entropy</div>
                <div className="text-lg font-bold text-cyan-400">
                  {(currentTick?.entropy * 100).toFixed(0)}%
                </div>
              </div>
            </div>
          </motion.div>
          
          {/* Mood Indicator */}
          <motion.div
            className="absolute glass-panel glass-depth-1 rounded-lg p-3"
            animate={{
              x: Math.cos(Date.now() * 0.001 + Math.PI * 1.33) * 150,
              y: Math.sin(Date.now() * 0.001 + Math.PI * 1.33) * 150
            }}
          >
            <div className="flex items-center gap-2">
              <Waves className="w-4 h-4" style={{ color: moodColors[currentTick?.mood || 'calm'] }} />
              <div>
                <div className="text-xs text-white/60">Mood</div>
                <div 
                  className="text-lg font-bold capitalize"
                  style={{ color: moodColors[currentTick?.mood || 'calm'] }}
                >
                  {currentTick?.mood || 'calm'}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
      
      {/* Bottom Panels */}
      <div className="space-y-3">
        {/* Tick Rate Graph */}
        <div className="glass-panel glass-depth-1 rounded-lg p-3">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-white/60">Tick History</span>
            <span className="text-xs text-white/40">Last 100 ticks</span>
          </div>
          <canvas
            ref={canvasRef}
            width={400}
            height={80}
            className="w-full h-20 rounded bg-black/30"
          />
        </div>
        
        {/* System Health */}
        <div className="flex gap-3">
          {/* Performance */}
          <div className="flex-1 glass-panel glass-depth-1 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-xs text-white/60">Performance</span>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-xs">
                <span className="text-white/50">Avg Duration</span>
                <span className="text-green-400">
                  {tickHistory.length > 0 
                    ? (tickHistory.reduce((acc, t) => acc + (t.duration || 0), 0) / tickHistory.length).toFixed(0)
                    : 0} ms
                </span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-white/50">Max Lag</span>
                <span className="text-yellow-400">
                  {Math.max(...tickHistory.map(t => t.lag || 0)).toFixed(0)} ms
                </span>
              </div>
            </div>
          </div>
          
          {/* Anomalies */}
          <div className="flex-1 glass-panel glass-depth-1 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-yellow-400" />
              <span className="text-xs text-white/60">Anomalies</span>
            </div>
            <div className="space-y-1 max-h-12 overflow-y-auto">
              {anomalies.length === 0 ? (
                <div className="text-xs text-white/40">System stable</div>
              ) : (
                anomalies.map((anomaly, i) => (
                  <div key={i} className="text-xs text-yellow-400">
                    {anomaly}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
      
      {/* WebSocket Status */}
      <div className="absolute bottom-2 right-2 text-xs text-white/30">
        {isConnected ? 'Connected' : 'Reconnecting...'}
      </div>
    </div>
  );
};

export default TickLoopMonitor; 