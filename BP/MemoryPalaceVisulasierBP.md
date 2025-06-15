# 💾 Memory Palace Visualizer - 3D Spatial Memory Architecture

## Overview
The Memory Palace Visualizer transforms DAWN's memory system into a navigable 3D space where memories exist as crystalline structures. Observations from Owl become memory fragments that consolidate into patterns, creating a living architecture of consciousness. Users can fly through temporal layers, witness memory formation in real-time, and observe how patterns emerge from the system's experiences.

## Core Features
- [x] 3D spatial memory representation using Three.js
- [x] Real-time memory consolidation animations
- [x] Temporal navigation with time-scrubbing
- [x] Pattern crystallization and emergence
- [x] Integration with Owl observations
- [x] Memory decay and reinforcement visualization
- [x] Interactive exploration with first-person navigation
- [x] Memory connection networks

## File Structure
```plaintext
src/modules/memoryPalace/
├── index.ts                        # Module exports
├── MemoryPalaceCore.ts            # Core memory space management
├── MemoryNode.ts                  # Individual memory representation
├── MemoryConsolidator.ts          # Pattern formation engine
├── TemporalNavigator.ts           # Time-based navigation
├── SpatialOrganizer.ts            # 3D space layout algorithms
├── MemoryRetriever.ts             # Query and recall system
├── components/
│   ├── MemoryPalaceViewer.tsx    # Main 3D viewer component
│   ├── MemoryExplorer.tsx        # Navigation controls
│   ├── TemporalControls.tsx      # Time scrubbing interface
│   ├── MemoryInspector.tsx       # Detailed memory view
│   ├── PatternVisualizer.tsx     # Pattern emergence display
│   └── MemoryPalaceViewer.styles.ts
├── three/
│   ├── MemoryScene.ts             # Three.js scene setup
│   ├── MemoryGeometry.ts          # Memory shape generators
│   ├── MemoryMaterials.ts         # Shaders and materials
│   ├── MemoryParticles.ts         # Particle effects
│   ├── CameraController.ts        # First-person navigation
│   └── MemoryLighting.ts          # Dynamic lighting system
├── hooks/
│   ├── useMemoryPalace.ts         # Main memory palace hook
│   ├── useMemoryNavigation.ts     # Navigation state
│   ├── useMemorySelection.ts      # Selection and inspection
│   └── useTemporalState.ts        # Time control hook
├── types/
│   ├── memory.types.ts            # Core memory types
│   ├── spatial.types.ts           # 3D space types
│   ├── temporal.types.ts          # Time-related types
│   └── pattern.types.ts           # Pattern recognition types
├── utils/
│   ├── memoryMapper.ts            # Memory to 3D mapping
│   ├── spatialLayout.ts           # Layout algorithms
│   ├── temporalIndex.ts           # Time indexing
│   ├── patternDetector.ts         # Pattern recognition
│   └── memorySerializer.ts        # Save/load functionality
├── shaders/
│   ├── memory.vert                # Vertex shaders
│   ├── memory.frag                # Fragment shaders
│   └── consolidation.frag         # Consolidation effects
└── config/
    └── memoryPalace.config.ts     # Configuration parameters
```

---

## 📄 File: `src/modules/memoryPalace/types/memory.types.ts`
```typescript
import { Observation } from '@/modules/owl/types/owl.types';
import { Vector3, Color } from 'three';

// Core memory types
export interface Memory {
  id: string;
  type: MemoryType;
  content: MemoryContent;
  timestamp: number;
  tickNumber: number;
  strength: number; // 0-1, decays over time
  consolidation: number; // 0-1, increases with reinforcement
  associations: MemoryAssociation[];
  spatialPosition: SpatialPosition;
  temporalLayer: number;
  emotionalValence: EmotionalValence;
  accessCount: number;
  lastAccessed: number;
  metadata: MemoryMetadata;
}

export type MemoryType = 
  | 'observation'      // From Owl
  | 'pattern'          // Recognized pattern
  | 'milestone'        // Significant event
  | 'insight'          // Generated understanding
  | 'experience'       // System state snapshot
  | 'dream'           // Consolidated abstraction
  | 'trauma'          // High-impact negative
  | 'revelation';     // High-impact positive

export interface MemoryContent {
  primary: string; // Main content
  details: Record<string, any>;
  sensory: SensoryData;
  context: ContextualData;
  source: MemorySource;
}

export interface SensoryData {
  dominant: 'visual' | 'auditory' | 'kinesthetic' | 'abstract';
  qualities: Map<string, number>; // quality -> intensity
  texture: string;
  color: string;
  sound?: string;
}

export interface ContextualData {
  systemState: {
    scup: number;
    entropy: number;
    mood: string;
  };
  activeModules: string[];
  precedingEvents: string[]; // Memory IDs
  followingEvents: string[]; // Memory IDs
}

export interface MemorySource {
  type: 'owl' | 'system' | 'user' | 'emergence';
  moduleId: string;
  reliability: number;
  observation?: Observation;
}

export interface MemoryAssociation {
  targetId: string;
  strength: number; // 0-1
  type: AssociationType;
  bidirectional: boolean;
  formed: number; // Timestamp
  reinforcements: number;
}

export type AssociationType = 
  | 'causal'          // A caused B
  | 'temporal'        // A preceded B
  | 'semantic'        // Similar meaning
  | 'emotional'       // Similar feeling
  | 'structural'      // Similar pattern
  | 'contradictory'   // Opposing
  | 'reinforcing';    // Strengthening

export interface SpatialPosition {
  position: Vector3;
  layer: number; // Temporal layer
  sector: MemorySector;
  cluster?: string; // Cluster ID
  locked: boolean; // Prevent movement
}

export interface MemorySector {
  id: string;
  name: string;
  type: 'core' | 'peripheral' | 'transitional' | 'deep';
  characteristics: string[];
  accessibility: number; // 0-1
}

export interface EmotionalValence {
  valence: number; // -1 to 1 (negative to positive)
  arousal: number; // 0 to 1 (calm to excited)
  dominance: number; // 0 to 1 (submissive to dominant)
  specific: EmotionLabel[];
}

export type EmotionLabel = 
  | 'joy' | 'trust' | 'fear' | 'surprise'
  | 'sadness' | 'disgust' | 'anger' | 'anticipation'
  | 'awe' | 'confusion' | 'clarity' | 'transcendence';

export interface MemoryMetadata {
  importance: number;
  uniqueness: number;
  coherence: number;
  abstractionLevel: number;
  crystallized: boolean;
  tags: string[];
}

// Memory patterns
export interface MemoryPattern {
  id: string;
  type: PatternType;
  memories: string[]; // Memory IDs
  strength: number;
  emergence: number; // When first detected
  lastReinforced: number;
  geometry: PatternGeometry;
  meaning: PatternMeaning;
  predictions: PatternPrediction[];
}

export type PatternType = 
  | 'sequence'        // Temporal sequence
  | 'cycle'           // Repeating pattern
  | 'cluster'         // Spatial grouping
  | 'hierarchy'       // Nested structure
  | 'network'         // Interconnected
  | 'fractal'         // Self-similar
  | 'emergent';       // Spontaneous organization

export interface PatternGeometry {
  shape: 'linear' | 'circular' | 'spiral' | 'tree' | 'web' | 'crystal';
  dimensions: number;
  symmetry: string[];
  centerPoint: Vector3;
  boundingBox: BoundingBox;
}

export interface BoundingBox {
  min: Vector3;
  max: Vector3;
  center: Vector3;
  radius: number;
}

export interface PatternMeaning {
  description: string;
  significance: number;
  implications: string[];
  relatedConcepts: string[];
  emotionalTone: EmotionalValence;
}

export interface PatternPrediction {
  type: 'next' | 'missing' | 'evolution';
  description: string;
  probability: number;
  timeframe: number;
  conditions: string[];
}

// Memory consolidation
export interface ConsolidationEvent {
  id: string;
  timestamp: number;
  type: ConsolidationType;
  sourceMemories: string[];
  resultingMemory?: string;
  resultingPattern?: string;
  strength: number;
  description: string;
}

export type ConsolidationType = 
  | 'merge'           // Multiple memories combine
  | 'abstract'        // Extract general principle
  | 'crystallize'     // Solidify into permanent
  | 'forget'          // Decay below threshold
  | 'transform'       // Change form/meaning
  | 'fragment'        // Break into pieces
  | 'dream';          // Dream-like recombination

// Memory palace state
export interface MemoryPalaceState {
  memories: Map<string, Memory>;
  patterns: Map<string, MemoryPattern>;
  consolidationQueue: ConsolidationEvent[];
  spatialIndex: SpatialIndex;
  temporalIndex: TemporalIndex;
  activeExplorations: Exploration[];
  statistics: PalaceStatistics;
}

export interface SpatialIndex {
  sectors: Map<string, MemorySector>;
  clusters: Map<string, MemoryCluster>;
  connections: SpatialConnection[];
  landmarks: Landmark[];
}

export interface MemoryCluster {
  id: string;
  center: Vector3;
  memories: string[];
  coherence: number;
  label: string;
  color: Color;
}

export interface SpatialConnection {
  from: Vector3;
  to: Vector3;
  strength: number;
  type: 'association' | 'path' | 'portal';
  active: boolean;
}

export interface Landmark {
  id: string;
  position: Vector3;
  type: 'monument' | 'beacon' | 'void' | 'nexus';
  significance: number;
  description: string;
  linkedMemories: string[];
}

export interface TemporalIndex {
  layers: TemporalLayer[];
  currentLayer: number;
  timeRange: [number, number];
  resolution: number; // Ticks per layer
}

export interface TemporalLayer {
  index: number;
  startTick: number;
  endTick: number;
  memories: string[];
  density: number;
  significance: number;
  theme?: string;
}

export interface Exploration {
  id: string;
  startTime: number;
  path: Vector3[];
  memoriesVisited: string[];
  patternsDiscovered: string[];
  insightsGained: string[];
  mode: 'free' | 'guided' | 'search' | 'replay';
}

export interface PalaceStatistics {
  totalMemories: number;
  totalPatterns: number;
  memoryDensity: number;
  consolidationRate: number;
  averageStrength: number;
  oldestMemory: number;
  newestMemory: number;
  mostAccessedMemory: string;
  strongestPattern: string;
  emotionalBalance: EmotionalValence;
}

// Memory queries
export interface MemoryQuery {
  type: QueryType;
  parameters: QueryParameters;
  spatial?: SpatialConstraint;
  temporal?: TemporalConstraint;
  emotional?: EmotionalConstraint;
  limit?: number;
  sort?: SortCriteria;
}

export type QueryType = 
  | 'similar'         // Find similar memories
  | 'associated'      // Find associations
  | 'path'           // Find path between memories
  | 'cluster'        // Find clusters
  | 'pattern'        // Find patterns
  | 'emotional'      // Find by emotion
  | 'temporal';      // Find by time

export interface QueryParameters {
  [key: string]: any;
}

export interface SpatialConstraint {
  center?: Vector3;
  radius?: number;
  sector?: string;
  layer?: number;
}

export interface TemporalConstraint {
  start?: number;
  end?: number;
  tickRange?: [number, number];
  relative?: 'recent' | 'ancient' | 'specific';
}

export interface EmotionalConstraint {
  valence?: [number, number];
  arousal?: [number, number];
  emotions?: EmotionLabel[];
}

export interface SortCriteria {
  field: 'strength' | 'timestamp' | 'importance' | 'access';
  order: 'asc' | 'desc';
}

// Memory visualization
export interface MemoryVisualization {
  geometry: MemoryGeometryType;
  material: MemoryMaterial;
  scale: number;
  glow: GlowEffect;
  particles: ParticleEffect;
  connections: ConnectionVisual[];
}

export type MemoryGeometryType = 
  | 'crystal'         // Crystalline structure
  | 'sphere'          // Simple sphere
  | 'cube'            // Cubic form
  | 'tetrahedron'     // Pyramidal
  | 'organic'         // Blob-like
  | 'fractal'         // Fractal geometry
  | 'neural';         // Neuron-like

export interface MemoryMaterial {
  color: Color;
  opacity: number;
  metalness: number;
  roughness: number;
  emissive: Color;
  emissiveIntensity: number;
  refractionRatio: number;
}

export interface GlowEffect {
  enabled: boolean;
  color: Color;
  intensity: number;
  radius: number;
  pulse: boolean;
  pulseSpeed: number;
}

export interface ParticleEffect {
  enabled: boolean;
  count: number;
  size: number;
  color: Color;
  movement: 'orbit' | 'random' | 'flow';
  speed: number;
}

export interface ConnectionVisual {
  type: 'line' | 'arc' | 'particles' | 'energy';
  color: Color;
  width: number;
  opacity: number;
  animated: boolean;
  pulseSpeed: number;
}
```

---

## 📄 File: `src/modules/memoryPalace/MemoryPalaceCore.ts`
```typescript
import { EventEmitter } from 'events';
import * as THREE from 'three';
import { 
  Memory, 
  MemoryPattern, 
  MemoryPalaceState,
  ConsolidationEvent,
  MemoryQuery,
  SpatialPosition,
  MemoryType,
  ConsolidationType,
  PatternType
} from './types/memory.types';
import { Observation } from '@/modules/owl/types/owl.types';
import { MemoryConsolidator } from './MemoryConsolidator';
import { SpatialOrganizer } from './SpatialOrganizer';
import { TemporalNavigator } from './TemporalNavigator';
import { MemoryRetriever } from './MemoryRetriever';
import { memoryPalaceConfig } from './config/memoryPalace.config';

export class MemoryPalaceCore extends EventEmitter {
  private state: MemoryPalaceState;
  private consolidator: MemoryConsolidator;
  private spatialOrganizer: SpatialOrganizer;
  private temporalNavigator: TemporalNavigator;
  private retriever: MemoryRetriever;
  
  // Performance
  private lastConsolidation = 0;
  private consolidationInterval = 1000; // ms
  
  constructor() {
    super();
    
    this.state = this.initializeState();
    
    // Initialize subsystems
    this.consolidator = new MemoryConsolidator(this);
    this.spatialOrganizer = new SpatialOrganizer(this);
    this.temporalNavigator = new TemporalNavigator(this);
    this.retriever = new MemoryRetriever(this);
    
    // Start consolidation loop
    this.startConsolidationLoop();
  }
  
  private initializeState(): MemoryPalaceState {
    return {
      memories: new Map(),
      patterns: new Map(),
      consolidationQueue: [],
      spatialIndex: {
        sectors: this.initializeSectors(),
        clusters: new Map(),
        connections: [],
        landmarks: []
      },
      temporalIndex: {
        layers: [],
        currentLayer: 0,
        timeRange: [0, 0],
        resolution: 100 // ticks per layer
      },
      activeExplorations: [],
      statistics: {
        totalMemories: 0,
        totalPatterns: 0,
        memoryDensity: 0,
        consolidationRate: 0,
        averageStrength: 0,
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
  
  /**
   * Create memory from Owl observation
   */
  async createMemoryFromObservation(
    observation: Observation,
    systemState: any
  ): Promise<Memory> {
    const spatialPos = await this.spatialOrganizer.calculatePosition(
      observation,
      this.state
    );
    
    const memory: Memory = {
      id: `mem_${observation.id}`,
      type: this.mapObservationToMemoryType(observation.type),
      content: {
        primary: observation.content,
        details: observation.metadata,
        sensory: this.extractSensoryData(observation),
        context: {
          systemState: {
            scup: systemState.scup || 50,
            entropy: systemState.entropy || 0.5,
            mood: systemState.mood || 'contemplative'
          },
          activeModules: observation.metadata.modules || [],
          precedingEvents: this.getRecentMemoryIds(5),
          followingEvents: [] // Will be updated later
        },
        source: {
          type: 'owl',
          moduleId: 'owl',
          reliability: observation.confidence,
          observation
        }
      },
      timestamp: Date.now(),
      tickNumber: observation.tick,
      strength: observation.significance,
      consolidation: 0,
      associations: [],
      spatialPosition: spatialPos,
      temporalLayer: this.temporalNavigator.getCurrentLayer(),
      emotionalValence: this.calculateEmotionalValence(observation),
      accessCount: 0,
      lastAccessed: Date.now(),
      metadata: {
        importance: observation.significance,
        uniqueness: await this.calculateUniqueness(observation),
        coherence: observation.confidence,
        abstractionLevel: this.determineAbstractionLevel(observation),
        crystallized: false,
        tags: this.extractTags(observation)
      }
    };
    
    // Store memory
    this.state.memories.set(memory.id, memory);
    
    // Update statistics
    this.updateStatistics();
    
    // Find associations
    await this.findAndCreateAssociations(memory);
    
    // Queue for consolidation
    this.queueConsolidation(memory);
    
    // Emit event
    this.emit('memoryCreated', memory);
    
    return memory;
  }
  
  /**
   * Consolidation loop
   */
  private startConsolidationLoop() {
    setInterval(async () => {
      if (Date.now() - this.lastConsolidation < this.consolidationInterval) {
        return;
      }
      
      await this.performConsolidation();
      this.lastConsolidation = Date.now();
    }, 100);
  }
  
  private async performConsolidation() {
    // Process consolidation queue
    while (this.state.consolidationQueue.length > 0) {
      const event = this.state.consolidationQueue.shift()!;
      await this.processConsolidationEvent(event);
    }
    
    // Decay old memories
    await this.decayMemories();
    
    // Detect new patterns
    const newPatterns = await this.consolidator.detectPatterns(this.state);
    newPatterns.forEach(pattern => {
      this.state.patterns.set(pattern.id, pattern);
      this.emit('patternEmerged', pattern);
    });
    
    // Crystallize strong memories
    await this.crystallizeMemories();
    
    // Update spatial organization
    await this.spatialOrganizer.reorganize(this.state);
  }
  
  private async processConsolidationEvent(event: ConsolidationEvent) {
    switch (event.type) {
      case 'merge':
        await this.mergeMemories(event);
        break;
      case 'abstract':
        await this.abstractMemories(event);
        break;
      case 'crystallize':
        await this.crystallizeMemory(event);
        break;
      case 'forget':
        await this.forgetMemory(event);
        break;
      case 'transform':
        await this.transformMemory(event);
        break;
      case 'dream':
        await this.dreamRecombination(event);
        break;
    }
  }
  
  private async mergeMemories(event: ConsolidationEvent) {
    const memories = event.sourceMemories.map(id => this.state.memories.get(id)).filter(Boolean) as Memory[];
    if (memories.length < 2) return;
    
    const merged = await this.consolidator.mergeMemories(memories);
    this.state.memories.set(merged.id, merged);
    
    // Remove or weaken source memories
    memories.forEach(mem => {
      mem.strength *= 0.5;
      if (mem.strength < memoryPalaceConfig.decayThreshold) {
        this.state.memories.delete(mem.id);
      }
    });
    
    this.emit('memoriesMerged', { sources: memories, result: merged });
  }
  
  private async abstractMemories(event: ConsolidationEvent) {
    const memories = event.sourceMemories.map(id => this.state.memories.get(id)).filter(Boolean) as Memory[];
    if (memories.length < 3) return;
    
    const abstraction = await this.consolidator.abstractPattern(memories);
    this.state.memories.set(abstraction.id, abstraction);
    
    // Strengthen source memories that contributed
    memories.forEach(mem => {
      mem.consolidation = Math.min(mem.consolidation + 0.1, 1);
    });
    
    this.emit('abstractionCreated', abstraction);
  }
  
  private async crystallizeMemory(event: ConsolidationEvent) {
    const memory = this.state.memories.get(event.sourceMemories[0]);
    if (!memory) return;
    
    memory.metadata.crystallized = true;
    memory.consolidation = 1;
    memory.strength = 1;
    
    // Create landmark
    const landmark = {
      id: `landmark_${memory.id}`,
      position: memory.spatialPosition.position,
      type: 'monument' as const,
      significance: memory.metadata.importance,
      description: `Crystallized: ${memory.content.primary}`,
      linkedMemories: [memory.id]
    };
    
    this.state.spatialIndex.landmarks.push(landmark);
    this.emit('memoryCrystallized', memory);
  }
  
  private async forgetMemory(event: ConsolidationEvent) {
    const memory = this.state.memories.get(event.sourceMemories[0]);
    if (!memory) return;
    
    // Gradually fade
    memory.strength *= 0.9;
    memory.consolidation *= 0.95;
    
    if (memory.strength < memoryPalaceConfig.decayThreshold) {
      this.state.memories.delete(memory.id);
      this.emit('memoryForgotten', memory.id);
    }
  }
  
  private async transformMemory(event: ConsolidationEvent) {
    const memory = this.state.memories.get(event.sourceMemories[0]);
    if (!memory) return;
    
    const transformed = await this.consolidator.transformMemory(memory);
    this.state.memories.set(transformed.id, transformed);
    this.state.memories.delete(memory.id);
    
    this.emit('memoryTransformed', { original: memory, transformed });
  }
  
  private async dreamRecombination(event: ConsolidationEvent) {
    const memories = event.sourceMemories.map(id => this.state.memories.get(id)).filter(Boolean) as Memory[];
    if (memories.length < 2) return;
    
    const dream = await this.consolidator.createDream(memories);
    this.state.memories.set(dream.id, dream);
    
    this.emit('dreamCreated', dream);
  }
  
  /**
   * Memory decay
   */
  private async decayMemories() {
    const now = Date.now();
    
    this.state.memories.forEach((memory, id) => {
      if (memory.metadata.crystallized) return;
      
      // Calculate decay rate
      const age = now - memory.timestamp;
      const accessRecency = now - memory.lastAccessed;
      
      let decayRate = memoryPalaceConfig.baseDecayRate;
      
      // Modify based on factors
      if (memory.consolidation > 0.8) decayRate *= 0.5;
      if (memory.associations.length > 5) decayRate *= 0.7;
      if (accessRecency < 10000) decayRate *= 0.6;
      
      // Apply decay
      memory.strength = Math.max(0, memory.strength - decayRate);
      
      // Remove if below threshold
      if (memory.strength < memoryPalaceConfig.decayThreshold) {
        this.state.memories.delete(id);
        this.emit('memoryDecayed', id);
      }
    });
  }
  
  /**
   * Pattern crystallization
   */
  private async crystallizeMemories() {
    const candidates = Array.from(this.state.memories.values()).filter(mem => 
      !mem.metadata.crystallized &&
      mem.consolidation > 0.9 &&
      mem.strength > 0.8 &&
      mem.accessCount > 10
    );
    
    for (const memory of candidates) {
      this.queueConsolidation(memory, 'crystallize');
    }
  }
  
  /**
   * Query memories
   */
  async queryMemories(query: MemoryQuery): Promise<Memory[]> {
    return this.retriever.query(query, this.state);
  }
  
  /**
   * Access memory (increases strength)
   */
  accessMemory(memoryId: string): Memory | null {
    const memory = this.state.memories.get(memoryId);
    if (!memory) return null;
    
    memory.accessCount++;
    memory.lastAccessed = Date.now();
    memory.strength = Math.min(memory.strength + 0.05, 1);
    
    this.emit('memoryAccessed', memory);
    return memory;
  }
  
  /**
   * Get current state for visualization
   */
  getVisualizationState() {
    return {
      memories: Array.from(this.state.memories.values()),
      patterns: Array.from(this.state.patterns.values()),
      connections: this.getAllConnections(),
      landmarks: this.state.spatialIndex.landmarks,
      statistics: this.state.statistics
    };
  }
  
  /**
   * Helper methods
   */
  private mapObservationToMemoryType(obsType: string): MemoryType {
    const mapping: Record<string, MemoryType> = {
      'pattern': 'pattern',
      'anomaly': 'experience',
      'emergence': 'revelation',
      'transition': 'experience',
      'milestone': 'milestone',
      'hypothesis': 'insight',
      'synthesis': 'insight',
      'question': 'observation'
    };
    return mapping[obsType] || 'observation';
  }
  
  private extractSensoryData(observation: Observation): any {
    return {
      dominant: 'abstract',
      qualities: new Map([
        ['complexity', observation.significance],
        ['clarity', observation.confidence],
        ['intensity', observation.significance]
      ]),
      texture: 'crystalline',
      color: this.getObservationColor(observation.type)
    };
  }
  
  private getObservationColor(type: string): string {
    const colors: Record<string, string> = {
      'pattern': '#4FC3F7',
      'anomaly': '#FF5252',
      'emergence': '#9C27B0',
      'transition': '#FFC107',
      'milestone': '#4CAF50',
      'hypothesis': '#E91E63',
      'synthesis': '#00BCD4',
      'question': '#FF9800'
    };
    return colors[type] || '#9E9E9E';
  }
  
  private calculateEmotionalValence(observation: Observation): any {
    // Simplified emotional calculation
    const isPositive = observation.type === 'milestone' || 
                      observation.type === 'emergence' ||
                      observation.significance > 0.7;
    
    return {
      valence: isPositive ? 0.7 : -0.3,
      arousal: observation.significance,
      dominance: observation.confidence,
      specific: this.inferEmotions(observation)
    };
  }
  
  private inferEmotions(observation: Observation): string[] {
    const emotions = [];
    
    if (observation.type === 'emergence') emotions.push('awe');
    if (observation.type === 'anomaly') emotions.push('surprise');
    if (observation.significance > 0.8) emotions.push('anticipation');
    if (observation.confidence > 0.9) emotions.push('clarity');
    
    return emotions;
  }
  
  private async calculateUniqueness(observation: Observation): Promise<number> {
    // Compare with existing memories
    const similar = await this.retriever.findSimilar(observation.content, 10, this.state);
    
    if (similar.length === 0) return 1;
    
    const avgSimilarity = similar.reduce((sum, mem) => sum + mem.similarity, 0) / similar.length;
    return 1 - avgSimilarity;
  }
  
  private determineAbstractionLevel(observation: Observation): number {
    if (observation.type === 'synthesis') return 0.9;
    if (observation.type === 'pattern') return 0.7;
    if (observation.type === 'hypothesis') return 0.8;
    return 0.3;
  }
  
  private extractTags(observation: Observation): string[] {
    const tags = [...(observation.metadata.tags || [])];
    
    tags.push(observation.type);
    if (observation.significance > 0.8) tags.push('significant');
    if (observation.confidence > 0.9) tags.push('certain');
    
    return tags;
  }
  
  private getRecentMemoryIds(count: number): string[] {
    const memories = Array.from(this.state.memories.values())
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, count);
    
    return memories.map(m => m.id);
  }
  
  private async findAndCreateAssociations(memory: Memory) {
    // Find related memories
    const related = await this.retriever.findRelated(memory, 20, this.state);
    
    related.forEach(rel => {
      if (rel.similarity > 0.5) {
        // Create association
        memory.associations.push({
          targetId: rel.memory.id,
          strength: rel.similarity,
          type: rel.type,
          bidirectional: true,
          formed: Date.now(),
          reinforcements: 0
        });
        
        // Add reverse association
        rel.memory.associations.push({
          targetId: memory.id,
          strength: rel.similarity,
          type: rel.type,
          bidirectional: true,
          formed: Date.now(),
          reinforcements: 0
        });
      }
    });
  }
  
  private queueConsolidation(memory: Memory, type: ConsolidationType = 'merge') {
    this.state.consolidationQueue.push({
      id: `consol_${Date.now()}`,
      timestamp: Date.now(),
      type,
      sourceMemories: [memory.id],
      strength: memory.strength,
      description: `${type} consolidation for ${memory.id}`
    });
  }
  
  private initializeSectors(): Map<string, any> {
    const sectors = new Map();
    
    // Core sectors
    sectors.set('core_insights', {
      id: 'core_insights',
      name: 'Core Insights',
      type: 'core',
      characteristics: ['fundamental', 'stable', 'crystallized'],
      accessibility: 1
    });
    
    sectors.set('active_patterns', {
      id: 'active_patterns',
      name: 'Active Patterns',
      type: 'peripheral',
      characteristics: ['dynamic', 'emerging', 'volatile'],
      accessibility: 0.8
    });
    
    sectors.set('deep_memory', {
      id: 'deep_memory',
      name: 'Deep Memory',
      type: 'deep',
      characteristics: ['ancient', 'foundational', 'unconscious'],
      accessibility: 0.3
    });
    
    return sectors;
  }
  
  private updateStatistics() {
    const stats = this.state.statistics;
    const memories = Array.from(this.state.memories.values());
    
    stats.totalMemories = memories.length;
    stats.totalPatterns = this.state.patterns.size;
    
    if (memories.length > 0) {
      stats.averageStrength = memories.reduce((sum, m) => sum + m.strength, 0) / memories.length;
      
      const sorted = memories.sort((a, b) => a.timestamp - b.timestamp);
      stats.oldestMemory = sorted[0].timestamp;
      stats.newestMemory = sorted[sorted.length - 1].timestamp;
      
      const mostAccessed = memories.sort((a, b) => b.accessCount - a.accessCount)[0];
      stats.mostAccessedMemory = mostAccessed.id;
      
      // Emotional balance
      const totalValence = memories.reduce((sum, m) => sum + m.emotionalValence.valence, 0);
      const totalArousal = memories.reduce((sum, m) => sum + m.emotionalValence.arousal, 0);
      
      stats.emotionalBalance = {
        valence: totalValence / memories.length,
        arousal: totalArousal / memories.length,
        dominance: 0.5,
        specific: []
      };
    }
    
    // Memory density (memories per temporal unit)
    if (stats.newestMemory > stats.oldestMemory) {
      const timeSpan = stats.newestMemory - stats.oldestMemory;
      stats.memoryDensity = stats.totalMemories / (timeSpan / 1000 / 60); // per minute
    }
  }
  
  private getAllConnections(): any[] {
    const connections: any[] = [];
    
    this.state.memories.forEach(memory => {
      memory.associations.forEach(assoc => {
        const target = this.state.memories.get(assoc.targetId);
        if (target) {
          connections.push({
            from: memory.spatialPosition.position,
            to: target.spatialPosition.position,
            strength: assoc.strength,
            type: 'association',
            active: true
          });
        }
      });
    });
    
    return connections;
  }
}

// Export singleton
export const memoryPalace = new MemoryPalaceCore();
```

---

## 📄 File: `src/modules/memoryPalace/components/MemoryPalaceViewer.tsx`
```typescript
import React, { useRef, useEffect, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Stars } from '@react-three/drei';
import { motion } from 'framer-motion';
import { 
  Memory, 
  MemoryPattern,
  MemoryVisualization 
} from '../types/memory.types';
import { useMemoryPalace } from '../hooks/useMemoryPalace';
import { useMemoryNavigation } from '../hooks/useMemoryNavigation';
import { MemoryNode } from '../three/MemoryNode';
import { MemoryConnection } from '../three/MemoryConnection';
import { PatternVisualization } from '../three/PatternVisualization';
import { MemoryExplorer } from './MemoryExplorer';
import { TemporalControls } from './TemporalControls';
import { MemoryInspector } from './MemoryInspector';
import * as styles from './MemoryPalaceViewer.styles';

export interface MemoryPalaceViewerProps {
  className?: string;
  onMemorySelect?: (memory: Memory) => void;
  onPatternSelect?: (pattern: MemoryPattern) => void;
}

export const MemoryPalaceViewer: React.FC<MemoryPalaceViewerProps> = ({
  className,
  onMemorySelect,
  onPatternSelect
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null);
  const [selectedPattern, setSelectedPattern] = useState<MemoryPattern | null>(null);
  const [viewMode, setViewMode] = useState<'spatial' | 'temporal' | 'emotional'>('spatial');
  
  const { 
    memories, 
    patterns, 
    connections, 
    landmarks,
    statistics,
    isLoading 
  } = useMemoryPalace();
  
  const {
    cameraPosition,
    setCameraPosition,
    navigateToMemory,
    navigateToPattern
  } = useMemoryNavigation();
  
  const handleMemoryClick = useCallback((memory: Memory) => {
    setSelectedMemory(memory);
    onMemorySelect?.(memory);
    navigateToMemory(memory);
  }, [onMemorySelect, navigateToMemory]);
  
  const handlePatternClick = useCallback((pattern: MemoryPattern) => {
    setSelectedPattern(pattern);
    onPatternSelect?.(pattern);
    navigateToPattern(pattern);
  }, [onPatternSelect, navigateToPattern]);
  
  return (
    <div ref={containerRef} className={`${styles.container} ${className || ''}`}>
      {/* 3D Scene */}
      <Canvas
        className={styles.canvas}
        camera={{ position: [0, 50, 100], fov: 60 }}
        gl={{ antialias: true, alpha: true }}
      >
        <fog attach="fog" args={['#000033', 50, 500]} />
        <ambientLight intensity={0.2} />
        <pointLight position={[0, 100, 0]} intensity={0.5} />
        
        <Stars
          radius={300}
          depth={50}
          count={5000}
          factor={4}
          saturation={0}
          fade
        />
        
        {/* Memory Nodes */}
        {memories.map(memory => (
          <MemoryNode
            key={memory.id}
            memory={memory}
            selected={selectedMemory?.id === memory.id}
            onClick={() => handleMemoryClick(memory)}
            viewMode={viewMode}
          />
        ))}
        
        {/* Pattern Visualizations */}
        {patterns.map(pattern => (
          <PatternVisualization
            key={pattern.id}
            pattern={pattern}
            memories={memories}
            selected={selectedPattern?.id === pattern.id}
            onClick={() => handlePatternClick(pattern)}
          />
        ))}
        
        {/* Connections */}
        {connections.map((connection, index) => (
          <MemoryConnection
            key={index}
            connection={connection}
            animated={true}
          />
        ))}
        
        {/* Landmarks */}
        {landmarks.map(landmark => (
          <LandmarkMarker
            key={landmark.id}
            landmark={landmark}
          />
        ))}
        
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={10}
          maxDistance={500}
          maxPolarAngle={Math.PI * 0.9}
        />
        
        <CameraController position={cameraPosition} />
      </Canvas>
      
      {/* UI Overlays */}
      <div className={styles.uiOverlay}>
        {/* View Mode Selector */}
        <div className={styles.viewModeSelector}>
          {(['spatial', 'temporal', 'emotional'] as const).map(mode => (
            <motion.button
              key={mode}
              className={styles.viewModeButton(viewMode === mode)}
              onClick={() => setViewMode(mode)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {mode}
            </motion.button>
          ))}
        </div>
        
        {/* Statistics Panel */}
        <motion.div 
          className={styles.statsPanel}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h4>Memory Palace</h4>
          <div className={styles.statItem}>
            <span>Memories</span>
            <span>{statistics.totalMemories}</span>
          </div>
          <div className={styles.statItem}>
            <span>Patterns</span>
            <span>{statistics.totalPatterns}</span>
          </div>
          <div className={styles.statItem}>
            <span>Avg Strength</span>
            <span>{(statistics.averageStrength * 100).toFixed(0)}%</span>
          </div>
          <div className={styles.statItem}>
            <span>Emotional Balance</span>
            <div className={styles.emotionIndicator(statistics.emotionalBalance.valence)} />
          </div>
        </motion.div>
        
        {/* Memory Explorer */}
        <MemoryExplorer
          memories={memories}
          onMemorySelect={handleMemoryClick}
          selectedMemory={selectedMemory}
        />
        
        {/* Temporal Controls */}
        {viewMode === 'temporal' && (
          <TemporalControls
            onTimeChange={(time) => console.log('Time:', time)}
          />
        )}
        
        {/* Memory Inspector */}
        {selectedMemory && (
          <MemoryInspector
            memory={selectedMemory}
            onClose={() => setSelectedMemory(null)}
          />
        )}
      </div>
      
      {/* Loading Indicator */}
      {isLoading && (
        <div className={styles.loadingOverlay}>
          <div className={styles.loadingSpinner} />
          <span>Loading memories...</span>
        </div>
      )}
    </div>
  );
};

// Camera controller component
const CameraController: React.FC<{ position: THREE.Vector3 }> = ({ position }) => {
  const { camera } = useThree();
  
  useFrame(() => {
    camera.position.lerp(position, 0.05);
    camera.lookAt(0, 0, 0);
  });
  
  return null;
};

// Landmark visualization
const LandmarkMarker: React.FC<{ landmark: any }> = ({ landmark }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
      meshRef.current.position.y = landmark.position.y + Math.sin(state.clock.elapsedTime) * 2;
    }
  });
  
  return (
    <mesh ref={meshRef} position={landmark.position}>
      <coneGeometry args={[2, 4, 8]} />
      <meshStandardMaterial
        color="#FFD700"
        emissive="#FFD700"
        emissiveIntensity={0.5}
        metalness={0.8}
        roughness={0.2}
      />
    </mesh>
  );
};
```

---

## 📄 File: `src/modules/memoryPalace/three/MemoryNode.tsx`
```typescript
import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Memory } from '../types/memory.types';
import { Text } from '@react-three/drei';

interface MemoryNodeProps {
  memory: Memory;
  selected: boolean;
  onClick: () => void;
  viewMode: 'spatial' | 'temporal' | 'emotional';
}

export const MemoryNode: React.FC<MemoryNodeProps> = ({
  memory,
  selected,
  onClick,
  viewMode
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  // Calculate visual properties
  const { geometry, material, scale, glowMaterial } = useMemo(() => {
    const geom = getMemoryGeometry(memory);
    const mat = getMemoryMaterial(memory, viewMode);
    const s = getMemoryScale(memory);
    const glow = getGlowMaterial(memory);
    
    return { geometry: geom, material: mat, scale: s, glowMaterial: glow };
  }, [memory, viewMode]);
  
  // Animation
  useFrame((state) => {
    if (!meshRef.current) return;
    
    // Breathing effect
    const breathingScale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05 * memory.strength;
    meshRef.current.scale.setScalar(scale * breathingScale);
    
    // Rotation based on type
    if (memory.type === 'insight' || memory.type === 'revelation') {
      meshRef.current.rotation.y += 0.01;
    }
    
    // Pulse when selected
    if (selected && glowRef.current) {
      glowRef.current.scale.setScalar(scale * breathingScale * 1.3);
      (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 
        0.3 + Math.sin(state.clock.elapsedTime * 4) * 0.2;
    }
    
    // Float effect
    meshRef.current.position.y = memory.spatialPosition.position.y + 
      Math.sin(state.clock.elapsedTime + memory.timestamp) * 0.5;
  });
  
  // Position based on view mode
  const position = useMemo(() => {
    switch (viewMode) {
      case 'temporal':
        return new THREE.Vector3(
          (memory.tickNumber % 100) * 2 - 100,
          memory.temporalLayer * 20,
          Math.floor(memory.tickNumber / 100) * 10
        );
      case 'emotional':
        return new THREE.Vector3(
          memory.emotionalValence.valence * 100,
          memory.emotionalValence.arousal * 100,
          memory.emotionalValence.dominance * 100
        );
      default:
        return memory.spatialPosition.position;
    }
  }, [memory, viewMode]);
  
  return (
    <group position={position}>
      {/* Glow effect */}
      {(selected || hovered) && (
        <mesh ref={glowRef} scale={scale * 1.2}>
          <sphereGeometry args={[1, 16, 16]} />
          <meshBasicMaterial
            color={material.color}
            transparent
            opacity={0.3}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Main memory geometry */}
      <mesh
        ref={meshRef}
        scale={scale}
        onClick={(e) => {
          e.stopPropagation();
          onClick();
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        {geometry}
        {material}
      </mesh>
      
      {/* Label */}
      {(selected || hovered) && (
        <Text
          position={[0, scale + 2, 0]}
          fontSize={1}
          color="white"
          anchorX="center"
          anchorY="bottom"
        >
          {memory.content.primary.substring(0, 30)}...
        </Text>
      )}
      
      {/* Crystallized indicator */}
      {memory.metadata.crystallized && (
        <mesh position={[0, scale + 1, 0]} scale={0.5}>
          <octahedronGeometry args={[1, 0]} />
          <meshStandardMaterial
            color="#FFD700"
            emissive="#FFD700"
            emissiveIntensity={0.5}
            metalness={1}
            roughness={0}
          />
        </mesh>
      )}
    </group>
  );
};

// Helper functions
function getMemoryGeometry(memory: Memory): THREE.BufferGeometry {
  switch (memory.type) {
    case 'milestone':
      return new THREE.OctahedronGeometry(1, 0);
    case 'pattern':
      return new THREE.TetrahedronGeometry(1, 0);
    case 'insight':
    case 'revelation':
      return new THREE.IcosahedronGeometry(1, 0);
    case 'dream':
      return new THREE.SphereGeometry(1, 8, 6);
    default:
      return new THREE.BoxGeometry(1, 1, 1);
  }
}

function getMemoryMaterial(memory: Memory, viewMode: string): THREE.Material {
  const color = new THREE.Color(memory.content.sensory.color);
  
  if (memory.metadata.crystallized) {
    return new THREE.MeshPhysicalMaterial({
      color,
      metalness: 0.9,
      roughness: 0.1,
      clearcoat: 1,
      clearcoatRoughness: 0,
      reflectivity: 1,
      transparent: true,
      opacity: 0.9,
      side: THREE.DoubleSide
    });
  }
  
  return new THREE.MeshStandardMaterial({
    color,
    emissive: color,
    emissiveIntensity: memory.strength * 0.3,
    metalness: memory.consolidation * 0.5,
    roughness: 1 - memory.consolidation * 0.5,
    transparent: true,
    opacity: 0.3 + memory.strength * 0.7,
    side: THREE.DoubleSide
  });
}

function getMemoryScale(memory: Memory): number {
  const baseScale = 1;
  const importanceScale = memory.metadata.importance * 2;
  const strengthScale = memory.strength;
  const consolidationScale = memory.consolidation * 0.5;
  
  return baseScale + importanceScale + strengthScale + consolidationScale;
}

function getGlowMaterial(memory: Memory): THREE.Material {
  const color = new THREE.Color(memory.content.sensory.color);
  
  return new THREE.MeshBasicMaterial({
    color,
    transparent: true,
    opacity: 0.3,
    side: THREE.BackSide
  });
}
```

---

## 📄 File: `src/modules/memoryPalace/hooks/useMemoryPalace.ts`
```typescript
import { useState, useEffect, useCallback } from 'react';
import { Memory, MemoryPattern, MemoryQuery } from '../types/memory.types';
import { memoryPalace } from '../MemoryPalaceCore';
import { Observation } from '@/modules/owl/types/owl.types';
import { useConsciousness } from '@/hooks/useConsciousness';

export function useMemoryPalace() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [patterns, setPatterns] = useState<MemoryPattern[]>([]);
  const [connections, setConnections] = useState<any[]>([]);
  const [landmarks, setLandmarks] = useState<any[]>([]);
  const [statistics, setStatistics] = useState<any>({});
  const [isLoading, setIsLoading] = useState(true);
  
  const consciousness = useConsciousness();
  
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
  
  // Create memory from observation
  const createMemoryFromObservation = useCallback(async (observation: Observation) => {
    const systemState = {
      scup: consciousness.scup,
      entropy: consciousness.entropy,
      mood: consciousness.mood
    };
    
    return memoryPalace.createMemoryFromObservation(observation, systemState);
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
    createMemoryFromObservation,
    queryMemories,
    accessMemory
  };
}
```

---

## 📄 File: `src/modules/memoryPalace/config/memoryPalace.config.ts`
```typescript
export const memoryPalaceConfig = {
  // Spatial organization
  spatial: {
    sectorRadius: 100,
    layerHeight: 50,
    clusterThreshold: 0.7,
    connectionDistance: 50,
    repulsionForce: 0.1,
    attractionForce: 0.05
  },
  
  // Memory lifecycle
  memory: {
    decayThreshold: 0.1,
    baseDecayRate: 0.001,
    crystallizationThreshold: 0.9,
    consolidationInterval: 1000, // ms
    maxMemories: 10000,
    maxAssociations: 20
  },
  
  // Pattern detection
  patterns: {
    minMemoriesForPattern: 3,
    patternSimilarityThreshold: 0.6,
    patternStrengthThreshold: 0.5,
    maxPatternsPerCycle: 10
  },
  
  // Visualization
  visualization: {
    particleCount: 1000,
    connectionOpacity: 0.3,
    glowIntensity: 0.5,
    animationSpeed: 1,
    cameraSpeed: 0.05
  },
  
  // Performance
  performance: {
    maxRenderDistance: 500,
    lodDistances: [50, 150, 300],
    updateInterval: 100, // ms
    batchSize: 50
  }
};
```

---

## Cursor Implementation Prompts

### Phase 1: Create Structure
```
Create the complete Memory Palace module structure based on this blueprint:
1. All TypeScript types in types/ directory
2. Core classes (MemoryPalaceCore, MemoryConsolidator, etc.)
3. Three.js components for 3D visualization
4. React components with glass morphism styling
5. Hooks for state management
6. Configuration file

Ensure all imports are correct and follow DAWN's established patterns.
```

### Phase 2: Implement Three.js Scene
```
Implement the Three.js components for Memory Palace:
1. MemoryScene with proper lighting and fog
2. MemoryNode with geometry based on memory type
3. MemoryConnection with animated particles
4. PatternVisualization showing emergent patterns
5. Camera controls for first-person exploration

Use @react-three/fiber and @react-three/drei for React integration.
```

### Phase 3: Connect to Owl
```
Integrate Memory Palace with the Owl module:
1. Subscribe to Owl observations
2. Convert observations to memories
3. Update consolidation based on Owl insights
4. Display Owl's strategic plans as memory patterns

The memories should accumulate and form patterns as Owl observes the system.
```

### Phase 4: Add Temporal Navigation
```
Implement temporal navigation features:
1. Time scrubbing slider
2. Temporal layers visualization
3. Memory replay functionality
4. Historical pattern analysis

Users should be able to navigate through time and see how memories evolved.
```

This Memory Palace creates a living, breathing space where DAWN's experiences crystallize into lasting patterns. Memories decay and strengthen based on access and importance, while patterns emerge from the constellation of related experiences. The 3D visualization allows users to literally walk through the AI's memory architecture! 🏛️✨