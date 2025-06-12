import React, { useState, useEffect, useRef } from 'react';

// Types for main props
export interface MetricsPanelProps {
  metrics: {
    entropy: number;
    heat: number;
    scup: number;
    tickRate: number;
  };
  history: {
    entropy: number[];
    heat: number[];
    scup: number[];
    tickRate: number[];
  };
  isConnected: boolean;
  lastUpdate: number;
}

// Types for subcomponent props
interface GaugeProps {
  value: number;
  history?: number[];
  thresholds?: number[];
}

interface CompositeMetricsProps {
  scup: number;
  entropy: number;
  heat: number;
  tickRate: number;
}

interface HistoricalChartsProps {
  metrics: {
    entropy: number[];
    heat: number[];
    scup: number[];
    tickRate: number[];
  };
}

// Individual Gauge Components
const EntropyGauge: React.FC<GaugeProps> = ({ value, history = [], thresholds = [0.3, 0.7] }) => {
  const [displayValue, setDisplayValue] = useState(0);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    // Smooth value animation
    const interval = setInterval(() => {
      setDisplayValue(prev => {
        const diff = value - prev;
        return Math.abs(diff) < 0.001 ? value : prev + diff * 0.1;
      });
    }, 16);
    return () => clearInterval(interval);
  }, [value]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 80;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Background arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI * 0.75, Math.PI * 2.25);
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 8;
    ctx.stroke();
    
    // Gradient fill
    const gradient = ctx.createConicGradient(Math.PI * 0.75, centerX, centerY);
    gradient.addColorStop(0, '#3b82f6'); // Blue (low)
    gradient.addColorStop(0.5, '#f59e0b'); // Yellow (medium)
    gradient.addColorStop(1, '#ef4444'); // Red (high)
    
    // Value arc
    ctx.beginPath();
    const endAngle = Math.PI * 0.75 + (displayValue * Math.PI * 1.5);
    ctx.arc(centerX, centerY, radius, Math.PI * 0.75, endAngle);
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 8;
    ctx.stroke();
    
    // Threshold markers
    thresholds.forEach(threshold => {
      const angle = Math.PI * 0.75 + (threshold * Math.PI * 1.5);
      const x1 = centerX + Math.cos(angle) * (radius - 15);
      const y1 = centerY + Math.sin(angle) * (radius - 15);
      const x2 = centerX + Math.cos(angle) * (radius + 5);
      const y2 = centerY + Math.sin(angle) * (radius + 5);
      
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = '#9ca3af';
      ctx.lineWidth = 2;
      ctx.stroke();
    });
    
    // Needle
    const needleAngle = Math.PI * 0.75 + (displayValue * Math.PI * 1.5);
    const needleLength = radius - 20;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(
      centerX + Math.cos(needleAngle) * needleLength,
      centerY + Math.sin(needleAngle) * needleLength
    );
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Center dot
    ctx.beginPath();
    ctx.arc(centerX, centerY, 6, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    
  }, [displayValue, thresholds]);

  // Sparkline for history
  const SparkLine: React.FC<{ data: number[]; width?: number; height?: number }> = ({ data, width = 100, height = 20 }) => {
    if (!data.length) return null;
    
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    
    const points = data.map((val, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${x},${y}`;
    }).join(' ');
    
    return (
      <svg width={width} height={height} className="ml-2">
        <polyline
          fill="none"
          stroke="#3b82f6"
          strokeWidth="1"
          points={points}
        />
      </svg>
    );
  };

  return (
    <div className="glass rounded-lg p-6 shadow-lg animate-float border border-purple-500/20">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">🌀 Entropy</h3>
        <SparkLine data={history} />
      </div>
      
      <div className="flex flex-col items-center">
        <canvas 
          ref={canvasRef}
          width={200}
          height={200}
          className="mb-4"
        />
        
        <div className="text-center">
          <div className="text-3xl font-bold text-white text-dawn-glow-teal animate-pulse-glow mb-1">{displayValue.toFixed(3)}</div>
          <div className={`text-sm px-2 py-1 rounded ${
            displayValue < 0.3 ? 'text-blue-400 bg-blue-400/20' :
            displayValue < 0.7 ? 'text-yellow-400 bg-yellow-400/20' :
            'text-red-400 bg-red-400/20'
          }`}>
            {displayValue < 0.3 ? 'Low' : displayValue < 0.7 ? 'Medium' : 'High'}
          </div>
        </div>
      </div>
    </div>
  );
};

const HeatGauge: React.FC<GaugeProps> = ({ value, history = [] }) => {
  const [displayValue, setDisplayValue] = useState(0);
  const [particles, setParticles] = useState<any[]>([]);

  useEffect(() => {
    // Smooth value animation
    const interval = setInterval(() => {
      setDisplayValue(prev => {
        const diff = value - prev;
        return Math.abs(diff) < 0.001 ? value : prev + diff * 0.1;
      });
    }, 16);
    return () => clearInterval(interval);
  }, [value]);

  useEffect(() => {
    // Generate steam particles for high heat
    if (displayValue > 0.7) {
      const newParticles = Array.from({ length: 5 }, (_, i) => ({
        id: Date.now() + i,
        x: Math.random() * 40 + 30,
        y: 0,
        life: 1
      }));
      setParticles(prev => [...prev, ...newParticles].slice(-20));
    }
    
    // Generate ice crystals for low heat
    if (displayValue < 0.3) {
      const newParticles = Array.from({ length: 3 }, (_, i) => ({
        id: Date.now() + i,
        x: Math.random() * 40 + 30,
        y: Math.random() * 100 + 50,
        life: 1,
        type: 'ice'
      }));
      setParticles(prev => [...prev, ...newParticles].slice(-15));
    }
  }, [displayValue]);

  useEffect(() => {
    // Animate particles
    const interval = setInterval(() => {
      setParticles(prev => prev.map(p => ({
        ...p,
        y: p.type === 'ice' ? p.y : p.y - 2,
        life: p.life - 0.02
      })).filter(p => p.life > 0));
    }, 50);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="glass rounded-lg p-6 shadow-lg animate-float border border-purple-500/20">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">🌡️ Heat</h3>
        <div className="text-xs text-gray-400">
          {displayValue > 0.7 ? '🔥 High' : displayValue < 0.3 ? '❄️ Cold' : '🌡️ Normal'}
        </div>
      </div>
      
      <div className="flex justify-center">
        <div className="relative">
          {/* Thermometer body */}
          <div className="w-8 h-40 bg-gray-700 rounded-full relative overflow-hidden">
            {/* Mercury */}
            <div 
              className={`absolute bottom-0 w-full transition-all duration-500 ease-out ${
                displayValue > 0.7 ? 'bg-gradient-to-t from-red-500 to-orange-400' :
                displayValue < 0.3 ? 'bg-gradient-to-t from-blue-400 to-cyan-300' :
                'bg-gradient-to-t from-yellow-400 to-orange-300'
              }`}
              style={{ 
                height: `${Math.max(10, displayValue * 90)}%`,
                borderRadius: displayValue > 0.8 ? '50% 50% 0 0' : '0'
              }}
            />
            
            {/* Scale marks */}
            {[0.2, 0.4, 0.6, 0.8].map(mark => (
              <div 
                key={mark}
                className="absolute right-0 w-2 h-0.5 bg-gray-500"
                style={{ bottom: `${mark * 90}%` }}
              />
            ))}
          </div>
          
          {/* Bulb */}
          <div className={`absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-12 h-12 rounded-full ${
            displayValue > 0.7 ? 'bg-red-500' :
            displayValue < 0.3 ? 'bg-blue-400' :
            'bg-yellow-400'
          }`} />
          
          {/* Particles */}
          <div className="absolute inset-0 pointer-events-none">
            {particles.map(particle => (
              <div
                key={particle.id}
                className={`absolute w-1 h-1 rounded-full transition-opacity duration-1000 ${
                  particle.type === 'ice' ? 'bg-cyan-300' : 'bg-white'
                }`}
                style={{
                  left: `${particle.x}px`,
                  top: `${particle.y}px`,
                  opacity: particle.life,
                  transform: particle.type === 'ice' ? 'rotate(45deg)' : 'none'
                }}
              />
            ))}
          </div>
        </div>
        
        {/* Value display */}
        <div className="ml-6 flex flex-col justify-center">
          <div className="text-3xl font-bold text-white text-dawn-glow-teal animate-pulse-glow mb-1">{displayValue.toFixed(3)}</div>
          <div className="text-sm text-gray-400">
            {Math.round(displayValue * 100)}°
          </div>
        </div>
      </div>
    </div>
  );
};

const SCUPGauge: React.FC<GaugeProps> = ({ value, history = [] }) => {
  const [displayValue, setDisplayValue] = useState(0);
  const [rotations, setRotations] = useState<number[]>([0, 0, 0, 0, 0]);

  useEffect(() => {
    // Smooth value animation
    const interval = setInterval(() => {
      setDisplayValue(prev => {
        const diff = value - prev;
        return Math.abs(diff) < 0.001 ? value : prev + diff * 0.1;
      });
    }, 16);
    return () => clearInterval(interval);
  }, [value]);

  useEffect(() => {
    // Update segment rotations based on sync value
    const targetRotations = Array.from({ length: 5 }, (_, i) => {
      if (displayValue > 0.8) {
        // High sync - all segments aligned
        return 0;
      } else {
        // Lower sync - segments scattered
        const scatterAmount = (1 - displayValue) * 360;
        return (i * 72 + Math.sin(Date.now() / 1000 + i) * scatterAmount) % 360;
      }
    });
    
    setRotations(prev => prev.map((rot, i) => {
      const diff = targetRotations[i] - rot;
      return rot + diff * 0.05;
    }));
  }, [displayValue]);

  return (
    <div className="glass rounded-lg p-6 shadow-lg animate-float border border-purple-500/20">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">🔄 SCUP</h3>
        <div className={`text-xs px-2 py-1 rounded ${
          displayValue > 0.8 ? 'text-green-400 bg-green-400/20 animate-pulse' :
          'text-yellow-400 bg-yellow-400/20'
        }`}>
          {displayValue > 0.8 ? 'SYNC!' : 'Aligning...'}
        </div>
      </div>
      
      <div className="flex flex-col items-center">
        <div className="relative w-32 h-32 mb-4">
          {/* Center circle */}
          <div className={`absolute inset-6 rounded-full border-4 transition-all duration-300 ${
            displayValue > 0.8 ? 'border-green-400 bg-green-400/20 shadow-lg shadow-green-400/50' :
            'border-gray-600 bg-gray-700'
          }`} />
          
          {/* Rotating segments */}
          {rotations.map((rotation, i) => (
            <div
              key={i}
              className={`absolute inset-0 transition-all duration-1000 ease-out`}
              style={{ transform: `rotate(${rotation}deg)` }}
            >
              <div className={`w-4 h-8 rounded-t-full mx-auto transition-colors duration-300 ${
                displayValue > 0.8 ? 'bg-green-400' :
                displayValue > 0.5 ? 'bg-yellow-400' :
                'bg-gray-500'
              }`} />
            </div>
          ))}
          
          {/* Pulse effect for perfect sync */}
          {displayValue > 0.9 && (
            <div className="absolute inset-0 rounded-full border-2 border-green-400 animate-ping" />
          )}
        </div>
        
        <div className="text-center">
          <div className="text-3xl font-bold text-white text-dawn-glow-teal animate-pulse-glow mb-1">{displayValue.toFixed(3)}</div>
          <div className="text-sm text-gray-400">
            Synchronization
          </div>
        </div>
      </div>
    </div>
  );
};

const TickRateGauge: React.FC<GaugeProps> = ({ value, history = [] }) => {
  const [displayValue, setDisplayValue] = useState(0);
  const [pendulumAngle, setPendulumAngle] = useState(0);

  useEffect(() => {
    // Smooth value animation
    const interval = setInterval(() => {
      setDisplayValue(prev => {
        const diff = value - prev;
        return Math.abs(diff) < 0.001 ? value : prev + diff * 0.1;
      });
    }, 16);
    return () => clearInterval(interval);
  }, [value]);

  useEffect(() => {
    // Animate pendulum based on tick rate
    const speed = Math.max(0.5, displayValue * 2); // Min speed to keep it moving
    const interval = setInterval(() => {
      setPendulumAngle(prev => prev + speed * 5);
    }, 50);
    return () => clearInterval(interval);
  }, [displayValue]);

  const bpm = Math.round(displayValue * 120); // Convert to BPM scale

  return (
    <div className="glass rounded-lg p-6 shadow-lg animate-float border border-purple-500/20">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">⏱️ Tick Rate</h3>
        <div className={`text-xs px-2 py-1 rounded ${
          displayValue > 0.8 ? 'text-red-400 bg-red-400/20' :
          displayValue < 0.3 ? 'text-blue-400 bg-blue-400/20' :
          'text-green-400 bg-green-400/20'
        }`}>
          {bpm} BPM
        </div>
      </div>
      
      <div className="flex flex-col items-center">
        {/* Metronome */}
        <div className="relative w-24 h-32 mb-4">
          <div className="absolute bottom-0 w-full h-4 bg-gray-700 rounded" />
          <div 
            className="absolute bottom-4 left-1/2 w-1 h-24 bg-gray-400 origin-bottom transition-transform duration-100 ease-linear"
            style={{ 
              transform: `translateX(-50%) rotate(${Math.sin(pendulumAngle * Math.PI / 180) * 30}deg)` 
            }}
          />
          <div 
            className={`absolute top-2 left-1/2 w-4 h-4 rounded-full transform -translate-x-1/2 transition-colors duration-300 ${
              displayValue > 0.8 ? 'bg-red-400' :
              displayValue < 0.3 ? 'bg-blue-400' :
              'bg-green-400'
            }`}
            style={{ 
              transform: `translateX(-50%) translateX(${Math.sin(pendulumAngle * Math.PI / 180) * 20}px)` 
            }}
          />
        </div>
        
        <div className="text-center">
          <div className="text-3xl font-bold text-white text-dawn-glow-teal animate-pulse-glow mb-1">{displayValue.toFixed(3)}</div>
          <div className="text-sm text-gray-400">
            Rate
          </div>
        </div>
      </div>
    </div>
  );
};

// Composite Metrics Components
const CompositeMetrics: React.FC<CompositeMetricsProps> = ({ scup, entropy, heat, tickRate }) => {
  const systemLoad = (entropy * 0.4 + heat * 0.3 + tickRate * 0.3);
  const stabilityIndex = (scup * 0.5 + (1 - entropy) * 0.3 + (1 - Math.abs(heat - 0.5)) * 0.2);
  const coherenceScore = (scup * 0.6 + stabilityIndex * 0.4);
  const pressureWarning = (entropy > 0.8 || heat > 0.9 || tickRate > 0.9);

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="glass rounded-lg p-4 shadow-lg animate-float border border-purple-500/20">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-300">⚡ System Load</h4>
          <div className={`w-2 h-2 rounded-full ${
            systemLoad > 0.8 ? 'bg-red-400 animate-pulse' :
            systemLoad > 0.6 ? 'bg-yellow-400' :
            'bg-green-400'
          }`} />
        </div>
        <div className="text-2xl font-bold text-white">
          {(systemLoad * 100).toFixed(0)}%
        </div>
        <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
          <div 
            className={`h-2 rounded-full transition-all duration-500 ${
              systemLoad > 0.8 ? 'bg-red-400' :
              systemLoad > 0.6 ? 'bg-yellow-400' :
              'bg-green-400'
            }`}
            style={{ width: `${systemLoad * 100}%` }}
          />
        </div>
      </div>

      <div className="glass rounded-lg p-4 shadow-lg animate-float border border-purple-500/20">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-300">🏛️ Stability</h4>
          <div className={`w-2 h-2 rounded-full ${
            stabilityIndex > 0.7 ? 'bg-green-400' :
            stabilityIndex > 0.4 ? 'bg-yellow-400' :
            'bg-red-400 animate-pulse'
          }`} />
        </div>
        <div className="text-2xl font-bold text-white">
          {(stabilityIndex * 100).toFixed(0)}%
        </div>
        <div className="text-xs text-gray-400 mt-1">
          {stabilityIndex > 0.7 ? 'Stable' : stabilityIndex > 0.4 ? 'Moderate' : 'Unstable'}
        </div>
      </div>

      <div className="glass rounded-lg p-4 shadow-lg animate-float border border-purple-500/20">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-300">🔗 Coherence</h4>
          <div className={`w-2 h-2 rounded-full ${
            coherenceScore > 0.8 ? 'bg-purple-400 animate-pulse' :
            coherenceScore > 0.5 ? 'bg-blue-400' :
            'bg-gray-400'
          }`} />
        </div>
        <div className="text-2xl font-bold text-white">
          {(coherenceScore * 100).toFixed(0)}%
        </div>
        <div className="text-xs text-gray-400 mt-1">
          {coherenceScore > 0.8 ? 'High' : coherenceScore > 0.5 ? 'Medium' : 'Low'}
        </div>
      </div>

      <div className={`glass rounded-lg p-4 shadow-lg transition-all duration-300 border border-purple-500/20 ${
        pressureWarning ? 'ring-2 ring-red-400 bg-red-900/20' : ''
      } animate-float`}>
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-medium text-gray-300">⚠️ Pressure</h4>
          <div className={`w-2 h-2 rounded-full ${
            pressureWarning ? 'bg-red-400 animate-pulse' : 'bg-green-400'
          }`} />
        </div>
        <div className={`text-2xl font-bold ${pressureWarning ? 'text-red-400' : 'text-green-400'}`}>
          {pressureWarning ? 'HIGH' : 'OK'}
        </div>
        <div className="text-xs text-gray-400 mt-1">
          {pressureWarning ? 'System pressure detected' : 'Normal operation'}
        </div>
      </div>
    </div>
  );
};

// Historical Charts Component
const HistoricalCharts: React.FC<HistoricalChartsProps> = ({ metrics }) => {
  const MiniChart: React.FC<{ title: string; data: number[]; color?: string; correlations?: { metric: string; value: number }[] }> = ({ title, data, color = '#3b82f6', correlations = [] }) => {
    if (!data || data.length < 2) return null;

    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    const width = 200;
    const height = 60;

    const points = data.map((val, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${x},${y}`;
    }).join(' ');

    // Find anomalies (values that deviate significantly from trend)
    const anomalies = data.map((val, i) => {
      if (i < 2 || i > data.length - 3) return false;
      const window = data.slice(i - 2, i + 3);
      const avg = window.reduce((a, b) => a + b) / window.length;
      const deviation = Math.abs(val - avg);
      return deviation > range * 0.3; // 30% deviation threshold
    });

    return (
      <div className="glass rounded-lg p-4 border border-purple-500/20">
        <div className="flex items-center justify-between mb-2">
          <h5 className="text-sm font-medium text-white">{title}</h5>
          <div className="flex space-x-1">
            {correlations.map((corr, i) => (
              <div 
                key={i}
                className={`text-xs px-1 py-0.5 rounded ${
                  Math.abs(corr.value) > 0.7 ? 'bg-green-400/20 text-green-400' :
                  Math.abs(corr.value) > 0.4 ? 'bg-yellow-400/20 text-yellow-400' :
                  'bg-gray-600/20 text-gray-400'
                }`}
                title={`Correlation with ${corr.metric}: ${corr.value.toFixed(2)}`}
              >
                {corr.metric.charAt(0).toUpperCase()}
              </div>
            ))}
          </div>
        </div>
        
        <div className="relative">
          <svg width={width} height={height} className="w-full">
            <defs>
              <linearGradient id={`gradient-${title}`} x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor={color} stopOpacity="0.3" />
                <stop offset="100%" stopColor={color} stopOpacity="0.1" />
              </linearGradient>
            </defs>
            
            {/* Area under curve */}
            <polygon
              fill={`url(#gradient-${title})`}
              points={`0,${height} ${points} ${width},${height}`}
            />
            
            {/* Main line */}
            <polyline
              fill="none"
              stroke={color}
              strokeWidth="2"
              points={points}
            />
            
            {/* Anomaly markers */}
            {anomalies.map((isAnomaly, i) => {
              if (!isAnomaly) return null;
              const x = (i / (data.length - 1)) * width;
              const y = height - ((data[i] - min) / range) * height;
              return (
                <circle
                  key={i}
                  cx={x}
                  cy={y}
                  r="3"
                  fill="#ef4444"
                  stroke="#ffffff"
                  strokeWidth="1"
                  className="animate-pulse"
                />
              );
            })}
          </svg>
        </div>
        
        <div className="flex justify-between text-xs text-gray-400 mt-1">
          <span>{min.toFixed(2)}</span>
          <span>5min</span>
          <span>{max.toFixed(2)}</span>
        </div>
      </div>
    );
  };

  // Calculate correlations between metrics
  const calculateCorrelation = (data1: number[], data2: number[]): number => {
    if (!data1 || !data2 || data1.length !== data2.length) return 0;
    const n = data1.length;
    const sum1 = data1.reduce((a: number, b: number) => a + b, 0);
    const sum2 = data2.reduce((a: number, b: number) => a + b, 0);
    const sum1Sq = data1.reduce((a: number, b: number) => a + b * b, 0);
    const sum2Sq = data2.reduce((a: number, b: number) => a + b * b, 0);
    const pSum = data1.reduce((a: number, b: number, i: number) => a + b * data2[i], 0);
    const num = pSum - (sum1 * sum2 / n);
    const den = Math.sqrt((sum1Sq - sum1 * sum1 / n) * (sum2Sq - sum2 * sum2 / n));
    return den === 0 ? 0 : num / den;
  };

  const correlations = {
    entropy: [
      { metric: 'heat', value: calculateCorrelation(metrics.entropy, metrics.heat) },
      { metric: 'scup', value: calculateCorrelation(metrics.entropy, metrics.scup) }
    ],
    heat: [
      { metric: 'entropy', value: calculateCorrelation(metrics.heat, metrics.entropy) },
      { metric: 'tick', value: calculateCorrelation(metrics.heat, metrics.tickRate) }
    ],
    scup: [
      { metric: 'entropy', value: calculateCorrelation(metrics.scup, metrics.entropy) },
      { metric: 'heat', value: calculateCorrelation(metrics.scup, metrics.heat) }
    ],
    tickRate: [
      { metric: 'heat', value: calculateCorrelation(metrics.tickRate, metrics.heat) },
      { metric: 'scup', value: calculateCorrelation(metrics.tickRate, metrics.scup) }
    ]
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-white mb-4">📊 Historical Analysis</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <MiniChart 
          title="Entropy History" 
          data={metrics.entropy} 
          color="#3b82f6"
          correlations={correlations.entropy}
        />
        <MiniChart 
          title="Heat History" 
          data={metrics.heat} 
          color="#ef4444"
          correlations={correlations.heat}
        />
        <MiniChart 
          title="SCUP History" 
          data={metrics.scup} 
          color="#10b981"
          correlations={correlations.scup}
        />
        <MiniChart 
          title="Tick Rate History" 
          data={metrics.tickRate} 
          color="#f59e0b"
          correlations={correlations.tickRate}
        />
      </div>
    </div>
  );
};

// Main MetricsPanel Component
const MetricsPanel: React.FC<MetricsPanelProps> = ({
  metrics = {
    entropy: 0.5,
    heat: 0.3,
    scup: 0.7,
    tickRate: 1.0
  },
  history = {
    entropy: [],
    heat: [],
    scup: [],
    tickRate: []
  },
  isConnected = true,
  lastUpdate = Date.now()
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="space-y-6">
      {/* Main Gauges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <EntropyGauge 
          value={metrics.entropy} 
          history={history.entropy}
          thresholds={[0.3, 0.7, 0.9]}
        />
        <HeatGauge 
          value={metrics.heat} 
          history={history.heat}
        />
        <SCUPGauge 
          value={metrics.scup} 
          history={history.scup}
        />
        <TickRateGauge 
          value={metrics.tickRate} 
          history={history.tickRate}
        />
      </div>

      {/* Composite Metrics */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">📈 System Overview</h3>
          <div className={`flex items-center space-x-2 text-sm ${
            isConnected ? 'text-green-400' : 'text-red-400'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'
            }`} />
            <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            <span className="text-gray-400">
              • Last update: {new Date(lastUpdate).toLocaleTimeString()}
            </span>
          </div>
        </div>
        
        <CompositeMetrics 
          scup={metrics.scup}
          entropy={metrics.entropy}
          heat={metrics.heat}
          tickRate={metrics.tickRate}
        />
      </div>

      {/* Historical Analysis (Expandable) */}
      <div className="space-y-4">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center space-x-2 text-white hover:text-blue-400 transition-colors"
        >
          <span className={`transform transition-transform ${isExpanded ? 'rotate-90' : ''}`}>
            ▶
          </span>
          <span>Historical Analysis & Correlations</span>
        </button>
        
        {isExpanded && (
          <div className="animate-fade-in">
            <HistoricalCharts metrics={history} />
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricsPanel; 