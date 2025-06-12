import { create } from 'zustand'

interface CosmicState {
  // Navigation
  currentView: 'neural' | 'quantum' | 'entropy' | 'system' | 'monitor' | 'processes' | 'neural-monitor'
  setView: (view: CosmicState['currentView']) => void

  // System metrics
  entropy: number
  neuralActivity: number
  quantumCoherence: number
  systemLoad: number

  // Update functions
  updateEntropy: (value: number) => void
  updateNeuralActivity: (value: number) => void
  updateQuantumCoherence: (value: number) => void
  updateSystemLoad: (value: number) => void

  // Features
  voiceEnabled: boolean
  toggleVoice: () => void
  
  particlesEnabled: boolean
  toggleParticles: () => void

  // Timeline preferences
  timelineZoom: number
  setTimelineZoom: (zoom: number) => void

  timelinePaused: boolean
  setTimelinePaused: (paused: boolean) => void

  timelineEventTypeFilters: string[]
  setTimelineEventTypeFilters: (filters: string[]) => void
}

export const useCosmicStore = create<CosmicState>((set) => ({
  // Navigation
  currentView: 'neural',
  setView: (view) => set({ currentView: view }),

  // System metrics
  entropy: 0.7,
  neuralActivity: 0.85,
  quantumCoherence: 0.92,
  systemLoad: 0.45,

  // Update functions
  updateEntropy: (value) => set({ entropy: value }),
  updateNeuralActivity: (value) => set({ neuralActivity: value }),
  updateQuantumCoherence: (value) => set({ quantumCoherence: value }),
  updateSystemLoad: (value) => set({ systemLoad: value }),

  // Features
  voiceEnabled: false,
  toggleVoice: () => set((state) => ({ voiceEnabled: !state.voiceEnabled })),
  
  particlesEnabled: true,
  toggleParticles: () => set((state) => ({ particlesEnabled: !state.particlesEnabled })),

  // Timeline preferences
  timelineZoom: 1,
  setTimelineZoom: (zoom: number) => set({ timelineZoom: zoom }),

  timelinePaused: false,
  setTimelinePaused: (paused: boolean) => set({ timelinePaused: paused }),

  timelineEventTypeFilters: Object.keys({
    tick: true,
    'metrics-update': true,
    'pattern-detected': true,
    'anomaly-detected': true,
    'cognitive-load': true,
    disturbance: true,
  }),
  setTimelineEventTypeFilters: (filters: string[]) => set({ timelineEventTypeFilters: filters }),
}))