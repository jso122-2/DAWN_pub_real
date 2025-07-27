import React, { useState, useEffect } from 'react';
import { ConsciousnessDisplay } from './ConsciousnessDisplay';
import { TickMonitorPanel } from './TickMonitorPanel';
import { DriftGraphPanel } from './DriftGraphPanel';
import { ThoughtRateHeatmap } from './ThoughtRateHeatmap';
import './DashboardPanel.css';

// System Status Component
const SystemStatusWidget: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState({
    tick: 1247,
    entropy: 0.342,
    mood: 'contemplative',
    scup: 0.087,
    uptime: '12m 34s',
    version: 'v1.3.0a',
    hash: 'dawn_471',
    cpuUsage: 23.4,
    memoryUsage: 67.2,
    diskUsage: 45.8
  });

  // Update status periodically
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemStatus(prev => ({
        ...prev,
        tick: prev.tick + Math.floor(Math.random() * 3) + 1,
        entropy: Math.max(0, Math.min(1, prev.entropy + (Math.random() - 0.5) * 0.05)),
        scup: Math.max(0, Math.min(1, prev.scup + (Math.random() - 0.5) * 0.02)),
        cpuUsage: Math.max(0, Math.min(100, prev.cpuUsage + (Math.random() - 0.5) * 5)),
        memoryUsage: Math.max(0, Math.min(100, prev.memoryUsage + (Math.random() - 0.5) * 3)),
        uptime: `${Math.floor((Date.now() / 1000) / 60)}m ${Math.floor((Date.now() / 1000) % 60)}s`
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="system-status-widget">
      <div className="status-header">
        <h3>System Status</h3>
        <div className="live-indicator" title="Live monitoring active"></div>
      </div>
      
      <div className="status-grid">
        {/* Core Metrics */}
        <div className="status-section core-metrics">
          <h4>Core Metrics</h4>
          <div className="metric-row">
            <span className="metric-label">TICK</span>
            <span className="metric-value tick">{systemStatus.tick}</span>
          </div>
          <div className="metric-row">
            <span className="metric-label">ENTROPY</span>
            <span className="metric-value entropy">{systemStatus.entropy.toFixed(3)}</span>
          </div>
          <div className="metric-row">
            <span className="metric-label">SCUP</span>
            <span className="metric-value scup">{systemStatus.scup.toFixed(3)}</span>
          </div>
          <div className="metric-row">
            <span className="metric-label">MOOD</span>
            <span className="metric-value mood">{systemStatus.mood}</span>
          </div>
        </div>

        {/* System Resources */}
        <div className="status-section resources">
          <h4>Resources</h4>
          <div className="resource-bar">
            <span className="resource-label">CPU</span>
            <div className="progress-bar">
              <div 
                className="progress-fill cpu" 
                style={{ width: `${systemStatus.cpuUsage}%` }}
              ></div>
            </div>
            <span className="resource-value">{systemStatus.cpuUsage.toFixed(1)}%</span>
          </div>
          <div className="resource-bar">
            <span className="resource-label">Memory</span>
            <div className="progress-bar">
              <div 
                className="progress-fill memory" 
                style={{ width: `${systemStatus.memoryUsage}%` }}
              ></div>
            </div>
            <span className="resource-value">{systemStatus.memoryUsage.toFixed(1)}%</span>
          </div>
          <div className="resource-bar">
            <span className="resource-label">Disk</span>
            <div className="progress-bar">
              <div 
                className="progress-fill disk" 
                style={{ width: `${systemStatus.diskUsage}%` }}
              ></div>
            </div>
            <span className="resource-value">{systemStatus.diskUsage.toFixed(1)}%</span>
          </div>
        </div>

        {/* System Info */}
        <div className="status-section system-info">
          <h4>System Info</h4>
          <div className="info-row">
            <span className="info-label">Version</span>
            <span className="info-value">{systemStatus.version}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Hash</span>
            <span className="info-value">{systemStatus.hash}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Uptime</span>
            <span className="info-value">{systemStatus.uptime}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

// Panel Component
interface PanelProps {
  title: string;
  children: React.ReactNode;
  icon?: string;
  className?: string;
}

const Panel: React.FC<PanelProps> = ({ title, children, icon, className = '' }) => {
  return (
    <div className={`dashboard-panel ${className}`}>
      <div className="panel-header">
        <div className="panel-title">
          {icon && <span className="panel-icon">{icon}</span>}
          {title}
        </div>
      </div>
      <div className="panel-content">
        {children}
      </div>
    </div>
  );
};

export const DashboardPanel: React.FC = () => {
  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>System Dashboard</h2>
        <p>Real-time monitoring of DAWN consciousness vitals, mood dynamics, and system performance</p>
      </div>

      <div className="dashboard-grid">
        {/* Row 1: Core Consciousness and System Status */}
        <div className="dashboard-row row-primary">
          <Panel title="Consciousness State" icon="🧠" className="consciousness-panel">
            <ConsciousnessDisplay />
          </Panel>
          
          <SystemStatusWidget />
        </div>

        {/* Row 2: Processing Monitors */}
        <div className="dashboard-row row-secondary">
          <Panel title="Tick Monitor" icon="⚡" className="tick-panel">
            <TickMonitorPanel />
          </Panel>
          
          <Panel title="Entropy Drift" icon="🌊" className="entropy-panel">
            <DriftGraphPanel />
          </Panel>
          
          <Panel title="Thought Rate" icon="💭" className="thought-panel">
            <ThoughtRateHeatmap />
          </Panel>
        </div>
      </div>
    </div>
  );
}; 