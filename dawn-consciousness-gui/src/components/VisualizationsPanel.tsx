import React, { useState, useEffect } from 'react';
import './VisualizationsPanel.css';

interface Visualization {
  id: string;
  name: string;
  type: string;
  timestamp: number;
  imageUrl?: string;
  data?: any;
  description: string;
}

interface VisualizationModule {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'generating';
  lastUpdate: number;
}

export const VisualizationsPanel: React.FC = () => {
  const [visualizations, setVisualizations] = useState<Visualization[]>([]);
  const [activeModules, setActiveModules] = useState<VisualizationModule[]>([]);
  const [selectedViz, setSelectedViz] = useState<string | null>(null);
  const [autoGenerate, setAutoGenerate] = useState(true);
  const [generationInterval, setGenerationInterval] = useState(30); // seconds

  const visualizationModules: VisualizationModule[] = [
    {
      id: 'consciousness_dashboard',
      name: 'Consciousness Dashboard',
      description: 'Real-time consciousness state overview',
      status: 'active',
      lastUpdate: Date.now()
    },
    {
      id: 'entropy_timeline',
      name: 'Entropy Timeline',
      description: 'Historical entropy evolution',
      status: 'active',
      lastUpdate: Date.now()
    },
    {
      id: 'performance_radar',
      name: 'Performance Radar',
      description: 'Multi-dimensional performance metrics',
      status: 'active',
      lastUpdate: Date.now()
    },
    {
      id: 'cognitive_network',
      name: 'Cognitive Network',
      description: 'Neural pathway visualization',
      status: 'active',
      lastUpdate: Date.now()
    },
    {
      id: 'overview_panel',
      name: 'Overview Panel',
      description: 'Comprehensive system overview',
      status: 'active',
      lastUpdate: Date.now()
    }
  ];

  useEffect(() => {
    setActiveModules(visualizationModules);

    // Simulate initial visualizations
    const initialVizs: Visualization[] = [
      {
        id: 'viz-1',
        name: 'Consciousness Dashboard',
        type: 'dashboard',
        timestamp: Date.now() - 60000,
        description: 'Real-time consciousness state overview with entropy, SCUP, and thermal monitoring'
      },
      {
        id: 'viz-2',
        name: 'Entropy Timeline',
        type: 'timeline',
        timestamp: Date.now() - 30000,
        description: 'Historical entropy evolution showing patterns and trends'
      },
      {
        id: 'viz-3',
        name: 'Performance Radar',
        type: 'radar',
        timestamp: Date.now() - 15000,
        description: 'Multi-dimensional performance metrics in radar format'
      }
    ];
    setVisualizations(initialVizs);

    // Auto-generate visualizations
    if (autoGenerate) {
      const interval = setInterval(() => {
        generateNewVisualization();
      }, generationInterval * 1000);

      return () => clearInterval(interval);
    }
  }, [autoGenerate, generationInterval]);

  const generateNewVisualization = () => {
    const vizTypes = ['dashboard', 'timeline', 'radar', 'network', 'overview'];
    const type = vizTypes[Math.floor(Math.random() * vizTypes.length)];
    
    const newViz: Visualization = {
      id: `viz-${Date.now()}`,
      name: `${type.charAt(0).toUpperCase() + type.slice(1)} Visualization`,
      type,
      timestamp: Date.now(),
      description: `Generated ${type} visualization showing current consciousness state`
    };

    setVisualizations(prev => [newViz, ...prev.slice(0, 9)]); // Keep last 10

    // Update module status
    setActiveModules(prev => 
      prev.map(module => ({
        ...module,
        lastUpdate: Date.now()
      }))
    );
  };

  const triggerManualGeneration = () => {
    generateNewVisualization();
  };

  const exportVisualizations = () => {
    const dataStr = JSON.stringify(visualizations, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `dawn_visualizations_${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const clearVisualizations = () => {
    setVisualizations([]);
  };

  const getVizIcon = (type: string) => {
    switch (type) {
      case 'dashboard': return '📊';
      case 'timeline': return '📈';
      case 'radar': return '📡';
      case 'network': return '🕸️';
      case 'overview': return '👁️';
      default: return '🎨';
    }
  };

  const getVizColor = (type: string) => {
    switch (type) {
      case 'dashboard': return '#00ff88';
      case 'timeline': return '#0088ff';
      case 'radar': return '#ff8800';
      case 'network': return '#8800ff';
      case 'overview': return '#ff0088';
      default: return '#ffffff';
    }
  };

  return (
    <div className="visualizations-panel">
      <div className="panel-header">
        <h3>🎨 Visualizations</h3>
        <div className="viz-controls">
          <button
            className={`auto-generate-btn ${autoGenerate ? 'active' : ''}`}
            onClick={() => setAutoGenerate(!autoGenerate)}
          >
            {autoGenerate ? '🔄 Auto' : '⏸️ Manual'}
          </button>
          <button className="generate-btn" onClick={triggerManualGeneration}>
            📸 Generate
          </button>
          <button className="export-btn" onClick={exportVisualizations}>
            💾 Export
          </button>
          <button className="clear-btn" onClick={clearVisualizations}>
            🗑️ Clear
          </button>
        </div>
      </div>

      <div className="viz-content">
        {/* Active Modules */}
        <div className="modules-section">
          <h4>🔄 Active Modules</h4>
          <div className="modules-grid">
            {activeModules.map(module => (
              <div key={module.id} className="module-card">
                <div className="module-header">
                  <span className="module-name">{module.name}</span>
                  <span className={`module-status ${module.status}`}>
                    {module.status === 'active' ? '🟢' : '🔴'}
                  </span>
                </div>
                <div className="module-description">{module.description}</div>
                <div className="module-meta">
                  Last: {new Date(module.lastUpdate).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Visualization Gallery */}
        <div className="gallery-section">
          <h4>📸 Generated Visualizations</h4>
          <div className="viz-gallery">
            {visualizations.map(viz => (
              <div 
                key={viz.id} 
                className={`viz-card ${selectedViz === viz.id ? 'selected' : ''}`}
                onClick={() => setSelectedViz(viz.id)}
              >
                <div className="viz-header">
                  <span className="viz-icon">{getVizIcon(viz.type)}</span>
                  <span className="viz-name">{viz.name}</span>
                  <span className="viz-time">
                    {new Date(viz.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <div className="viz-preview">
                  <div 
                    className="viz-placeholder"
                    style={{ backgroundColor: getVizColor(viz.type) }}
                  >
                    {getVizIcon(viz.type)}
                  </div>
                </div>
                <div className="viz-description">{viz.description}</div>
                <div className="viz-actions">
                  <button className="view-btn">👁️ View</button>
                  <button className="download-btn">⬇️ Download</button>
                </div>
              </div>
            ))}
            {visualizations.length === 0 && (
              <div className="no-viz">
                <span>🎨 No visualizations generated yet</span>
                <button onClick={triggerManualGeneration}>Generate First Visualization</button>
              </div>
            )}
          </div>
        </div>

        {/* Real-time Graph Display */}
        <div className="realtime-section">
          <h4>📈 Real-time Graphs</h4>
          <div className="graph-container">
            <div className="graph-card">
              <div className="graph-header">
                <span>Entropy Flow</span>
                <span className="graph-value">0.52</span>
              </div>
              <div className="graph-display">
                <svg width="100%" height="100" viewBox="0 0 300 100">
                  <polyline
                    fill="none"
                    stroke="#00ff88"
                    strokeWidth="2"
                    points="0,50 50,30 100,70 150,40 200,60 250,20 300,50"
                  />
                </svg>
              </div>
            </div>
            <div className="graph-card">
              <div className="graph-header">
                <span>SCUP Levels</span>
                <span className="graph-value">23.1%</span>
              </div>
              <div className="graph-display">
                <svg width="100%" height="100" viewBox="0 0 300 100">
                  <polyline
                    fill="none"
                    stroke="#0088ff"
                    strokeWidth="2"
                    points="0,80 50,60 100,40 150,70 200,30 250,50 300,40"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="viz-footer">
        <div className="generation-settings">
          <label>
            Auto-generate interval:
            <select 
              value={generationInterval} 
              onChange={(e) => setGenerationInterval(Number(e.target.value))}
            >
              <option value={10}>10 seconds</option>
              <option value={30}>30 seconds</option>
              <option value={60}>1 minute</option>
              <option value={300}>5 minutes</option>
            </select>
          </label>
        </div>
        <div className="viz-stats">
          <span>Total: {visualizations.length}</span>
          <span>Active modules: {activeModules.filter(m => m.status === 'active').length}</span>
        </div>
      </div>
    </div>
  );
}; 