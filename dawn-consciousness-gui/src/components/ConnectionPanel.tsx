import React, { useState } from 'react';

interface ConnectionPanelProps {
  connected: boolean;
  connecting: boolean;
  error: string | null;
  mmapPath: string;
  onMmapPathChange: (path: string) => void;
  onConnect: () => void;
  autoConnect: boolean;
  onAutoConnectChange: (auto: boolean) => void;
}

const ConnectionPanel: React.FC<ConnectionPanelProps> = ({
  connected,
  connecting,
  error,
  mmapPath,
  onMmapPathChange,
  onConnect,
  autoConnect,
  onAutoConnectChange
}) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusText = () => {
    if (connecting) return 'CONNECTING...';
    if (connected) return 'CONNECTED';
    if (error) return 'CONNECTION ERROR';
    return 'DISCONNECTED';
  };

  const getStatusClass = () => {
    if (connecting) return 'connecting';
    if (connected) return 'connected';
    if (error) return 'error';
    return 'disconnected';
  };

  return (
    <div className={`connection-panel ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="panel-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="connection-indicator">
          <div className={`status-light ${getStatusClass()}`} />
          <span className="status-text">{getStatusText()}</span>
        </div>
        
        <div className="expand-arrow">
          {isExpanded ? '▼' : '▲'}
        </div>
      </div>

      {isExpanded && (
        <div className="panel-content">
          <div className="connection-settings">
            <div className="setting-group">
              <label className="tech-label">Memory-Mapped File Path</label>
              <input
                type="text"
                value={mmapPath}
                onChange={(e) => onMmapPathChange(e.target.value)}
                className="path-input"
                placeholder="./runtime/dawn_consciousness.mmap"
                disabled={connected}
              />
            </div>

            <div className="setting-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={autoConnect}
                  onChange={(e) => onAutoConnectChange(e.target.checked)}
                  className="auto-connect-checkbox"
                />
                <span className="tech-label">Auto-connect on launch</span>
              </label>
            </div>

            <div className="connection-actions">
              <button
                onClick={onConnect}
                disabled={connecting}
                className={`connect-button ${connected ? 'disconnect' : 'connect'}`}
              >
                {connecting ? (
                  <>
                    <div className="spinner" />
                    CONNECTING...
                  </>
                ) : connected ? (
                  'DISCONNECT'
                ) : (
                  'CONNECT'
                )}
              </button>
            </div>

            {error && (
              <div className="error-display">
                <div className="tech-label">Error Details</div>
                <div className="error-text">{error}</div>
              </div>
            )}

            <div className="connection-info">
              <div className="tech-label">Connection Protocol</div>
              <div className="protocol-details">
                <div>• Memory-mapped file I/O</div>
                <div>• 60Hz consciousness polling</div>
                <div>• Zero-latency local interface</div>
                <div>• No network dependencies</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConnectionPanel; 