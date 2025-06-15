import React, { useState, useEffect, useRef } from 'react';
import { useConsciousnessStore } from '../../stores/consciousnessStore';
import { useWebSocketService } from '../../services/websocket/WebSocketService';

const AlertAnomalyPanel = () => {
  const [alerts, setAlerts] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [patterns, setPatterns] = useState([]);
  const [filter, setFilter] = useState('all');
  const [predictiveMode, setPredictiveMode] = useState(true);
  const rippleContainerRef = useRef(null);
  
  // Alert severity levels
  const severityConfig = {
    low: { color: '#10b981', bg: 'bg-green-900', text: 'text-green-400', ripple: 'rgba(16, 185, 129, 0.4)' },
    medium: { color: '#f59e0b', bg: 'bg-yellow-900', text: 'text-yellow-400', ripple: 'rgba(245, 158, 11, 0.4)' },
    high: { color: '#ef4444', bg: 'bg-red-900', text: 'text-red-400', ripple: 'rgba(239, 68, 68, 0.4)' },
    critical: { color: '#dc2626', bg: 'bg-red-950', text: 'text-red-500', ripple: 'rgba(220, 38, 38, 0.6)' }
  };
  
  // Pattern types
  const patternTypes = {
    convergence: { icon: '◈', color: '#3b82f6' },
    divergence: { icon: '◇', color: '#ec4899' },
    oscillation: { icon: '∞', color: '#8b5cf6' },
    cascade: { icon: '≋', color: '#10b981' },
    recursion: { icon: '↻', color: '#f59e0b' }
  };
  
  // Ripple effect component
  const RippleEffect = ({ x, y, color, size = 100 }) => {
    return (
      <div
        className="absolute pointer-events-none animate-ripple"
        style={{
          left: x - size / 2,
          top: y - size / 2,
          width: size,
          height: size,
        }}
      >
        <div
          className="w-full h-full rounded-full"
          style={{
            background: `radial-gradient(circle, ${color} 0%, transparent 70%)`,
            animation: 'ripple 2s ease-out forwards'
          }}
        />
      </div>
    );
  };
  
  // Create ripple effect for new alerts
  const createRipple = (severity) => {
    if (!rippleContainerRef.current) return;
    
    const container = rippleContainerRef.current;
    const rect = container.getBoundingClientRect();
    const x = Math.random() * rect.width;
    const y = Math.random() * rect.height;
    
    const ripple = document.createElement('div');
    ripple.className = 'absolute pointer-events-none';
    ripple.style.left = `${x - 50}px`;
    ripple.style.top = `${y - 50}px`;
    ripple.innerHTML = `
      <div class="w-24 h-24 rounded-full animate-ping" 
           style="background: radial-gradient(circle, ${severityConfig[severity].ripple} 0%, transparent 70%)">
      </div>
    `;
    
    container.appendChild(ripple);
    setTimeout(() => ripple.remove(), 2000);
  };
  
  // Generate alerts
  useEffect(() => {
    const alertInterval = setInterval(() => {
      if (Math.random() > 0.7) {
        const alertTypes = [
          { type: 'Pattern Anomaly', category: 'pattern', message: 'Unusual neural firing pattern detected in sector 7' },
          { type: 'Coherence Drop', category: 'coherence', message: 'Signal coherence below threshold' },
          { type: 'Entropy Spike', category: 'entropy', message: 'Unexpected entropy increase detected' },
          { type: 'Buffer Overflow', category: 'buffer', message: 'Cognitive buffer approaching capacity' },
          { type: 'Phase Drift', category: 'phase', message: 'Phase correlation drifting from baseline' }
        ];
        
        const severities = ['low', 'medium', 'high', 'critical'];
        const alert = alertTypes[Math.floor(Math.random() * alertTypes.length)];
        const severity = severities[Math.floor(Math.random() * severities.length)];
        
        const newAlert = {
          id: Date.now(),
          ...alert,
          severity,
          timestamp: new Date(),
          resolved: false
        };
        
        setAlerts(prev => [newAlert, ...prev.slice(0, 49)]);
        createRipple(severity);
      }
    }, 3000);
    
    // Generate anomalies
    const anomalyInterval = setInterval(() => {
      if (Math.random() > 0.8) {
        const newAnomaly = {
          id: Date.now(),
          type: Object.keys(patternTypes)[Math.floor(Math.random() * Object.keys(patternTypes).length)],
          confidence: 60 + Math.random() * 40,
          location: `Node ${Math.floor(Math.random() * 20)}`,
          timestamp: new Date()
        };
        
        setAnomalies(prev => [newAnomaly, ...prev.slice(0, 29)]);
      }
    }, 5000);
    
    // Predictive warnings
    const predictiveInterval = setInterval(() => {
      if (predictiveMode && Math.random() > 0.85) {
        const prediction = {
          id: Date.now(),
          type: 'Predictive Warning',
          message: `Pattern suggests ${Math.floor(Math.random() * 30 + 10)}% probability of coherence drop in next ${Math.floor(Math.random() * 60 + 30)}s`,
          confidence: 70 + Math.random() * 30,
          timestamp: new Date()
        };
        
        setPatterns(prev => [prediction, ...prev.slice(0, 19)]);
      }
    }, 8000);
    
    return () => {
      clearInterval(alertInterval);
      clearInterval(anomalyInterval);
      clearInterval(predictiveInterval);
    };
  }, [predictiveMode]);
  
  // Filter alerts
  const filteredAlerts = alerts.filter(alert => 
    filter === 'all' || alert.severity === filter
  );
  
  // Calculate statistics
  const stats = {
    total: alerts.length,
    critical: alerts.filter(a => a.severity === 'critical').length,
    unresolved: alerts.filter(a => !a.resolved).length,
    avgConfidence: anomalies.length > 0 
      ? anomalies.reduce((sum, a) => sum + a.confidence, 0) / anomalies.length 
      : 0
  };
  
  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700 relative overflow-hidden">
      {/* Ripple container */}
      <div ref={rippleContainerRef} className="absolute inset-0 overflow-hidden pointer-events-none" />
      
      {/* Header */}
      <div className="relative z-10 flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="relative">
            <span className="absolute inset-0 w-3 h-3 bg-red-500 rounded-full animate-ping"></span>
            <span className="relative block w-3 h-3 bg-red-500 rounded-full mr-2"></span>
          </span>
          Alert & Anomaly Detection
        </h3>
        <div className="flex items-center space-x-4">
          <label className="flex items-center text-sm">
            <input
              type="checkbox"
              checked={predictiveMode}
              onChange={(e) => setPredictiveMode(e.target.checked)}
              className="mr-2"
            />
            <span className="text-gray-400">Predictive Mode</span>
          </label>
          <button className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700">
            Configure
          </button>
        </div>
      </div>
      
      {/* Statistics Bar */}
      <div className="relative z-10 grid grid-cols-4 gap-4 mb-4 bg-gray-800 rounded p-3">
        <div className="text-center">
          <p className="text-xs text-gray-400">Active Alerts</p>
          <p className="text-lg font-bold text-white">{stats.unresolved}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-gray-400">Critical</p>
          <p className="text-lg font-bold text-red-400">{stats.critical}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-gray-400">Anomalies</p>
          <p className="text-lg font-bold text-purple-400">{anomalies.length}</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-gray-400">Confidence</p>
          <p className="text-lg font-bold text-blue-400">{stats.avgConfidence.toFixed(1)}%</p>
        </div>
      </div>
      
      {/* Filter Tabs */}
      <div className="relative z-10 flex space-x-2 mb-4">
        {['all', 'critical', 'high', 'medium', 'low'].map(level => (
          <button
            key={level}
            onClick={() => setFilter(level)}
            className={`px-3 py-1 rounded text-sm capitalize transition-colors ${
              filter === level
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
            }`}
          >
            {level}
          </button>
        ))}
      </div>
      
      {/* Main Content Grid */}
      <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Alerts Section */}
        <div className="bg-gray-800 rounded p-4 border border-gray-700">
          <h4 className="text-sm font-bold text-white mb-3 flex items-center justify-between">
            <span>Active Alerts</span>
            <span className="text-xs text-gray-400">{filteredAlerts.length} items</span>
          </h4>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {filteredAlerts.map(alert => (
              <div
                key={alert.id}
                className={`p-2 rounded border ${severityConfig[alert.severity].bg} border-opacity-50 border-gray-600 transition-all hover:border-opacity-100`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className={`text-sm font-semibold ${severityConfig[alert.severity].text}`}>
                      {alert.type}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">{alert.message}</p>
                  </div>
                  <div className="text-right ml-2">
                    <p className="text-xs text-gray-500">
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </p>
                    {!alert.resolved && (
                      <button
                        onClick={() => {
                          setAlerts(prev => 
                            prev.map(a => a.id === alert.id ? { ...a, resolved: true } : a)
                          );
                        }}
                        className="text-xs text-blue-400 hover:text-blue-300 mt-1"
                      >
                        Resolve
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Anomalies & Patterns Section */}
        <div className="space-y-4">
          {/* Anomalies */}
          <div className="bg-gray-800 rounded p-4 border border-gray-700">
            <h4 className="text-sm font-bold text-white mb-3">Pattern Anomalies</h4>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {anomalies.slice(0, 5).map(anomaly => (
                <div key={anomaly.id} className="flex items-center justify-between text-xs">
                  <div className="flex items-center">
                    <span className="text-lg mr-2" style={{ color: patternTypes[anomaly.type].color }}>
                      {patternTypes[anomaly.type].icon}
                    </span>
                    <span className="text-gray-300">{anomaly.type} @ {anomaly.location}</span>
                  </div>
                  <span className="text-gray-500">{anomaly.confidence.toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Predictive Warnings */}
          <div className="bg-gray-800 rounded p-4 border border-gray-700">
            <h4 className="text-sm font-bold text-white mb-3 flex items-center">
              <span className="w-2 h-2 bg-yellow-500 rounded-full mr-2 animate-pulse"></span>
              Predictive Analysis
            </h4>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {patterns.slice(0, 3).map(pattern => (
                <div key={pattern.id} className="bg-gray-700 rounded p-2">
                  <p className="text-xs text-yellow-400">{pattern.message}</p>
                  <div className="flex justify-between mt-1">
                    <span className="text-xs text-gray-500">
                      Confidence: {pattern.confidence.toFixed(1)}%
                    </span>
                    <span className="text-xs text-gray-600">
                      {new Date(pattern.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      {/* CSS for animations */}
      <style jsx>{`
        @keyframes ripple {
          0% {
            transform: scale(0.1);
            opacity: 1;
          }
          100% {
            transform: scale(2);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default AlertAnomalyPanel;