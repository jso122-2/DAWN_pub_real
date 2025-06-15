import React, { useState, useEffect } from 'react';
import WebSocketManager from '../utils/websocketManager';

// Create a singleton instance
const wsManager = new WebSocketManager();

// Export the singleton instance
export const wsService = wsManager;

// Export the WebSocketManager class for type information
export { WebSocketManager };

// Export a hook for using the WebSocket service
export const useWebSocket = () => {
  const [connected, setConnected] = useState(false);
  const [neuralMetrics, setNeuralMetrics] = useState<any>(null);

  useEffect(() => {
    // Set up connection change handler
    wsManager.setConnectionChangeHandler(setConnected);

    // Set up message handlers
    wsManager.on('neural_metrics', (data) => {
      setNeuralMetrics(data);
    });

    // Connect to WebSocket
    wsManager.connect();

    // Cleanup on unmount
    return () => {
      wsManager.disconnect();
    };
  }, []);

  return {
    connected,
    neuralMetrics,
    connect: () => wsManager.connect(),
    disconnect: () => wsManager.disconnect(),
    send: (type: string, payload: any) => wsManager.send(type, payload),
    on: (type: string, handler: (payload: any) => void) => wsManager.on(type, handler),
    off: (type: string, handler: (payload: any) => void) => wsManager.off(type, handler)
  };
}; 