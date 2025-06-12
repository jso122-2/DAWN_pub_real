import React, { useState, useEffect, useRef } from 'react';
import { Activity, Zap, AlertTriangle, Terminal } from 'lucide-react';
import { useEntropyState } from './hooks/useEntropyState';

const EntropyRingHUD = () => {
  const { systemEntropy, subprocesses } = useEntropyState();
  const [coherence, setCoherence] = useState(78);
  const [isHovered, setIsHovered] = useState(false);
  const [showTracer, setShowTracer] = useState(false);
  const [pulseIntensity, setPulseIntensity] = useState(0);
  const svgRef = useRef(null);

  // Calculate ring colors based on entropy
  const getEntropyColor = (value) => {
    if (value < 30) return '#14b8a6'; // stable - teal
    if (value < 70) return '#f59e0b'; // flux - amber
    return '#ef4444'; // critical - red
  };

  const getCoherenceColor = (value) => {
    if (value > 70) return '#00ffcc'; // high coherence
    if (value > 40) return '#9945ff'; // medium
    return '#ff0080'; // low coherence
  };

  // Auto-show when entropy is high
  useEffect(() => {
    if (systemEntropy > 75) {
      setIsHovered(true);
      setPulseIntensity(Math.min((systemEntropy - 75) / 25, 1));
    } else if (!isHovered) {
      setTimeout(() => setIsHovered(false), 3000);
    }
  }, [systemEntropy]);

  const radius = 80;
  const strokeWidth = 8;
  const normalizedRadius = radius - strokeWidth * 2;
  const circumference = normalizedRadius * 2 * Math.PI;

  return (
    <div className="fixed top-20 right-8 z-50">
      {/* Main Ring Container */}
      <div
        className={`relative transition-all duration-500 ${
          isHovered || systemEntropy > 75 ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
        }`}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => systemEntropy <= 75 && setIsHovered(false)}
      >
        {/* SVG Ring */}
        <svg
          ref={svgRef}
          height={radius * 2}
          width={radius * 2}
          className="transform -rotate-90 animate-entropy-spin"
          style={{ animationDuration: `${20 + systemEntropy / 5}s` }}
        >
          {/* Outer Glow */}
          <circle
            stroke={getEntropyColor(systemEntropy)}
            fill="transparent"
            strokeWidth={strokeWidth + 4}
            strokeDasharray={circumference + ' ' + circumference}
            style={{
              strokeDashoffset: circumference - (systemEntropy / 100) * circumference,
              filter: `drop-shadow(0 0 ${10 + pulseIntensity * 20}px ${getEntropyColor(systemEntropy)})`,
              opacity: 0.3 + pulseIntensity * 0.7,
              transition: 'all 0.5s ease-out'
            }}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
          
          {/* Inner Coherence Ring */}
          <circle
            stroke={getCoherenceColor(coherence)}
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference + ' ' + circumference}
            style={{
              strokeDashoffset: circumference - (coherence / 100) * circumference,
              filter: `drop-shadow(0 0 10px ${getCoherenceColor(coherence)})`,
              transition: 'all 0.3s ease-out'
            }}
            r={normalizedRadius - 15}
            cx={radius}
            cy={radius}
          />

          {/* Pulse Ring */}
          {pulseIntensity > 0 && (
            <circle
              stroke={getEntropyColor(systemEntropy)}
              fill="transparent"
              strokeWidth={2}
              r={normalizedRadius + 10}
              cx={radius}
              cy={radius}
              className="animate-ping"
              style={{
                opacity: pulseIntensity * 0.5,
              }}
            />
          )}
        </svg>

        {/* Center Metrics */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center">
            <div className="text-2xl font-bold text-dawn-glow-teal text-glow">
              {systemEntropy.toFixed(0)}%
            </div>
            <div className="text-xs text-gray-400">entropy</div>
          </div>
        </div>

        {/* Status Icons */}
        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 flex gap-2">
          {systemEntropy > 30 && <Activity className="w-4 h-4 text-dawn-glow-amber animate-pulse" />}
          {systemEntropy > 60 && <Zap className="w-4 h-4 text-dawn-glow-pink animate-pulse" />}
          {systemEntropy > 80 && <AlertTriangle className="w-4 h-4 text-red-500 animate-bounce" />}
        </div>

        {/* Tracer Toggle */}
        <button
          onClick={() => setShowTracer(!showTracer)}
          className="absolute -bottom-8 right-0 p-1 glass rounded hover:shadow-glow-sm transition-all"
        >
          <Terminal className="w-4 h-4 text-dawn-glow-teal" />
        </button>
      </div>

      {/* Subprocess Tracer Panel */}
      <div className={`absolute top-full mt-4 right-0 w-80 transition-all duration-300 ${
        showTracer ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4 pointer-events-none'
      }`}>
        <div className="glass-dark rounded-lg p-4 shadow-glow-sm">
          <h3 className="text-sm font-bold text-dawn-glow-teal mb-3 text-glow">Subprocess Tracer</h3>
          
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {subprocesses.map((proc, idx) => (
              <div
                key={`${proc.pid}-${idx}`}
                className="glass rounded p-2 border border-dawn-glow-teal/20 animate-breathe"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-xs font-mono text-dawn-glow-purple">
                      PID: {proc.pid}
                    </div>
                    <div className="text-sm text-gray-300">{proc.name}</div>
                  </div>
                  <div className={`text-xs px-2 py-1 rounded ${
                    proc.status === 'active' ? 'bg-green-500/20 text-green-400' :
                    proc.status === 'idle' ? 'bg-blue-500/20 text-blue-400' :
                    'bg-yellow-500/20 text-yellow-400'
                  }`}>
                    {proc.status}
                  </div>
                </div>
                
                <div className="mt-2 grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <div className="text-gray-500">CPU</div>
                    <div className="text-dawn-glow-amber">{proc.cpu.toFixed(1)}%</div>
                  </div>
                  <div>
                    <div className="text-gray-500">MEM</div>
                    <div className="text-dawn-glow-purple">{proc.memory.toFixed(0)}MB</div>
                  </div>
                  <div>
                    <div className="text-gray-500">ENT</div>
                    <div className={`${proc.entropy > 70 ? 'text-red-400' : 'text-dawn-glow-teal'}`}>
                      {proc.entropy.toFixed(0)}%
                    </div>
                  </div>
                </div>

                {/* Mini entropy bar */}
                <div className="mt-2 h-1 bg-dawn-void rounded-full overflow-hidden">
                  <div 
                    className="h-full transition-all duration-300"
                    style={{
                      width: `${proc.entropy}%`,
                      backgroundColor: getEntropyColor(proc.entropy),
                      boxShadow: `0 0 10px ${getEntropyColor(proc.entropy)}`
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* System Summary */}
          <div className="mt-3 pt-3 border-t border-dawn-glow-teal/20">
            <div className="flex justify-between text-xs">
              <span className="text-gray-400">System Coherence</span>
              <span className="text-dawn-glow-teal">{coherence.toFixed(1)}%</span>
            </div>
            <div className="flex justify-between text-xs mt-1">
              <span className="text-gray-400">Active Processes</span>
              <span className="text-dawn-glow-purple">{subprocesses.filter(p => p.status === 'active').length}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EntropyRingHUD;