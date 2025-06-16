import { useEffect, useState } from 'react';

interface ConnectionStatus {
  vite: boolean;
  websocket: boolean;
}

const ConnectionStatusBadge = () => {
  const [status, setStatus] = useState<ConnectionStatus>({ vite: true, websocket: false });
  const [showTooltip, setShowTooltip] = useState(false);

  useEffect(() => {
    const checkViteHealth = async () => {
      try {
        const response = await fetch('/@vite/client');
        setStatus(prev => ({ ...prev, vite: response.ok }));
      } catch (error) {
        setStatus(prev => ({ ...prev, vite: false }));
      }
    };

    const checkWebSocket = () => {
      // Check if WebSocket is connected by looking for the WebSocketManager instance
      const wsConnected = window.WebSocket && 
        document.querySelector('[data-websocket-connected="true"]') !== null;
      setStatus(prev => ({ ...prev, websocket: wsConnected }));
    };

    // Check immediately and then every 5 seconds
    checkViteHealth();
    checkWebSocket();
    const interval = setInterval(() => {
      checkViteHealth();
      checkWebSocket();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    if (status.vite && status.websocket) return '#10b981'; // Green
    if (status.vite || status.websocket) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getStatusText = () => {
    if (status.vite && status.websocket) return 'All Systems Connected';
    if (status.vite) return 'Vite Connected, WebSocket Disconnected';
    if (status.websocket) return 'WebSocket Connected, Vite Disconnected';
    return 'All Systems Disconnected';
  };

  return (
    <div 
      style={{
        position: 'fixed',
        top: '1rem',
        right: '1rem',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        padding: '0.5rem 1rem',
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderRadius: '1rem',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        cursor: 'help'
      }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <div
        style={{
          width: '0.75rem',
          height: '0.75rem',
          borderRadius: '50%',
          backgroundColor: getStatusColor(),
          boxShadow: `0 0 8px ${getStatusColor()}`,
          transition: 'all 0.3s ease'
        }}
      />
      {showTooltip && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            right: 0,
            marginTop: '0.5rem',
            padding: '0.5rem 1rem',
            background: 'rgba(0, 0, 0, 0.8)',
            borderRadius: '0.5rem',
            fontSize: '0.875rem',
            whiteSpace: 'nowrap',
            pointerEvents: 'none'
          }}
        >
          {getStatusText()}
        </div>
      )}
    </div>
  );
};

export default ConnectionStatusBadge; 