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
  mood: string;
  entropy: number;
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
    wsService.on('tick_update', (data: any) => {
      setSystemState(data.state);
    });

    wsService.on('response', (data: any) => {
      addDAWNMessage(data.content, data.metadata);
      setIsProcessing(false);
    });

    wsService.on('visualization', (data: any) => {
      handleVisualization(data);
    });

    wsService.on('process_event', (data: any) => {
      handleProcessEvent(data);
    });

    wsService.on('consciousness_shift', (data: any) => {
      addSystemMessage(`Consciousness shift: ${data.from} → ${data.to}`);
    });

    // Request initial state
    wsService.send('init', {
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
    wsService.send('message', {
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
        wsService.send('get_status', {});
        break;
      
      case '/viz':
        toggleVisualization(parts[1]);
        break;
      
      case '/process':
        manageProcess(parts[1], parts[2]);
        break;
      
      case '/entropy':
        wsService.send('adjust_entropy', { value: parseFloat(parts[1]) });
        break;
      
      case '/mood':
        wsService.send('set_mood', { mood: parts[1] });
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
      wsService.send('disable_viz', { viz: vizType });
    } else {
      updated.add(vizType);
      wsService.send('enable_viz', { viz: vizType });
    }
    setActiveVisualizations(updated);
  };

  const manageProcess = (action: string, process: string) => {
    wsService.send('process_control', {
      action,
      process
    });
  };

  const showHelp = () => {
    addSystemMessage(`
Available commands:
/status - Show system status
/viz [type] - Toggle visualization
/process [action] [name] - Control processes
/entropy [value] - Adjust entropy
/mood [mood] - Set system mood
/help - Show this help
    `);
  };

  return (
    <div className="talk-interface">
      <div className="messages" ref={terminalRef}>
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <div className="message-header">
              <span className="timestamp">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
              {msg.type === 'dawn' && msg.metadata?.tick && (
                <span className="tick">Tick #{msg.metadata.tick}</span>
              )}
            </div>
            <div className="message-content">{msg.content}</div>
            {msg.type === 'dawn' && msg.metadata && (
              <div className="message-metadata">
                {msg.metadata.scup && (
                  <span className="scup">SCUP: {msg.metadata.scup}%</span>
                )}
                {msg.metadata.mood && (
                  <span className="mood">Mood: {msg.metadata.mood}</span>
                )}
                {msg.metadata.process && (
                  <span className="process">Process: {msg.metadata.process}</span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="input-area">
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
          placeholder="Type a message or command..."
          disabled={isProcessing}
        />
        <button onClick={sendMessage} disabled={isProcessing || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}; 