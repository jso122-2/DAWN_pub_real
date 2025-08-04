import React, { useState, useEffect } from 'react';
import './SystemsPanel.css';

interface SystemStatus {
  name: string;
  status: 'online' | 'offline' | 'error' | 'connecting';
  endpoint: string;
  lastPing: number;
  responseTime: number;
  uptime: number;
}

interface SystemMetric {
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  threshold: number;
}

interface LogEntry {
  id: string;
  timestamp: number;
  level: 'info' | 'warning' | 'error' | 'debug';
  message: string;
  source: string;
}

export const SystemsPanel: React.FC = () => {
  const [systemStatuses, setSystemStatuses] = useState<SystemStatus[]>([]);
  const [systemMetrics, setSystemMetrics] = useState<SystemMetric[]>([]);
  const [logEntries, setLogEntries] = useState<LogEntry[]>([]);
  const [selectedSystem, setSelectedSystem] = useState<string | null>(null);

  const backendSystems: SystemStatus[] = [
    {
      name: 'Consciousness Engine',
      status: 'online',
      endpoint: 'ws://localhost:8000/ws',
      lastPing: Date.now(),
      responseTime: 45,
      uptime: 3600
    },
    {
      name: 'Conversation System',
      status: 'online',
      endpoint: 'ws://localhost:8001/ws',
      lastPing: Date.now(),
      responseTime: 32,
      uptime: 1800
    },
    {
      name: 'Visualization Engine',
      status: 'online',
      endpoint: 'ws://localhost:8002/ws',
      lastPing: Date.now(),
      responseTime: 78,
      uptime: 900
    },
    {
      name: 'Tick Engine',
      status: 'online',
      endpoint: 'ws://localhost:8003/ws',
      lastPing: Date.now(),
      responseTime: 12,
      uptime: 7200
    },
    {
      name: 'Memory System',
      status: 'online',
      endpoint: 'ws://localhost:8004/ws',
      lastPing: Date.now(),
      responseTime: 56,
      uptime: 5400
    }
  ];

  useEffect(() => {
    setSystemStatuses(backendSystems);

    // Initialize system metrics
    const metrics: SystemMetric[] = [
      {
        name: 'CPU Usage',
        value: 23.5,
        unit: '%',
        trend: 'stable',
        threshold: 80
      },
      {
        name: 'Memory Usage',
        value: 1.2,
        unit: 'GB',
        trend: 'up',
        threshold: 4
      },
      {
        name: 'Network Latency',
        value: 45,
        unit: 'ms',
        trend: 'stable',
        threshold: 100
      },
      {
        name: 'Active Connections',
        value: 12,
        unit: '',
        trend: 'up',
        threshold: 50
      },
      {
        name: 'Tick Rate',
        value: 8.5,
        unit: 'Hz',
        trend: 'stable',
        threshold: 10
      },
      {
        name: 'Error Rate',
        value: 0.02,
        unit: '%',
        trend: 'down',
        threshold: 1
      }
    ];
    setSystemMetrics(metrics);

    // Simulate log entries
    const logs: LogEntry[] = [
      {
        id: 'log-1',
        timestamp: Date.now() - 60000,
        level: 'info',
        message: 'Consciousness engine started successfully',
        source: 'consciousness-engine'
      },
      {
        id: 'log-2',
        timestamp: Date.now() - 45000,
        level: 'info',
        message: 'WebSocket connections established',
        source: 'websocket-service'
      },
      {
        id: 'log-3',
        timestamp: Date.now() - 30000,
        level: 'warning',
        message: 'High entropy detected, activating stabilization protocols',
        source: 'entropy-monitor'
      },
      {
        id: 'log-4',
        timestamp: Date.now() - 15000,
        level: 'info',
        message: 'Visualization snapshot generated',
        source: 'visualization-engine'
      }
    ];
    setLogEntries(logs);

    // Simulate real-time updates
    const interval = setInterval(() => {
      // Update system statuses
      setSystemStatuses(prev => 
        prev.map(system => ({
          ...system,
          lastPing: Date.now(),
          responseTime: Math.max(10, Math.min(200, system.responseTime + (Math.random() - 0.5) * 20)),
          uptime: system.uptime + 1
        }))
      );

      // Update metrics
      setSystemMetrics(prev => 
        prev.map(metric => ({
          ...metric,
          value: Math.max(0, metric.value + (Math.random() - 0.5) * metric.value * 0.1)
        }))
      );

      // Add occasional log entries
      if (Math.random() > 0.95) {
        const newLog: LogEntry = {
          id: `log-${Date.now()}`,
          timestamp: Date.now(),
          level: Math.random() > 0.9 ? 'warning' : 'info',
          message: generateLogMessage(),
          source: ['consciousness-engine', 'websocket-service', 'entropy-monitor', 'visualization-engine'][Math.floor(Math.random() * 4)]
        };
        setLogEntries(prev => [newLog, ...prev.slice(0, 19)]); // Keep last 20
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const generateLogMessage = (): string => {
    const messages = [
      'Tick processed successfully',
      'Memory allocation optimized',
      'Neural pathway activated',
      'Consciousness state updated',
      'Visualization data processed',
      'WebSocket message received',
      'System health check passed',
      'Performance metrics recorded'
    ];
    return messages[Math.floor(Math.random() * messages.length)];
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return '#00ff88';
      case 'offline': return '#ff4444';
      case 'error': return '#ff8800';
      case 'connecting': return '#ffaa00';
      default: return '#ffffff';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '📈';
      case 'down': return '📉';
      case 'stable': return '➡️';
      default: return '➡️';
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'info': return '#00ff88';
      case 'warning': return '#ffaa00';
      case 'error': return '#ff4444';
      case 'debug': return '#888888';
      default: return '#ffffff';
    }
  };

  const pingSystem = (systemName: string) => {
    setSystemStatuses(prev => 
      prev.map(system => 
        system.name === systemName 
          ? { ...system, status: 'connecting' as const }
          : system
      )
    );

    // Simulate ping response
    setTimeout(() => {
      setSystemStatuses(prev => 
        prev.map(system => 
          system.name === systemName 
            ? { ...system, status: 'online' as const, lastPing: Date.now() }
            : system
        )
      );
    }, 1000);
  };

  const restartSystem = (systemName: string) => {
    setSystemStatuses(prev => 
      prev.map(system => 
        system.name === systemName 
          ? { ...system, status: 'connecting' as const }
          : system
      )
    );

    // Simulate restart
    setTimeout(() => {
      setSystemStatuses(prev => 
        prev.map(system => 
          system.name === systemName 
            ? { ...system, status: 'online' as const, uptime: 0 }
            : system
        )
      );
    }, 3000);
  };

  return (
    <div className="systems-panel">
      <div className="panel-header">
        <h3>⚙️ Systems</h3>
        <div className="system-controls">
          <button className="refresh-btn">🔄 Refresh</button>
          <button className="config-btn">⚙️ Config</button>
        </div>
      </div>

      <div className="systems-content">
        {/* System Status */}
        <div className="status-section">
          <h4>🔗 Backend Connections</h4>
          <div className="systems-grid">
            {systemStatuses.map(system => (
              <div key={system.name} className="system-card">
                <div className="system-header">
                  <span className="system-name">{system.name}</span>
                  <span 
                    className="system-status"
                    style={{ color: getStatusColor(system.status) }}
                  >
                    {system.status.toUpperCase()}
                  </span>
                </div>
                <div className="system-details">
                  <div className="detail">
                    <span>Endpoint:</span>
                    <span className="endpoint">{system.endpoint}</span>
                  </div>
                  <div className="detail">
                    <span>Response:</span>
                    <span>{system.responseTime}ms</span>
                  </div>
                  <div className="detail">
                    <span>Uptime:</span>
                    <span>{Math.floor(system.uptime / 60)}m {system.uptime % 60}s</span>
                  </div>
                  <div className="detail">
                    <span>Last Ping:</span>
                    <span>{new Date(system.lastPing).toLocaleTimeString()}</span>
                  </div>
                </div>
                <div className="system-actions">
                  <button 
                    className="ping-btn"
                    onClick={() => pingSystem(system.name)}
                  >
                    📡 Ping
                  </button>
                  <button 
                    className="restart-btn"
                    onClick={() => restartSystem(system.name)}
                  >
                    🔄 Restart
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Metrics */}
        <div className="metrics-section">
          <h4>📊 System Metrics</h4>
          <div className="metrics-grid">
            {systemMetrics.map(metric => (
              <div key={metric.name} className="metric-card">
                <div className="metric-header">
                  <span className="metric-name">{metric.name}</span>
                  <span className="metric-trend">{getTrendIcon(metric.trend)}</span>
                </div>
                <div className="metric-value">
                  {metric.value.toFixed(2)} {metric.unit}
                </div>
                <div className="metric-threshold">
                  Threshold: {metric.threshold} {metric.unit}
                </div>
                <div className="metric-bar">
                  <div 
                    className="metric-fill"
                    style={{
                      width: `${Math.min(100, (metric.value / metric.threshold) * 100)}%`,
                      backgroundColor: metric.value > metric.threshold * 0.8 ? '#ff4444' : '#00ff88'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Logs */}
        <div className="logs-section">
          <h4>📝 System Logs</h4>
          <div className="logs-container">
            {logEntries.map(log => (
              <div key={log.id} className="log-entry">
                <div className="log-header">
                  <span 
                    className="log-level"
                    style={{ color: getLevelColor(log.level) }}
                  >
                    {log.level.toUpperCase()}
                  </span>
                  <span className="log-time">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="log-source">{log.source}</span>
                </div>
                <div className="log-message">{log.message}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="systems-footer">
        <div className="system-summary">
          <span>Online: {systemStatuses.filter(s => s.status === 'online').length}/{systemStatuses.length}</span>
          <span>Avg Response: {Math.round(systemStatuses.reduce((sum, s) => sum + s.responseTime, 0) / systemStatuses.length)}ms</span>
          <span>Logs: {logEntries.length}</span>
        </div>
      </div>
    </div>
  );
}; 