import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { webSocketService } from '../services/WebSocketService';
import { useConsciousnessStore } from '../stores/consciousnessStore';

interface ConsciousnessData {
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
  tickRate: number;
  isConnected: boolean;
  nodes: number;
  connections: number;
  networkHealth: number;
}

interface ConsciousnessContextType {
  data: ConsciousnessData;
  isLoading: boolean;
  updateData: (newData: Partial<ConsciousnessData>) => void;
}

const defaultData: ConsciousnessData = {
  scup: 85,
  entropy: 0.62,
  heat: 0.78,
  mood: 'confident',
  tickRate: 142,
  isConnected: true,
  nodes: 2847,
  connections: 15983,
  networkHealth: 96
};

const ConsciousnessContext = createContext<ConsciousnessContextType | undefined>(undefined);

export const ConsciousnessProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [data, setData] = useState<ConsciousnessData>(defaultData);
  const [isLoading, setIsLoading] = useState(true);
  const { updateTickData, setConnectionState } = useConsciousnessStore();

  const updateData = (newData: Partial<ConsciousnessData>) => {
    setData(prev => ({ ...prev, ...newData }));
  };

  // 🔥 CONNECT TO REAL TICK ENGINE!
  useEffect(() => {
    console.log('🔌 Initializing DAWN Tick Engine Connection...');
    
    // Connect to WebSocket
    webSocketService.connect();
    
    // Subscribe to real tick data
    const unsubscribe = webSocketService.subscribe((tickData) => {
      console.log('📡 Received tick data:', tickData);
      
      // Update the consciousness store (for OptimizedDashboard)
      updateTickData(tickData);
      
      // Update local state (for compatibility with existing components)
      setData(prev => ({
        ...prev,
        scup: tickData.scup * 100, // Convert 0-1 to 0-100
        entropy: tickData.entropy,
        heat: tickData.heat,
        mood: tickData.mood,
        isConnected: webSocketService.isConnected(),
        tickRate: webSocketService.getTickRate(), // Get real tick rate from service
        // Keep existing values for backward compatibility
        nodes: prev.nodes,
        connections: prev.connections,
        networkHealth: Math.round(((tickData.scup + (1-tickData.entropy) + tickData.heat) / 3) * 100)
      }));
      
      setIsLoading(false);
    });
    
    // Monitor connection state
    const checkConnection = () => {
      const state = webSocketService.getConnectionState();
      setConnectionState(state);
      setData(prev => ({
        ...prev,
        isConnected: webSocketService.isConnected()
      }));
      
      if (state === 'connected') {
        setIsLoading(false);
        console.log('✅ Connected to DAWN Tick Engine!');
      } else if (state === 'disconnected') {
        console.log('🔄 Attempting to reconnect to DAWN Tick Engine...');
      }
    };
    
    // Check connection every 5 seconds
    const connectionInterval = setInterval(checkConnection, 5000);
    checkConnection(); // Check immediately
    
    // Cleanup
    return () => {
      console.log('🔌 Disconnecting from DAWN Tick Engine...');
      unsubscribe();
      clearInterval(connectionInterval);
      webSocketService.disconnect();
    };
  }, [updateTickData, setConnectionState]);

  return (
    <ConsciousnessContext.Provider value={{ data, isLoading, updateData }}>
      {children}
    </ConsciousnessContext.Provider>
  );
};

export const useConsciousness = () => {
  const context = useContext(ConsciousnessContext);
  if (context === undefined) {
    throw new Error('useConsciousness must be used within a ConsciousnessProvider');
  }
  return context;
}; 