import React, { useState, useCallback, useRef } from 'react';
import './CognitionReplayDashboard.css';

// Interfaces for semantic snapshot data structure
interface CognitiveSnapshot {
  tick_id: number;
  timestamp: number;
  datetime_iso: string;
  entropy: number;
  mood: string;
  coherence: number;
  heat: number;
  complexity: number;
  memory_activity: number;
  forecast_reliability: number;
  
  // Component data
  reflections: ReflectionEntry[];
  rebloom_lineage: LineageEntry[];
  symbolic_roots: SymbolicRoot[];
  tracer_alerts: TracerAlert[];
  spoken_events: SpokenEvent[];
  voice_modulations: VoiceModulation[];
  mycelium_graph?: MyceliumGraph;
  
  // Metadata
  snapshot_source: string;
  component_status: Record<string, boolean>;
  log_file_sizes: Record<string, number>;
}

interface ReflectionEntry {
  timestamp: number;
  content: string;
  source: string;
}

interface LineageEntry {
  child_id: string;
  parent_id: string;
  method: string;
  depth: number;
  significance: number;
  timestamp: number;
}

interface SymbolicRoot {
  tick: number;
  type: string;
  symbolic_root: string;
  significance: number;
  timestamp: number;
}

interface TracerAlert {
  timestamp: number;
  tracer_type: string;
  severity: string;
  message: string;
  tick_id: number;
}

interface SpokenEvent {
  timestamp: number;
  text: string;
  tracer_type?: string;
  modulation_type?: string;
}

interface VoiceModulation {
  timestamp: number;
  mood: string;
  entropy: number;
  voice_profile: {
    rate: number;
    volume: number;
    pitch_modifier: number;
  };
}

interface MyceliumGraph {
  metadata: {
    node_count: number;
    edge_count: number;
    source: string;
  };
  nodes: Array<{
    id: string;
    label: string;
    type: string;
  }>;
  edges: Array<{
    from: string;
    to: string;
    type: string;
    weight: number;
  }>;
}

const CognitionReplayDashboard: React.FC = () => {
  const [snapshot, setSnapshot] = useState<CognitiveSnapshot | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedPanels, setExpandedPanels] = useState<Set<string>>(new Set(['overview']));
  const [selectedFile, setSelectedFile] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadSnapshotFromFile = useCallback(async (file: File) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      // Validate snapshot structure
      if (!data.tick_id || !data.timestamp) {
        throw new Error('Invalid snapshot format - missing required fields');
      }
      
      setSnapshot(data as CognitiveSnapshot);
      setSelectedFile(file.name);
      
    } catch (err) {
      setError(`Error loading snapshot: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleFileSelect = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.name.endsWith('.json')) {
      loadSnapshotFromFile(file);
    }
  }, [loadSnapshotFromFile]);

  const togglePanel = useCallback((panelId: string) => {
    setExpandedPanels(prev => {
      const newSet = new Set(prev);
      if (newSet.has(panelId)) {
        newSet.delete(panelId);
      } else {
        newSet.add(panelId);
      }
      return newSet;
    });
  }, []);

  const getEntropyColor = (entropy: number): string => {
    if (entropy > 0.8) return '#ff9800'; // Orange for high entropy
    if (entropy > 0.6) return '#ffeb3b'; // Yellow for medium-high
    if (entropy < 0.3) return '#4caf50'; // Green for low entropy
    return '#2196f3'; // Blue for normal
  };

  const getMoodColor = (mood: string): string => {
    const moodColors: Record<string, string> = {
      'CALM': '#4caf50',
      'ANXIOUS': '#ff5722',
      'FOCUSED': '#2196f3',
      'EXCITED': '#ff9800',
      'ANALYTICAL': '#9c27b0',
      'CREATIVE': '#e91e63',
      'CONTEMPLATIVE': '#607d8b',
      'DRIFTING': '#795548',
      'UNCERTAIN': '#ff9800',
      'NEUTRAL': '#757575'
    };
    return moodColors[mood] || '#757575';
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity.toLowerCase()) {
      case 'critical': return '#f44336';
      case 'warning': return '#ff9800';
      case 'important': return '#9c27b0';
      default: return '#2196f3';
    }
  };

  const formatTimestamp = (timestamp: number): string => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const formatDuration = (timestamp: number): string => {
    const now = Date.now() / 1000;
    const diffSeconds = Math.floor(now - timestamp);
    
    if (diffSeconds < 60) return `${diffSeconds}s ago`;
    if (diffSeconds < 3600) return `${Math.floor(diffSeconds / 60)}m ago`;
    if (diffSeconds < 86400) return `${Math.floor(diffSeconds / 3600)}h ago`;
    return `${Math.floor(diffSeconds / 86400)}d ago`;
  };

  const renderPanel = (id: string, title: string, icon: string, children: React.ReactNode) => {
    const isExpanded = expandedPanels.has(id);
    
    return (
      <div className={`replay-panel ${isExpanded ? 'expanded' : 'collapsed'}`}>
        <div className="panel-header" onClick={() => togglePanel(id)}>
          <span className="panel-icon">{icon}</span>
          <span className="panel-title">{title}</span>
          <span className="panel-toggle">{isExpanded ? '▼' : '▶'}</span>
        </div>
        {isExpanded && (
          <div className="panel-content">
            {children}
          </div>
        )}
      </div>
    );
  };

  const renderMyceliumMiniGraph = (graph: MyceliumGraph) => {
    const maxNodes = 20; // Limit for performance
    const displayNodes = graph.nodes.slice(0, maxNodes);
    
    return (
      <div className="mycelium-mini-graph">
        <div className="graph-info">
          <span>Nodes: {graph.metadata.node_count}</span>
          <span>Edges: {graph.metadata.edge_count}</span>
          <span>Source: {graph.metadata.source}</span>
        </div>
        <div className="graph-preview">
          <svg width="300" height="200" viewBox="0 0 300 200">
            {/* Simple node layout in a grid */}
            {displayNodes.map((node, index) => {
              const x = 50 + (index % 5) * 50;
              const y = 50 + Math.floor(index / 5) * 30;
              return (
                <g key={node.id}>
                  <circle
                    cx={x}
                    cy={y}
                    r="8"
                    fill="#2196f3"
                    stroke="#fff"
                    strokeWidth="2"
                  />
                  <text
                    x={x}
                    y={y + 20}
                    textAnchor="middle"
                    fontSize="10"
                    fill="#666"
                  >
                    {node.label.substring(0, 8)}
                  </text>
                </g>
              );
            })}
            
            {/* Draw some sample edges */}
            {graph.edges.slice(0, 10).map((edge, index) => {
              const fromNode = displayNodes.find(n => n.id === edge.from);
              const toNode = displayNodes.find(n => n.id === edge.to);
              
              if (!fromNode || !toNode) return null;
              
              const fromIndex = displayNodes.indexOf(fromNode);
              const toIndex = displayNodes.indexOf(toNode);
              
              const x1 = 50 + (fromIndex % 5) * 50;
              const y1 = 50 + Math.floor(fromIndex / 5) * 30;
              const x2 = 50 + (toIndex % 5) * 50;
              const y2 = 50 + Math.floor(toIndex / 5) * 30;
              
              return (
                <line
                  key={index}
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke="#666"
                  strokeWidth="1"
                  opacity="0.6"
                />
              );
            })}
          </svg>
        </div>
      </div>
    );
  };

  return (
    <div className="cognition-replay-dashboard">
      <div className="dashboard-header">
        <h2>🧠📈 Cognition Replay Dashboard</h2>
        <div className="file-controls">
          <input
            ref={fileInputRef}
            type="file"
            accept=".json"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          <button
            className="load-button"
            onClick={() => fileInputRef.current?.click()}
          >
            📁 Load Snapshot
          </button>
          {selectedFile && (
            <span className="selected-file">📄 {selectedFile}</span>
          )}
        </div>
      </div>

      {isLoading && (
        <div className="loading-state">
          <div className="loading-spinner">⏳</div>
          <span>Loading cognitive snapshot...</span>
        </div>
      )}

      {error && (
        <div className="error-state">
          <span className="error-icon">❌</span>
          <span>{error}</span>
        </div>
      )}

      {!snapshot && !isLoading && !error && (
        <div className="empty-state">
          <div className="empty-icon">🧠</div>
          <h3>No Snapshot Loaded</h3>
          <p>Load a semantic trace JSON file to visualize DAWN's cognitive state at that moment.</p>
          <button
            className="load-button primary"
            onClick={() => fileInputRef.current?.click()}
          >
            📁 Load Semantic Snapshot
          </button>
        </div>
      )}

      {snapshot && (
        <div className="snapshot-content">
          {/* Overview Panel */}
          {renderPanel('overview', 'Cognitive Overview', '🎯', (
            <div className="overview-grid">
              <div className="metric-card">
                <div className="metric-label">Tick</div>
                <div className="metric-value large">{snapshot.tick_id}</div>
                <div className="metric-subtitle">{formatTimestamp(snapshot.timestamp)}</div>
              </div>
              
              <div className="metric-card">
                <div className="metric-label">Entropy</div>
                <div
                  className="metric-value"
                  style={{ color: getEntropyColor(snapshot.entropy) }}
                >
                  {snapshot.entropy.toFixed(3)}
                </div>
                <div className="metric-progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${snapshot.entropy * 100}%`,
                      backgroundColor: getEntropyColor(snapshot.entropy)
                    }}
                  />
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-label">Mood</div>
                <div
                  className="metric-value"
                  style={{ color: getMoodColor(snapshot.mood) }}
                >
                  {snapshot.mood}
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-label">Coherence</div>
                <div className="metric-value">{snapshot.coherence.toFixed(3)}</div>
                <div className="metric-progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${snapshot.coherence * 100}%`,
                      backgroundColor: snapshot.coherence > 0.7 ? '#4caf50' : '#ff9800'
                    }}
                  />
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-label">Heat</div>
                <div className="metric-value">{snapshot.heat.toFixed(3)}</div>
                <div className="metric-progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${snapshot.heat * 100}%`,
                      backgroundColor: snapshot.heat > 0.8 ? '#f44336' : '#2196f3'
                    }}
                  />
                </div>
              </div>
              
              <div className="metric-card">
                <div className="metric-label">Memory Activity</div>
                <div className="metric-value">{snapshot.memory_activity.toFixed(3)}</div>
                <div className="metric-progress">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${snapshot.memory_activity * 100}%`,
                      backgroundColor: '#9c27b0'
                    }}
                  />
                </div>
              </div>
            </div>
          ))}

          {/* Reflections Panel */}
          {renderPanel('reflections', `Reflections (${snapshot.reflections.length})`, '💭', (
            <div className="reflections-list">
              {snapshot.reflections.slice(-5).reverse().map((reflection, index) => (
                <div key={index} className="reflection-item">
                  <div className="reflection-header">
                    <span className="reflection-source">{reflection.source}</span>
                    <span className="reflection-time">{formatDuration(reflection.timestamp)}</span>
                  </div>
                  <div className="reflection-content">{reflection.content}</div>
                </div>
              ))}
              {snapshot.reflections.length === 0 && (
                <div className="empty-content">No reflections in this snapshot</div>
              )}
            </div>
          ))}

          {/* Tracer Alerts Panel */}
          {renderPanel('alerts', `Tracer Alerts (${snapshot.tracer_alerts.length})`, '🔍', (
            <div className="alerts-list">
              {snapshot.tracer_alerts.map((alert, index) => (
                <div key={index} className="alert-item">
                  <div className="alert-header">
                    <span
                      className="alert-tracer"
                      style={{ color: getSeverityColor(alert.severity) }}
                    >
                      {alert.tracer_type.toUpperCase()}
                    </span>
                    <span className="alert-severity">{alert.severity}</span>
                    <span className="alert-time">{formatDuration(alert.timestamp)}</span>
                  </div>
                  <div className="alert-message">{alert.message}</div>
                </div>
              ))}
              {snapshot.tracer_alerts.length === 0 && (
                <div className="empty-content">No tracer alerts in this snapshot</div>
              )}
            </div>
          ))}

          {/* Symbolic Roots Panel */}
          {renderPanel('roots', `Symbolic Roots (${snapshot.symbolic_roots.length})`, '✨', (
            <div className="roots-list">
              {snapshot.symbolic_roots.map((root, index) => (
                <div key={index} className="root-item">
                  <div className="root-header">
                    <span className="root-type">{root.type}</span>
                    <span className="root-significance">
                      Sig: {(root.significance * 100).toFixed(0)}%
                    </span>
                    <span className="root-time">{formatDuration(root.timestamp)}</span>
                  </div>
                  <div className="root-name">{root.symbolic_root}</div>
                </div>
              ))}
              {snapshot.symbolic_roots.length === 0 && (
                <div className="empty-content">No symbolic roots detected</div>
              )}
            </div>
          ))}

          {/* Rebloom Lineage Panel */}
          {renderPanel('lineage', `Rebloom Lineage (${snapshot.rebloom_lineage.length})`, '🌸', (
            <div className="lineage-list">
              {snapshot.rebloom_lineage.slice(-10).map((lineage, index) => (
                <div key={index} className="lineage-item">
                  <div className="lineage-connection">
                    <span className="lineage-parent">{lineage.parent_id}</span>
                    <span className="lineage-arrow">→</span>
                    <span className="lineage-child">{lineage.child_id}</span>
                  </div>
                  <div className="lineage-details">
                    <span className="lineage-method">{lineage.method}</span>
                    <span className="lineage-depth">Depth: {lineage.depth}</span>
                    <span className="lineage-significance">
                      Sig: {(lineage.significance * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
              {snapshot.rebloom_lineage.length === 0 && (
                <div className="empty-content">No rebloom lineage data</div>
              )}
            </div>
          ))}

          {/* Voice Events Panel */}
          {renderPanel('voice', `Voice Events (${snapshot.spoken_events.length})`, '🔊', (
            <div className="voice-events-list">
              {snapshot.spoken_events.slice(-10).map((event, index) => (
                <div key={index} className="voice-event-item">
                  <div className="voice-event-header">
                    <span className="voice-event-type">{event.tracer_type || 'SYSTEM'}</span>
                    <span className="voice-event-time">{formatDuration(event.timestamp)}</span>
                  </div>
                  <div className="voice-event-text">"{event.text}"</div>
                </div>
              ))}
              {snapshot.spoken_events.length === 0 && (
                <div className="empty-content">No voice events recorded</div>
              )}
            </div>
          ))}

          {/* Voice Modulations Panel */}
          {snapshot.voice_modulations.length > 0 && renderPanel('modulations', `Voice Modulations (${snapshot.voice_modulations.length})`, '🎤', (
            <div className="modulations-list">
              {snapshot.voice_modulations.slice(-5).map((mod, index) => (
                <div key={index} className="modulation-item">
                  <div className="modulation-header">
                    <span
                      className="modulation-mood"
                      style={{ color: getMoodColor(mod.mood) }}
                    >
                      {mod.mood}
                    </span>
                    <span className="modulation-entropy">E: {mod.entropy.toFixed(2)}</span>
                    <span className="modulation-time">{formatDuration(mod.timestamp)}</span>
                  </div>
                  <div className="modulation-profile">
                    <span>Rate: {mod.voice_profile.rate} WPM</span>
                    <span>Volume: {(mod.voice_profile.volume * 100).toFixed(0)}%</span>
                    <span>Pitch: {mod.voice_profile.pitch_modifier > 0 ? '+' : ''}{mod.voice_profile.pitch_modifier}</span>
                  </div>
                </div>
              ))}
            </div>
          ))}

          {/* Mycelium Graph Panel */}
          {snapshot.mycelium_graph && renderPanel('mycelium', 'Memory Network Graph', '🧬', (
            renderMyceliumMiniGraph(snapshot.mycelium_graph)
          ))}

          {/* System Status Panel */}
          {renderPanel('status', 'System Status', '⚙️', (
            <div className="status-grid">
              <div className="status-section">
                <h4>Component Status</h4>
                <div className="status-list">
                  {Object.entries(snapshot.component_status).map(([component, status]) => (
                    <div key={component} className="status-item">
                      <span className={`status-indicator ${status ? 'active' : 'inactive'}`}>
                        {status ? '✅' : '❌'}
                      </span>
                      <span className="status-label">{component}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="status-section">
                <h4>Log File Sizes</h4>
                <div className="status-list">
                  {Object.entries(snapshot.log_file_sizes).map(([file, size]) => (
                    <div key={file} className="status-item">
                      <span className="status-label">{file}</span>
                      <span className="status-value">
                        {size > 0 ? `${(size / 1024).toFixed(1)} KB` : '0 B'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CognitionReplayDashboard; 