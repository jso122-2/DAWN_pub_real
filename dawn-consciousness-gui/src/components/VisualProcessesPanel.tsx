import React, { useState, useEffect, useRef } from 'react';
import './VisualProcessesPanel.css';

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

interface VisualProcessesPanelProps {
  tickData?: any;
  isActive?: boolean;
}

// Simulate the Python visual integration
const simulateVisualIntegration = async (data: any): Promise<VisualizationData> => {
  // Simulate the Python visual integration response
  return {
    tick_number: data?.tick_number || Math.floor(Date.now() / 1000) % 1000,
    scup: data?.scup || 0.5 + 0.3 * Math.sin(Date.now() * 0.001),
    entropy: data?.entropy || 0.4 + 0.4 * Math.sin(Date.now() * 0.0008),
    heat: data?.heat || 25.0 + 10.0 * Math.sin(Date.now() * 0.0005),
    zone: data?.zone || ['CALM', 'STABLE', 'OSCILLATING', 'TRENDING'][Math.floor(Date.now() / 2000) % 4],
    mood: data?.mood || ['serene', 'focused', 'curious', 'contemplative'][Math.floor(Date.now() / 3000) % 4],
    active_sigils: data?.active_sigils || (Math.floor(Date.now() / 3000) % 3 === 0 ? ['attention', 'memory'] : []),
    rebloom_count: data?.rebloom_count || Math.floor(Date.now() / 2000) % 5,
    tracer_alerts: data?.tracer_alerts || (Math.floor(Date.now() / 10000) % 10 === 0 ? ['pressure_warning'] : []),
    timestamp: Date.now()
  };
};

// Available visual modules
const AVAILABLE_MODULES: VisualModule[] = [
  {
    id: 'tick_pulse',
    name: 'Tick Pulse',
    description: 'Real-time cognitive heartbeat visualization',
    type: 'real-time'
  },
  {
    id: 'consciousness_constellation',
    name: 'Consciousness Constellation',
    description: '3D SCUP trajectory visualization',
    type: 'real-time'
  },
  {
    id: 'heat_monitor',
    name: 'Heat Monitor',
    description: 'Cognitive heat intensity gauge',
    type: 'real-time'
  },
  {
    id: 'dawn_mood_state',
    name: 'Mood State',
    description: 'Emotional landscape heatmap',
    type: 'real-time'
  },
  {
    id: 'SCUP_pressure_grid',
    name: 'SCUP Pressure Grid',
    description: 'Cognitive pressure interaction matrix',
    type: 'real-time'
  },
  {
    id: 'entropy_flow',
    name: 'Entropy Flow',
    description: 'Information entropy dynamics',
    type: 'real-time'
  },
  {
    id: 'scup_zone_animator',
    name: 'SCUP Zone Animator',
    description: 'Cognitive zone transition visualization',
    type: 'real-time'
  },
  {
    id: 'sigil_command_stream',
    name: 'Sigil Command Stream',
    description: 'Command processing visualization',
    type: 'real-time'
  }
];

// Generate text-based visualizations
const generateTextVisualization = (moduleId: string, data: VisualizationData): string => {
  const currentTime = Date.now();
  const timestamp = new Date(currentTime).toLocaleTimeString();
  
  switch (moduleId) {
    case 'tick_pulse':
      return `
🔄 TICK PULSE VISUALIZATION
==========================
Time: ${timestamp}
Module: Tick Pulse
Description: Real-time cognitive heartbeat visualization

Current State:
  Tick Number: ${data.tick_number}
  SCUP: ${data.scup.toFixed(3)}
  Entropy: ${data.entropy.toFixed(3)}
  Heat: ${data.heat.toFixed(1)}°C
  Zone: ${data.zone}
  Mood: ${data.mood}

Pulse Analysis:
  Amplitude: ${(0.5 + 0.3 * Math.sin(currentTime * 0.001)).toFixed(2)}
  Frequency: ${(0.1 + 0.05 * Math.sin(currentTime * 0.0005)).toFixed(3)} Hz
  Phase: ${(currentTime * 0.001).toFixed(1)} rad

Visual Representation:
${'█'.repeat(Math.floor(10 + 5 * Math.sin(currentTime * 0.001)))}
${'░'.repeat(20 - Math.floor(10 + 5 * Math.sin(currentTime * 0.001)))}
`;

    case 'consciousness_constellation':
      return `
🌌 CONSCIOUSNESS CONSTELLATION
==============================
Time: ${timestamp}
Module: Consciousness Constellation
Description: 3D SCUP trajectory visualization

SCUP Space Coordinates:
  Schema: ${data.scup.toFixed(3)}
  Coherence: ${data.entropy.toFixed(3)}
  Utility: ${(1.0 - data.entropy).toFixed(3)}

Current Position:
  Zone: ${data.zone}
  Mood: ${data.mood}
  Heat: ${data.heat.toFixed(1)}°C

Constellation Map:
    🌟 Dormant (0.0-0.2)
       |
    🌟 Contemplative (0.2-0.4)
       |
    🌟 Active (0.4-0.6) ← Current
       |
    🌟 Intense (0.6-0.8)
       |
    🌟 Transcendent (0.8-1.0)

Trajectory: ${['↗', '→', '↘', '↙', '←', '↖'][Math.floor(currentTime / 1000) % 6]}
`;

    case 'heat_monitor':
      const heatNormalized = Math.max(0.0, Math.min(1.0, (data.heat - 20.0) / 30.0));
      return `
🌡️ HEAT MONITOR VISUALIZATION
=============================
Time: ${timestamp}
Module: Heat Monitor
Description: Cognitive heat intensity gauge

Current Heat: ${data.heat.toFixed(1)}°C
Heat Level: ${heatNormalized.toFixed(1)} (0.0-1.0)

Heat Zones:
  Dormant (20-25°C): ${'█'.repeat(Math.floor(5 * (1.0 - heatNormalized)))}${'░'.repeat(Math.floor(5 * heatNormalized))}
  Warming (25-30°C): ${'█'.repeat(Math.floor(5 * Math.max(0, heatNormalized - 0.2)))}${'░'.repeat(Math.floor(5 * (1.0 - Math.max(0, heatNormalized - 0.2))))}
  Active (30-35°C): ${'█'.repeat(Math.floor(5 * Math.max(0, heatNormalized - 0.4)))}${'░'.repeat(Math.floor(5 * (1.0 - Math.max(0, heatNormalized - 0.4))))}
  Intense (35-40°C): ${'█'.repeat(Math.floor(5 * Math.max(0, heatNormalized - 0.6)))}${'░'.repeat(Math.floor(5 * (1.0 - Math.max(0, heatNormalized - 0.6))))}
  Critical (40-50°C): ${'█'.repeat(Math.floor(5 * Math.max(0, heatNormalized - 0.8)))}${'░'.repeat(Math.floor(5 * (1.0 - Math.max(0, heatNormalized - 0.8))))}

Current Zone: ${['Dormant', 'Warming', 'Active', 'Intense', 'Critical'][Math.min(4, Math.floor(heatNormalized * 5))]}
`;

    case 'dawn_mood_state':
      return `
😊 MOOD STATE VISUALIZATION
===========================
Time: ${timestamp}
Module: Mood State
Description: Emotional landscape heatmap

Current Mood: ${data.mood}
Zone: ${data.zone}

Emotional Landscape:
  Transcendent: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 0)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 0)))}
  Ecstatic: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 1)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 1)))}
  Serene: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 2)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 2)))}
  Curious: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 3)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 3)))}
  Focused: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 4)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 4)))}
  Contemplative: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 5)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 5)))}
  Uncertain: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 6)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 6)))}
  Turbulent: ${'█'.repeat(Math.floor(3 * Math.sin(currentTime * 0.001 + 7)))}${'░'.repeat(10 - Math.floor(3 * Math.sin(currentTime * 0.001 + 7)))}
`;

    default:
      return `
📊 ${moduleId.toUpperCase().replace('_', ' ')} VISUALIZATION
${'='.repeat(moduleId.length + 15)}
Time: ${timestamp}
Module: ${AVAILABLE_MODULES.find(m => m.id === moduleId)?.name || moduleId}
Description: ${AVAILABLE_MODULES.find(m => m.id === moduleId)?.description || 'Visualization module'}

Current Data:
  Tick: ${data.tick_number}
  SCUP: ${data.scup.toFixed(3)}
  Entropy: ${data.entropy.toFixed(3)}
  Heat: ${data.heat.toFixed(1)}°C
  Zone: ${data.zone}
  Mood: ${data.mood}
  Active Sigils: ${data.active_sigils.length}
  Rebloom Count: ${data.rebloom_count}
  Tracer Alerts: ${data.tracer_alerts.length}

Status: Active and monitoring
`;
  }
};

export const VisualProcessesPanel: React.FC<VisualProcessesPanelProps> = ({
  tickData,
  isActive = true
}) => {
  const [visualData, setVisualData] = useState<VisualizationData | null>(null);
  const [selectedModule, setSelectedModule] = useState<string>('tick_pulse');
  const [visualizationOutput, setVisualizationOutput] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [autoUpdate, setAutoUpdate] = useState(true);
  const intervalRef = useRef<number | null>(null);

  // Update visual data when tick data changes
  useEffect(() => {
    if (tickData && isActive && autoUpdate) {
      updateVisualData(tickData);
    }
  }, [tickData, isActive, autoUpdate]);

  // Auto-refresh interval
  useEffect(() => {
    if (autoUpdate && isActive) {
      intervalRef.current = setInterval(() => {
        if (tickData) {
          updateVisualData(tickData);
        }
      }, 2000); // Update every 2 seconds

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [autoUpdate, isActive, tickData]);

  const updateVisualData = async (data: any) => {
    setLoading(true);
    setError(null);

    try {
      const visualData = await simulateVisualIntegration(data);
      setVisualData(visualData);
      
      // Auto-generate visualization for selected module
      if (selectedModule) {
        const output = generateTextVisualization(selectedModule, visualData);
        setVisualizationOutput(output);
      }
    } catch (err) {
      setError(`Failed to update visual data: ${err}`);
      console.error('Visual data update error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleModuleSelect = (moduleId: string) => {
    setSelectedModule(moduleId);
    if (visualData) {
      const output = generateTextVisualization(moduleId, visualData);
      setVisualizationOutput(output);
    }
  };

  const generateVisualization = () => {
    if (!visualData) {
      setError('No visual data available');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const output = generateTextVisualization(selectedModule, visualData);
      setVisualizationOutput(output);
    } catch (err) {
      setError(`Failed to generate visualization: ${err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="visual-processes-panel">
      <div className="visual-header">
        <h2>🌅 Visual Processes</h2>
        <p>Memory graphs, symbolic flows, rebloom patterns, and consciousness network visualization</p>
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
          >
            {AVAILABLE_MODULES.map(module => (
              <option key={module.id} value={module.id}>
                📊 {module.name}
              </option>
            ))}
          </select>
        </div>

        <button
          className="generate-btn"
          onClick={generateVisualization}
          disabled={loading || !visualData}
        >
          {loading ? 'Generating...' : 'Generate Visualization'}
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
            <div className="no-data">No visual data available</div>
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
              <p>Select a module and click "Generate Visualization" to see real-time consciousness data.</p>
              {!visualData && (
                <p>⚠️ Running in demo mode with synthetic data.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}; 