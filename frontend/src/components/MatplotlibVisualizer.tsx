import React, { useEffect, useRef, useState } from 'react';
import { wsService } from '../services/websocket';

interface VisualizationData {
  type: string;
  data: any;
  timestamp: string;
}

export const MatplotlibVisualizer: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [visualizationData, setVisualizationData] = useState<VisualizationData | null>(null);
  const mounted = useRef(true);
  const connectionSubscription = useRef<{ unsubscribe: () => void } | null>(null);
  const retryTimeout = useRef<NodeJS.Timeout | null>(null);

  const requestVisualization = async () => {
    if (!mounted.current) return;

    try {
      await wsService.send({
        type: 'visualization_request',
        content: JSON.stringify({ type: 'matplotlib' })
      });
    } catch (err) {
      console.error('Failed to request visualization:', err);
      if (mounted.current) {
        setError('Failed to request visualization');
        setIsLoading(false);
      }
    }
  };

  useEffect(() => {
    mounted.current = true;

    const handleConnectionState = (connected: boolean) => {
      if (!mounted.current) return;
      
      setIsConnected(connected);
      if (connected) {
        setIsLoading(true);
        setError(null);
        requestVisualization();
      } else {
        // If disconnected, retry connection after a delay
        if (retryTimeout.current) {
          clearTimeout(retryTimeout.current);
        }
        retryTimeout.current = setTimeout(() => {
          if (mounted.current) {
            requestVisualization();
          }
        }, 5000); // Retry after 5 seconds
      }
    };

    const handleMessage = (message: any) => {
      if (!mounted.current) return;

      if (message.type === 'visualization') {
        try {
          const data = JSON.parse(message.content);
          setVisualizationData(data);
          setIsLoading(false);
          setError(null);
        } catch (err) {
          console.error('Failed to parse visualization data:', err);
          setError('Failed to parse visualization data');
          setIsLoading(false);
        }
      }
    };

    // Subscribe to connection changes
    connectionSubscription.current = wsService.onConnectionChange(handleConnectionState);

    // Subscribe to visualization messages
    wsService.onMessage('visualization', handleMessage);

    // Request initial visualization data
    requestVisualization();

    // Cleanup function
    return () => {
      mounted.current = false;

      // Clear any pending retry timeout
      if (retryTimeout.current) {
        clearTimeout(retryTimeout.current);
        retryTimeout.current = null;
      }

      // Unsubscribe from connection changes
      if (connectionSubscription.current) {
        connectionSubscription.current.unsubscribe();
        connectionSubscription.current = null;
      }

      // Unsubscribe from messages
      wsService.offMessage('visualization', handleMessage);
    };
  }, []);

  if (error) {
    return (
      <div style={{ padding: '1rem', textAlign: 'center' }}>
        <div style={{ color: 'red' }}>{error}</div>
        {!isConnected && (
          <div style={{ marginTop: '1rem' }}>
            <button onClick={requestVisualization}>Retry Connection</button>
          </div>
        )}
      </div>
    );
  }

  if (isLoading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div style={{ padding: '1rem' }}>
      {visualizationData ? (
        <div>
          <h3>Visualization</h3>
          <pre>{JSON.stringify(visualizationData, null, 2)}</pre>
        </div>
      ) : (
        <div>No visualization data available</div>
      )}
    </div>
  );
};

export default MatplotlibVisualizer; 