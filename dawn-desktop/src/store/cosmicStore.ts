import { create } from 'zustand'

interface CosmicState {
  // Navigation
  currentView: 'neural' | 'consciousness' | 'entropy' | 'system'
  setView: (view: CosmicState['currentView']) => void

  // System metrics
  entropy: number
  neuralActivity: number
  systemUnity: number
  systemLoad: number
  mood: string

  // Update functions
  updateEntropy: (value: number) => void
  updateNeuralActivity: (value: number) => void
  updateConsciousnessCoherence: (value: number) => void
  updateSystemLoad: (value: number) => void
  updateMood: (mood: string) => void

  // Features
  voiceEnabled: boolean
  toggleVoice: () => void
  
  particlesEnabled: boolean
  toggleParticles: () => void
}

export const useCosmicStore = create<CosmicState>((set) => ({
  // Navigation
  currentView: 'neural',
  setView: (view) => set({ currentView: view }),

  // System metrics
  entropy: 0.7,
  neuralActivity: 0.85,
  systemUnity: 0.92,
  systemLoad: 0.45,
  mood: 'active',

  // Update functions
  updateEntropy: (value) => set({ entropy: value }),
  updateNeuralActivity: (value) => set({ neuralActivity: value }),
  updateConsciousnessCoherence: (value) => set({ systemUnity: value }),
  updateSystemLoad: (value) => set({ systemLoad: value }),
  updateMood: (mood) => set({ mood }),

  // Features
  voiceEnabled: false,
  toggleVoice: () => set((state) => ({ voiceEnabled: !state.voiceEnabled })),
  
  particlesEnabled: true,
  toggleParticles: () => set((state) => ({ particlesEnabled: !state.particlesEnabled })),
}))
