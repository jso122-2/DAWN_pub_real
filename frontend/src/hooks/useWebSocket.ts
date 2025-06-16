import { useState, useEffect, useCallback } from 'react';
import { WebSocketManager } from '../utils/websocketManager';
import { config } from '../config';

export const useWebSocket = () => {
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [wsManager, setWsManager] = useState<WebSocketManager | null>(null);

  const connect = useCallback(async () => {
    try {
      const manager = new WebSocketManager({
        url: config.wsUrl,
        maxReconnectAttempts: 5,
        reconnectDelay: 1000,
        debug: config.debug
      });
      await manager.connect();
      setWsManager(manager);
      setConnected(true);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to connect'));
      setConnected(false);
    }
  }, []);

  const disconnect = useCallback(() => {
    if (wsManager) {
      wsManager.disconnect();
      setWsManager(null);
      setConnected(false);
    }
  }, [wsManager]);

  const send = useCallback((message: any) => {
    if (!wsManager) {
      console.error('WebSocket is not connected');
      return false;
    }
    return wsManager.send(message);
  }, [wsManager]);

  const on = useCallback((event: string, handler: (data: any) => void) => {
    if (wsManager) {
      wsManager.on(event, handler);
    }
  }, [wsManager]);

  const off = useCallback((event: string, handler: (data: any) => void) => {
    if (wsManager) {
      wsManager.off(event, handler);
    }
  }, [wsManager]);

  const emit = useCallback((event: string, data: any) => {
    if (wsManager) {
      wsManager.emit(event, data);
    }
  }, [wsManager]);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    connected,
    error,
    wsManager,
    connect,
    disconnect,
    send,
    on,
    off,
    emit
  };
}; 