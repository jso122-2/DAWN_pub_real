import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface Process {
  id: string;
  name: string;
  script: string;
  description: string;
  status: 'running' | 'stopped' | 'error' | 'starting';
  pid?: number;
  cpu?: number;
  memory?: number;
  output?: string[];
}

const AVAILABLE_PROCESSES: Omit<Process, 'status' | 'pid' | 'cpu' | 'memory' | 'output'>[] = [
  {
    id: 'neural_network',
    name: 'Neural Network Visualizer',
    script: 'visual_executables/neural_network.py',
    description: 'Real-time neural pathway visualization'
  },
  {
    id: 'quantum_field',
    name: 'Quantum Field Renderer',
    script: 'visual_executables/quantum_field.py',
    description: 'Quantum state probability clouds'
  },
  {
    id: 'memory_palace',
    name: 'Memory Palace',
    script: 'visual_executables/memory_palace.py',
    description: 'Spatial memory architecture'
  },
  {
    id: 'entropy_cascade',
    name: 'Entropy Cascade',
    script: 'visual_executables/entropy_cascade.py',
    description: 'Chaos dynamics visualization'
  },
  {
    id: 'consciousness_map',
    name: 'Consciousness Mapper',
    script: 'visual_executables/consciousness_map.py',
    description: 'SCUP state topology'
  }
];

const ProcessManager: React.FC = () => {
  const [processes, setProcesses] = useState<Process[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);

  // Initialize processes
  useEffect(() => {
    const initialized = AVAILABLE_PROCESSES.map(p => ({
      ...p,
      status: 'stopped' as const,
      output: []
    }));
    setProcesses(initialized);
    
    // Poll for status updates
    const interval = setInterval(updateProcessStatuses, 2000);
    return () => clearInterval(interval);
  }, []);

  const updateProcessStatuses = async () => {
    try {
      const response = await axios.get('http://localhost:8000/processes/status');
      setProcesses(current => 
        current.map(p => {
          const status = response.data[p.id];
          return status ? { ...p, ...status } : p;
        })
      );
    } catch (error) {
      console.error('Failed to update process statuses:', error);
    }
  };

  const toggleProcess = async (processId: string) => {
    const process = processes.find(p => p.id === processId);
    if (!process) return;

    const action = process.status === 'running' ? 'stop' : 'start';
    
    // Optimistic update
    setProcesses(current =>
      current.map(p =>
        p.id === processId
          ? { ...p, status: action === 'start' ? 'starting' : 'stopped' }
          : p
      )
    );

    try {
      await axios.post(`http://localhost:8000/processes/${processId}/${action}`);
      // Status will be updated by the polling mechanism
    } catch (error) {
      console.error(`Failed to ${action} process:`, error);
      // Revert on error
      updateProcessStatuses();
    }
  };

  const getStatusIcon = (status: Process['status']) => {
    switch (status) {
      case 'running': return '●';
      case 'stopped': return '○';
      case 'starting': return '◐';
      case 'error': return '✕';
    }
  };

  const getStatusColor = (status: Process['status']) => {
    switch (status) {
      case 'running': return '#00ff88';
      case 'stopped': return '#808080';
      case 'starting': return '#ffaa00';
      case 'error': return '#ff0040';
    }
  };

  return (
    <div className="process-manager">
      <style>{`
        .process-manager {
          height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: 'JetBrains Mono', 'Consolas', monospace;
          display: flex;
        }

        .process-list {
          width: 400px;
          border-right: 1px solid #2a2a2a;
          background: #0f0f0f;
        }

        .list-header {
          padding: 20px;
          border-bottom: 1px solid #2a2a2a;
          background: #141414;
          font-size: 12px;
          color: #808080;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .process-item {
          padding: 15px 20px;
          border-bottom: 1px solid #1a1a1a;
          cursor: pointer;
          transition: background 0.2s;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .process-item:hover {
          background: #141414;
        }

        .process-item.selected {
          background: #1a1a1a;
          border-left: 2px solid #00ff88;
        }

        .process-info {
          flex: 1;
        }

        .process-name {
          font-size: 14px;
          margin-bottom: 4px;
        }

        .process-description {
          font-size: 11px;
          color: #808080;
        }

        .process-status {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
        }

        .status-icon {
          font-size: 16px;
          line-height: 1;
        }

        .toggle-button {
          padding: 4px 12px;
          border: 1px solid #2a2a2a;
          background: #141414;
          color: #e0e0e0;
          font-size: 11px;
          cursor: pointer;
          transition: all 0.2s;
          text-transform: uppercase;
          font-family: inherit;
        }

        .toggle-button:hover {
          background: #1a1a1a;
          border-color: #00ff88;
        }

        .toggle-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .process-details {
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        .details-header {
          padding: 20px;
          background: #141414;
          border-bottom: 1px solid #2a2a2a;
        }

        .details-title {
          font-size: 16px;
          margin-bottom: 10px;
        }

        .metrics {
          display: flex;
          gap: 30px;
          margin-top: 10px;
        }

        .metric {
          font-size: 12px;
        }

        .metric-label {
          color: #808080;
          margin-bottom: 2px;
        }

        .metric-value {
          font-size: 14px;
          color: #00ff88;
        }

        .output-container {
          flex: 1;
          padding: 20px;
          overflow-y: auto;
          font-size: 12px;
          line-height: 1.6;
          background: #0a0a0a;
        }

        .output-line {
          margin-bottom: 2px;
          color: #808080;
          font-family: inherit;
        }

        .output-line.error {
          color: #ff0040;
        }

        .no-selection {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #808080;
          font-size: 14px;
        }

        .ascii-art {
          text-align: center;
          font-size: 10px;
          line-height: 1.2;
          margin-bottom: 20px;
          color: #2a2a2a;
        }
      `}</style>

      <div className="process-list">
        <div className="list-header">Visual Sub-Processes</div>
        {processes.map(process => (
          <div
            key={process.id}
            className={`process-item ${selectedProcess === process.id ? 'selected' : ''}`}
            onClick={() => setSelectedProcess(process.id)}
          >
            <div className="process-info">
              <div className="process-name">{process.name}</div>
              <div className="process-description">{process.description}</div>
            </div>
            <div className="process-status">
              <span 
                className="status-icon" 
                style={{ color: getStatusColor(process.status) }}
              >
                {getStatusIcon(process.status)}
              </span>
              <button
                className="toggle-button"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleProcess(process.id);
                }}
                disabled={process.status === 'starting'}
              >
                {process.status === 'running' ? 'Stop' : 'Start'}
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="process-details">
        {selectedProcess ? (
          <>
            {(() => {
              const process = processes.find(p => p.id === selectedProcess);
              if (!process) return null;
              
              return (
                <>
                  <div className="details-header">
                    <div className="details-title">{process.name}</div>
                    <div className="metrics">
                      <div className="metric">
                        <div className="metric-label">STATUS</div>
                        <div className="metric-value">{process.status.toUpperCase()}</div>
                      </div>
                      {process.pid && (
                        <div className="metric">
                          <div className="metric-label">PID</div>
                          <div className="metric-value">{process.pid}</div>
                        </div>
                      )}
                      {process.cpu !== undefined && (
                        <div className="metric">
                          <div className="metric-label">CPU</div>
                          <div className="metric-value">{process.cpu.toFixed(1)}%</div>
                        </div>
                      )}
                      {process.memory !== undefined && (
                        <div className="metric">
                          <div className="metric-label">MEMORY</div>
                          <div className="metric-value">{(process.memory / 1024 / 1024).toFixed(1)} MB</div>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="output-container">
                    {process.output && process.output.length > 0 ? (
                      process.output.map((line, i) => (
                        <div key={i} className="output-line">
                          {line}
                        </div>
                      ))
                    ) : (
                      <div className="output-line">No output available</div>
                    )}
                  </div>
                </>
              );
            })()}
          </>
        ) : (
          <div className="no-selection">
            <div>
              <pre className="ascii-art">{`
     ╔═══════════════════════════╗
     ║   SELECT A PROCESS TO     ║
     ║   VIEW DETAILS & OUTPUT   ║
     ╚═══════════════════════════╝
              `}</pre>
              <div>Click on a process to manage</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessManager; 