import React, { useState, useEffect } from 'react';

interface WebSocketStatusProps {
  className?: string;
}

export const WebSocketStatus: React.FC<WebSocketStatusProps> = ({ className = '' }) => {
  const [status, setStatus] = useState<'connected' | 'connecting' | 'disconnected'>('disconnected');
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    // Simulate WebSocket connection status changes
    const interval = setInterval(() => {
      const states: Array<'connected' | 'connecting' | 'disconnected'> = ['connected', 'connecting', 'disconnected'];
      const randomState = states[Math.floor(Math.random() * states.length)];
      setStatus(randomState);
      setLastUpdate(new Date());
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'text-green-500';
      case 'connecting':
        return 'text-yellow-500';
      case 'disconnected':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'ONLINE';
      case 'connecting':
        return 'CONNECTING...';
      case 'disconnected':
        return 'OFFLINE';
      default:
        return 'UNKNOWN';
    }
  };

  return (
    <div className={`terminal-module ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`status-indicator ${status === 'connected' ? 'online' : 'offline'}`} />
          <span className={`terminal-text ${getStatusColor()}`}>{getStatusText()}</span>
        </div>
        <div className="terminal-text text-sm text-gray-400">
          Last Update: {lastUpdate.toLocaleTimeString()}
        </div>
      </div>
      
      <div className="mt-2">
        <div className="metric">
          <span className="metric-label">Connection Status</span>
          <span className={`metric-value ${getStatusColor()}`}>{getStatusText()}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Last Update</span>
          <span className="metric-value">{lastUpdate.toLocaleTimeString()}</span>
        </div>
        <div className="metric">
          <span className="metric-label">Uptime</span>
          <span className="metric-value">00:00:00</span>
        </div>
      </div>
    </div>
  );
}; 