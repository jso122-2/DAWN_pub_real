import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { ConnectionStatus } from './ConnectionStatus';
import './Dashboard.css';

interface SystemState {
  tick: number;
  scup: number;
  entropy: number;
  mood: string;
}

export const Dashboard: React.FC = () => {
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [response, setResponse] = useState<string | null>(null);
  const { connected, connect, on, send } = useWebSocket();

  useEffect(() => {
    const handleConnectionStatus = (data: any) => {
      console.log('Connection status:', data);
    };

    const handleSystemState = (data: any) => {
      if (data && typeof data === 'object') {
        setSystemState(data);
      }
    };

    const handleResponse = (data: any) => {
      setResponse(data.message || JSON.stringify(data));
    };

    // Add message handlers
    on('connection_status', handleConnectionStatus);
    on('system_state', handleSystemState);
    on('response', handleResponse);

    // Connect to WebSocket
    connect();

    // Cleanup
    return () => {
      // No need to remove handlers as they are managed by the hook
    };
  }, [connect, on]);

  const handleCommand = (command: string) => {
    if (!connected) return;

    send({
      type: 'command',
      content: command,
      timestamp: Date.now()
    });
  };

  return (
    <div className="dashboard">
      <ConnectionStatus />
      
      <div className="dashboard-content">
        <div className="system-metrics">
          {systemState && (
            <>
              <div className="metric">
                <span className="label">TICK:</span>
                <span className="value">{systemState.tick}</span>
              </div>
              <div className="metric">
                <span className="label">SCUP:</span>
                <span className="value">{systemState.scup}%</span>
              </div>
              <div className="metric">
                <span className="label">ENTROPY:</span>
                <span className="value">{systemState.entropy.toFixed(3)}</span>
              </div>
              <div className="metric">
                <span className="label">MOOD:</span>
                <span className="value">{systemState.mood}</span>
              </div>
            </>
          )}
        </div>

        {response && (
          <div className="response-container">
            <pre className="response">{response}</pre>
          </div>
        )}
      </div>
    </div>
  );
}; 