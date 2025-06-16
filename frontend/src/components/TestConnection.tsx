import { useEffect, useState, useRef } from 'react';

interface WebSocketLog {
  timestamp: string;
  type: 'sent' | 'received';
  message: string;
}

const TestConnection = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<string>('');
  const [logs, setLogs] = useState<WebSocketLog[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const addLog = (type: 'sent' | 'received', message: string) => {
    setLogs(prev => [{
      timestamp: new Date().toISOString(),
      type,
      message
    }, ...prev].slice(0, 50)); // Keep last 50 logs
  };

  useEffect(() => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws');
    
    wsRef.current.onopen = () => {
      setIsConnected(true);
      addLog('received', 'Connected to WebSocket server');
    };
    
    wsRef.current.onclose = () => {
      setIsConnected(false);
      addLog('received', 'Disconnected from WebSocket server');
    };
    
    wsRef.current.onerror = (error) => {
      addLog('received', `WebSocket error: ${error}`);
    };
    
    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastMessage(data);
        addLog('received', `Received: ${JSON.stringify(data)}`);
      } catch (error) {
        addLog('received', `Error parsing message: ${error}`);
      }
    };
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const sendTestMessage = () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const testMessage = {
        type: 'test',
        data: {
          timestamp: new Date().toISOString(),
          message: 'Test message from frontend'
        }
      };
      wsRef.current.send(JSON.stringify(testMessage));
      addLog('sent', JSON.stringify(testMessage));
    }
  };

  return (
    <div
      style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderRadius: '1rem',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        padding: '1.5rem',
        margin: '1rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
      }}
    >
      <h3 style={{ 
        margin: '0 0 1rem 0',
        color: '#00ff88',
        fontSize: '1.25rem',
        fontFamily: 'var(--font-mono)'
      }}>
        WebSocket Connection Test
      </h3>

      <div style={{ marginBottom: '1rem' }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '0.5rem',
          marginBottom: '0.5rem'
        }}>
          <span style={{ color: '#9ca3af' }}>Status:</span>
          <span style={{ 
            color: isConnected ? '#10b981' : '#ef4444',
            fontFamily: 'var(--font-mono)'
          }}>
            {isConnected ? '✅ Connected' : '❌ Disconnected'}
          </span>
        </div>

        <button
          onClick={sendTestMessage}
          disabled={!isConnected}
          style={{
            padding: '0.5rem 1rem',
            background: isConnected ? '#00ff88' : '#4b5563',
            color: '#000',
            border: 'none',
            borderRadius: '0.5rem',
            cursor: isConnected ? 'pointer' : 'not-allowed',
            fontFamily: 'var(--font-mono)',
            transition: 'all 0.2s ease'
          }}
        >
          Send Test Message
        </button>
      </div>

      {lastMessage && (
        <div style={{ marginBottom: '1rem' }}>
          <div style={{ color: '#9ca3af', marginBottom: '0.5rem' }}>Last Message:</div>
          <pre style={{
            background: 'rgba(0, 0, 0, 0.2)',
            padding: '1rem',
            borderRadius: '0.5rem',
            overflow: 'auto',
            maxHeight: '200px',
            fontFamily: 'var(--font-mono)',
            fontSize: '0.875rem'
          }}>
            {lastMessage}
          </pre>
        </div>
      )}

      <div>
        <div style={{ color: '#9ca3af', marginBottom: '0.5rem' }}>WebSocket Logs:</div>
        <div style={{
          background: 'rgba(0, 0, 0, 0.2)',
          padding: '1rem',
          borderRadius: '0.5rem',
          overflow: 'auto',
          maxHeight: '300px',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.875rem'
        }}>
          {logs.map((log, index) => (
            <div 
              key={index}
              style={{
                marginBottom: '0.5rem',
                padding: '0.25rem 0',
                borderBottom: '1px solid rgba(255, 255, 255, 0.1)'
              }}
            >
              <div style={{ 
                color: log.type === 'sent' ? '#00ff88' : '#10b981',
                marginBottom: '0.25rem'
              }}>
                [{new Date(log.timestamp).toLocaleTimeString()}] {log.type.toUpperCase()}
              </div>
              <pre style={{ 
                margin: 0,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-all'
              }}>
                {log.message}
              </pre>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TestConnection; 