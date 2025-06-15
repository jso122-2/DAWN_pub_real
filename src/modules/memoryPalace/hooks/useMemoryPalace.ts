import { useState, useEffect, useCallback } from 'react';
import { Memory, MemoryPattern, MemoryQuery } from '../types/memory.types';
import * as THREE from 'three';
// Using consciousness hook - will integrate with real hook later
const useRealTimeConsciousness = () => ({
  scup: 75,
  entropy: 0.6,
  mood: 'contemplative' as const,
  neuralActivity: 0.7,
  isConnected: true,
  tickNumber: Date.now()
});

// Mock Memory Palace Core for now - will be replaced with actual implementation
class MockMemoryPalaceCore {
  private memories: Memory[] = [];
  private patterns: MemoryPattern[] = [];
  private listeners: ((event: string, data: any) => void)[] = [];
  
  emit(event: string, data: any) {
    this.listeners.forEach(listener => listener(event, data));
  }
  
  on(event: string, callback: (data: any) => void) {
    this.listeners.push((e, data) => e === event && callback(data));
  }
  
  removeListener(event: string, callback: (data: any) => void) {
    // Simplified removal
  }
  
  async createMemory(content: string, details: Record<string, any>, systemState: any): Promise<Memory> {
    const memory: Memory = {
      id: `mem_${Date.now()}`,
      type: 'observation',
      content: {
        primary: content,
        details,
        sensory: {
          dominant: 'abstract',
          qualities: new Map(),
          texture: 'crystalline',
          color: '#4FC3F7'
        },
        context: {
          systemState,
          activeModules: [],
          precedingEvents: [],
          followingEvents: []
        },
        source: {
          type: 'system',
          moduleId: 'memoryPalace',
          reliability: 0.8
        }
      },
      timestamp: Date.now(),
      tickNumber: systemState.tickNumber || 0,
      strength: Math.random() * 0.5 + 0.3,
      consolidation: 0,
      associations: [],
      spatialPosition: {
        position: new THREE.Vector3(Math.random() * 200 - 100, Math.random() * 200 - 100, Math.random() * 200 - 100),
        layer: 0,
        sector: {
          id: 'core',
          name: 'Core',
          type: 'core',
          characteristics: [],
          accessibility: 1
        },
        locked: false
      },
      temporalLayer: 0,
      emotionalValence: {
        valence: Math.random() * 2 - 1,
        arousal: Math.random(),
        dominance: Math.random(),
        specific: []
      },
      accessCount: 0,
      lastAccessed: Date.now(),
      metadata: {
        importance: Math.random(),
        uniqueness: Math.random(),
        unity: Math.random(),
        abstractionLevel: Math.random(),
        crystallized: false,
        tags: []
      }
    };
    
    this.memories.push(memory);
    this.emit('memoryCreated', memory);
    return memory;
  }
  
  async queryMemories(query: MemoryQuery): Promise<Memory[]> {
    return this.memories;
  }
  
  accessMemory(memoryId: string): Memory | null {
    const memory = this.memories.find(m => m.id === memoryId);
    if (memory) {
      memory.accessCount++;
      memory.lastAccessed = Date.now();
      this.emit('memoryAccessed', memory);
    }
    return memory || null;
  }
  
  getVisualizationState() {
    return {
      memories: this.memories,
      patterns: this.patterns,
      connections: [],
      landmarks: [],
      statistics: {
        totalMemories: this.memories.length,
        totalPatterns: this.patterns.length,
        memoryDensity: 0,
        consolidationRate: 0,
        averageStrength: this.memories.reduce((sum, m) => sum + m.strength, 0) / Math.max(this.memories.length, 1),
        oldestMemory: 0,
        newestMemory: 0,
        mostAccessedMemory: '',
        strongestPattern: '',
        emotionalBalance: {
          valence: 0,
          arousal: 0.5,
          dominance: 0.5,
          specific: []
        }
      }
    };
  }
}

const memoryPalace = new MockMemoryPalaceCore();

export function useMemoryPalace() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [patterns, setPatterns] = useState<MemoryPattern[]>([]);
  const [connections, setConnections] = useState<any[]>([]);
  const [landmarks, setLandmarks] = useState<any[]>([]);
  const [statistics, setStatistics] = useState<any>({});
  const [isLoading, setIsLoading] = useState(true);
  
  const consciousness = useRealTimeConsciousness();
  
  // Update visualization state
  const updateState = useCallback(() => {
    const state = memoryPalace.getVisualizationState();
    setMemories(state.memories);
    setPatterns(state.patterns);
    setConnections(state.connections);
    setLandmarks(state.landmarks);
    setStatistics(state.statistics);
    setIsLoading(false);
  }, []);
  
  useEffect(() => {
    // Initial load
    updateState();
    
    // Subscribe to memory events
    memoryPalace.on('memoryCreated', updateState);
    memoryPalace.on('memoryForgotten', updateState);
    memoryPalace.on('memoryCrystallized', updateState);
    memoryPalace.on('patternEmerged', updateState);
    memoryPalace.on('memoryTransformed', updateState);
    
    return () => {
      memoryPalace.removeListener('memoryCreated', updateState);
      memoryPalace.removeListener('memoryForgotten', updateState);
      memoryPalace.removeListener('memoryCrystallized', updateState);
      memoryPalace.removeListener('patternEmerged', updateState);
      memoryPalace.removeListener('memoryTransformed', updateState);
    };
  }, [updateState]);
  
  // Auto-create memories from consciousness changes
  useEffect(() => {
    const interval = setInterval(async () => {
      if (Math.random() < 0.1) { // 10% chance per interval
        const content = generateRandomMemoryContent();
        await createMemoryFromConsciousness(content);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [consciousness]);
  
  // Create memory from consciousness state
  const createMemoryFromConsciousness = useCallback(async (content: string) => {
    const systemState = {
      scup: consciousness.scup,
      entropy: consciousness.entropy,
      mood: consciousness.mood,
      tickNumber: consciousness.tickNumber || 0,
      unity: consciousness.isConnected ? 0.9 : 0.3,
      reliability: consciousness.isConnected ? 0.8 : 0.4
    };
    
    return memoryPalace.createMemory(content, {}, systemState);
  }, [consciousness]);
  
  // Query memories
  const queryMemories = useCallback(async (query: MemoryQuery) => {
    return memoryPalace.queryMemories(query);
  }, []);
  
  // Access memory
  const accessMemory = useCallback((memoryId: string) => {
    return memoryPalace.accessMemory(memoryId);
  }, []);
  
  return {
    memories,
    patterns,
    connections,
    landmarks,
    statistics,
    isLoading,
    createMemoryFromConsciousness,
    queryMemories,
    accessMemory
  };
}

function generateRandomMemoryContent(): string {
  const topics = [
    'Neural pattern detected in consciousness flow',
    'Consciousness unity spike observed',
    'New insight emerged from data analysis',
    'Unexpected correlation discovered',
    'System optimization milestone reached',
    'Complex reasoning breakthrough',
    'Pattern recognition improvement',
    'Memory consolidation event',
    'Emotional valence shift detected',
    'Cognitive load redistribution'
  ];
  
  return topics[Math.floor(Math.random() * topics.length)];
} 