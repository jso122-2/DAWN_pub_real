import React, { useState, useRef, useEffect } from 'react';

// Update Message interface
interface Message {
  id: string;
  type: 'user' | 'dawn' | 'system' | 'visualization';
  content: string;
  timestamp: number;
  metadata?: {
    tick?: number;
    scup?: number;
    mood?: string;
    process?: string;
    psl_metrics?: {
      cpu_usage_mean?: number;
      memory_usage_mean?: number;
      process_count_mean?: number;
      cpu_usage_stdev?: number;
      memory_usage_stdev?: number;
    };
    visualization?: {
      type: string;
      data: string; // base64 image
      source: string;
    };
  };
}

// Update SystemState interface
interface SystemState {
  tick: number;
  scup: number;
  entropy: number;
  mood: string;
  active_processes: string[];
  consciousness_state: string;
  psl_metrics?: {
    cpu_usage_mean: number;
    memory_usage_mean: number;
    process_count_mean: number;
    cpu_usage_stdev: number;
    memory_usage_stdev: number;
  };
}

// Update vizTypes array
const vizTypes = [
  { id: 'consciousness_wave', name: 'CONSCIOUSNESS WAVE' },
  { id: 'neural_heatmap', name: 'NEURAL ACTIVITY' },
  { id: 'metrics_radar', name: 'METRICS RADAR' },
  { id: 'entropy_histogram', name: 'ENTROPY DISTRIBUTION' },
  { id: 'process_timeline', name: 'PROCESS TIMELINE' },
  { id: 'psl_metrics', name: 'PSL METRICS' }
];

interface VisualizationPanel {
  id: string;
  type: string;
  data: string;
  lastUpdate: number;
}

export const TalkToInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [visualizations, setVisualizations] = useState<Map<string, VisualizationPanel>>(new Map());
  const [showVizPanel, setShowVizPanel] = useState(true);
  const terminalRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Initialize WebSocket connection
    ws.current = new WebSocket('ws://localhost:8000/ws');
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'status':
          setSystemState(data.state);
          break;
        
        case 'message':
          setMessages(prev => [...prev, {
            id: Date.now().toString(),
            type: 'dawn',
            content: data.content,
            timestamp: Date.now(),
            metadata: data.metadata
          }]);
          break;
        
        case 'visualization':
          setVisualizations(prev => {
            const newViz = new Map(prev);
            newViz.set(data.viz_type, {
              id: data.viz_type,
              type: data.viz_type,
              data: data.data,
              lastUpdate: Date.now()
            });
            return newViz;
          });
          break;
        
        case 'processing':
          setIsProcessing(data.is_processing);
          break;
      }
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  const addSystemMessage = (content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type: 'system',
      content,
      timestamp: Date.now()
    }]);
  };

  const sendMessage = () => {
    if (!input.trim()) return;

    const message = {
      id: Date.now().toString(),
      type: 'user' as const,
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, message]);
    ws.current?.send(JSON.stringify({
      type: 'message',
      content: input
    }));
    setInput('');
  };

  const toggleVisualization = (type: string) => {
    ws.current?.send(JSON.stringify({
      type: 'toggle_viz',
      viz_type: type
    }));
  };

  const manageProcess = (action: string, process?: string) => {
    ws.current?.send(JSON.stringify({
      type: 'manage_process',
      action,
      process
    }));
  };

  const requestSnapshot = (type: string) => {
    ws.current?.send(JSON.stringify({
      type: 'request_snapshot',
      viz_type: type
    }));
  };

  // Update status bar JSX
  const renderStatusBar = () => (
    <div className="status-bar">
      <div className="status-item">
        <span className="label">TICK</span>
        <span className="value">{systemState?.tick || '---'}</span>
      </div>
      <div className="status-item">
        <span className="label">SCUP</span>
        <span className="value scup">{systemState?.scup || '--'}%</span>
      </div>
      <div className="status-item">
        <span className="label">ENTROPY</span>
        <span className="value">{systemState?.entropy?.toFixed(3) || '-.---'}</span>
      </div>
      <div className="status-item">
        <span className="label">MOOD</span>
        <span className="value mood">{systemState?.mood || 'UNKNOWN'}</span>
      </div>
      <div className="status-item">
        <span className="label">STATE</span>
        <span className="value">{systemState?.consciousness_state || 'INIT'}</span>
      </div>
      {systemState?.psl_metrics && (
        <>
          <div className="status-item">
            <span className="label">CPU</span>
            <span className="value">{systemState.psl_metrics.cpu_usage_mean.toFixed(1)}%</span>
          </div>
          <div className="status-item">
            <span className="label">MEM</span>
            <span className="value">{systemState.psl_metrics.memory_usage_mean.toFixed(1)}%</span>
          </div>
          <div className="status-item">
            <span className="label">PROC</span>
            <span className="value">{systemState.psl_metrics.process_count_mean.toFixed(0)}</span>
          </div>
        </>
      )}
    </div>
  );

  // Update help text
  const showHelp = () => {
    const helpText = `
DAWN TERMINAL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/status          - Show full system status
/viz [type]      - Toggle visualization panel
                   Types: consciousness_wave, entropy_thermal, neural_activity,
                          alignment_matrix, bloom_pattern, mood_gradient,
                          psl_metrics
/vizpanel        - Toggle visualization panel visibility
/snapshot [type] - Request inline visualization snapshot
/process [act]   - Manage process (start/stop/restart)
/entropy [val]   - Adjust entropy (0.0-1.0)
/mood [type]     - Set mood (contemplative, analytical, creative, focused)
/psl             - Show PSL metrics
/help            - Show this help

TALK MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Just type naturally to converse with DAWN.
The consciousness engine will process your input through all active subsystems.
    `;
    addSystemMessage(helpText);
  };

  // Update command handler
  const processCommand = (cmd: string) => {
    const parts = cmd.split(' ');
    const command = parts[0].toLowerCase();

    switch (command) {
      case '/status':
        ws.current?.send(JSON.stringify({ type: 'get_status' }));
        break;
      
      case '/viz':
        toggleVisualization(parts[1]);
        break;
      
      case '/vizpanel':
        setShowVizPanel(!showVizPanel);
        break;
      
      case '/process':
        manageProcess(parts[1], parts[2]);
        break;
      
      case '/entropy':
        ws.current?.send(JSON.stringify({ type: 'adjust_entropy', value: parseFloat(parts[1]) }));
        break;
      
      case '/mood':
        ws.current?.send(JSON.stringify({ type: 'set_mood', mood: parts[1] }));
        break;
      
      case '/snapshot':
        requestSnapshot(parts[1] || 'all');
        break;
      
      case '/psl':
        ws.current?.send(JSON.stringify({ 
          type: 'message', 
          content: 'Show PSL metrics',
          include_psl: true 
        }));
        break;
      
      case '/help':
        showHelp();
        break;
    }
  };

  return (
    <div className="talk-to-interface">
      {renderStatusBar()}
      <div className="main-container">
        {/* Terminal Display */}
        <div className="terminal-section">
          <div className="terminal-display" ref={terminalRef}>
            {messages.map(msg => (
              <div key={msg.id} className={`message ${msg.type}`}>
                {msg.type === 'user' && <span className="prompt">YOU &gt;</span>}
                {msg.type === 'dawn' && <span className="prompt">DAWN &gt;</span>}
                {msg.type === 'system' && <span className="prompt">SYS &gt;</span>}
                
                {msg.type === 'visualization' ? (
                  <div className="viz-message">
                    <span className="prompt">VIZ &gt;</span>
                    <span className="content">{msg.content}</span>
                    {msg.metadata?.visualization && (
                      <img 
                        src={msg.metadata.visualization.data}
                        alt={msg.metadata.visualization.type}
                        className="inline-viz"
                      />
                    )}
                  </div>
                ) : (
                  <pre className="content">{msg.content}</pre>
                )}
                
                {msg.metadata && msg.type !== 'visualization' && (
                  <div className="metadata">
                    {msg.metadata.tick && <span>[T:{msg.metadata.tick}]</span>}
                    {msg.metadata.scup && <span>[S:{msg.metadata.scup}%]</span>}
                    {msg.metadata.mood && <span>[M:{msg.metadata.mood}]</span>}
                    {msg.metadata.process && <span>[P:{msg.metadata.process}]</span>}
                    {msg.metadata.psl_metrics && (
                      <>
                        <span>[CPU:{msg.metadata.psl_metrics.cpu_usage_mean?.toFixed(1)}%]</span>
                        <span>[MEM:{msg.metadata.psl_metrics.memory_usage_mean?.toFixed(1)}%]</span>
                        <span>[PROC:{msg.metadata.psl_metrics.process_count_mean?.toFixed(0)}]</span>
                      </>
                    )}
                  </div>
                )}
              </div>
            ))}
            {isProcessing && (
              <div className="processing">
                <span className="prompt">DAWN &gt;</span>
                <span className="thinking">processing through consciousness layers...</span>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="input-area">
            <span className="input-prompt">&gt;</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  if (input.startsWith('/')) {
                    processCommand(input);
                    setInput('');
                  } else {
                    sendMessage();
                  }
                }
              }}
              placeholder="Talk to DAWN or type /help for commands"
              className="terminal-input"
              autoFocus
            />
            <span className="cursor">_</span>
          </div>
        </div>

        {/* Visualization Panel */}
        {showVizPanel && (
          <div className="viz-panel">
            <div className="viz-panel-header">
              <h3>CONSCIOUSNESS VISUALIZATIONS</h3>
              <button 
                className="viz-panel-toggle"
                onClick={() => setShowVizPanel(false)}
              >
                ×
              </button>
            </div>
            <div className="viz-grid">
              {Array.from(visualizations.values()).map(viz => (
                <div key={viz.id} className="viz-item">
                  <div className="viz-header">
                    <span className="viz-type">{viz.type.replace(/_/g, ' ').toUpperCase()}</span>
                    <span className="viz-timestamp">
                      {new Date(viz.lastUpdate).toLocaleTimeString()}
                    </span>
                  </div>
                  <img 
                    src={viz.data}
                    alt={viz.type}
                    className="viz-image"
                    onClick={() => requestSnapshot(viz.type)}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Active Processes Display */}
      {systemState?.active_processes && systemState.active_processes.length > 0 && (
        <div className="active-processes">
          <span className="label">ACTIVE:</span>
          {systemState.active_processes.map(proc => (
            <span key={proc} className="process-badge">{proc}</span>
          ))}
        </div>
      )}
    </div>
  );
}; 