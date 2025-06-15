// useDAWNConnection.ts
// React hooks for DAWN subprocess integration

import { useState, useEffect, useCallback } from 'react';
import { 
  webSocketService, 
  TickData 
} from '../services/WebSocketService';

export interface ProcessData {
  id: string;
  name: string;
  value: number;
  trend: number[];
  status: 'active' | 'idle' | 'warning' | 'error';
  category: 'neural' | 'quantum' | 'system' | 'memory' | 'io';
  unit?: string;
  threshold?: { min: number; max: number };
}

// Hook for tick data
export function useTickData() {
  const [tickData, setTickData] = useState<TickData>({
    tick_count: 0,
    scup: 0.5,
    entropy: 0.5,
    heat: 0.5,
    mood: 'focused',
    timestamp: Date.now()
  });

  useEffect(() => {
    const unsubscribe = webSocketService.subscribe((data: TickData) => {
      setTickData(data);
    });

    return () => {
      unsubscribe();
    };
  }, []);

  return tickData;
}

// Hook for connection status
export function useDAWNConnection() {
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check connection status periodically
    const checkConnection = () => {
      const isConnected = webSocketService.isConnected();
      setConnected(isConnected);
    };

    // Initial check
    checkConnection();

    // Check every second
    const interval = setInterval(checkConnection, 1000);

    // Try to connect if not connected
    if (!webSocketService.isConnected()) {
      webSocketService.connect();
    }

    return () => {
      clearInterval(interval);
    };
  }, []);

  const connect = useCallback(() => {
    setError(null);
    webSocketService.connect();
  }, []);

  const disconnect = useCallback(() => {
    webSocketService.disconnect();
    setConnected(false);
  }, []);

  return {
    connected,
    error,
    connect,
    disconnect,
    isConnected: connected
  };
}

// Hook for mock subprocess data (since we don't have real subprocesses yet)
export function useSubprocesses() {
  const [subprocesses, setSubprocesses] = useState<ProcessData[]>([]);
  const tickData = useTickData();

  useEffect(() => {
    // Create mock subprocess data based on tick data
    const mockProcesses: ProcessData[] = [
      {
        id: 'neural_activity',
        name: 'Neural Activity Visualizer',
        value: tickData.scup * 100,
        trend: [],
        status: tickData.scup > 0.7 ? 'active' : tickData.scup > 0.3 ? 'idle' : 'warning',
        category: 'neural',
        unit: '%',
        threshold: { min: 20, max: 90 }
      },
      {
        id: 'consciousness_analyzer',
        name: 'Consciousness Analyzer',
        value: tickData.entropy * 100,
        trend: [],
        status: 'active',
        category: 'neural',
        unit: '%'
      },
      {
        id: 'memory_consolidator',
        name: 'Memory Consolidator',
        value: tickData.heat * 100,
        trend: [],
        status: 'idle',
        category: 'memory',
        unit: '%'
      },
      {
        id: 'entropy_reducer',
        name: 'Entropy Reducer',
        value: (1 - tickData.entropy) * 100,
        trend: [],
        status: 'active',
        category: 'system',
        unit: '%'
      },
      {
        id: 'quantum_processor',
        name: 'Quantum State Processor',
        value: Math.sin(Date.now() * 0.001) * 50 + 50,
        trend: [],
        status: 'active',
        category: 'quantum',
        unit: '%'
      }
    ];

    setSubprocesses(mockProcesses);
  }, [tickData]);

  const controlSubprocess = useCallback((subprocessId: string, action: 'start' | 'stop' | 'restart') => {
    console.log(`Mock action: ${action} on subprocess ${subprocessId}`);
    // In a real implementation, this would send commands to the backend
  }, []);

  return {
    subprocesses,
    controlSubprocess,
    connected: webSocketService.isConnected()
  };
} 