import React, { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import './MatplotlibVisualizer.css';

interface VisualizationData {
  type: string;
  data: any;
  timestamp: number;
}

export const MatplotlibVisualizer: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { connected, connect, on, send } = useWebSocket();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const handleConnectionStatus = (data: any) => {
      setIsConnected(data.status === 'connected');
      setError(null);
    };

    const handleMessage = (data: VisualizationData) => {
      if (data.type === 'matplotlib' && canvasRef.current) {
        const ctx = canvasRef.current.getContext('2d');
        if (ctx) {
          // Handle matplotlib data rendering
          // This is a placeholder - actual rendering logic will depend on the data format
          console.log('Received visualization data:', data);
        }
      }
    };

    // Add message handlers
    on('connection_status', handleConnectionStatus);
    on('visualization', handleMessage);

    // Connect to WebSocket
    connect();

    // Request visualization data
    send({
      type: 'visualization_request',
      data: { type: 'matplotlib' }
    });

    // Cleanup
    return () => {
      // No need to remove handlers as they are managed by the hook
    };
  }, [connect, on, send]);

  return (
    <div className="matplotlib-visualizer">
      <div className="status-bar">
        <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
        {error && <span className="error-message">{error}</span>}
      </div>
      <canvas ref={canvasRef} className="visualization-canvas" />
    </div>
  );
};

export default MatplotlibVisualizer; 