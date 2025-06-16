import React, { useEffect, useState, useRef, useCallback } from 'react';
import { createWebSocket } from '../api/client';
import { healthCheck } from '../api/client';
import TickDataDisplay from '../components/TickDataDisplay';
import TestConnection from '../components/TestConnection';
import ProcessManagerDashboard from '../components/ProcessManagerDashboard';
import ConsciousnessVisualizer from '../components/ConsciousnessVisualizer';
import MemoryPalaceViewer from '../components/MemoryPalaceViewer';
import OWLDashboard from '../components/OWLDashboard';

interface SystemStatus {
  status: string;
  message: string;
  timestamp: string;
}

interface WebSocketMessage {
  type: string;
  data: any;
}

const ActivityMonitor: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const wsRef = useRef<WebSocket | null>(null);
  const messageQueue = useRef<WebSocketMessage[]>([]);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const [error, setError] = useState<string | null>(null);

  const connectWebSocket = useCallback(async () => {
    try {
      // Wait for a short delay to ensure component is mounted
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        return; // Already connected
      }

      wsRef.current = createWebSocket('/ws');
      
      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setIsLoading(false);
        // Process any queued messages
        while (messageQueue.current.length > 0) {
          const message = messageQueue.current.shift();
          if (message && wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(message));
          }
        }
      };

      wsRef.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        // Attempt to reconnect after a delay
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
        }
        reconnectTimeoutRef.current = setTimeout(() => {
          connectWebSocket();
        }, 3000);
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      wsRef.current.onmessage = (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'status') {
            setStatus(data.data);
          }
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Failed to establish WebSocket connection:', error);
      setIsConnected(false);
      // Attempt to reconnect after a delay
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      reconnectTimeoutRef.current = setTimeout(() => {
        connectWebSocket();
      }, 3000);
    }
  }, []);

  const checkHealth = async () => {
    try {
      const data = await healthCheck();
      setStatus(data);
      setError(null);
    } catch (err) {
      console.error('Health check error:', err);
      setError('Failed to connect to DAWN system');
      // Set a default status
      setStatus({
        status: 'unhealthy',
        message: 'Unable to connect to DAWN system',
        timestamp: new Date().toISOString()
      });
    }
  };

  useEffect(() => {
    connectWebSocket();

    // Cleanup on unmount
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectWebSocket]);

  const sendMessage = (message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      // Queue message if not connected
      messageQueue.current.push(message);
    }
  };

  if (isLoading) {
    return (
      <div className="activity-monitor loading">
        <h2>Connecting to DAWN System...</h2>
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div style={{ padding: '1rem' }}>
      <h1 style={{ 
        color: '#00ff88',
        marginBottom: '1rem',
        fontFamily: 'var(--font-mono)'
      }}>
        Activity Monitor
      </h1>
      
      <div style={{ marginBottom: '2rem' }}>
        <OWLDashboard />
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <TestConnection />
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <ConsciousnessVisualizer />
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <TickDataDisplay />
      </div>

      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ 
          color: '#00ff88',
          marginBottom: '1rem',
          fontFamily: 'var(--font-mono)'
        }}>
          Memory Palace
        </h2>
        <MemoryPalaceViewer />
      </div>

      <div>
        <ProcessManagerDashboard />
      </div>
    </div>
  );
};

export default ActivityMonitor; 