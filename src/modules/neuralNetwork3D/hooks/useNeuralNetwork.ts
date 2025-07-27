import { useState, useEffect, useCallback } from 'react';
import { neuralNetwork } from '../NeuralNetworkCore';

export function useNeuralNetwork() {
  const [neurons, setNeurons] = useState<any[]>([]);
  const [connections, setConnections] = useState<any[]>([]);
  const [regions, setRegions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Update visualization state
  const updateState = useCallback(() => {
    const state = neuralNetwork.getVisualizationState();
    setNeurons(state.neurons);
    setConnections(state.connections);
    setRegions(state.regions);
    setIsLoading(false);
  }, []);
  
  useEffect(() => {
    // Initial load
    updateState();
    
    // Subscribe to network events
    neuralNetwork.on('networkUpdate', updateState);
    neuralNetwork.on('networkGenerated', updateState);
    
    return () => {
      neuralNetwork.removeListener('networkUpdate', updateState);
      neuralNetwork.removeListener('networkGenerated', updateState);
    };
  }, [updateState]);
  
  // Interaction methods
  const stimulateNeuron = useCallback((neuronId: string, strength: number = 1) => {
    neuralNetwork.stimulateNeuron(neuronId, strength);
  }, []);
  
  return {
    neurons,
    connections,
    regions,
    isLoading,
    stimulateNeuron
  };
} 