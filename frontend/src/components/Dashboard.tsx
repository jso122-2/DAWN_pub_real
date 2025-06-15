import React, { useEffect, useState } from 'react';
import { wsService } from '../services/websocket';
import './Dashboard.css';

interface Message {
  id: string;
  content: string;
  timestamp: number;
  type: 'user' | 'system';
}

interface SystemState {
  consciousness_state: string;
}

export const Dashboard: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    const handleConnectionStatus = (status: string) => {
      setIsConnected(status === 'connected');
    };

    const handleSystemState = (data: any) => {
      if (data && typeof data === 'object') {
        setSystemState(data);
      }
    };

    const handleResponse = (data: any) => {
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        content: data.content,
        timestamp: Date.now(),
        type: 'system'
      }]);
    };

    // Subscribe to events
    wsService.on('connection_status', handleConnectionStatus);
    wsService.on('system_state', handleSystemState);
    wsService.on('response', handleResponse);

    // Connect to WebSocket
    wsService.connect();

    return () => {
      // Cleanup
      wsService.off('connection_status', handleConnectionStatus);
      wsService.off('system_state', handleSystemState);
      wsService.off('response', handleResponse);
      wsService.disconnect();
    };
  }, []);

  const sendMessage = () => {
    if (!isConnected || !input.trim()) return;

    // Add user message to display
    setMessages(prev => [...prev, {
      id: Date.now().toString(),
      content: input,
      timestamp: Date.now(),
      type: 'user'
    }]);

    // Send to server
    wsService.send('message', {
      content: input,
      timestamp: Date.now()
    });

    setInput('');
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>DAWN Dashboard</h1>
        {systemState && (
          <div className="state-info">
            State: {systemState.consciousness_state}
          </div>
        )}
      </div>

      <div className="messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message ${msg.type}`}>
            <span className="timestamp">
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
            <span className="content">{msg.content}</span>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Send a message..."
          disabled={!isConnected}
        />
        <button onClick={sendMessage} disabled={!isConnected}>
          Send
        </button>
      </div>
    </div>
  );
}; 