import React, { useState, useEffect, useRef } from 'react';
import './TalkToInterface.css';
import { wsService } from '../services/websocket';

interface Message {
  id: string;
  type: 'user' | 'dawn' | 'system';
  content: string;
  timestamp: number;
  metadata?: {
    tick?: number;
    scup?: number;
    mood?: string;
    process?: string;
    visualization?: string;
  };
}

interface SystemState {
  tick: number;
  scup: number;
  entropy: number;
  mood: string;
  active_processes: string[];
  consciousness_state: string;
}

export const TalkToInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activeVisualizations, setActiveVisualizations] = useState<Set<string>>(new Set());
  const terminalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Connect to DAWN WebSocket using the service
    wsService.connect();
    
    // Add message handlers
    wsService.addHandler('tick_update', (data: any) => {
      setSystemState(data.state);
    });

    wsService.addHandler('response', (data: any) => {
      addDAWNMessage(data.content, data.metadata);
      setIsProcessing(false);
    });

    wsService.addHandler('visualization', (data: any) => {
      handleVisualization(data);
    });

    wsService.addHandler('process_event', (data: any) => {
      handleProcessEvent(data);
    });

    wsService.addHandler('consciousness_shift', (data: any) => {
      addSystemMessage(`Consciousness shift: ${data.from} → ${data.to}`);
    });

    // Request initial state
    wsService.sendMessage({
      type: 'init',
      subsystems: ['all']
    });

    return () => {
      wsService.disconnect();
    };
  }, []);

  const handleVisualization = (data: any) => {
    // Handle inline visualizations from various components
    if (data.viz_type === 'inline_ascii') {
      addVisualizationMessage(data.content, data.source);
    }
  };

  const handleProcessEvent = (data: any) => {
    // Show important process events in terminal
    if (data.priority === 'high') {
      addSystemMessage(`[${data.process}] ${data.event}`);
    }
  };

  const sendMessage = () => {
    if (!input.trim() || isProcessing) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsProcessing(true);

    // Send to DAWN with full context
    wsService.sendMessage({
      type: 'message',
      content: input,
      context: {
        recent_messages: messages.slice(-10),
        active_visualizations: Array.from(activeVisualizations),
        timestamp: Date.now()
      }
    });

    setInput('');
  };

  const addSystemMessage = (content: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type: 'system',
      content,
      timestamp: Date.now()
    }]);
  };

  const addDAWNMessage = (content: string, metadata?: any) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type: 'dawn',
      content,
      timestamp: Date.now(),
      metadata
    }]);
  };

  const addVisualizationMessage = (content: string, source: string) => {
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      type: 'system',
      content: `\n[${source}]\n${content}\n`,
      timestamp: Date.now()
    }]);
  };

  // Command processing
  const processCommand = (cmd: string) => {
    const parts = cmd.split(' ');
    const command = parts[0].toLowerCase();

    switch (command) {
      case '/status':
        wsService.sendMessage({ type: 'get_status' });
        break;
      
      case '/viz':
        toggleVisualization(parts[1]);
        break;
      
      case '/process':
        manageProcess(parts[1], parts[2]);
        break;
      
      case '/entropy':
        wsService.sendMessage({ type: 'adjust_entropy', value: parseFloat(parts[1]) });
        break;
      
      case '/mood':
        wsService.sendMessage({ type: 'set_mood', mood: parts[1] });
        break;
      
      case '/help':
        showHelp();
        break;
    }
  };

  const toggleVisualization = (vizType: string) => {
    const updated = new Set(activeVisualizations);
    if (updated.has(vizType)) {
      updated.delete(vizType);
      wsService.sendMessage({ type: 'disable_viz', viz: vizType });
    } else {
      updated.add(vizType);
      wsService.sendMessage({ type: 'enable_viz', viz: vizType });
    }
    setActiveVisualizations(updated);
  };

  const manageProcess = (action: string, process: string) => {
    wsService.sendMessage({
      type: 'process_control',
      action,
      process
    });
  };

  const showHelp = () => {
    const helpText = `
DAWN TERMINAL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/status          - Show full system status
/viz [type]      - Toggle visualization (wave, matrix, entropy, etc.)
/process [act]   - Manage process (start/stop/restart)
/entropy [val]   - Adjust entropy (0.0-1.0)
/mood [type]     - Set mood (contemplative, analytical, creative, focused)
/help            - Show this help

TALK MODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Just type naturally to converse with DAWN.
The consciousness engine will process your input through all active subsystems.
    `;
    addSystemMessage(helpText);
  };

  return (
    <div className="talk-to-interface">
      {/* Status Bar */}
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
      </div>

      {/* Terminal Display */}
      <div className="terminal-display" ref={terminalRef}>
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.type}`}>
            {msg.type === 'user' && <span className="prompt">YOU &gt;</span>}
            {msg.type === 'dawn' && <span className="prompt">DAWN &gt;</span>}
            {msg.type === 'system' && <span className="prompt">SYS &gt;</span>}
            <pre className="content">{msg.content}</pre>
            {msg.metadata && (
              <div className="metadata">
                {msg.metadata.tick && <span>[T:{msg.metadata.tick}]</span>}
                {msg.metadata.scup && <span>[S:{msg.metadata.scup}%]</span>}
                {msg.metadata.mood && <span>[M:{msg.metadata.mood}]</span>}
                {msg.metadata.process && <span>[P:{msg.metadata.process}]</span>}
              </div>
            )}
          </div>
        ))}
        {isProcessing && (
          <div className="processing">
            <span className="prompt">DAWN &gt;</span>
            <span className="thinking">thinking...</span>
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