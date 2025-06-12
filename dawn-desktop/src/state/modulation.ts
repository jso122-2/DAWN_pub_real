import { create } from 'zustand';

interface ModulationState {
  mood: number;        // 0-100
  pulse: number;       // 0-100
  noiseInjection: number; // 0-100
  setMood: (value: number) => void;
  setPulse: (value: number) => void;
  setNoiseInjection: (value: number) => void;
  resetToDefaults: () => void;
}

export const useModulationStore = create<ModulationState>((set) => ({
  mood: 50,
  pulse: 30,
  noiseInjection: 10,
  
  setMood: (value) => set({ mood: value }),
  setPulse: (value) => set({ pulse: value }),
  setNoiseInjection: (value) => set({ noiseInjection: value }),
  
  resetToDefaults: () => set({
    mood: 50,
    pulse: 30,
    noiseInjection: 10,
  }),
})); 