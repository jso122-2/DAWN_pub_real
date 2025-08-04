import React, { useState, useEffect, useRef } from 'react';
import './ConsciousnessVisualizationPanel.css';

interface VisualizationData {
  emotional_landscape?: string;
  cognitive_pulse?: string;
  network_flow?: string;
  timestamp: number;
}

interface ConsciousnessVisualizationPanelProps {
  tickData?: any;
  isActive?: boolean;
}

export const ConsciousnessVisualizationPanel: React.FC<ConsciousnessVisualizationPanelProps> = ({
  tickData,
  isActive = true
}) => {
  const [visualizations, setVisualizations] = useState<VisualizationData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'emotional' | 'pulse' | 'network'>('emotional');
  const [autoUpdate, setAutoUpdate] = useState(true);
  const intervalRef = useRef<number | null>(null);

  // Update visualizations when tick data changes
  useEffect(() => {
    if (tickData && isActive && autoUpdate) {
      updateVisualizations(tickData);
    }
  }, [tickData, isActive, autoUpdate]);

  // Auto-refresh interval
  useEffect(() => {
    if (autoUpdate && isActive) {
      intervalRef.current = setInterval(() => {
        if (tickData) {
          updateVisualizations(tickData);
        }
      }, 2000); // Update every 2 seconds

      return () => {
        if (intervalRef.current) {
          clearInterval(intervalRef.current);
        }
      };
    }
  }, [autoUpdate, isActive, tickData]);

  const updateVisualizations = async (data: any) => {
    setLoading(true);
    setError(null);

    try {
      // In a real implementation, this would call the Python bridge
      // For now, we'll simulate the visualization update
      const response = await simulateVisualizationUpdate(data);
      
      setVisualizations({
        ...response,
        timestamp: Date.now()
      });
    } catch (err) {
      setError(`Failed to update visualizations: ${err}`);
      console.error('Visualization update error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Simulate calling the Python visualization bridge
  const simulateVisualizationUpdate = async (data: any): Promise<Partial<VisualizationData>> => {
    // This would be replaced with actual calls to the Python bridge
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          emotional_landscape: generateSimulatedVisualization('emotional'),
          cognitive_pulse: generateSimulatedVisualization('pulse'),
          network_flow: generateSimulatedVisualization('network')
        });
      }, 500);
    });
  };

  // Generate placeholder visualization data (in real implementation, comes from Python)
  const generateSimulatedVisualization = (type: string): string => {
    // This would be actual base64 image data from the Python bridge
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 300;
    const ctx = canvas.getContext('2d');
    
    if (!ctx) return '';

    // Create different visualizations based on type
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, 400, 300);

    switch (type) {
      case 'emotional':
        // Simulate emotional landscape heatmap
        ctx.fillStyle = '#ff4444';
        ctx.fillText('Emotional Landscape Simulation', 10, 30);
        for (let i = 0; i < 8; i++) {
          for (let j = 0; j < 8; j++) {
            const intensity = Math.random();
            ctx.fillStyle = `rgba(255, ${Math.floor(intensity * 255)}, 128, ${intensity})`;
            ctx.fillRect(j * 45 + 20, i * 30 + 50, 40, 25);
          }
        }
        break;

      case 'pulse':
        // Simulate cognitive pulse waveform
        ctx.strokeStyle = '#00ff88';
        ctx.lineWidth = 2;
        ctx.beginPath();
        for (let x = 0; x < 400; x++) {
          const y = 150 + Math.sin(x * 0.05) * 50 * Math.random();
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        ctx.fillStyle = '#00ff88';
        ctx.fillText('Cognitive Pulse Simulation', 10, 30);
        break;

      case 'network':
        // Simulate network nodes
        ctx.fillStyle = '#4488ff';
        ctx.fillText('Network Flow Simulation', 10, 30);
        for (let i = 0; i < 10; i++) {
          const x = Math.random() * 350 + 25;
          const y = Math.random() * 200 + 50;
          const radius = Math.random() * 10 + 5;
          ctx.beginPath();
          ctx.arc(x, y, radius, 0, 2 * Math.PI);
          ctx.fill();
        }
        break;
    }

    return canvas.toDataURL();
  };

  const refreshVisualizations = () => {
    if (tickData) {
      updateVisualizations(tickData);
    }
  };

  const getCurrentVisualization = (): string | undefined => {
    if (!visualizations) return undefined;
    
    switch (selectedTab) {
      case 'emotional':
        return visualizations.emotional_landscape;
      case 'pulse':
        return visualizations.cognitive_pulse;
      case 'network':
        return visualizations.network_flow;
      default:
        return undefined;
    }
  };

  const getVisualizationTitle = (): string => {
    switch (selectedTab) {
      case 'emotional':
        return '🎭 Emotional Landscape';
      case 'pulse':
        return '⚡ Cognitive Pulse';
      case 'network':
        return '🌐 Network Flow';
      default:
        return 'Consciousness Visualization';
    }
  };

  const getVisualizationDescription = (): string => {
    switch (selectedTab) {
      case 'emotional':
        return 'Real-time 8x8 emotional state heatmap showing consciousness mood dynamics across 64 affective dimensions';
      case 'pulse':
        return 'Live cognitive heartbeat monitoring with pulse waveforms and rhythm frequency analysis';
      case 'network':
        return 'Semantic flow network showing thought connections and consciousness state relationships';
      default:
        return 'Advanced consciousness monitoring visualization';
    }
  };

  return (
    <div className="consciousness-visualization-panel">
      <div className="panel-header">
        <h2>🧠 Consciousness Visualizations</h2>
        <div className="panel-controls">
          <button
            className={`auto-update-btn ${autoUpdate ? 'active' : ''}`}
            onClick={() => setAutoUpdate(!autoUpdate)}
            title="Toggle auto-update"
          >
            {autoUpdate ? '⏸️' : '▶️'}
          </button>
          <button
            className="refresh-btn"
            onClick={refreshVisualizations}
            disabled={loading}
            title="Refresh visualizations"
          >
            🔄
          </button>
        </div>
      </div>

      <div className="visualization-tabs">
        <button
          className={`tab-btn ${selectedTab === 'emotional' ? 'active' : ''}`}
          onClick={() => setSelectedTab('emotional')}
        >
          🎭 Emotional
        </button>
        <button
          className={`tab-btn ${selectedTab === 'pulse' ? 'active' : ''}`}
          onClick={() => setSelectedTab('pulse')}
        >
          ⚡ Pulse
        </button>
        <button
          className={`tab-btn ${selectedTab === 'network' ? 'active' : ''}`}
          onClick={() => setSelectedTab('network')}
        >
          🌐 Network
        </button>
      </div>

      <div className="visualization-content">
        <div className="visualization-info">
          <h3>{getVisualizationTitle()}</h3>
          <p>{getVisualizationDescription()}</p>
        </div>

        <div className="visualization-display">
          {loading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
              <span>Updating visualization...</span>
            </div>
          )}

          {error && (
            <div className="error-display">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
              <button onClick={refreshVisualizations}>Retry</button>
            </div>
          )}

          {!loading && !error && getCurrentVisualization() && (
            <div className="visualization-image-container">
              <img
                src={getCurrentVisualization()}
                alt={getVisualizationTitle()}
                className="visualization-image"
              />
              <div className="visualization-overlay">
                <div className="timestamp">
                  Last updated: {visualizations?.timestamp ? 
                    new Date(visualizations.timestamp).toLocaleTimeString() : 'Never'}
                </div>
              </div>
            </div>
          )}

          {!loading && !error && !getCurrentVisualization() && (
            <div className="no-data-display">
              <span className="no-data-icon">📊</span>
              <span>No visualization data available</span>
              <button onClick={refreshVisualizations}>Generate</button>
            </div>
          )}
        </div>
      </div>

      <div className="visualization-metrics">
        {tickData && (
          <div className="metrics-grid">
            <div className="metric-item">
              <span className="metric-label">Tick:</span>
              <span className="metric-value">{tickData.tick || 0}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Entropy:</span>
              <span className="metric-value">{(tickData.entropy || 0).toFixed(3)}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">SCUP:</span>
              <span className="metric-value">{(tickData.scup || 0).toFixed(3)}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Mood:</span>
              <span className="metric-value">{tickData.mood || 'UNKNOWN'}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}; 