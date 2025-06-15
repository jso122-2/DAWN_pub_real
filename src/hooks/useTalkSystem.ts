import { useState, useEffect, useRef } from 'react';

interface ResponseState {
  response?: string;
  confidence?: number;
  consciousness_influence?: {
    scup: number;
    entropy: number;
    mood: string;
  };
}

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
}

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

function generateId() {
  return Math.random().toString(36).substr(2, 9) + Date.now();
}

export function useTalkSystem() {
  const [responseState, setResponseState] = useState<ResponseState>({});
  const [consciousness, setConsciousness] = useState<ConsciousnessState>({
    scup: 50,
    entropy: 0,
    mood: 'NEUTRAL',
  });
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connecting');
  const [loading, setLoading] = useState(false);
  const [lastError, setLastError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let ws: WebSocket;
    let reconnectTimeout: NodeJS.Timeout | null = null;
    let isUnmounted = false;

    function connect() {
      setConnectionStatus('connecting');
      setLastError(null);
      ws = new WebSocket('ws://localhost:8768');
      wsRef.current = ws;

      ws.onopen = () => {
        setConnectionStatus('connected');
        setLastError(null);
      };

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === 'user_input_response') {
            const data = msg.data;
            setResponseState({
              response: data.response,
              confidence: data.resonance_strength,
              consciousness_influence: data.consciousness || {
                scup: data.scup || 50,
                entropy: data.entropy || 0,
                mood: data.mood || 'NEUTRAL',
              },
            });
            setLoading(false);
          } else if (msg.type === 'consciousness_update' || msg.type === 'consciousness_state') {
            const data = msg.data;
            setConsciousness({
              scup: data.scup || 50,
              entropy: data.entropy || 0,
              mood: data.mood || 'NEUTRAL',
            });
          } else if (msg.type === 'error') {
            setLastError(msg.error || 'Unknown backend error');
            setLoading(false);
          }
        } catch (e) {
          // Ignore parse errors
        }
      };

      ws.onclose = () => {
        setConnectionStatus('disconnected');
        if (!isUnmounted) {
          reconnectTimeout = setTimeout(connect, 2000);
        }
      };
      ws.onerror = () => {
        setConnectionStatus('error');
        setLastError('WebSocket connection error');
        ws.close();
      };
    }

    connect();

    return () => {
      isUnmounted = true;
      if (wsRef.current) wsRef.current.close();
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
    };
  }, []);

  function sendMessage(input: string) {
    const ws = wsRef.current;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setLastError('Not connected to DAWN backend');
      return;
    }
    setLoading(true);
    setLastError(null);
    const id = generateId();
    ws.send(
      JSON.stringify({
        type: 'user_input',
        input,
        id,
      })
    );
  }

  return { sendMessage, responseState, consciousness, connectionStatus, loading, lastError };
} 