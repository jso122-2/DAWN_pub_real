import React, { useEffect, useState } from 'react';
import { useProcessFlowStore } from '../../store/processFlowStore';
import { ProcessUtils } from '../../services/processManager';

interface ProcessMonitorProps {
  processId: string;
}

interface MetricHistoryPoint {
  time: number;
  cpu: number;
  memory: number;
  tick: number;
}

export const ProcessMonitor: React.FC<ProcessMonitorProps> = ({ processId }) => {
  const { 
    processes, 
    startProcess, 
    stopProcess, 
    restartProcess, 
    clearErrors,
    removeProcess
  } = useProcessFlowStore();
  
  const [metrics, setMetrics] = useState<MetricHistoryPoint[]>([]);
  const [showLogs, setShowLogs] = useState(true);
  const [showErrors, setShowErrors] = useState(true);
  
  const process = processes.get(processId);
  
  useEffect(() => {
    if (!process) return;
    
    // Update metrics history
    const interval = setInterval(() => {
      setMetrics((prev) => {
        const newMetric: MetricHistoryPoint = {
          time: Date.now(),
          cpu: process.cpuUsage,
          memory: process.memoryUsage,
          tick: process.lastTick
        };
        
        // Keep only last 50 points
        return [...prev.slice(-49), newMetric];
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, [process]);
  
  if (!process) {
    return (
      <div className="process-monitor">
        <div className="monitor-error">
          ⚠️ Process not found
        </div>
      </div>
    );
  }
  
  const formatUptime = (executionTime: number): string => {
    if (executionTime < 60) return `${executionTime}s`;
    if (executionTime < 3600) return `${Math.floor(executionTime / 60)}m ${executionTime % 60}s`;
    return `${Math.floor(executionTime / 3600)}h ${Math.floor((executionTime % 3600) / 60)}m`;
  };
  
  const formatTimestamp = (timestamp: number): string => {
    return new Date(timestamp).toLocaleTimeString();
  };
  
  return (
    <div className="process-monitor">
      <div className="monitor-header">
        <h3>
          <span className="process-icon">🔍</span>
          {process.name}
        </h3>
        <button 
          className="close-monitor"
          onClick={() => useProcessFlowStore.getState().selectProcess(null)}
          title="Close monitor"
        >
          ✕
        </button>
      </div>
      
      <div className="monitor-section">
        <h4>Status</h4>
        <div className={`status-indicator ${process.status}`}>
          <span className="status-icon">
            {process.status === 'running' ? '🟢' : 
             process.status === 'error' ? '🔴' : 
             process.status === 'paused' ? '🟡' : 
             process.status === 'completed' ? '🔵' : '⚫'}
          </span>
          {process.status.toUpperCase()}
        </div>
        
        <div className="process-meta">
          <div className="meta-item">
            <span className="meta-label">Script:</span>
            <span className="meta-value">{process.script}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Category:</span>
            <span className={`meta-value category-${process.category}`}>
              {process.category.toUpperCase()}
            </span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Version:</span>
            <span className="meta-value">{process.version}</span>
          </div>
          {process.executionTime > 0 && (
            <div className="meta-item">
              <span className="meta-label">Uptime:</span>
              <span className="meta-value">{formatUptime(process.executionTime)}</span>
            </div>
          )}
        </div>
      </div>
      
      <div className="monitor-section">
        <h4>Performance</h4>
        <div className="metrics-grid">
          <div className="metric">
            <span className="metric-label">CPU Usage:</span>
            <div className="metric-value">
              <span className="metric-number">{process.cpuUsage.toFixed(1)}%</span>
              <div className="metric-bar">
                <div 
                  className="metric-fill cpu" 
                  style={{width: `${Math.min(process.cpuUsage, 100)}%`}}
                ></div>
              </div>
            </div>
          </div>
          
          <div className="metric">
            <span className="metric-label">Memory:</span>
            <div className="metric-value">
              <span className="metric-number">{process.memoryUsage.toFixed(1)} MB</span>
              <div className="metric-bar">
                <div 
                  className="metric-fill memory" 
                  style={{width: `${Math.min(process.memoryUsage / 10, 100)}%`}}
                ></div>
              </div>
            </div>
          </div>
          
          <div className="metric">
            <span className="metric-label">Last Tick:</span>
            <div className="metric-value">
              <span className="metric-number">{process.lastTick}</span>
            </div>
          </div>
        </div>
        
        {metrics.length > 0 && (
          <div className="metrics-chart">
            <svg width="100%" height="60" viewBox="0 0 300 60">
              <defs>
                <linearGradient id="cpuGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#00ff88" stopOpacity="0.8"/>
                  <stop offset="100%" stopColor="#00ff88" stopOpacity="0.1"/>
                </linearGradient>
              </defs>
              
              {/* CPU Usage Line */}
              <polyline
                fill="none"
                stroke="#00ff88"
                strokeWidth="2"
                points={metrics.map((m, i) => 
                  `${(i / (metrics.length - 1)) * 300},${60 - (m.cpu / 100) * 60}`
                ).join(' ')}
              />
              
              {/* Memory Usage Line */}
              <polyline
                fill="none"
                stroke="#0088ff"
                strokeWidth="2"
                strokeDasharray="5,5"
                points={metrics.map((m, i) => 
                  `${(i / (metrics.length - 1)) * 300},${60 - (m.memory / 1000) * 60}`
                ).join(' ')}
              />
            </svg>
            
            <div className="chart-legend">
              <span className="legend-item">
                <span className="legend-color cpu"></span>
                CPU %
              </span>
              <span className="legend-item">
                <span className="legend-color memory"></span>
                Memory MB
              </span>
            </div>
          </div>
        )}
      </div>
      
      <div className="monitor-section">
        <div className="section-header">
          <h4>I/O Ports</h4>
        </div>
        
        <div className="ports-container">
          <div className="ports-column">
            <h5>Inputs</h5>
            {process.inputs.map((input) => (
              <div key={input.id} className={`port-item ${input.connected ? 'connected' : 'disconnected'}`}>
                <span className="port-indicator">
                  {input.connected ? '🟢' : '⚫'}
                </span>
                <span className="port-name">{input.name}</span>
                <span className="port-type">{input.dataType}</span>
              </div>
            ))}
          </div>
          
          <div className="ports-column">
            <h5>Outputs</h5>
            {process.outputs.map((output) => (
              <div key={output.id} className={`port-item ${output.connected ? 'connected' : 'disconnected'}`}>
                <span className="port-indicator">
                  {output.connected ? '🟢' : '⚫'}
                </span>
                <span className="port-name">{output.name}</span>
                <span className="port-type">{output.dataType}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {process.logs.length > 0 && (
        <div className="monitor-section">
          <div className="section-header">
            <h4>Recent Logs</h4>
            <button 
              className={`toggle-btn ${showLogs ? 'active' : ''}`}
              onClick={() => setShowLogs(!showLogs)}
            >
              {showLogs ? '👁️' : '👁️‍🗨️'}
            </button>
          </div>
          
          {showLogs && (
            <div className="log-container">
              {process.logs.slice(-10).map((log, index) => (
                <div key={index} className={`log-entry ${log.level}`}>
                  <span className="log-time">
                    {formatTimestamp(log.timestamp)}
                  </span>
                  <span className={`log-level ${log.level}`}>
                    {log.level.toUpperCase()}
                  </span>
                  <span className="log-message">{log.message}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      {process.errors.length > 0 && (
        <div className="monitor-section errors">
          <div className="section-header">
            <h4>Errors ({process.errors.length})</h4>
            <div className="error-actions">
              <button 
                className={`toggle-btn ${showErrors ? 'active' : ''}`}
                onClick={() => setShowErrors(!showErrors)}
              >
                {showErrors ? '👁️' : '👁️‍🗨️'}
              </button>
              <button 
                className="clear-btn"
                onClick={() => clearErrors(process.id)}
                title="Clear errors"
              >
                🗑️
              </button>
            </div>
          </div>
          
          {showErrors && (
            <div className="error-container">
              {process.errors.slice(-5).map((error, index) => (
                <div key={index} className="error-entry">
                  <div className="error-header">
                    <span className="error-type">{error.type}</span>
                    <span className="error-time">
                      {formatTimestamp(error.timestamp)}
                    </span>
                  </div>
                  <div className="error-message">{error.message}</div>
                  {error.stack && (
                    <div className="error-stack">{error.stack}</div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      
      <div className="monitor-actions">
        <button 
          onClick={() => startProcess(process.id)}
          disabled={process.status === 'running'}
          className="action-btn start"
          title="Start process"
        >
          ▶ Start
        </button>
        <button 
          onClick={() => stopProcess(process.id)}
          disabled={process.status === 'idle'}
          className="action-btn stop"
          title="Stop process"
        >
          ■ Stop
        </button>
        <button 
          onClick={() => restartProcess(process.id)}
          className="action-btn restart"
          title="Restart process"
        >
          🔄 Restart
        </button>
        <button 
          onClick={() => removeProcess(process.id)}
          className="action-btn remove"
          title="Remove process"
        >
          🗑️ Remove
        </button>
      </div>
    </div>
  );
}; 