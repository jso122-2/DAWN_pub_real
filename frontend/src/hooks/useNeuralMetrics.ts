import { useEffect, useState } from 'react';
import { useWebSocket } from '../services/websocket';
import { NeuralMetrics } from '../types/neural';

export const useNeuralMetrics = () => {
  const { connected, neuralMetrics, connect, disconnect } = useWebSocket();
  const [metrics, setMetrics] = useState<NeuralMetrics | null>(null);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  useEffect(() => {
    if (neuralMetrics) {
      setMetrics(neuralMetrics);
    }
  }, [neuralMetrics]);

  return {
    connected,
    metrics,
    error: null
  };
}; 