import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

interface VisualProcess {
  id: string;
  name: string;
  description: string;
  script: string;
  isActive: boolean;
}

const AVAILABLE_PROCESSES: VisualProcess[] = [
  {
    id: 'drift-vector',
    name: 'Drift Vector Field',
    description: 'Visualizes consciousness drift vectors and field patterns',
    script: 'drift_vector_field.py',
    isActive: false
  },
  {
    id: 'mood-heatmap',
    name: 'Mood Heatmap',
    description: 'Shows mood distribution and transitions',
    script: 'mood_heatmap.py',
    isActive: false
  },
  {
    id: 'sigil-trace',
    name: 'Sigil Trace',
    description: 'Displays sigil patterns and their evolution',
    script: 'sigil_trace_visualizer.py',
    isActive: false
  },
  {
    id: 'scup-zone',
    name: 'SCUP Zone',
    description: 'Animates SCUP zones and consciousness boundaries',
    script: 'scup_zone_animator.py',
    isActive: false
  },
  {
    id: 'pulse-waveform',
    name: 'Pulse Waveform',
    description: 'Renders consciousness pulse patterns',
    script: 'pulse_waveform_renderer.py',
    isActive: false
  },
  {
    id: 'synthesis-entropy',
    name: 'Synthesis Entropy',
    description: 'Charts entropy patterns in consciousness synthesis',
    script: 'synthesis_entropy_chart.py',
    isActive: false
  },
  {
    id: 'tracer-trail',
    name: 'Tracer Trail',
    description: 'Shows consciousness tracer movement patterns',
    script: 'tracer_trail_animator.py',
    isActive: false
  },
  {
    id: 'synthesis-lineage',
    name: 'Synthesis Lineage',
    description: 'Visualizes consciousness synthesis lineages',
    script: 'synthesis_lineage_animator.py',
    isActive: false
  },
  {
    id: 'stall-density',
    name: 'Stall Density',
    description: 'Maps consciousness stall patterns',
    script: 'stall_density_animator.py',
    isActive: false
  },
  {
    id: 'signature-grid',
    name: 'Signature Grid',
    description: 'Displays consciousness signature patterns',
    script: 'signature_grid_animator.py',
    isActive: false
  },
  {
    id: 'semantic-timeline',
    name: 'Semantic Timeline',
    description: 'Shows semantic evolution over time',
    script: 'semantic_timeline_animator.py',
    isActive: false
  },
  {
    id: 'hybrid-field',
    name: 'Hybrid Field',
    description: 'Visualizes hybrid consciousness fields',
    script: 'hybrid_field_visualizer.py',
    isActive: false
  }
];

const Visualizations: React.FC = () => {
  const [processes, setProcesses] = useState<VisualProcess[]>(AVAILABLE_PROCESSES);
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket for visual process updates
    const ws = new WebSocket('ws://localhost:8000/visual/stream');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('Connected to visual process stream');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'visual_frame' && canvasRef.current) {
        const ctx = canvasRef.current.getContext('2d');
        if (ctx) {
          // Draw the visual frame
          const image = new Image();
          image.onload = () => {
            ctx.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);
            ctx.drawImage(image, 0, 0);
          };
          image.src = `data:image/png;base64,${data.frame}`;
        }
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  const toggleProcess = async (processId: string) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/visual/toggle', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          process_id: processId,
          action: processes.find(p => p.id === processId)?.isActive ? 'stop' : 'start'
        }),
      });

      if (response.ok) {
        setProcesses(prev => prev.map(p => 
          p.id === processId ? { ...p, isActive: !p.isActive } : p
        ));
        setSelectedProcess(processId);
      }
    } catch (error) {
      console.error('Error toggling process:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="visualizations-page">
      <style>{`
        .visualizations-page {
          min-height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          padding: 20px;
          display: grid;
          grid-template-columns: 300px 1fr;
          gap: 20px;
        }

        .process-list {
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .process-item {
          padding: 15px;
          background: #1a1a1a;
          border: 1px solid #2a2a2a;
          cursor: pointer;
          transition: all 0.2s;
        }

        .process-item:hover {
          border-color: #00ff88;
        }

        .process-item.active {
          border-color: #00ff88;
          background: #1a2a1a;
        }

        .process-name {
          font-size: 14px;
          color: #e0e0e0;
          margin-bottom: 5px;
        }

        .process-description {
          font-size: 12px;
          color: #808080;
        }

        .visualization-area {
          background: #141414;
          border: 1px solid #2a2a2a;
          padding: 20px;
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .canvas-container {
          flex: 1;
          position: relative;
          background: #0a0a0a;
          border: 1px solid #2a2a2a;
        }

        canvas {
          width: 100%;
          height: 100%;
          object-fit: contain;
        }

        .controls {
          display: flex;
          gap: 10px;
          padding: 10px;
          background: #1a1a1a;
          border: 1px solid #2a2a2a;
        }

        .control-button {
          padding: 8px 16px;
          background: #2a2a2a;
          border: none;
          color: #e0e0e0;
          font-family: inherit;
          font-size: 12px;
          cursor: pointer;
          transition: background 0.2s;
        }

        .control-button:hover {
          background: #3a3a3a;
        }

        .control-button.active {
          background: #00ff88;
          color: #0a0a0a;
        }

        .loading-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(10, 10, 10, 0.8);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          color: #00ff88;
        }

        .loading-spinner {
          width: 20px;
          height: 20px;
          border: 2px solid #2a2a2a;
          border-top-color: #00ff88;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-right: 10px;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>

      <div className="process-list">
        <h2 style={{ marginBottom: '20px', fontSize: '16px', color: '#e0e0e0' }}>
          VISUAL PROCESSES
        </h2>
        {processes.map(process => (
          <motion.div
            key={process.id}
            className={`process-item ${process.isActive ? 'active' : ''}`}
            onClick={() => toggleProcess(process.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div className="process-name">{process.name}</div>
            <div className="process-description">{process.description}</div>
          </motion.div>
        ))}
      </div>

      <div className="visualization-area">
        <div className="canvas-container">
          <canvas ref={canvasRef} width={800} height={600} />
          {isLoading && (
            <div className="loading-overlay">
              <div className="loading-spinner"></div>
              <span>Loading visual process...</span>
            </div>
          )}
        </div>
        {selectedProcess && (
          <div className="controls">
            <button 
              className="control-button"
              onClick={() => toggleProcess(selectedProcess)}
            >
              {processes.find(p => p.id === selectedProcess)?.isActive ? 'STOP' : 'START'}
            </button>
            <button className="control-button">RESET</button>
            <button className="control-button">SAVE FRAME</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Visualizations; 