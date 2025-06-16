import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import './TalkToInterface.css';

interface Message {
  type: string;
  content: string;
  timestamp: number;
}

export const TalkToInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const { connected, connect, on, send } = useWebSocket();

  useEffect(() => {
    const handleTickUpdate = (data: any) => {
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Tick: ${data.tick}`,
        timestamp: Date.now()
      }]);
    };

    const handleResponse = (data: any) => {
      setMessages(prev => [...prev, {
        type: 'system',
        content: data.message || JSON.stringify(data),
        timestamp: Date.now()
      }]);
    };

    const handleVisualization = (data: any) => {
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Visualization: ${data.type}`,
        timestamp: Date.now()
      }]);
    };

    const handleProcessEvent = (data: any) => {
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Process: ${data.event}`,
        timestamp: Date.now()
      }]);
    };

    const handleConsciousnessShift = (data: any) => {
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Consciousness Shift: ${data.state}`,
        timestamp: Date.now()
      }]);
    };

    // Add message handlers
    on('tick_update', handleTickUpdate);
    on('response', handleResponse);
    on('visualization', handleVisualization);
    on('process_event', handleProcessEvent);
    on('consciousness_shift', handleConsciousnessShift);

    // Connect to WebSocket
    connect();

    // Initialize connection
    send({
      type: 'init',
      data: {
        client: 'web',
        version: '1.0.0'
      }
    });

    // Cleanup
    return () => {
      // No need to remove handlers as they are managed by the hook
    };
  }, [connect, on, send]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !connected) return;

    // Add user message
    const userMessage: Message = {
      type: 'user',
      content: input,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, userMessage]);

    // Send to server
    send({
      type: 'message',
      data: {
        content: input,
        timestamp: Date.now()
      }
    });

    // Clear input
    setInput('');

    // Handle special commands
    const parts = input.toLowerCase().split(' ');
    if (parts[0] === 'status') {
      send({
        type: 'get_status',
        data: {}
      });
    } else if (parts[0] === 'entropy' && parts[1]) {
      send({
        type: 'adjust_entropy',
        data: { value: parseFloat(parts[1]) }
      });
    } else if (parts[0] === 'mood' && parts[1]) {
      send({
        type: 'set_mood',
        data: { mood: parts[1] }
      });
    } else if (parts[0] === 'disable' && parts[1]) {
      const vizType = parts[1];
      send({
        type: 'disable_viz',
        data: { viz: vizType }
      });
    } else if (parts[0] === 'enable' && parts[1]) {
      const vizType = parts[1];
      send({
        type: 'enable_viz',
        data: { viz: vizType }
      });
    } else if (parts[0] === 'process' && parts[1]) {
      send({
        type: 'process_control',
        data: {
          action: parts[1],
          params: parts.slice(2)
        }
      });
    }
  };

  return (
    <div className="talk-to-interface">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.type}`}>
            <span className="timestamp">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
            <span className="content">{msg.content}</span>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={connected ? "Type a message..." : "Connecting..."}
          disabled={!connected}
        />
        <button type="submit" disabled={!connected}>
          Send
        </button>
      </form>
    </div>
  );
}; 