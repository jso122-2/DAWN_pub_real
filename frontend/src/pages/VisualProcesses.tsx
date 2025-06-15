import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface TickSnapshot {
  tick_number: number;
  timestamp: string;
  data: any;
  visualization: string; // Base64 encoded image or canvas data
}

interface VisualProcess {
  id: string;
  name: string;
  icon: string;
  description: string;
  status: 'running' | 'stopped' | 'capturing';
  lastCapture?: TickSnapshot;
  captureInterval: number; // milliseconds
  visualType: 'canvas' | 'ascii' | 'matrix' | 'graph';
}

// Define all visual processes
const VISUAL_PROCESSES: Omit<VisualProcess, 'status' | 'lastCapture'>[] = [
  {
    id: 'drift_vector_field',
    name: 'Drift Vector Field',
    icon: '🌀',
    description: 'Semantic drift and vector field analysis',
    captureInterval: 1000,
    visualType: 'canvas'
  },
  {
    id: 'mood_heatmap',
    name: 'Mood Heatmap',
    icon: '🌡️',
    description: 'Real-time emotional state heatmap',
    captureInterval: 1000,
    visualType: 'matrix'
  },
  {
    id: 'sigil_trace_visualizer',
    name: 'Sigil Trace',
    icon: '🔮',
    description: 'Emotional sigil patterns and traces',
    captureInterval: 1000,
    visualType: 'canvas'
  },
  {
    id: 'scup_zone_animator',
    name: 'SCUP Zone',
    icon: '🟩',
    description: 'SCUP zone visualization',
    captureInterval: 1000,
    visualType: 'canvas'
  },
  {
    id: 'attention_map',
    name: 'Attention Map',
    icon: '🎯',
    description: 'Neural attention weights heatmap',
    captureInterval: 1000,
    visualType: 'matrix'
  },
  {
    id: 'temporal_activity_raster',
    name: 'Temporal Activity Raster',
    icon: '📈',
    description: 'Spike train/raster plot',
    captureInterval: 1000,
    visualType: 'matrix'
  },
  {
    id: 'latent_space_trajectory',
    name: 'Latent Space Trajectory',
    icon: '🛤️',
    description: '2D latent space trajectory',
    captureInterval: 1000,
    visualType: 'canvas'
  },
  {
    id: 'loss_landscape',
    name: 'Loss Landscape',
    icon: '🌋',
    description: 'Loss landscape with optimization path',
    captureInterval: 1000,
    visualType: 'matrix'
  },
  {
    id: 'correlation_matrix',
    name: 'Correlation Matrix',
    icon: '🔗',
    description: 'Correlation matrix visualization',
    captureInterval: 1000,
    visualType: 'matrix'
  },
  {
    id: 'activation_histogram',
    name: 'Activation Histogram',
    icon: '📊',
    description: 'Activation values histogram',
    captureInterval: 1000,
    visualType: 'graph'
  },
  {
    id: 'state_transition_graph',
    name: 'State Transition Graph',
    icon: '🔄',
    description: 'State transition graph',
    captureInterval: 1000,
    visualType: 'graph'
  },
  {
    id: 'anomaly_timeline',
    name: 'Anomaly Timeline',
    icon: '🚨',
    description: 'Anomaly timeline visualization',
    captureInterval: 1000,
    visualType: 'graph'
  }
];

const VisualProcesses: React.FC = () => {
  const [processes, setProcesses] = useState<VisualProcess[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);
  const captureIntervals = useRef<{ [key: string]: number }>({});
  const canvasRefs = useRef<{ [key: string]: HTMLCanvasElement | null }>({});

  // Initialize processes
  useEffect(() => {
    const initialized = VISUAL_PROCESSES.map(p => ({
      ...p,
      status: 'stopped' as const
    }));
    setProcesses(initialized);
  }, []);

  // Cleanup intervals on unmount
  useEffect(() => {
    return () => {
      Object.values(captureIntervals.current).forEach(intervalId => {
        clearInterval(intervalId);
      });
    };
  }, []);

  const toggleProcess = async (processId: string) => {
    const process = processes.find(p => p.id === processId);
    if (!process) return;

    if (process.status === 'running') {
      // Stop the process
      if (captureIntervals.current[processId]) {
        clearInterval(captureIntervals.current[processId]);
        delete captureIntervals.current[processId];
      }
      
      setProcesses(prev => prev.map(p => 
        p.id === processId ? { ...p, status: 'stopped' } : p
      ));

      // Notify backend
      await axios.post(`http://localhost:8000/processes/${processId}/stop`);
    } else {
      // Start the process
      setProcesses(prev => prev.map(p => 
        p.id === processId ? { ...p, status: 'running' } : p
      ));

      // Start capture interval
      captureIntervals.current[processId] = window.setInterval(() => {
        captureTickSnapshot(processId);
      }, process.captureInterval);

      // Notify backend
      await axios.post(`http://localhost:8000/processes/${processId}/start`);
    }
  };

  const captureTickSnapshot = async (processId: string) => {
    try {
      setProcesses(prev => prev.map(p => 
        p.id === processId ? { ...p, status: 'capturing' } : p
      ));

      // Get current tick data
      const response = await axios.get(`http://localhost:8000/tick-snapshot/${processId}`);
      const tickData = response.data;

      // Generate visualization based on process type
      const visualization = await generateVisualization(processId, tickData);

      setProcesses(prev => prev.map(p => 
        p.id === processId ? {
          ...p,
          status: 'running',
          lastCapture: {
            tick_number: tickData.tick_number,
            timestamp: new Date().toISOString(),
            data: tickData,
            visualization
          }
        } : p
      ));
    } catch (error) {
      console.error(`Failed to capture snapshot for ${processId}:`, error);
      // Set process back to stopped state on error
      setProcesses(prev => prev.map(p => 
        p.id === processId ? { ...p, status: 'stopped' } : p
      ));
    }
  };

  const generateVisualization = async (processId: string, tickData: any): Promise<string> => {
    const process = processes.find(p => p.id === processId);
    if (!process) return '';

    // If the backend provided a visualization, use it
    if (tickData.visualization) {
      return tickData.visualization;
    }

    // Otherwise generate one based on the process type
    switch (process.visualType) {
      case 'canvas':
        return generateCanvasVisualization(processId, tickData);
      case 'ascii':
        return generateAsciiVisualization(processId, tickData);
      case 'matrix':
        return generateMatrixVisualization(processId, tickData);
      case 'graph':
        return generateGraphVisualization(processId, tickData);
      default:
        return '';
    }
  };

  const generateCanvasVisualization = (processId: string, data: any): string => {
    const canvas = canvasRefs.current[processId];
    if (!canvas) return '';

    const ctx = canvas.getContext('2d');
    if (!ctx) return '';

    // Clear canvas
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Process-specific visualizations
    switch (processId) {
      case 'drift_vector_field':
        // Draw vector field
        const vectors = data.vectors || [];
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        
        vectors.forEach((vector: any) => {
          const { x, y, dx, dy, magnitude } = vector;
          const startX = centerX + x;
          const startY = centerY + y;
          const endX = startX + dx * magnitude;
          const endY = startY + dy * magnitude;
          
          ctx.beginPath();
          ctx.moveTo(startX, startY);
          ctx.lineTo(endX, endY);
          ctx.strokeStyle = `rgba(0, 255, 136, ${magnitude})`;
          ctx.stroke();
          
          // Draw arrow head
          const angle = Math.atan2(endY - startY, endX - startX);
          const arrowSize = 5;
          ctx.beginPath();
          ctx.moveTo(endX, endY);
          ctx.lineTo(
            endX - arrowSize * Math.cos(angle - Math.PI / 6),
            endY - arrowSize * Math.sin(angle - Math.PI / 6)
          );
          ctx.lineTo(
            endX - arrowSize * Math.cos(angle + Math.PI / 6),
            endY - arrowSize * Math.sin(angle + Math.PI / 6)
          );
          ctx.closePath();
          ctx.fillStyle = `rgba(0, 255, 136, ${magnitude})`;
          ctx.fill();
        });
        break;

      case 'mood_heatmap':
        // Draw mood heatmap
        const heatmap = data.heatmap || [];
        const cellSize = Math.min(canvas.width, canvas.height) / Math.sqrt(heatmap.length);
        
        heatmap.forEach((value: number, i: number) => {
          const x = (i % Math.sqrt(heatmap.length)) * cellSize;
          const y = Math.floor(i / Math.sqrt(heatmap.length)) * cellSize;
          
          ctx.fillStyle = `rgba(255, ${255 * (1 - value)}, ${255 * (1 - value)}, ${value})`;
          ctx.fillRect(x, y, cellSize, cellSize);
        });
        break;

      case 'sigil_trace':
        // Draw sigil traces
        const traces = data.traces || [];
        traces.forEach((trace: any) => {
          ctx.beginPath();
          ctx.moveTo(trace.points[0].x, trace.points[0].y);
          trace.points.forEach((point: any) => {
            ctx.lineTo(point.x, point.y);
          });
          ctx.strokeStyle = `rgba(255, 0, 136, ${trace.intensity})`;
          ctx.stroke();
        });
        break;

      case 'scup_zone':
        // Draw SCUP zones
        const zones = data.zones || [];
        zones.forEach((zone: any) => {
          const { x, y, radius, intensity } = zone;
          const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
          gradient.addColorStop(0, `rgba(0, 255, 136, ${intensity})`);
          gradient.addColorStop(1, 'rgba(0, 255, 136, 0)');
          ctx.fillStyle = gradient;
          ctx.beginPath();
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fill();
        });
        break;

      case 'pulse_waveform':
        // Draw pulse waveform
        const waveform = data.waveform || [];
        const width = canvas.width;
        const height = canvas.height;
        const step = width / waveform.length;
        
        ctx.beginPath();
        ctx.moveTo(0, height / 2);
        waveform.forEach((value: number, i: number) => {
          const x = i * step;
          const y = height / 2 - value * height / 2;
          ctx.lineTo(x, y);
        });
        ctx.strokeStyle = 'rgba(0, 255, 136, 0.8)';
        ctx.stroke();
        break;

      case 'synthesis_entropy':
        // Draw entropy chart
        const entropy = data.entropy || [];
        const barWidth = canvas.width / entropy.length;
        
        entropy.forEach((value: number, i: number) => {
          const x = i * barWidth;
          const barHeight = value * canvas.height;
          ctx.fillStyle = `rgba(0, 255, 136, ${value})`;
          ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        });
        break;
    }

    return canvas.toDataURL();
  };

  const generateAsciiVisualization = (processId: string, data: any): string => {
    switch (processId) {
      case 'memory_palace':
        return `
╔═══════════════════════════════╗
║      MEMORY PALACE LAYOUT     ║
╠═══════════════════════════════╣
║ [HALL] ──┬── [CHAMBER A]      ║
║    │     │        │           ║
║    │     └── [CHAMBER B]      ║
║    │              │           ║
║ [VAULT] ──── [ARCHIVES]       ║
║                   │           ║
║            [DEEP STORAGE]     ║
╚═══════════════════════════════╝
TICK: ${data.tick_number} | MEM: ${(data.memory_usage || 0).toFixed(2)}%`;

      case 'subsystem_health':
        const systems = [
          { name: 'NEURAL', health: 0.92 },
          { name: 'QUANTUM', health: 0.78 },
          { name: 'MEMORY', health: 0.85 },
          { name: 'CHAOS', health: 0.45 }
        ];
        
        let ascii = '┌─────────────────────────┐\n';
        systems.forEach(sys => {
          const bars = Math.floor(sys.health * 10);
          const health = '█'.repeat(bars) + '░'.repeat(10 - bars);
          ascii += `│ ${sys.name.padEnd(7)} │${health}│\n`;
        });
        ascii += '└─────────────────────────┘';
        return ascii;

      default:
        return 'ASCII visualization';
    }
  };

  const generateMatrixVisualization = (processId: string, data: any): string => {
    const width = 40;
    const height = 20;
    let matrix = '';

    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        const value = Math.random();
        if (value > 0.8) {
          matrix += '█';
        } else if (value > 0.6) {
          matrix += '▓';
        } else if (value > 0.4) {
          matrix += '▒';
        } else if (value > 0.2) {
          matrix += '░';
        } else {
          matrix += ' ';
        }
      }
      matrix += '\n';
    }
    return matrix;
  };

  const generateGraphVisualization = (processId: string, data: any): string => {
    // Simple ASCII graph
    const values = Array(20).fill(0).map(() => Math.random());
    const height = 10;
    let graph = '';

    for (let y = height; y >= 0; y--) {
      const threshold = y / height;
      let line = '│';
      values.forEach(v => {
        line += v >= threshold ? '█' : ' ';
      });
      graph += line + '\n';
    }
    graph += '└' + '─'.repeat(20) + '\n';
    graph += ` TICK: ${data.tick_number}`;
    
    return graph;
  };

  return (
    <div className="visual-processes">
      <style>{`
        .visual-processes {
          height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          display: flex;
          overflow: hidden;
        }

        .process-grid {
          width: 400px;
          background: #0f0f0f;
          border-right: 1px solid #2a2a2a;
          overflow-y: auto;
          padding: 20px;
        }

        .grid-header {
          font-size: 12px;
          color: #808080;
          text-transform: uppercase;
          letter-spacing: 1px;
          margin-bottom: 20px;
          padding-bottom: 10px;
          border-bottom: 1px solid #2a2a2a;
        }

        .process-card {
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 15px;
          margin-bottom: 10px;
          cursor: pointer;
          transition: all 0.2s;
          position: relative;
        }

        .process-card:hover {
          background: #1a1a1a;
          border-color: #3a3a3a;
        }

        .process-card.selected {
          border-color: #00ff88;
          background: #1a1a1a;
        }

        .process-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }

        .process-title {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
        }

        .process-icon {
          font-size: 18px;
        }

        .process-status {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .status-indicator {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #808080;
        }

        .status-indicator.running {
          background: #00ff88;
          animation: pulse 2s infinite;
        }

        .status-indicator.capturing {
          background: #ffaa00;
          animation: pulse 0.5s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 0.4; }
          50% { opacity: 1; }
        }

        .toggle-btn {
          padding: 2px 8px;
          border: 1px solid #2a2a2a;
          background: #0a0a0a;
          color: #808080;
          font-size: 10px;
          cursor: pointer;
          text-transform: uppercase;
          transition: all 0.2s;
        }

        .toggle-btn:hover {
          border-color: #00ff88;
          color: #00ff88;
        }

        .process-description {
          font-size: 11px;
          color: #808080;
          line-height: 1.4;
        }

        .visualization-panel {
          flex: 1;
          padding: 20px;
          display: flex;
          flex-direction: column;
          background: #0a0a0a;
        }

        .viz-header {
          padding: 20px;
          background: #141414;
          border: 1px solid #2a2a2a;
          margin-bottom: 20px;
        }

        .viz-title {
          font-size: 16px;
          margin-bottom: 10px;
        }

        .viz-info {
          display: flex;
          gap: 20px;
          font-size: 12px;
          color: #808080;
        }

        .viz-content {
          flex: 1;
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          position: relative;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .viz-canvas {
          max-width: 100%;
          max-height: 100%;
        }

        .viz-ascii {
          font-size: 12px;
          line-height: 1.2;
          white-space: pre;
          color: #00ff88;
        }

        .viz-matrix {
          font-size: 10px;
          line-height: 1;
          white-space: pre;
          color: #00ff88;
          letter-spacing: 2px;
        }

        .no-selection {
          color: #808080;
          text-align: center;
        }

        .last-capture {
          position: absolute;
          top: 10px;
          right: 10px;
          font-size: 10px;
          color: #808080;
        }
      `}</style>

      <div className="process-grid">
        <div className="grid-header">
          Visual Process Controllers • {processes.filter(p => p.status === 'running').length}/12 Active
        </div>
        
        {processes.map(process => (
          <div
            key={process.id}
            className={`process-card ${selectedProcess === process.id ? 'selected' : ''}`}
            onClick={() => setSelectedProcess(process.id)}
          >
            <div className="process-header">
              <div className="process-title">
                <span className="process-icon">{process.icon}</span>
                <span>{process.name}</span>
              </div>
              <div className="process-status">
                <div className={`status-indicator ${process.status}`}></div>
                <button
                  className="toggle-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleProcess(process.id);
                  }}
                >
                  {process.status === 'running' ? 'STOP' : 'START'}
                </button>
              </div>
            </div>
            <div className="process-description">{process.description}</div>
          </div>
        ))}
      </div>

      <div className="visualization-panel">
        {selectedProcess ? (
          <>
            {(() => {
              const process = processes.find(p => p.id === selectedProcess);
              if (!process) return null;

              return (
                <>
                  <div className="viz-header">
                    <div className="viz-title">
                      {process.icon} {process.name}
                    </div>
                    <div className="viz-info">
                      <span>Status: {process.status.toUpperCase()}</span>
                      <span>Update Rate: {process.captureInterval}ms</span>
                      {process.lastCapture && (
                        <span>Last Tick: {process.lastCapture.tick_number}</span>
                      )}
                    </div>
                  </div>
                  
                  <div className="viz-content">
                    {process.lastCapture && (
                      <div className="last-capture">
                        {new Date(process.lastCapture.timestamp).toLocaleTimeString()}
                      </div>
                    )}
                    
                    {process.visualType === 'canvas' && (
                      <>
                        <canvas
                          ref={el => canvasRefs.current[process.id] = el}
                          className="viz-canvas"
                          width={800}
                          height={600}
                          style={{ display: 'none' }}
                        />
                        {process.lastCapture && (
                          <img 
                            src={process.lastCapture.visualization} 
                            alt={process.name}
                            style={{ maxWidth: '100%', maxHeight: '100%' }}
                          />
                        )}
                      </>
                    )}
                    
                    {process.visualType === 'ascii' && process.lastCapture && (
                      <pre className="viz-ascii">{process.lastCapture.visualization}</pre>
                    )}
                    
                    {process.visualType === 'matrix' && process.lastCapture && (
                      <pre className="viz-matrix">{process.lastCapture.visualization}</pre>
                    )}
                    
                    {process.visualType === 'graph' && process.lastCapture && (
                      <pre className="viz-ascii">{process.lastCapture.visualization}</pre>
                    )}
                    
                    {!process.lastCapture && (
                      <div className="no-selection">
                        {process.status === 'stopped' ? 'Process not running' : 'Waiting for first capture...'}
                      </div>
                    )}
                  </div>
                </>
              );
            })()}
          </>
        ) : (
          <div className="viz-content">
            <div className="no-selection">
              <pre style={{ fontSize: '10px', color: '#2a2a2a' }}>{`
    ╔═══════════════════════════════════╗
    ║  SELECT A VISUAL PROCESS TO VIEW  ║
    ║     REAL-TIME TICK LOOP DATA      ║
    ╚═══════════════════════════════════╝
              `}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VisualProcesses; 