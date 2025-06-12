import React, { useState, useEffect, useRef } from 'react';
import CognitivePerformanceMatrix from './CognitivePerformanceMatrix';
import { connectWebSocket, onMetricsUpdate } from '../../lib/api';
import { motion } from 'framer-motion';
import { useCosmicStore } from '../../store/cosmic.store';
import eventBus, { emitMetricsUpdate, emitAlert } from '../../lib/eventBus';

// Add interfaces for state
interface MainAlert {
  message: string;
  timestamp: string;
}
interface CognitiveMetrics {
  intensity: number;
  symbolicLoad: number;
  entropyRate: number;
  bufferDepth: number;
}
interface Disturbance {
  type: string;
  message: string;
  timestamp: string;
  id?: string;
}

const PerformanceMetricsDashboard = () => {
  const [metrics, setMetrics] = useState({
    intensity: { current: 44.2, history: Array(20).fill(44) },        // HEAT
    symbolicLoad: { current: 2.8, total: 8.0, history: Array(20).fill(2.8) }, // memory
    entropy: { rate: 12, bandwidth: 156.3, history: Array(20).fill(12) },    // network
    buffer: { depth: 847, processed: 15234, history: Array(20).fill(847) }  // queue
  });
  
  const [liveCognitiveMetrics, setLiveCognitiveMetrics] = useState<CognitiveMetrics | null>(null);
  const [disturbances, setDisturbances] = useState<Disturbance[]>([]);
  const sparklineRefs = useRef<{}>({});
  const [mainAlert, setMainAlert] = useState<MainAlert | null>(null);
  
  // Get global state from cosmicStore
  const entropy = useCosmicStore((s) => s.entropy);
  const neuralActivity = useCosmicStore((s) => s.neuralActivity);
  const quantumCoherence = useCosmicStore((s) => s.quantumCoherence);
  const systemLoad = useCosmicStore((s) => s.systemLoad);
  
  // Circular progress component with cosmic gradient
  interface GradientStop {
    offset: string;
    color: string;
  }
  interface CircularProgressProps {
    value: number;
    max: number;
    label: string;
    gradient: GradientStop[];
    size?: number;
    volatility?: number;
  }
  const CircularProgress: React.FC<CircularProgressProps> = ({ value, max, label, gradient, size = 120, volatility = 0 }) => {
    const radius = size / 2 - 10;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (value / max) * circumference;
    const centerX = size / 2;
    const centerY = size / 2;
    
    return (
      <div className="relative" style={{ width: size, height: size }}>
        {/* Radial aura based on volatility */}
        <div 
          className="absolute inset-0 rounded-full animate-pulse"
          style={{
            background: `radial-gradient(circle, #a78bfa${Math.floor(volatility * 40).toString(16).padStart(2, '0')} 0%, transparent 70%)`,
            filter: 'blur(20px)',
            transform: `scale(${1 + volatility * 0.3})`
          }}
        />
        
        <svg width={size} height={size} className="transform -rotate-90 relative z-10">
          {/* Background circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke="#374151"
            strokeWidth="8"
            fill="none"
          />
          {/* Progress circle with gradient */}
          <defs>
            <linearGradient id={`cosmic-gradient-${label}`} x1="0%" y1="0%" x2="100%" y2="100%">
              {gradient.map((stop: GradientStop, i: number) => (
                <stop key={i} offset={stop.offset} stopColor={stop.color} />
              ))}
            </linearGradient>
          </defs>
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke={`url(#cosmic-gradient-${label})`}
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-500 ease-out"
            strokeLinecap="round"
          />
          {/* Glow effect */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke={`url(#cosmic-gradient-${label})`}
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            opacity="0.3"
            filter="blur(4px)"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-2xl font-bold text-white text-dawn-glow-teal animate-pulse-glow">{value.toFixed(1)}%</div>
          <div className="text-xs text-gray-400 text-center">{label}</div>
        </div>
      </div>
    );
  };
  
  // Neon Sparkline
  interface SparklineProps {
    data: number[];
    color: string;
    height?: number;
  }
  const Sparkline: React.FC<SparklineProps> = ({ data, color, height = 40 }) => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    
    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      
      const width = canvas.width;
      const padding = 2;
      
      // Clear canvas
      ctx.clearRect(0, 0, width, height);
      
      // Calculate points
      const points = data.map((value: number, index: number) => ({
        x: (index / (data.length - 1)) * (width - 2 * padding) + padding,
        y: height - (value / Math.max(...data)) * (height - 2 * padding) - padding
      }));
      
      // Draw neural field gradient
      const gradient = ctx.createLinearGradient(0, 0, 0, height);
      gradient.addColorStop(0, color + 'cc');
      gradient.addColorStop(0.5, color + '88');
      gradient.addColorStop(1, color + '33');
      
      // Draw area with neural aesthetics
      ctx.beginPath();
      ctx.moveTo(points[0].x, height);
      points.forEach((point) => ctx.lineTo(point.x, point.y));
      ctx.lineTo(points[points.length - 1].x, height);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Draw main line
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      points.forEach((point) => ctx.lineTo(point.x, point.y));
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw neural pulse at end point
      const lastPoint = points[points.length - 1];
      ctx.beginPath();
      ctx.arc(lastPoint.x, lastPoint.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      
      // Add glow to end point
      ctx.shadowBlur = 8;
      ctx.shadowColor = color;
      ctx.fill();
      ctx.shadowBlur = 0;
    }, [data, color, height]);
    
    return (
      <canvas 
        ref={canvasRef} 
        width={150} 
        height={height}
        className="w-full"
      />
    );
  };
  
  // Glowing status dot
  interface StatusDotProps {
    status: string;
    color: string;
  }
  const StatusDot: React.FC<StatusDotProps> = ({ status, color }) => (
    <span className={`inline-block w-3 h-3 rounded-full shadow-glow-md mr-2`} style={{ background: color, boxShadow: `0 0 12px 2px ${color}` }} />
  );
  
  // Calculate cognitive status
  interface StatusThresholds {
    warning: number;
    critical: number;
  }
  const getStatus = (value: number, thresholds: StatusThresholds): 'coherent' | 'unstable' | 'dissonant' => {
    if (value >= thresholds.critical) return 'dissonant';
    if (value >= thresholds.warning) return 'unstable';
    return 'coherent';
  };
  
  // Calculate volatility for visual effects
  const calculateVolatility = (history: number[]): number => {
    if (history.length < 2) return 0;
    const recent = history.slice(-5);
    const avg = recent.reduce((a: number, b: number) => a + b, 0) / recent.length;
    const variance = recent.reduce((sum: number, val: number) => sum + Math.pow(val - avg, 2), 0) / recent.length;
    return Math.min(1, Math.sqrt(variance) / 50);
  };
  
  // Subscribe to global state changes and update metrics
  useEffect(() => {
    setMetrics((prev) => ({
      ...prev,
      intensity: {
        ...prev.intensity,
        current: systemLoad * 100,
        history: [...prev.intensity.history.slice(-19), systemLoad * 100],
      },
      symbolicLoad: {
        ...prev.symbolicLoad,
        current: (neuralActivity + quantumCoherence) * 50,
        history: [...prev.symbolicLoad.history.slice(-19), (neuralActivity + quantumCoherence) * 50],
      },
      entropy: {
        ...prev.entropy,
        rate: entropy * 100,
        history: [...prev.entropy.history.slice(-19), entropy * 100],
      },
      buffer: {
        ...prev.buffer,
        depth: Math.round((1 - entropy) * 2000 + systemLoad * 1000),
        history: [...prev.buffer.history.slice(-19), Math.round((1 - entropy) * 2000 + systemLoad * 1000)],
      },
    }));
    // Emit metrics-update event
    emitMetricsUpdate({
      metrics: {
        entropy: entropy * 100,
        neuralActivity: neuralActivity * 100,
        quantumCoherence: quantumCoherence * 100,
        systemLoad: systemLoad * 100,
      },
      timestamp: Date.now(),
    });
    // Emit alert if entropy or systemLoad is critical
    if (entropy > 0.95 || systemLoad > 0.95) {
      emitAlert({
        message: `Critical ${entropy > 0.95 ? 'entropy' : 'system load'} detected!`,
        severity: 'error',
        timestamp: Date.now(),
      });
    }
  }, [entropy, neuralActivity, quantumCoherence, systemLoad]);
  
  const intensityStatus = getStatus(metrics.intensity.current, { warning: 70, critical: 85 });
  const loadStatus = getStatus((metrics.symbolicLoad.current / metrics.symbolicLoad.total) * 100, { warning: 70, critical: 85 });
  const entropyStatus = getStatus(metrics.entropy.rate, { warning: 50, critical: 100 });
  const bufferStatus = getStatus(metrics.buffer.depth, { warning: 2000, critical: 4000 });
  
  // Global disturbance handler
  const handleCognitiveDisturbance = (disturbance: Disturbance) => {
    setMainAlert({
      message: disturbance.message,
      timestamp: disturbance.timestamp
    });
    setDisturbances(prev => [
      ...prev,
      { ...disturbance, id: disturbance.id || Math.random().toString(36).slice(2) }
    ]);
    if (disturbance.type === 'intensity' && disturbance.message.includes('surge')) {
      console.log('Triggering pulse effect for intensity surge');
    }
  };
  
  return (
    <>
      <div className="bg-gray-900 rounded-lg p-6 border border-gray-700 animate-float">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-white flex items-center">
            <span className="w-3 h-3 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
            Cognitive Performance Matrix
          </h3>
          <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition-colors">
            Extract Telemetry
          </button>
        </div>
        
        {/* Neural Progress Indicators */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
          <div className="flex flex-col items-center">
            <motion.div whileHover={{ scale: 1.03, boxShadow: '0 0 32px #a78bfa55' }} className="glass rounded-xl p-6 shadow-glow-md transition-all">
              <CircularProgress 
                value={metrics.intensity.current} 
                max={100} 
                label="Processing Intensity" 
                gradient={[
                  { offset: '0%', color: '#ec4899' },
                  { offset: '50%', color: '#ec4899' },
                  { offset: '100%', color: '#ec4899' }
                ]}
                volatility={calculateVolatility(metrics.intensity.history)}
              />
              <StatusDot status={intensityStatus} color={intensityStatus === 'coherent' ? '#10b981' : intensityStatus === 'unstable' ? '#f59e0b' : '#f472b6'} />
            </motion.div>
          </div>
          
          <div className="flex flex-col items-center">
            <motion.div whileHover={{ scale: 1.03, boxShadow: '0 0 32px #a78bfa55' }} className="glass rounded-xl p-6 shadow-glow-md transition-all">
              <CircularProgress 
                value={(metrics.symbolicLoad.current / metrics.symbolicLoad.total) * 100} 
                max={100} 
                label="Symbolic Load" 
                gradient={[
                  { offset: '0%', color: '#3b82f6' },
                  { offset: '50%', color: '#3b82f6' },
                  { offset: '100%', color: '#3b82f6' }
                ]}
                volatility={calculateVolatility(metrics.symbolicLoad.history)}
              />
              <StatusDot status={loadStatus} color={loadStatus === 'coherent' ? '#10b981' : loadStatus === 'unstable' ? '#f59e0b' : '#f472b6'} />
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.symbolicLoad.current.toFixed(1)} / {metrics.symbolicLoad.total} units</span>
            </motion.div>
          </div>
          
          <div className="flex flex-col items-center">
            <motion.div whileHover={{ scale: 1.03, boxShadow: '0 0 32px #a78bfa55' }} className="glass rounded-xl p-6 shadow-glow-md transition-all">
              <CircularProgress 
                value={100 - (metrics.entropy.rate / 100) * 100} 
                max={100} 
                label="Entropy Drift" 
                gradient={[
                  { offset: '0%', color: '#10b981' },
                  { offset: '50%', color: '#10b981' },
                  { offset: '100%', color: '#10b981' }
                ]}
                volatility={calculateVolatility(metrics.entropy.history)}
              />
              <StatusDot status={entropyStatus} color={entropyStatus === 'coherent' ? '#10b981' : entropyStatus === 'unstable' ? '#f59e0b' : '#f472b6'} />
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.entropy.rate.toFixed(1)}%</span>
            </motion.div>
          </div>
          
          <div className="flex flex-col items-center">
            <motion.div whileHover={{ scale: 1.03, boxShadow: '0 0 32px #a78bfa55' }} className="glass rounded-xl p-6 shadow-glow-md transition-all">
              <CircularProgress 
                value={100 - (metrics.buffer.depth / 5000) * 100} 
                max={100} 
                label="Cognitive Buffer" 
                gradient={[
                  { offset: '0%', color: '#f59e0b' },
                  { offset: '50%', color: '#f59e0b' },
                  { offset: '100%', color: '#f59e0b' }
                ]}
                volatility={calculateVolatility(metrics.buffer.history)}
              />
              <StatusDot status={bufferStatus} color={bufferStatus === 'coherent' ? '#10b981' : bufferStatus === 'unstable' ? '#f59e0b' : '#f472b6'} />
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.buffer.depth} threads</span>
            </motion.div>
          </div>
        </div>
        
        {/* Neural Activity Trends */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-800 rounded p-4 border border-gray-700 animate-float">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-400">Intensity Waves</span>
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.intensity.current.toFixed(1)}%</span>
            </div>
            <Sparkline data={metrics.intensity.history} color="#ec4899" />
          </div>
          
          <div className="bg-gray-800 rounded p-4 border border-gray-700 animate-float">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-400">Symbolic Density</span>
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.symbolicLoad.current.toFixed(1)} units</span>
            </div>
            <Sparkline data={metrics.symbolicLoad.history} color="#3b82f6" />
          </div>
          
          <div className="bg-gray-800 rounded p-4 border border-gray-700 animate-float">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-400">Entropy Field</span>
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.entropy.rate.toFixed(1)}%</span>
            </div>
            <Sparkline data={metrics.entropy.history} color="#10b981" />
          </div>
          
          <div className="bg-gray-800 rounded p-4 border border-gray-700 animate-float">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm text-gray-400">Buffer Depth</span>
              <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.buffer.depth}</span>
            </div>
            <Sparkline data={metrics.buffer.history} color="#f59e0b" />
          </div>
        </div>
        
        {/* Cognitive Stats */}
        <div className="grid grid-cols-3 gap-4 mb-4">
          <div className="text-center">
            <p className="text-xs text-gray-400">Signal Bandwidth</p>
            <p className="text-lg font-bold text-white">{metrics.entropy.bandwidth.toFixed(1)} Hz</p>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-400">Patterns Resolved</p>
            <p className="text-lg font-bold text-white">{metrics.buffer.processed.toLocaleString()}</p>
          </div>
          <div className="text-center">
            <p className="text-xs text-gray-400">Coherence</p>
            <p className="text-lg font-bold text-green-400">99.97%</p>
          </div>
        </div>
        
        {/* Cognitive Disturbances */}
        {disturbances.length > 0 && (
          <div className="mt-4 bg-gray-800 rounded p-3 border border-purple-900">
            <h4 className="text-sm font-bold text-white mb-2 flex items-center">
              <span className="w-2 h-2 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
              Cognitive Disturbances
            </h4>
            <div className="space-y-1 max-h-20 overflow-y-auto">
              {disturbances.map((disturbance) => (
                <div key={disturbance.id} className="text-xs flex justify-between">
                  <span className="text-purple-400">{disturbance.message}</span>
                  <span className="text-gray-600">{disturbance.timestamp}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
      {/* CognitivePerformanceMatrix full-width below main dashboard */}
      <div className="w-full mt-8">
        <CognitivePerformanceMatrix
          intensity={liveCognitiveMetrics?.intensity ?? 0}
          symbolicLoad={liveCognitiveMetrics?.symbolicLoad ?? 0}
          entropyRate={liveCognitiveMetrics?.entropyRate ?? 0}
          bufferDepth={liveCognitiveMetrics?.bufferDepth ?? 0}
          onDisturbance={handleCognitiveDisturbance}
        />
      </div>
      {/* Render main alert if present */}
      {mainAlert && (
        <div className="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 bg-red-700 text-white px-6 py-2 rounded shadow-lg">
          <strong>Cognitive Warning:</strong> {mainAlert.message} <span className="text-xs text-gray-300 ml-2">{mainAlert.timestamp}</span>
        </div>
      )}
    </>
  );
};

export default PerformanceMetricsDashboard;