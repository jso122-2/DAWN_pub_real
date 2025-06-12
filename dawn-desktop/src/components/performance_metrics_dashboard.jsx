import React, { useState, useEffect, useRef } from 'react';
import CognitivePerformanceMatrix from './CognitivePerformanceMatrix';
import { connectWebSocket, onMetricsUpdate } from '../lib/api.js';

const PerformanceMetricsDashboard = () => {
  const [metrics, setMetrics] = useState({
    intensity: { current: 44.2, history: Array(20).fill(44) },        // HEAT
    symbolicLoad: { current: 2.8, total: 8.0, history: Array(20).fill(2.8) }, // memory
    entropy: { rate: 12, bandwidth: 156.3, history: Array(20).fill(12) },    // network
    buffer: { depth: 847, processed: 15234, history: Array(20).fill(847) }  // queue
  });
  
  const [liveCognitiveMetrics, setLiveCognitiveMetrics] = useState(null);
  const [disturbances, setDisturbances] = useState([]);
  const sparklineRefs = useRef({});
  const [mainAlert, setMainAlert] = useState(null);
  
  // Circular progress component with neural glow
  const CircularProgress = ({ value, max, label, color, size = 120, volatility = 0 }) => {
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
            background: `radial-gradient(circle, ${color}${Math.floor(volatility * 40).toString(16).padStart(2, '0')} 0%, transparent 70%)`,
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
          {/* Progress circle */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke={color}
            strokeWidth="8"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            className="transition-all duration-500 ease-out"
            strokeLinecap="round"
          />
          {/* Neural glow effect */}
          <circle
            cx={centerX}
            cy={centerY}
            r={radius}
            stroke={color}
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            opacity="0.3"
            filter="blur(4px)"
            className={volatility > 0.5 ? 'animate-pulse' : ''}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-2xl font-bold text-white text-dawn-glow-teal animate-pulse-glow">{value.toFixed(1)}%</div>
          <div className="text-xs text-gray-400 text-center">{label}</div>
        </div>
      </div>
    );
  };
  
  // Sparkline component with neural aesthetics
  const Sparkline = ({ data, color, height = 40 }) => {
    const canvasRef = useRef(null);
    
    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const padding = 2;
      
      // Clear canvas
      ctx.clearRect(0, 0, width, height);
      
      // Calculate points
      const points = data.map((value, index) => ({
        x: (index / (data.length - 1)) * (width - 2 * padding) + padding,
        y: height - (value / Math.max(...data)) * (height - 2 * padding) - padding
      }));
      
      // Draw neural field gradient
      const gradient = ctx.createLinearGradient(0, 0, 0, height);
      gradient.addColorStop(0, `${color}66`);
      gradient.addColorStop(0.5, `${color}33`);
      gradient.addColorStop(1, `${color}11`);
      
      // Draw area with neural aesthetics
      ctx.beginPath();
      ctx.moveTo(points[0].x, height);
      points.forEach(point => ctx.lineTo(point.x, point.y));
      ctx.lineTo(points[points.length - 1].x, height);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();
      
      // Draw main line
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      points.forEach(point => ctx.lineTo(point.x, point.y));
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
      ctx.shadowBlur = 10;
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
  
  // Status indicator with cognitive states
  const StatusIndicator = ({ status }) => {
    const config = {
      coherent: { color: 'bg-green-500', text: 'Coherent' },
      unstable: { color: 'bg-yellow-500', text: 'Unstable' },
      dissonant: { color: 'bg-red-500', text: 'Dissonant' }
    };
    
    return (
      <div className="flex items-center space-x-2">
        <div className={`w-2 h-2 rounded-full ${config[status].color} animate-pulse`} />
        <span className="text-xs text-gray-400">{config[status].text}</span>
      </div>
    );
  };
  
  // Calculate cognitive status
  const getStatus = (value, thresholds) => {
    if (value >= thresholds.critical) return 'dissonant';
    if (value >= thresholds.warning) return 'unstable';
    return 'coherent';
  };
  
  // Calculate volatility for visual effects
  const calculateVolatility = (history) => {
    if (history.length < 2) return 0;
    const recent = history.slice(-5);
    const avg = recent.reduce((a, b) => a + b, 0) / recent.length;
    const variance = recent.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / recent.length;
    return Math.min(1, Math.sqrt(variance) / 50);
  };
  
  // Update metrics with cognitive patterns
  useEffect(() => {
    connectWebSocket();
    const unsubscribe = onMetricsUpdate((data) => {
      // Map metrics.heat to intensity
      const intensity = data.heat || 0;
      // Calculate symbolicLoad from scup and entropy (example: average)
      const symbolicLoad = (typeof data.scup === 'number' && typeof data.entropy === 'number')
        ? (data.scup + data.entropy) / 2
        : 0;
      // Use entropy for entropy.rate
      const entropyRate = data.entropy || 0;
      // Map mood recalibration state to buffer.depth (example: hash or length)
      let bufferDepth = 0;
      if (typeof data.mood === 'string') {
        bufferDepth = data.mood.length * 100; // Example mapping
      } else if (typeof data.mood === 'number') {
        bufferDepth = data.mood * 100;
      }
      setLiveCognitiveMetrics({
        intensity,
        symbolicLoad,
        entropyRate,
        bufferDepth
      });
    });
    return () => {
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, []);
  
  const intensityStatus = getStatus(metrics.intensity.current, { warning: 70, critical: 85 });
  const loadStatus = getStatus((metrics.symbolicLoad.current / metrics.symbolicLoad.total) * 100, { warning: 70, critical: 85 });
  const entropyStatus = getStatus(metrics.entropy.rate, { warning: 50, critical: 100 });
  const bufferStatus = getStatus(metrics.buffer.depth, { warning: 2000, critical: 4000 });
  
  // Global disturbance handler
  const handleCognitiveDisturbance = (disturbance) => {
    // 1. Update main alert system
    setMainAlert({
      type: 'cognitive',
      message: disturbance.message,
      timestamp: disturbance.timestamp
    });
    // 2. Trigger visual effects in other components (placeholder)
    if (disturbance.type === 'intensity' && disturbance.message.includes('surge')) {
      // e.g., trigger a pulse effect
      console.log('Triggering pulse effect for intensity surge');
    }
    // Add more logic for other types as needed
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
            <CircularProgress 
              value={metrics.intensity.current} 
              max={100} 
              label="Processing Intensity" 
              color="#ec4899"
              volatility={calculateVolatility(metrics.intensity.history)}
            />
            <StatusIndicator status={intensityStatus} />
          </div>
          
          <div className="flex flex-col items-center">
            <CircularProgress 
              value={(metrics.symbolicLoad.current / metrics.symbolicLoad.total) * 100} 
              max={100} 
              label="Symbolic Load" 
              color="#3b82f6"
              volatility={calculateVolatility(metrics.symbolicLoad.history)}
            />
            <StatusIndicator status={loadStatus} />
            <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.symbolicLoad.current.toFixed(1)} / {metrics.symbolicLoad.total} units</span>
          </div>
          
          <div className="flex flex-col items-center">
            <CircularProgress 
              value={100 - (metrics.entropy.rate / 100) * 100} 
              max={100} 
              label="Entropy Drift" 
              color="#10b981"
              volatility={calculateVolatility(metrics.entropy.history)}
            />
            <StatusIndicator status={entropyStatus} />
            <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.entropy.rate.toFixed(1)}%</span>
          </div>
          
          <div className="flex flex-col items-center">
            <CircularProgress 
              value={100 - (metrics.buffer.depth / 5000) * 100} 
              max={100} 
              label="Cognitive Buffer" 
              color="#f59e0b"
              volatility={calculateVolatility(metrics.buffer.history)}
            />
            <StatusIndicator status={bufferStatus} />
            <span className="text-sm font-bold text-white text-dawn-glow-teal animate-pulse-glow">{metrics.buffer.depth} threads</span>
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
              {disturbances.map(disturbance => (
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
          intensity={liveCognitiveMetrics?.intensity}
          symbolicLoad={liveCognitiveMetrics?.symbolicLoad}
          entropyRate={liveCognitiveMetrics?.entropyRate}
          bufferDepth={liveCognitiveMetrics?.bufferDepth}
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