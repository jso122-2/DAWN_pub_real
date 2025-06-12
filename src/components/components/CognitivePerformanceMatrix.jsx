import React, { useState, useEffect, useRef } from 'react';
import eventBus from './eventBus';

const CognitivePerformanceMatrix = (props) => {
  const { intensity, symbolicLoad, entropyRate, bufferDepth, onDisturbance } = props;
  const [metrics, setMetrics] = useState({
    intensity: { current: 44.2, history: Array(20).fill(44) },        // Processing Intensity
    symbolicLoad: { current: 2.8, total: 8.0, history: Array(20).fill(2.8) }, // Symbolic Load
    entropy: { drift: 12, bandwidth: 156.3, history: Array(20).fill(12) },    // Entropy Drift
    buffer: { depth: 847, processed: 15234, history: Array(20).fill(847) }  // Cognitive Buffer
  });
  const [disturbances, setDisturbances] = useState([]);
  const sessionStartRef = useRef(Date.now());

  // Update metrics from props if provided
  useEffect(() => {
    if (
      intensity !== undefined ||
      symbolicLoad !== undefined ||
      entropyRate !== undefined ||
      bufferDepth !== undefined
    ) {
      setMetrics(prev => ({
        intensity: {
          current: intensity !== undefined ? intensity : prev.intensity.current,
          history: [...prev.intensity.history.slice(1), intensity !== undefined ? intensity : prev.intensity.current]
        },
        symbolicLoad: {
          current: symbolicLoad !== undefined ? symbolicLoad : prev.symbolicLoad.current,
          total: prev.symbolicLoad.total,
          history: [...prev.symbolicLoad.history.slice(1), symbolicLoad !== undefined ? symbolicLoad : prev.symbolicLoad.current]
        },
        entropy: {
          drift: entropyRate !== undefined ? entropyRate : prev.entropy.drift,
          bandwidth: prev.entropy.bandwidth,
          history: [...prev.entropy.history.slice(1), entropyRate !== undefined ? entropyRate : prev.entropy.drift]
        },
        buffer: {
          depth: bufferDepth !== undefined ? bufferDepth : prev.buffer.depth,
          processed: prev.buffer.processed,
          history: [...prev.buffer.history.slice(1), bufferDepth !== undefined ? bufferDepth : prev.buffer.depth]
        }
      }));
    }
  }, [intensity, symbolicLoad, entropyRate, bufferDepth]);

  // Circular progress with neural glow
  const CircularProgress = ({ value, max, label, color, size = 120, volatility = 0 }) => {
    const radius = size / 2 - 10;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (value / max) * circumference;
    const centerX = size / 2;
    const centerY = size / 2;
    return (
      <div className="relative" style={{ width: size, height: size }}>
        <div 
          className="absolute inset-0 rounded-full animate-pulse"
          style={{
            background: `radial-gradient(circle, ${color}${Math.floor(volatility * 40).toString(16).padStart(2, '0')} 0%, transparent 70%)`,
            filter: 'blur(20px)',
            transform: `scale(${1 + volatility * 0.3})`
          }}
        />
        <svg width={size} height={size} className="transform -rotate-90 relative z-10">
          <circle cx={centerX} cy={centerY} r={radius} stroke="#374151" strokeWidth="8" fill="none" />
          <circle cx={centerX} cy={centerY} r={radius} stroke={color} strokeWidth="8" fill="none" strokeDasharray={circumference} strokeDashoffset={offset} className="transition-all duration-500 ease-out" strokeLinecap="round" />
          <circle cx={centerX} cy={centerY} r={radius} stroke={color} strokeWidth="12" fill="none" strokeDasharray={circumference} strokeDashoffset={offset} opacity="0.3" filter="blur(4px)" className={volatility > 0.5 ? 'animate-pulse' : ''} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-2xl font-bold text-white">{value.toFixed(1)}%</div>
          <div className="text-xs text-gray-400 text-center">{label}</div>
        </div>
      </div>
    );
  };

  // Sparkline for trends
  const Sparkline = ({ data, color, height = 40 }) => {
    const canvasRef = useRef(null);
    useEffect(() => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const width = canvas.width;
      const padding = 2;
      ctx.clearRect(0, 0, width, height);
      const points = data.map((value, index) => ({
        x: (index / (data.length - 1)) * (width - 2 * padding) + padding,
        y: height - (value / Math.max(...data)) * (height - 2 * padding) - padding
      }));
      const gradient = ctx.createLinearGradient(0, 0, 0, height);
      gradient.addColorStop(0, `${color}66`);
      gradient.addColorStop(0.5, `${color}33`);
      gradient.addColorStop(1, `${color}11`);
      ctx.beginPath();
      ctx.moveTo(points[0].x, height);
      points.forEach(point => ctx.lineTo(point.x, point.y));
      ctx.lineTo(points[points.length - 1].x, height);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      points.forEach(point => ctx.lineTo(point.x, point.y));
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
      const lastPoint = points[points.length - 1];
      ctx.beginPath();
      ctx.arc(lastPoint.x, lastPoint.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.shadowBlur = 10;
      ctx.shadowColor = color;
      ctx.fill();
      ctx.shadowBlur = 0;
    }, [data, color, height]);
    return (
      <canvas ref={canvasRef} width={150} height={height} className="w-full" />
    );
  };

  // Status indicator
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

  // Status logic
  const getStatus = (value, thresholds) => {
    if (value >= thresholds.critical) return 'dissonant';
    if (value >= thresholds.warning) return 'unstable';
    return 'coherent';
  };

  // Volatility for visuals
  const calculateVolatility = (history) => {
    if (history.length < 2) return 0;
    const recent = history.slice(-5);
    const avg = recent.reduce((a, b) => a + b, 0) / recent.length;
    const variance = recent.reduce((sum, val) => sum + Math.pow(val - avg, 2), 0) / recent.length;
    return Math.min(1, Math.sqrt(variance) / 50);
  };

  // Simulate metric updates
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => {
        const intensityChange = (Math.random() - 0.5) * 10;
        const newIntensity = Math.max(0, Math.min(100, prev.intensity.current + intensityChange));
        const loadChange = (Math.random() - 0.5) * 0.5;
        const newLoad = Math.max(0.5, Math.min(prev.symbolicLoad.total, prev.symbolicLoad.current + loadChange));
        const entropyChange = (Math.random() - 0.5) * 5;
        const newEntropy = Math.max(1, Math.min(100, prev.entropy.drift + entropyChange));
        const bandwidthChange = (Math.random() - 0.5) * 20;
        const newBandwidth = Math.max(10, Math.min(500, prev.entropy.bandwidth + bandwidthChange));
        const bufferChange = Math.floor((Math.random() - 0.5) * 200);
        const newBuffer = Math.max(0, Math.min(5000, prev.buffer.depth + bufferChange));
        return {
          intensity: {
            current: newIntensity,
            history: [...prev.intensity.history.slice(1), newIntensity]
          },
          symbolicLoad: {
            current: newLoad,
            total: prev.symbolicLoad.total,
            history: [...prev.symbolicLoad.history.slice(1), newLoad]
          },
          entropy: {
            drift: newEntropy,
            bandwidth: newBandwidth,
            history: [...prev.entropy.history.slice(1), newEntropy]
          },
          buffer: {
            depth: newBuffer,
            processed: prev.buffer.processed + Math.floor(Math.random() * 100),
            history: [...prev.buffer.history.slice(1), newBuffer]
          }
        };
      });
      if (Math.random() > 0.95) {
        const disturbanceTypes = [
          { type: 'intensity', message: 'Cognitive surge detected' },
          { type: 'symbolicLoad', message: 'Symbolic memory overload' },
          { type: 'entropy', message: 'Entropy drift spike' },
          { type: 'buffer', message: 'Cognitive buffer overflow' }
        ];
        const disturbance = disturbanceTypes[Math.floor(Math.random() * disturbanceTypes.length)];
        const disturbanceObj = {
          ...disturbance,
          timestamp: new Date().toLocaleTimeString(),
          id: Date.now()
        };
        setDisturbances(prev => [disturbanceObj, ...prev.slice(0, 19)]);
        // Emit to event bus
        eventBus.dispatchEvent(new CustomEvent('cognitive-disturbance', { detail: disturbanceObj }));
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [onDisturbance]);

  const intensityStatus = getStatus(metrics.intensity.current, { warning: 70, critical: 85 });
  const loadStatus = getStatus((metrics.symbolicLoad.current / metrics.symbolicLoad.total) * 100, { warning: 70, critical: 85 });
  const entropyStatus = getStatus(metrics.entropy.drift, { warning: 50, critical: 100 });
  const bufferStatus = getStatus(metrics.buffer.depth, { warning: 2000, critical: 4000 });

  // Extract Telemetry handler
  const handleExtractTelemetry = () => {
    const now = Date.now();
    const durationMs = now - sessionStartRef.current;
    const durationSec = Math.floor(durationMs / 1000);
    const timestamp = new Date(sessionStartRef.current).toISOString();
    // Simple pattern analysis: count disturbance types
    const patternCounts = disturbances.reduce((acc, d) => {
      acc[d.type] = (acc[d.type] || 0) + 1;
      return acc;
    }, {});
    const report = {
      report_type: 'neural_activity',
      session: {
        started_at: timestamp,
        duration_seconds: durationSec,
        ended_at: new Date(now).toISOString()
      },
      metrics: {
        intensity: metrics.intensity,
        symbolicLoad: metrics.symbolicLoad,
        entropy: metrics.entropy,
        buffer: metrics.buffer
      },
      disturbances,
      pattern_analysis: patternCounts
    };
    const blob = new Blob([
      JSON.stringify(report, null, 2)
    ], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `neural_telemetry_${timestamp.replace(/[:.]/g, '-')}.dawn`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="w-3 h-3 bg-purple-500 rounded-full mr-2 animate-pulse"></span>
          Cognitive Performance Matrix
        </h3>
        <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition-colors" onClick={handleExtractTelemetry}>
          Extract Telemetry
        </button>
      </div>
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
          <span className="text-xs text-gray-500 mt-1">
            {metrics.symbolicLoad.current.toFixed(1)} / {metrics.symbolicLoad.total} units
          </span>
        </div>
        <div className="flex flex-col items-center">
          <CircularProgress 
            value={100 - (metrics.entropy.drift / 100) * 100} 
            max={100} 
            label="Entropy Drift" 
            color="#10b981"
            volatility={calculateVolatility(metrics.entropy.history)}
          />
          <StatusIndicator status={entropyStatus} />
          <span className="text-xs text-gray-500 mt-1">{metrics.entropy.drift.toFixed(1)}%</span>
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
          <span className="text-xs text-gray-500 mt-1">{metrics.buffer.depth} threads</span>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-800 rounded p-4 border border-gray-700">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-400">Intensity Waves</span>
            <span className="text-sm font-bold text-white">{metrics.intensity.current.toFixed(1)}%</span>
          </div>
          <Sparkline data={metrics.intensity.history} color="#ec4899" />
        </div>
        <div className="bg-gray-800 rounded p-4 border border-gray-700">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-400">Symbolic Density</span>
            <span className="text-sm font-bold text-white">{metrics.symbolicLoad.current.toFixed(1)} units</span>
          </div>
          <Sparkline data={metrics.symbolicLoad.history} color="#3b82f6" />
        </div>
        <div className="bg-gray-800 rounded p-4 border border-gray-700">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-400">Entropy Drift</span>
            <span className="text-sm font-bold text-white">{metrics.entropy.drift.toFixed(1)}%</span>
          </div>
          <Sparkline data={metrics.entropy.history} color="#10b981" />
        </div>
        <div className="bg-gray-800 rounded p-4 border border-gray-700">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-400">Buffer Depth</span>
            <span className="text-sm font-bold text-white">{metrics.buffer.depth}</span>
          </div>
          <Sparkline data={metrics.buffer.history} color="#f59e0b" />
        </div>
      </div>
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
  );
};

export default CognitivePerformanceMatrix; 