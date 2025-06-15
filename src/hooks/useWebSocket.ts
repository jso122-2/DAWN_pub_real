import { useState, useEffect, useCallback } from 'react';

interface WebSocketMessage {
  type: string;
  process?: string;
  frame?: string;
  message?: string;
}

export const useWebSocket = (url: string = 'ws://localhost:8000/ws') => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => {
      setIsConnected(true);
      setError(null);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    ws.onerror = (event) => {
      setError('WebSocket error occurred');
      console.error('WebSocket error:', event);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
      } catch (e) {
        console.error('Error parsing WebSocket message:', e);
      }
    };

    setSocket(ws);

    // Cleanup on unmount
    return () => {
      ws.close();
    };
  }, [url]);

  // Send message through WebSocket
  const send = useCallback((message: WebSocketMessage) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify(message));
    }
  }, [socket, isConnected]);

  return {
    isConnected,
    lastMessage,
    error,
    send
  };
}; 