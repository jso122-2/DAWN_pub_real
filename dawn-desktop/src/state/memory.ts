import { create } from 'zustand';
import { MemoryEvent, EventType, EventSeverity } from '../types/memory';

interface MemoryState {
  events: MemoryEvent[];
  addEvent: (event: Omit<MemoryEvent, 'id' | 'timestamp'>) => void;
  clearEvents: () => void;
  getFilteredEvents: (types: EventType[]) => MemoryEvent[];
}

export const useMemoryStore = create<MemoryState>((set, get) => ({
  events: [],
  
  addEvent: (event) => set((state) => ({
    events: [
      ...state.events,
      {
        ...event,
        id: `evt-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date(),
      },
    ].slice(-1000), // Keep last 1000 events
  })),
  
  clearEvents: () => set({ events: [] }),
  
  getFilteredEvents: (types) => {
    const { events } = get();
    return types.length === 0 
      ? events 
      : events.filter(event => types.includes(event.type));
  },
}));

// Demo event generator
export const startMemorySimulation = () => {
  const { addEvent } = useMemoryStore.getState();
  
  const sources = ['CoreProcessor', 'EmotionEngine', 'SystemMonitor', 'UserOverride', 'MemoryBank'];
  const messages = {
    mood: [
      'Emotional state shifted to contemplative',
      'Mood stabilization achieved',
      'Detecting user emotional resonance',
    ],
    system: [
      'Memory compression cycle initiated',
      'Cognitive load balanced',
      'Process priority adjusted',
    ],
    override: [
      'Manual intervention detected',
      'User preference applied',
      'System parameters modified',
    ],
    error: [
      'Memory overflow detected',
      'Coherence threshold exceeded',
      'Critical entropy spike',
    ],
  };
  
  setInterval(() => {
    const type = ['mood', 'system', 'override', 'error'][Math.floor(Math.random() * 4)] as EventType;
    const severity = type === 'error' 
      ? ['warning', 'critical'][Math.floor(Math.random() * 2)] as EventSeverity
      : Math.random() > 0.9 ? 'warning' : 'info';
    
    addEvent({
      source: sources[Math.floor(Math.random() * sources.length)],
      type,
      severity,
      message: messages[type][Math.floor(Math.random() * messages[type].length)],
      emotionalWeight: Math.random(),
    });
  }, 2000 + Math.random() * 3000);
}; 