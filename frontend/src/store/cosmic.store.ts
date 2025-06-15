import { create } from 'zustand';

interface CosmicState {
  systemUnity: number;
  entropy: number;
  neuralActivity: number;
  systemLoad: number;
  mood: string;
  quantumCoherence: number;
  updateSystemUnity: (value: number) => void;
  updateEntropy: (value: number) => void;
  updateNeuralActivity: (value: number) => void;
  updateSystemLoad: (value: number) => void;
  updateMood: (value: string) => void;
  updateQuantumCoherence: (value: number) => void;
}

export const useCosmicStore = create<CosmicState>((set) => ({
  systemUnity: 0.75,
  entropy: 0.5,
  neuralActivity: 0.6,
  systemLoad: 0.45,
  mood: 'contemplative',
  quantumCoherence: 0.7,
  
  updateSystemUnity: (value) => set({ systemUnity: value }),
  updateEntropy: (value) => set({ entropy: value }),
  updateNeuralActivity: (value) => set({ neuralActivity: value }),
  updateSystemLoad: (value) => set({ systemLoad: value }),
  updateMood: (value) => set({ mood: value }),
  updateQuantumCoherence: (value) => set({ quantumCoherence: value }),
})); 