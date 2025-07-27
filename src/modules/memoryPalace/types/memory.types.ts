import * as THREE from 'three';

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
  observation?: any; // Owl observation
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
  position: THREE.Vector3;
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
  unity: number;
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
  centerPoint: THREE.Vector3;
  boundingBox: BoundingBox;
}

export interface BoundingBox {
  min: THREE.Vector3;
  max: THREE.Vector3;
  center: THREE.Vector3;
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
  center: THREE.Vector3;
  memories: string[];
  unity: number;
  label: string;
  color: THREE.Color;
}

export interface SpatialConnection {
  from: THREE.Vector3;
  to: THREE.Vector3;
  strength: number;
  type: 'association' | 'path' | 'portal';
  active: boolean;
}

export interface Landmark {
  id: string;
  position: THREE.Vector3;
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
  path: THREE.Vector3[];
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
  center?: THREE.Vector3;
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
  color: THREE.Color;
  opacity: number;
  metalness: number;
  roughness: number;
  emissive: THREE.Color;
  emissiveIntensity: number;
  refractionRatio: number;
}

export interface GlowEffect {
  enabled: boolean;
  color: THREE.Color;
  intensity: number;
  radius: number;
  pulse: boolean;
  pulseSpeed: number;
}

export interface ParticleEffect {
  enabled: boolean;
  count: number;
  size: number;
  color: THREE.Color;
  movement: 'orbit' | 'random' | 'flow';
  speed: number;
}

export interface ConnectionVisual {
  type: 'line' | 'arc' | 'particles' | 'energy';
  color: THREE.Color;
  width: number;
  opacity: number;
  animated: boolean;
  pulseSpeed: number;
} 