import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { webSocketService } from '../services/websocket/WebSocketService';
import type { TickData, ConsciousnessData } from '../services/websocket/WebSocketService';

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  tickNumber: number;
  memoryUsage: number;
  neuralActivity: number;
  systemUnity: number;
  isConnected: boolean;
}

interface ConsciousnessContextType extends ConsciousnessState {
  updateConsciousness: (updates: Partial<ConsciousnessState>) => void;
  reset: () => void;
}

const defaultState: ConsciousnessState = {
  scup: 50,
  entropy: 0.3,
  mood: 'calm',
  tickNumber: 0,
  memoryUsage: 0,
  neuralActivity: 0.5,
  systemUnity: 0.8,
  isConnected: false
};

const ConsciousnessContext = createContext<ConsciousnessContextType>({
  ...defaultState,
  updateConsciousness: () => {},
  reset: () => {}
});

export const ConsciousnessProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<ConsciousnessState>(defaultState);
  
  useEffect(() => {
    // Subscribe to WebSocket events
    const unsubscribeTick = webSocketService.on('tick', (data: TickData) => {
      setState(prev => ({
        ...prev,
        scup: data.scup,
        entropy: data.entropy,
        mood: data.mood,
        tickNumber: data.tick_count
      }));
    });
    
    const unsubscribeConsciousness = webSocketService.on('consciousness', (data: ConsciousnessData) => {
      setState(prev => ({
        ...prev,
        memoryUsage: data.memory_usage,
        neuralActivity: data.neural_activity,
        systemUnity: data.consciousness_unity
      }));
    });
    
    const unsubscribeConnection = webSocketService.onConnectionChange((connected) => {
      setState(prev => ({ ...prev, isConnected: connected }));
    });
    
    return () => {
      unsubscribeTick();
      unsubscribeConsciousness();
      unsubscribeConnection();
    };
  }, []);
  
  const updateConsciousness = useCallback((updates: Partial<ConsciousnessState>) => {
    setState(prev => ({ ...prev, ...updates }));
  }, []);
  
  const reset = useCallback(() => {
    setState(defaultState);
    webSocketService.send('consciousness_reset', {});
  }, []);
  
  return (
    <ConsciousnessContext.Provider value={{ ...state, updateConsciousness, reset }}>
      {children}
    </ConsciousnessContext.Provider>
  );
};

export const useConsciousness = () => {
  const context = useContext(ConsciousnessContext);
  if (!context) {
    throw new Error('useConsciousness must be used within ConsciousnessProvider');
  }
  return context;
}; 