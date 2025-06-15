import { useState, useEffect, useCallback } from 'react';
import { wsService } from '../services/websocket';

export const useWebSocket = () => {
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    wsService.connect();
    setConnected(wsService.isConnected());

    // Set up connection status monitoring
    const checkConnection = () => {
      setConnected(wsService.isConnected());
    };
    const interval = setInterval(checkConnection, 1000);

    return () => {
      clearInterval(interval);
      wsService.disconnect();
    };
  }, []);

  const connect = useCallback(() => {
    wsService.connect();
  }, []);

  const disconnect = useCallback(() => {
    wsService.disconnect();
  }, []);

  const send = useCallback((type: string, payload: any) => {
    wsService.sendMessage({ type, ...payload });
  }, []);

  const on = useCallback((type: string, handler: (payload: any) => void) => {
    wsService.addHandler(type, handler);
  }, []);

  const off = useCallback((type: string, handler: (payload: any) => void) => {
    wsService.removeHandler(type, handler);
  }, []);

  return {
    connected,
    connect,
    disconnect,
    send,
    on,
    off,
  };
}; 