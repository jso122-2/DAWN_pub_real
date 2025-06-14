import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { mainWebSocket } from '@/services/websocket/WebSocketService';
import { ConsciousnessState, TickData } from '@/types/consciousness.types';

interface ConsciousnessContextValue {
  state: ConsciousnessState;
  tickHistory: TickData[];
  isConnected: boolean;
  updateState: (updates: Partial<ConsciousnessState>) => void;
}

const defaultState: ConsciousnessState = {
  scup: 50,
  entropy: 0.5,
  mood: 'contemplative',
  neuralActivity: 0.5,
  quantumCoherence: 0.5,
  memoryPressure: 0.3,
  timestamp: Date.now(),
};

const ConsciousnessContext = createContext<ConsciousnessContextValue | null>(null);

export const ConsciousnessProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<ConsciousnessState>(defaultState);
  const [tickHistory, setTickHistory] = useState<TickData[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    mainWebSocket.connect();

    // Handle connection events
    mainWebSocket.on('connected', () => {
      setIsConnected(true);
      console.log('Connected to consciousness engine');
    });

    mainWebSocket.on('disconnected', () => {
      setIsConnected(false);
      console.log('Disconnected from consciousness engine');
    });

    // Handle tick data
    mainWebSocket.on('tick', (data: TickData) => {
      setState({
        scup: data.scup,
        entropy: data.entropy,
        mood: data.mood,
        neuralActivity: data.neural_activity,
        quantumCoherence: data.quantum_coherence,
        memoryPressure: data.memory_pressure,
        timestamp: data.timestamp,
      });

      setTickHistory(prev => {
        const newHistory = [...prev, data];
        // Keep only last 1000 ticks
        return newHistory.slice(-1000);
      });
    });

    return () => {
      mainWebSocket.disconnect();
      mainWebSocket.removeAllListeners();
    };
  }, []);

  const updateState = useCallback((updates: Partial<ConsciousnessState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);

  return (
    <ConsciousnessContext.Provider value={{ state, tickHistory, isConnected, updateState }}>
      {children}
    </ConsciousnessContext.Provider>
  );
};

export const useConsciousness = () => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousness must be used within ConsciousnessProvider');
  }
  return context.state;
};

export const useConsciousnessContext = () => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousnessContext must be used within ConsciousnessProvider');
  }
  return context;
}; 