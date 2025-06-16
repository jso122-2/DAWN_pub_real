import React, { useState, useEffect } from 'react';
import { wsManager } from '../utils/websocketManager';
import { config } from '../config';

// Export the singleton instance
export const wsService = wsManager;

// Export the WebSocketManager class for type information
export { WebSocketManager } from '../utils/websocketManager';

// Export a hook for using the WebSocket service
export const useWebSocket = () => {
  const [connected, setConnected] = useState(false);
  const [neuralMetrics, setNeuralMetrics] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Set up connection change handler
    wsManager.setConnectionChangeHandler((isConnected) => {
      console.log('WebSocket connection status changed:', isConnected);
      setConnected(isConnected);
      if (!isConnected) {
        setError(new Error('WebSocket disconnected'));
      } else {
        setError(null);
      }
    });

    // Set up message handlers
    wsManager.on('neural_metrics', (data) => {
      console.log('Received neural metrics:', data);
      setNeuralMetrics(data);
    });

    // Set up error handler
    wsManager.on('error', (err) => {
      console.error('WebSocket error:', err);
      setError(err);
    });

    // Connect to WebSocket
    console.log('Connecting to WebSocket:', config.wsUrl);
    wsManager.connect().catch((err) => {
      console.error('Failed to connect to WebSocket:', err);
      setError(err);
    });

    // Cleanup on unmount
    return () => {
      console.log('Cleaning up WebSocket connection');
      wsManager.disconnect();
    };
  }, []);

  return {
    connected,
    neuralMetrics,
    error,
    connect: () => wsManager.connect(),
    disconnect: () => wsManager.disconnect(),
    send: (message: any) => wsManager.send(message),
    on: (type: string, handler: (payload: any) => void) => 
      wsManager.on(type, handler),
    removeMessageHandler: (type: string, handler: (payload: any) => void) => 
      wsManager.removeMessageHandler(type, handler)
  };
}; 