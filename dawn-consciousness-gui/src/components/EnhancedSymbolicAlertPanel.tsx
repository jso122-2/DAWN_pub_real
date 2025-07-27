import React, { useState, useEffect, useRef, useCallback } from 'react';
import './SymbolicAlertPanel.css';

// Enhanced interfaces for the integrated system
interface SymbolicAlert {
  id: string;
  timestamp: number;
  datetime: string;
  type: string;
  tracer_type?: string;
  severity: string;
  message: string;
  data?: any;
  tick_id?: number;
  significance?: number;
}

interface TracerAlert {
  timestamp: number;
  datetime: string;
  tracer_type: string;
  severity: string;
  message: string;
  data: any;
  tick_id: number;
}

interface RootEvent {
  tick: number;
  type: string;
  symbolic_root: string;
  significance: number;
  timestamp: number;
  datetime: string;
}

interface EventStreamEntry {
  tick_id: number;
  timestamp: number;
  tracer_alerts: TracerAlert[];
  symbolic_roots: RootEvent[];
  memory_updates: any;
  runtime_state: any;
  status: string;
}

const EnhancedSymbolicAlertPanel: React.FC = () => {
  const [alerts, setAlerts] = useState<SymbolicAlert[]>([]);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [newAlertId, setNewAlertId] = useState<string | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<string>('disconnected');
  const [lastUpdate, setLastUpdate] = useState<number>(0);
  
  const intervalRef = useRef<number>();
  const filePositions = useRef({
    tracer_alerts: 0,
    root_trace: 0,
    event_stream: 0
  });

  // GUI Event Listener Setup
  useEffect(() => {
    // Listen for real-time symbolic alerts via window.emit
    const handleSymbolicAlert = (event: any) => {
      const alertData = event.payload || event.detail;
      processGuiEvent(alertData);
    };

    // Try to set up event listeners (Tauri or custom events)
    if (typeof window !== 'undefined') {
      // @ts-ignore - Tauri listen function
      if (window.__TAURI__?.event?.listen) {
        // @ts-ignore
        window.__TAURI__.event.listen('symbolic_alert', handleSymbolicAlert);
      } else if (window.addEventListener) {
        // Fallback to custom events
        window.addEventListener('symbolic_alert', handleSymbolicAlert);
      }
    }

    return () => {
      if (typeof window !== 'undefined' && window.removeEventListener) {
        window.removeEventListener('symbolic_alert', handleSymbolicAlert);
      }
    };
  }, []);

  const processGuiEvent = useCallback((eventData: any) => {
    try {
      let newAlert: SymbolicAlert;

      if (eventData.type === 'TRACER') {
        newAlert = {
          id: `gui_${Date.now()}_${Math.random()}`,
          timestamp: eventData.timestamp,
          datetime: new Date(eventData.timestamp * 1000).toISOString(),
          type: 'TRACER',
          tracer_type: eventData.tracer_type,
          severity: eventData.severity,
          message: eventData.message,
          tick_id: eventData.tick_id
        };
      } else if (eventData.type === 'ROOT') {
        newAlert = {
          id: `gui_${Date.now()}_${Math.random()}`,
          timestamp: eventData.timestamp,
          datetime: new Date(eventData.timestamp * 1000).toISOString(),
          type: 'ROOT',
          severity: 'important',
          message: `Symbolic root: ${eventData.symbolic_root}`,
          data: { 
            root_type: eventData.root_type,
            significance: eventData.significance
          },
          tick_id: eventData.tick_id,
          significance: eventData.significance
        };
      } else {
        return; // Unknown event type
      }

      addAlert(newAlert);
      setConnectionStatus('connected');
      setLastUpdate(Date.now());

    } catch (error) {
      console.error('Error processing GUI event:', error);
    }
  }, []);

  const startMonitoring = useCallback(() => {
    if (isMonitoring) return;
    
    setIsMonitoring(true);
    setConnectionStatus('connecting');
    
    // Start polling log files
    intervalRef.current = window.setInterval(() => {
      checkForNewAlerts();
    }, 2000); // Check every 2 seconds

    setConnectionStatus('polling');
  }, [isMonitoring]);

  const stopMonitoring = useCallback(() => {
    setIsMonitoring(false);
    setConnectionStatus('disconnected');
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  }, []);

  const checkForNewAlerts = async () => {
    try {
      // Check tracer alerts
      await checkTracerAlerts();
      
      // Check root trace
      await checkRootTrace();
      
      // Check event stream
      await checkEventStream();
      
      setLastUpdate(Date.now());
      
    } catch (error) {
      console.error('Error checking alerts:', error);
      setConnectionStatus('error');
    }
  };

  const checkTracerAlerts = async () => {
    try {
      const response = await fetch('/api/logs/tracer_alerts');
      if (!response.ok) return;
      
      const text = await response.text();
      const lines = text.split('\n').filter(line => line.trim());
      
      // Process new lines since last check
      const newLines = lines.slice(filePositions.current.tracer_alerts);
      filePositions.current.tracer_alerts = lines.length;
      
      for (const line of newLines) {
        try {
          const tracerAlert: TracerAlert = JSON.parse(line);
          processTracerAlert(tracerAlert);
        } catch (e) {
          // Skip invalid JSON lines
        }
      }
    } catch (error) {
      // Log file may not exist yet
    }
  };

  const checkRootTrace = async () => {
    try {
      const response = await fetch('/api/logs/root_trace');
      if (!response.ok) return;
      
      const text = await response.text();
      const lines = text.split('\n').filter(line => line.trim());
      
      const newLines = lines.slice(filePositions.current.root_trace);
      filePositions.current.root_trace = lines.length;
      
      for (const line of newLines) {
        try {
          const rootEvent: RootEvent = JSON.parse(line);
          processRootEvent(rootEvent);
        } catch (e) {
          // Skip invalid JSON lines
        }
      }
    } catch (error) {
      // Log file may not exist yet
    }
  };

  const checkEventStream = async () => {
    try {
      const response = await fetch('/api/logs/event_stream');
      if (!response.ok) return;
      
      const text = await response.text();
      const lines = text.split('\n').filter(line => line.trim());
      
      const newLines = lines.slice(filePositions.current.event_stream);
      filePositions.current.event_stream = lines.length;
      
      for (const line of newLines) {
        try {
          const eventEntry: EventStreamEntry = JSON.parse(line);
          processEventStreamEntry(eventEntry);
        } catch (e) {
          // Skip invalid JSON lines
        }
      }
    } catch (error) {
      // Log file may not exist yet
    }
  };

  const processTracerAlert = (tracerAlert: TracerAlert) => {
    const alert: SymbolicAlert = {
      id: `tracer_${tracerAlert.tick_id}_${tracerAlert.timestamp}`,
      timestamp: tracerAlert.timestamp,
      datetime: tracerAlert.datetime,
      type: 'TRACER',
      tracer_type: tracerAlert.tracer_type,
      severity: tracerAlert.severity,
      message: tracerAlert.message,
      data: tracerAlert.data,
      tick_id: tracerAlert.tick_id
    };
    
    addAlert(alert);
  };

  const processRootEvent = (rootEvent: RootEvent) => {
    const alert: SymbolicAlert = {
      id: `root_${rootEvent.tick}_${rootEvent.timestamp}`,
      timestamp: rootEvent.timestamp,
      datetime: rootEvent.datetime,
      type: 'ROOT',
      severity: 'important',
      message: `${rootEvent.type}: ${rootEvent.symbolic_root}`,
      data: { 
        root_type: rootEvent.type,
        significance: rootEvent.significance
      },
      tick_id: rootEvent.tick,
      significance: rootEvent.significance
    };
    
    addAlert(alert);
  };

  const processEventStreamEntry = (eventEntry: EventStreamEntry) => {
    // Process tracer alerts from event stream
    for (const tracerAlert of eventEntry.tracer_alerts || []) {
      processTracerAlert(tracerAlert);
    }
    
    // Process symbolic roots from event stream
    for (const rootEvent of eventEntry.symbolic_roots || []) {
      processRootEvent(rootEvent);
    }
  };

  const addAlert = (alert: SymbolicAlert) => {
    setAlerts(prev => {
      // Check for duplicates
      const isDuplicate = prev.some(existing => existing.id === alert.id);
      if (isDuplicate) return prev;
      
      // Add new alert and keep last 50
      const updated = [alert, ...prev].slice(0, 50);
      return updated;
    });
    
    // Flash animation for new alerts
    setNewAlertId(alert.id);
    setTimeout(() => setNewAlertId(null), 2000);
  };

  const filteredAlerts = alerts.filter(alert => {
    if (filterType === 'ALL') return true;
    
    if (filterType === 'ROOT' && alert.type === 'ROOT') return true;
    if (filterType === 'TRACER' && alert.type === 'TRACER') return true;
    
    // Filter by specific tracer types
    if (alert.tracer_type && alert.tracer_type.toUpperCase() === filterType) return true;
    
    return false;
  });

  const getSeverityClass = (severity: string): string => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'severity-critical';
      case 'warning': return 'severity-warning';
      case 'important': return 'severity-important';
      default: return 'severity-info';
    }
  };

  const getTypeColor = (type: string): string => {
    if (type === 'ROOT') return '#9C27B0'; // Purple for symbolic roots
    
    switch (type.toLowerCase()) {
      case 'owl': return '#2196F3'; // Blue
      case 'drift': return '#FF9800'; // Orange  
      case 'thermal': return '#F44336'; // Red
      case 'forecast': return '#9C27B0'; // Purple
      default: return '#607D8B'; // Blue Grey
    }
  };

  const formatTimestamp = (timestamp: number): string => {
    return new Date(timestamp * 1000).toLocaleTimeString();
  };

  const clearAlerts = () => {
    setAlerts([]);
    setNewAlertId(null);
  };

  const getConnectionStatusClass = (): string => {
    switch (connectionStatus) {
      case 'connected': return 'status-connected';
      case 'connecting': case 'polling': return 'status-connecting';
      case 'error': return 'status-error';
      default: return 'status-disconnected';
    }
  };

  // Auto-start monitoring on component mount
  useEffect(() => {
    startMonitoring();
    
    return () => {
      stopMonitoring();
    };
  }, [startMonitoring, stopMonitoring]);

  return (
    <div className="symbolic-alert-panel enhanced">
      <div className="alert-panel-header">
        <h3>🧠 Enhanced Symbolic Cognition Alerts</h3>
        <div className="alert-controls">
          <select
            value={filterType}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setFilterType(e.target.value)}
            className="filter-select"
          >
            <option value="ALL">All Events</option>
            <option value="TRACER">🔍 All Tracers</option>
            <option value="OWL">🦉 Owl Cognitive</option>
            <option value="DRIFT">🌊 Drift Detection</option>
            <option value="THERMAL">🌡️ Thermal State</option>
            <option value="FORECAST">🔮 Forecast Analysis</option>
            <option value="ROOT">✨ Symbolic Roots</option>
          </select>
          
          <button
            className={`control-button ${isMonitoring ? 'monitoring' : 'paused'}`}
            onClick={() => isMonitoring ? stopMonitoring() : startMonitoring()}
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
        <span className={`stat-tag ${getConnectionStatusClass()}`}>
          {connectionStatus.toUpperCase()}
        </span>
        {lastUpdate > 0 && (
          <span className="stat-tag">
            Updated: {new Date(lastUpdate).toLocaleTimeString()}
          </span>
        )}
      </div>
      
      <div className="alert-list">
        {filteredAlerts.length === 0 ? (
          <div className="no-alerts">
            {isMonitoring ? (
              <div>
                <div>🧠 Monitoring symbolic cognition events...</div>
                <div className="monitoring-status">
                  Connection: {connectionStatus} | 
                  Real-time GUI events: {typeof window !== 'undefined' && window.__TAURI__ ? 'enabled' : 'fallback'}
                </div>
              </div>
            ) : (
              '⏸️ Monitoring paused'
            )}
          </div>
        ) : (
          filteredAlerts.map(alert => (
            <div
              key={alert.id}
              className={`alert-item ${alert.severity} ${newAlertId === alert.id ? 'flash' : ''}`}
              style={{
                borderLeft: `4px solid ${getTypeColor(alert.tracer_type || alert.type)}`,
                backgroundColor: newAlertId === alert.id ? 'rgba(79, 171, 247, 0.1)' : undefined
              }}
            >
              <div className="alert-header">
                <span className={`severity-tag ${getSeverityClass(alert.severity)}`}>
                  {alert.severity.toUpperCase()}
                </span>
                <span className="alert-type">
                  {alert.type === 'ROOT' ? '✨ ROOT' : `🔍 ${(alert.tracer_type || 'TRACER').toUpperCase()}`}
                </span>
                <span className="alert-time">{formatTimestamp(alert.timestamp)}</span>
                {alert.tick_id && (
                  <span className="alert-tick">Tick {alert.tick_id}</span>
                )}
                {alert.significance && (
                  <span className="alert-significance">
                    Sig: {(alert.significance * 100).toFixed(0)}%
                  </span>
                )}
              </div>
              <div className="alert-message">{alert.message}</div>
              {alert.data && Object.keys(alert.data).length > 0 && (
                <div className="alert-data">
                  <pre>{JSON.stringify(alert.data, null, 2)}</pre>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EnhancedSymbolicAlertPanel; 