import React, { useState, useEffect, useRef } from 'react';
import './SymbolicAlertPanel.css';

interface SymbolicAlert {
  id: string;
  timestamp: number;
  datetime: string;
  type: 'owl' | 'drift' | 'thermal' | 'forecast' | 'root' | 'mycelium' | 'rhizome';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  data?: any;
  tick_id?: number;
}

interface RootEvent {
  tick: number;
  type: string;
  symbolic_root: string;
  significance: number;
  branch: string[];
}

const SymbolicAlertPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<SymbolicAlert[]>([]);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [newAlertId, setNewAlertId] = useState<string | null>(null);
  const intervalRef = useRef<number>();
  const filePositions = useRef({
    event_stream: 0,
    root_trace: 0,
    tracer_alerts: 0
  });

  // Start/stop monitoring
  useEffect(() => {
    if (isMonitoring) {
      startMonitoring();
    } else {
      stopMonitoring();
    }
    
    return () => stopMonitoring();
  }, [isMonitoring]);

  const startMonitoring = () => {
    // Poll for new alerts every 2 seconds
    intervalRef.current = setInterval(async () => {
      await checkForNewAlerts();
    }, 2000);
  };

  const stopMonitoring = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  const checkForNewAlerts = async () => {
    try {
      // Check event stream log
      await checkEventStream();
      
      // Check root trace log
      await checkRootTrace();
      
      // Check tracer alerts log
      await checkTracerAlerts();
      
    } catch (error) {
      console.error('Error checking for alerts:', error);
    }
  };

  const checkEventStream = async () => {
    try {
      const response = await fetch('/api/logs/event_stream');
      if (response.ok) {
        const lines = await response.text();
        const newLines = lines.split('\n').slice(filePositions.current.event_stream);
        
        for (const line of newLines) {
          if (line.trim()) {
            try {
              const event = JSON.parse(line);
              processEventStreamEntry(event);
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
        
        filePositions.current.event_stream += newLines.length;
      }
    } catch (error) {
      // File might not exist yet
    }
  };

  const checkRootTrace = async () => {
    try {
      const response = await fetch('/api/logs/root_trace');
      if (response.ok) {
        const lines = await response.text();
        const newLines = lines.split('\n').slice(filePositions.current.root_trace);
        
        for (const line of newLines) {
          if (line.trim()) {
            try {
              const rootEvent: RootEvent = JSON.parse(line);
              processRootEvent(rootEvent);
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
        
        filePositions.current.root_trace += newLines.length;
      }
    } catch (error) {
      // File might not exist yet
    }
  };

  const checkTracerAlerts = async () => {
    try {
      const response = await fetch('/api/logs/tracer_alerts');
      if (response.ok) {
        const lines = await response.text();
        const newLines = lines.split('\n').slice(filePositions.current.tracer_alerts);
        
        for (const line of newLines) {
          if (line.trim()) {
            try {
              const tracerAlert = JSON.parse(line);
              processTracerAlert(tracerAlert);
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
        
        filePositions.current.tracer_alerts += newLines.length;
      }
    } catch (error) {
      // File might not exist yet
    }
  };

  const processEventStreamEntry = (event: any) => {
    const observations = event.observations || {};
    
    // Process memory updates
    const memoryUpdates = observations.memory_updates || {};
    for (const [updateType, data] of Object.entries(memoryUpdates)) {
      if (updateType === 'mycelium_growth' && data && typeof data === 'object') {
        const growthData = data as any;
        if (growthData.nutrients > 0.1) {
          addAlert({
            type: 'mycelium',
            severity: 'info',
            message: `Network growth: new root with ${growthData.nutrients.toFixed(2)} nutrient flow`,
            data: growthData,
            tick_id: event.tick_id
          });
        }
      }
    }
    
    // Process forecast adjustments
    const forecastAdjustments = observations.forecast_adjustments || [];
    for (const adjustment of forecastAdjustments) {
      if (['STABILITY_INCREASE', 'UNCERTAINTY_INCREASE'].includes(adjustment.type)) {
        addAlert({
          type: 'forecast',
          severity: 'warning',
          message: `Forecast: ${adjustment.reason}`,
          data: adjustment,
          tick_id: event.tick_id
        });
      }
    }
  };

  const processRootEvent = (rootEvent: RootEvent) => {
    const significance = rootEvent.significance || 0.5;
    
    // Only show significant root events
    if (significance < 0.6) return;
    
    let alertType: SymbolicAlert['type'] = 'root';
    let message = '';
    
    switch (rootEvent.type) {
      case 'MYCELIUM_EXPANSION':
        alertType = 'mycelium';
        message = `🌿 ROOT: Network expansion - ${rootEvent.symbolic_root}`;
        break;
      case 'RHIZOME_CLUSTER':
        alertType = 'rhizome';
        message = `🕸️ ROOT: Cluster formed - ${rootEvent.symbolic_root}`;
        break;
      case 'LINEAGE_MILESTONE':
        alertType = 'root';
        message = `🌳 ROOT: Memory milestone - ${rootEvent.symbolic_root}`;
        break;
      case 'COGNITIVE_EMERGENCE':
        alertType = 'root';
        message = `🧠 ROOT: Cognitive emergence - ${rootEvent.symbolic_root}`;
        break;
      default:
        message = `✨ ROOT: Symbolic pattern - ${rootEvent.symbolic_root}`;
    }
    
    addAlert({
      type: alertType,
      severity: significance > 0.8 ? 'critical' : 'warning',
      message,
      data: rootEvent,
      tick_id: rootEvent.tick
    });
  };

  const processTracerAlert = (tracerAlert: any) => {
    const tracerType = tracerAlert.tracer_type || 'unknown';
    const severity = tracerAlert.severity || 'info';
    const message = tracerAlert.message || '';
    const data = tracerAlert.data || {};
    
    let displayMessage = '';
    let alertType: SymbolicAlert['type'] = 'owl';
    
    switch (tracerType) {
      case 'owl':
        alertType = 'owl';
        displayMessage = `🦉 OWL: ${message}`;
        break;
      case 'drift':
        alertType = 'drift';
        const driftType = data.drift_type || 'unknown';
        const magnitude = data.magnitude || 0;
        displayMessage = `🌊 DRIFT: ${driftType} deviation ${magnitude.toFixed(2)}`;
        break;
      case 'thermal':
        alertType = 'thermal';
        displayMessage = `🌡️ THERMAL: ${message}`;
        break;
      case 'forecast':
        alertType = 'forecast';
        displayMessage = `🔮 FORECAST: ${message}`;
        break;
      default:
        displayMessage = `⚡ ${tracerType.toUpperCase()}: ${message}`;
    }
    
    addAlert({
      type: alertType,
      severity: severity as SymbolicAlert['severity'],
      message: displayMessage,
      data,
      tick_id: tracerAlert.tick_id
    });
  };

  const addAlert = (alertData: Omit<SymbolicAlert, 'id' | 'timestamp' | 'datetime'>) => {
    const now = Date.now();
    const alert: SymbolicAlert = {
      id: `alert_${now}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: now,
      datetime: new Date().toISOString(),
      ...alertData
    };
    
    setAlerts(prev => {
      const updated = [alert, ...prev].slice(0, 50); // Keep only last 50
      return updated;
    });
    
    // Flash effect for new alert
    setNewAlertId(alert.id);
    setTimeout(() => setNewAlertId(null), 2000);
  };

  const filteredAlerts = alerts.filter(alert => 
    filterType === 'ALL' || alert.type.toUpperCase() === filterType
  );

  const getSeverityClass = (severity: string): string => {
    switch (severity) {
      case 'critical': return 'severity-critical';
      case 'warning': return 'severity-warning';
      case 'info': return 'severity-info';
      default: return 'severity-default';
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'critical': return '#ff6b6b';
      case 'warning': return '#ffa500';
      case 'info': return '#4dabf7';
      default: return '#adb5bd';
    }
  };

  const getTypeColor = (type: string): string => {
    switch (type) {
      case 'owl': return '#845ec2';
      case 'drift': return '#4dabf7';
      case 'thermal': return '#ff6b6b';
      case 'forecast': return '#ffa500';
      case 'root': return '#51cf66';
      case 'mycelium': return '#69db7c';
      case 'rhizome': return '#40c057';
      default: return '#adb5bd';
    }
  };

  const formatTimestamp = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  };

  const clearAlerts = () => {
    setAlerts([]);
  };

  return (
    <div className="symbolic-alert-panel">
      <div className="alert-panel-header">
        <h3>🧠 Symbolic Cognition Alerts</h3>
        <div className="alert-controls">
          <select
            value={filterType}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFilterType(e.target.value)}
            className="filter-select"
          >
            <option value="ALL">All Tracers</option>
            <option value="OWL">🦉 Owl</option>
            <option value="DRIFT">🌊 Drift</option>
            <option value="THERMAL">🌡️ Thermal</option>
            <option value="FORECAST">🔮 Forecast</option>
            <option value="ROOT">✨ Symbolic Roots</option>
            <option value="MYCELIUM">🌿 Mycelium</option>
            <option value="RHIZOME">🕸️ Rhizome</option>
          </select>
          
          <button
            className={`control-button ${isMonitoring ? 'monitoring' : 'paused'}`}
            onClick={() => setIsMonitoring(!isMonitoring)}
          >
            {isMonitoring ? '⏸️ Pause' : '▶️ Monitor'}
          </button>
          
          <button
            className="control-button clear-button"
            onClick={clearAlerts}
          >
            🗑️ Clear
          </button>
        </div>
      </div>
      
      <div className="alert-stats">
        <span className="stat-tag">Total: {alerts.length}</span>
        <span className="stat-tag">Filtered: {filteredAlerts.length}</span>
        <span className={`stat-tag ${isMonitoring ? 'monitoring' : 'paused'}`}>
          {isMonitoring ? 'MONITORING' : 'PAUSED'}
        </span>
      </div>
      
      <div className="alert-list">
        {filteredAlerts.length === 0 ? (
          <div className="no-alerts">
            {isMonitoring ? '🧠 Monitoring for symbolic events...' : '⏸️ Monitoring paused'}
          </div>
        ) : (
          filteredAlerts.map(alert => (
            <div
              key={alert.id}
              className={`alert-item ${alert.severity} ${newAlertId === alert.id ? 'flash' : ''}`}
              style={{
                borderLeft: `4px solid ${getTypeColor(alert.type)}`,
                backgroundColor: newAlertId === alert.id ? 'rgba(79, 171, 247, 0.1)' : undefined
              }}
            >
              <div className="alert-header">
                <span className={`severity-tag ${getSeverityClass(alert.severity)}`}>
                  {alert.severity.toUpperCase()}
                </span>
                <span className="alert-time">{formatTimestamp(alert.timestamp)}</span>
                {alert.tick_id && (
                  <span className="alert-tick">Tick {alert.tick_id}</span>
                )}
              </div>
              <div className="alert-message">{alert.message}</div>
              {alert.data && Object.keys(alert.data).length > 0 && (
                <div className="alert-data">
                  {JSON.stringify(alert.data, null, 2)}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SymbolicAlertPanel; 