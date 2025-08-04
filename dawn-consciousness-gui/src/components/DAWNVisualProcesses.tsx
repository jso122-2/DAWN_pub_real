import React, { useState, useEffect, useRef } from 'react';
import './DAWNVisualProcesses.css';

interface VisualizationData {
  tick_number: number;
  scup: number;
  entropy: number;
  heat: number;
  zone: string;
  mood: string;
  active_sigils: string[];
  rebloom_count: number;
  tracer_alerts: string[];
  timestamp: number;
}

interface VisualModule {
  id: string;
  name: string;
  description: string;
  type: string;
}

interface DAWNVisualProcessesProps {
  className?: string;
}

export const DAWNVisualProcesses: React.FC<DAWNVisualProcessesProps> = ({ className = '' }) => {
  const [visualData, setVisualData] = useState<VisualizationData | null>(null);
  const [availableModules, setAvailableModules] = useState<Record<string, VisualModule>>({});
  const [selectedModule, setSelectedModule] = useState<string>('tick_pulse');
  const [visualizationOutput, setVisualizationOutput] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('connecting');
  const [autoUpdate, setAutoUpdate] = useState(true);
  const intervalRef = useRef<number | null>(null);

  const API_BASE_URL = 'http://localhost:5001/api/visual';

  // Fetch status and initialize
  useEffect(() => {
    checkStatus();
    fetchModules();
  }, []);

  // Auto-refresh data
  useEffect(() => {
    if (autoUpdate && status === 'connected') {
      intervalRef.current = setInterval(() => {
        fetchVisualData();
      }, 2000);

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [autoUpdate, status]);

  const checkStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/status`);
      if (response.ok) {
        const data = await response.json();
        setStatus(data.status);
        if (data.status === 'connected') {
          fetchVisualData();
        }
      } else {
        setStatus('error');
        setError('Failed to connect to visual API');
      }
    } catch (err) {
      setStatus('error');
      setError('Cannot connect to visual API server');
    }
  };

  const fetchModules = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/modules`);
      if (response.ok) {
        const modules = await response.json();
        setAvailableModules(modules);
      }
    } catch (err) {
      console.error('Failed to fetch modules:', err);
    }
  };

  const fetchVisualData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/data`);
      if (response.ok) {
        const data = await response.json();
        setVisualData(data);
        
        // Auto-generate visualization for selected module
        if (selectedModule) {
          generateVisualization(selectedModule);
        }
      }
    } catch (err) {
      console.error('Failed to fetch visual data:', err);
    }
  };

  const generateVisualization = async (moduleId: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/generate/${moduleId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          setVisualizationOutput(result.visualization);
        } else {
          setError(result.error || 'Failed to generate visualization');
        }
      } else {
        setError('Failed to generate visualization');
      }
    } catch (err) {
      setError(`Failed to generate visualization: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  const handleModuleSelect = (moduleId: string) => {
    setSelectedModule(moduleId);
    generateVisualization(moduleId);
  };

  const handleRefresh = () => {
    fetchVisualData();
    if (selectedModule) {
      generateVisualization(selectedModule);
    }
  };

  return (
    <div className={`dawn-visual-processes ${className}`}>
      <div className="visual-header">
        <h2>🌅 DAWN Visual Processes</h2>
        <div className="status-indicator">
          <span className={`status-dot ${status}`}></span>
          <span className="status-text">
            {status === 'connected' ? 'Connected' : 
             status === 'demo' ? 'Demo Mode' : 
             status === 'error' ? 'Error' : 'Connecting...'}
          </span>
        </div>
      </div>

      <div className="visual-controls">
        <div className="control-group">
          <label>Auto Update:</label>
          <input
            type="checkbox"
            checked={autoUpdate}
            onChange={(e) => setAutoUpdate(e.target.checked)}
          />
        </div>
        
        <div className="control-group">
          <label>Module:</label>
          <select
            value={selectedModule}
            onChange={(e) => handleModuleSelect(e.target.value)}
            disabled={Object.keys(availableModules).length === 0}
          >
            {Object.entries(availableModules).map(([id, module]) => (
              <option key={id} value={id}>
                📊 {module.name}
              </option>
            ))}
          </select>
        </div>

        <button
          className="refresh-btn"
          onClick={handleRefresh}
          disabled={loading || status !== 'connected'}
        >
          {loading ? 'Generating...' : '🔄 Refresh'}
        </button>
      </div>

      <div className="visual-content">
        <div className="metrics-panel">
          <h3>📊 Consciousness Metrics</h3>
          {visualData ? (
            <div className="metrics-grid">
              <div className="metric">
                <span className="metric-label">🔄 Tick:</span>
                <span className="metric-value">{visualData.tick_number}</span>
              </div>
              <div className="metric">
                <span className="metric-label">📊 SCUP:</span>
                <span className="metric-value">{visualData.scup.toFixed(3)}</span>
              </div>
              <div className="metric">
                <span className="metric-label">⚡ Entropy:</span>
                <span className="metric-value">{visualData.entropy.toFixed(3)}</span>
              </div>
              <div className="metric">
                <span className="metric-label">🌡️ Heat:</span>
                <span className="metric-value">{visualData.heat.toFixed(1)}°C</span>
              </div>
              <div className="metric">
                <span className="metric-label">🎯 Zone:</span>
                <span className="metric-value">{visualData.zone}</span>
              </div>
              <div className="metric">
                <span className="metric-label">😊 Mood:</span>
                <span className="metric-value">{visualData.mood}</span>
              </div>
              <div className="metric">
                <span className="metric-label">🔮 Sigils:</span>
                <span className="metric-value">{visualData.active_sigils.length} active</span>
              </div>
              <div className="metric">
                <span className="metric-label">🌸 Rebloom:</span>
                <span className="metric-value">{visualData.rebloom_count}</span>
              </div>
              <div className="metric">
                <span className="metric-label">⚡ Alerts:</span>
                <span className="metric-value">{visualData.tracer_alerts.length} alerts</span>
              </div>
            </div>
          ) : (
            <div className="no-data">
              {status === 'error' ? 'Cannot connect to visual API' : 'No visual data available'}
            </div>
          )}
        </div>

        <div className="visualization-panel">
          <h3>🎨 Visualization Output</h3>
          {error && (
            <div className="error-message">
              ❌ {error}
            </div>
          )}
          
          {visualizationOutput ? (
            <pre className="visualization-output">{visualizationOutput}</pre>
          ) : (
            <div className="no-visualization">
              <p>Select a module and click "Refresh" to see real-time consciousness data.</p>
              {status === 'demo' && (
                <p>⚠️ Running in demo mode with synthetic data.</p>
              )}
              {status === 'error' && (
                <p>❌ Make sure the visual API server is running on port 5001.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}; 