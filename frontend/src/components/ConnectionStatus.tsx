import React, { useState, useEffect } from 'react';
import { wsService } from '../services/websocket';
import './ConnectionStatus.css';

interface SystemState {
  tick: number;
  scup: number;
  entropy: number;
  mood: string;
}

export const ConnectionStatus: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [systemState, setSystemState] = useState<SystemState | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleConnectionStatus = (status: string) => {
      setIsConnected(status === 'connected');
    };

    const handleSystemState = (data: any) => {
      if (data && typeof data === 'object') {
        setSystemState(data);
      }
    };

    const handleError = (err: any) => {
      setError(err.message || 'Connection error');
    };

    // Subscribe to events
    wsService.on('connection_status', handleConnectionStatus);
    wsService.on('system_state', handleSystemState);
    wsService.on('error', handleError);

    // Connect to WebSocket
    wsService.connect();

    return () => {
      // Cleanup
      wsService.off('connection_status', handleConnectionStatus);
      wsService.off('system_state', handleSystemState);
      wsService.off('error', handleError);
      wsService.disconnect();
    };
  }, []);

  return (
    <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
      <div className="status-indicator">
        <span className="status-dot"></span>
        <span className="status-text">
          {isConnected ? 'CONNECTED' : 'DISCONNECTED'}
        </span>
      </div>
      
      {isConnected && systemState && (
        <div className="system-metrics">
          <span>TICK: {systemState.tick}</span>
          <span>SCUP: {systemState.scup}%</span>
          <span>ENTROPY: {systemState.entropy.toFixed(3)}</span>
          <span>MOOD: {systemState.mood}</span>
        </div>
      )}
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
    </div>
  );
}; 