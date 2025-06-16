import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import './ConnectionStatus.css';

interface ConnectionStatusProps {
  className?: string;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ className }) => {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected');
  const [systemState, setSystemState] = useState<string>('initializing');
  const [error, setError] = useState<string | null>(null);
  const { connected, connect, on } = useWebSocket();

  useEffect(() => {
    const handleConnectionStatus = (data: any) => {
      setStatus(data.status);
      setError(null);
    };

    const handleSystemState = (data: any) => {
      setSystemState(data.state);
    };

    const handleError = (data: any) => {
      setError(data.message);
      setStatus('disconnected');
    };

    // Add message handlers
    on('connection_status', handleConnectionStatus);
    on('system_state', handleSystemState);
    on('error', handleError);

    // Connect to WebSocket
    connect();

    // Cleanup
    return () => {
      // No need to remove handlers as they are managed by the hook
    };
  }, [connect, on]);

  return (
    <div className={`connection-status ${className || ''}`}>
      <div className="status-indicator">
        <span className={`status-dot ${status}`} />
        <span className="status-text">{status}</span>
      </div>
      {systemState && (
        <div className="system-state">
          <span className="state-label">System State:</span>
          <span className="state-value">{systemState}</span>
        </div>
      )}
      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span className="error-text">{error}</span>
        </div>
      )}
    </div>
  );
}; 