// ActivityMonitor.tsx
import React, { useState, useEffect, useRef } from 'react';
import './ActivityMonitor.css';

interface MonitorData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
  timestamp: string;
  processes: ProcessStatus[];
}

interface ProcessStatus {
  id: string;
  name: string;
  status: 'running' | 'idle' | 'error';
  cpu: number;
  memory: number;
  lastOutput?: string;
}

interface HistoryPoint {
  tick: number;
  scup: number;
  entropy: number;
  timestamp: string;
}

export const ActivityMonitor: React.FC = () => {
  const [data, setData] = useState<MonitorData | null>(null);
  const [history, setHistory] = useState<HistoryPoint[]>([]);
  const [selectedMetric, setSelectedMetric] = useState<'scup' | 'entropy'>('scup');
  const terminalRef = useRef<HTMLDivElement>(null);

  // Simulated data update - replace with WebSocket subscription
  useEffect(() => {
    const interval = setInterval(() => {
      const mockData: MonitorData = {
        tick_number: Math.floor(Date.now() / 1000),
        scup: Math.floor(Math.random() * 30 + 70), // 70-100%
        entropy: Math.random() * 0.5 + 0.2, // 0.2-0.7
        mood: ['contemplative', 'analytical', 'creative', 'focused'][Math.floor(Math.random() * 4)],
        timestamp: new Date().toISOString(),
        processes: [
          { id: '1', name: 'neural_network', status: 'running', cpu: Math.random() * 100, memory: Math.random() * 100 },
          { id: '2', name: 'quantum_engine', status: 'running', cpu: Math.random() * 100, memory: Math.random() * 100 },
          { id: '3', name: 'chaos_module', status: 'idle', cpu: 0, memory: Math.random() * 50 },
          { id: '4', name: 'memory_palace', status: 'running', cpu: Math.random() * 100, memory: Math.random() * 100 },
        ]
      };
      
      setData(mockData);
      setHistory(prev => [...prev.slice(-50), {
        tick: mockData.tick_number,
        scup: mockData.scup,
        entropy: mockData.entropy,
        timestamp: mockData.timestamp
      }]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const renderASCIIChart = (metric: 'scup' | 'entropy') => {
    const height = 10;
    const width = 60;
    const values = history.map(h => metric === 'scup' ? h.scup : h.entropy * 100);
    
    if (values.length === 0) return null;

    const max = Math.max(...values);
    const min = Math.min(...values);
    const range = max - min || 1;

    const chart: string[] = [];
    
    // Create chart grid
    for (let y = height; y >= 0; y--) {
      let line = '';
      const threshold = min + (range * y / height);
      
      for (let x = 0; x < Math.min(width, values.length); x++) {
        const valueIndex = values.length - width + x;
        if (valueIndex >= 0) {
          const value = values[valueIndex];
          if (value >= threshold) {
            line += '█';
          } else if (value >= threshold - range / height * 0.5) {
            line += '▄';
          } else {
            line += ' ';
          }
        } else {
          line += ' ';
        }
      }
      
      const label = y === height ? `${max.toFixed(0)}%` : y === 0 ? `${min.toFixed(0)}%` : '';
      chart.push(`${label.padStart(4)} │${line}│`);
    }
    
    chart.push(`     └${'─'.repeat(width)}┘`);
    chart.push(`      ${' '.repeat(width - 10)}LAST 60s`);
    
    return chart.join('\n');
  };

  const getStatusSymbol = (status: string) => {
    switch (status) {
      case 'running': return '●';
      case 'idle': return '○';
      case 'error': return '×';
      default: return '?';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'status-running';
      case 'idle': return 'status-idle';
      case 'error': return 'status-error';
      default: return '';
    }
  };

  const renderProgressBar = (value: number, width: number = 20) => {
    const filled = Math.round(value / 100 * width);
    const empty = width - filled;
    return `[${'+'.repeat(filled)}${'-'.repeat(empty)}]`;
  };

  if (!data) {
    return <div className="activity-monitor loading">INITIALIZING MONITORING SYSTEMS...</div>;
  }

  return (
    <div className="activity-monitor">
      <div className="monitor-header">
        <h2>ACTIVITY MONITOR</h2>
        <div className="monitor-stats">
          <span>TICK: {data.tick_number}</span>
          <span className="separator">│</span>
          <span>UPTIME: {Math.floor(history.length / 60)}m {history.length % 60}s</span>
        </div>
      </div>

      <div className="monitor-grid">
        <div className="monitor-section consciousness-metrics">
          <div className="section-header">
            <h3>CONSCIOUSNESS METRICS</h3>
          </div>
          <div className="metrics-display">
            <div className="metric-item">
              <span className="metric-label">SCUP</span>
              <span className="metric-value scup-value">{data.scup}%</span>
              <div className="metric-bar">{renderProgressBar(data.scup, 30)}</div>
            </div>
            <div className="metric-item">
              <span className="metric-label">ENTROPY</span>
              <span className="metric-value entropy-value">{data.entropy.toFixed(3)}</span>
              <div className="metric-bar">{renderProgressBar(data.entropy * 100, 30)}</div>
            </div>
            <div className="metric-item">
              <span className="metric-label">MOOD</span>
              <span className="metric-value mood-value">{data.mood.toUpperCase()}</span>
            </div>
          </div>
        </div>

        <div className="monitor-section process-status">
          <div className="section-header">
            <h3>PROCESS STATUS</h3>
          </div>
          <div className="process-list">
            <div className="process-header">
              <span className="col-status">ST</span>
              <span className="col-name">PROCESS</span>
              <span className="col-cpu">CPU</span>
              <span className="col-mem">MEM</span>
            </div>
            {data.processes.map(process => (
              <div key={process.id} className="process-row">
                <span className={`col-status ${getStatusColor(process.status)}`}>
                  {getStatusSymbol(process.status)}
                </span>
                <span className="col-name">{process.name}</span>
                <span className="col-cpu">{process.cpu.toFixed(0)}%</span>
                <span className="col-mem">{process.memory.toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="monitor-section chart-section">
          <div className="section-header">
            <h3>HISTORICAL DATA</h3>
            <div className="chart-controls">
              <button 
                className={`chart-toggle ${selectedMetric === 'scup' ? 'active' : ''}`}
                onClick={() => setSelectedMetric('scup')}
              >
                SCUP
              </button>
              <button 
                className={`chart-toggle ${selectedMetric === 'entropy' ? 'active' : ''}`}
                onClick={() => setSelectedMetric('entropy')}
              >
                ENTROPY
              </button>
            </div>
          </div>
          <pre className="ascii-chart">
            {renderASCIIChart(selectedMetric)}
          </pre>
        </div>

        <div className="monitor-section log-output">
          <div className="section-header">
            <h3>SYSTEM LOG</h3>
          </div>
          <div className="log-content" ref={terminalRef}>
            <div className="log-entry">[{new Date().toLocaleTimeString()}] System initialized</div>
            <div className="log-entry">[{new Date().toLocaleTimeString()}] Neural network: processing batch 42</div>
            <div className="log-entry success">[{new Date().toLocaleTimeString()}] Quantum engine: entanglement stable</div>
            <div className="log-entry">[{new Date().toLocaleTimeString()}] Memory palace: indexing memories</div>
            <div className="log-entry warning">[{new Date().toLocaleTimeString()}] Chaos module: entropy spike detected</div>
            <div className="log-entry">[{new Date().toLocaleTimeString()}] SCUP threshold maintained at {data.scup}%</div>
            <div className="log-entry">_</div>
          </div>
        </div>
      </div>
    </div>
  );
};