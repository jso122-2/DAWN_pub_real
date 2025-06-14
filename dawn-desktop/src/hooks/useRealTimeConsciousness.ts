import { useEffect, useState, useCallback } from 'react';
import { consciousnessDataService, ConsciousnessMetrics } from '../services/ConsciousnessDataService';
import { useConsciousness } from './useConsciousness';
import { useCosmicStore } from '../store/cosmicStore';

export interface RealTimeConsciousnessState extends ConsciousnessMetrics {
  isConnected: boolean;
  lastUpdate: number;
  connectionStatus: 'connecting' | 'connected' | 'disconnected' | 'error';
}

export function useRealTimeConsciousness(): RealTimeConsciousnessState {
  const fallbackConsciousness = useConsciousness();
  const cosmicStore = useCosmicStore();
  
  const [realTimeData, setRealTimeData] = useState<ConsciousnessMetrics | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(0);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected' | 'error'>('disconnected');

  // Update cosmic store when real-time data changes
  const updateCosmicStore = useCallback((metrics: ConsciousnessMetrics) => {
    cosmicStore.updateEntropy(metrics.entropy);
    cosmicStore.updateNeuralActivity(metrics.neuralActivity);
    cosmicStore.updateQuantumCoherence(metrics.quantumCoherence);
    cosmicStore.updateSystemLoad(metrics.systemLoad);
    cosmicStore.updateMood(metrics.mood);
  }, [cosmicStore]);

  useEffect(() => {
    console.log('🧠 Real-time Consciousness Hook: Initializing');

    // Subscribe to consciousness data updates
    const unsubscribe = consciousnessDataService.subscribeToUpdates((metrics: ConsciousnessMetrics) => {
      setRealTimeData(metrics);
      setLastUpdate(Date.now());
      setIsConnected(true);
      setConnectionStatus('connected');
      
      // Update cosmic store with real-time data
      updateCosmicStore(metrics);
      
      console.log('🧠 Consciousness Update:', {
        scup: metrics.scup.toFixed(1),
        entropy: (metrics.entropy * 100).toFixed(1),
        mood: metrics.mood
      });
    });

    // Start the consciousness data service
    const startService = async () => {
      try {
        setConnectionStatus('connecting');
        consciousnessDataService.start();
        
        // Check connection status periodically
        const statusInterval = setInterval(() => {
          const isServiceRunning = consciousnessDataService.isRunning();
          setIsConnected(isServiceRunning);
          
          if (!isServiceRunning && connectionStatus === 'connected') {
            setConnectionStatus('error');
            console.warn('🧠 Consciousness Data Service: Connection lost');
          }
        }, 5000);

        return () => {
          clearInterval(statusInterval);
        };
      } catch (error) {
        console.error('🧠 Consciousness Data Service: Failed to start:', error);
        setConnectionStatus('error');
        setIsConnected(false);
      }
    };

    startService();

    // Cleanup on unmount
    return () => {
      unsubscribe();
      consciousnessDataService.stop();
      console.log('🧠 Real-time Consciousness Hook: Cleanup');
    };
  }, [updateCosmicStore, connectionStatus]);

  // Return real-time data if available, otherwise fallback to simulated data
  if (realTimeData && isConnected) {
    return {
      ...realTimeData,
      isConnected,
      lastUpdate,
      connectionStatus
    };
  }

  // Fallback to simulated consciousness data
  return {
    scup: fallbackConsciousness.scup,
    entropy: fallbackConsciousness.entropy,
    neuralActivity: fallbackConsciousness.neuralActivity,
    quantumCoherence: fallbackConsciousness.quantumCoherence,
    systemLoad: fallbackConsciousness.systemLoad,
    mood: fallbackConsciousness.mood,
    isConnected: false,
    lastUpdate: 0,
    connectionStatus: 'disconnected'
  };
}

// Hook for testing - allows manual data injection
export function useConsciousnessTestData() {
  const injectTestData = useCallback((data: Partial<ConsciousnessMetrics>) => {
    consciousnessDataService.injectTestData({
      timestamp: Date.now(),
      entropy: data.entropy || 0.5,
      neuralActivity: data.neuralActivity || 0.5,
      quantumCoherence: data.quantumCoherence || 0.5,
      systemLoad: data.systemLoad || 0.3,
      mood: data.mood,
      scup: data.scup
    });
  }, []);

  const generateRandomData = useCallback(() => {
    injectTestData({
      entropy: Math.random(),
      neuralActivity: Math.random(),
      quantumCoherence: Math.random(),
      systemLoad: Math.random() * 0.8,
      mood: ['contemplative', 'excited', 'serene', 'anxious', 'euphoric', 'chaotic'][Math.floor(Math.random() * 6)]
    });
  }, [injectTestData]);

  return {
    injectTestData,
    generateRandomData
  };
} 