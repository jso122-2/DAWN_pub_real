// Core Owl state
export interface OwlState {
  id: string;
  currentFocus: SemanticFocus;
  activeSchemas: ActiveSchema[];
  planHorizon: TemporalHorizon;
  observationBuffer: Observation[];
  reflectionDepth: number; // 0-10, contemplation depth
  unityScore: number; // 0-1, internal consistency
  lastReflection: number; // timestamp
  semanticPosition: SemanticPosition;
  attentionAllocation: AttentionMap;
}

// What Owl is contemplating
export interface SemanticFocus {
  primary: string; // Main concept
  secondary: string[]; // Related concepts
  weight: number; // 0-1 importance
  ticksInFocus: number;
  momentum: SemanticVector; // Direction of thought
}

// Attention distribution across modules
export interface AttentionMap {
  modules: Map<string, number>; // module -> attention weight
  totalCapacity: number;
  utilizationRate: number;
}

// Active narrative schemas
export interface ActiveSchema {
  id: string;
  name: string;
  type: SchemaType;
  alignment: number; // 0-1
  trajectory: TrajectoryPoint[];
  confidence: number;
  phase: SchemaPhase;
  metadata: SchemaMetadata;
}

export type SchemaType = 
  | 'narrative'      // Story progression
  | 'cyclical'       // Repeating patterns
  | 'convergent'     // Goal-directed
  | 'divergent'      // Exploratory
  | 'emergent'       // Self-organizing
  | 'archetypal'     // Universal patterns
  | 'transformative' // State transitions
  | 'harmonic';      // Resonant patterns

export interface SchemaPhase {
  current: string;
  elapsed: number; // ticks in phase
  expected: number; // expected duration
  transitions: SchemaTransition[];
}

export interface SchemaTransition {
  to: string;
  probability: number;
  conditions: string[];
}

export interface SchemaMetadata {
  origin: 'detected' | 'induced' | 'inherited';
  strength: number;
  resonance: number; // with other schemas
  lastUpdated: number;
}

// Position in semantic space
export interface SemanticPosition {
  coordinates: Map<string, number>; // dimension -> value
  embedding?: number[]; // Vector representation
  neighborhood: SemanticRegion;
}

export interface SemanticRegion {
  name: string;
  characteristics: string[];
  stability: number;
  attractors: SemanticAttractor[];
}

export interface SemanticAttractor {
  position: SemanticPosition;
  strength: number;
  basin: number; // radius of influence
}

// Movement in semantic space
export interface SemanticVector {
  components: Map<string, number>;
  magnitude: number;
  normalized: Map<string, number>;
}

// Temporal reasoning spans
export interface TemporalHorizon {
  immediate: number;   // 1-10 ticks
  near: number;       // 10-100 ticks  
  medium: number;     // 100-1000 ticks
  far: number;        // 1000-10000 ticks
  epochal: number;    // 10000+ ticks
  adaptiveWindows: AdaptiveWindow[];
}

export interface AdaptiveWindow {
  name: string;
  start: number;
  end: number;
  significance: number;
  events: string[];
}

// Point on trajectory
export interface TrajectoryPoint {
  tick: number;
  position: SemanticPosition;
  velocity: SemanticVector;
  acceleration: SemanticVector;
  significance: number;
  markers: TrajectoryMarker[];
}

export interface TrajectoryMarker {
  type: 'milestone' | 'inflection' | 'anomaly' | 'attractor';
  description: string;
  impact: number;
}

// Observations
export interface Observation {
  id: string;
  tick: number;
  type: ObservationType;
  subject: string;
  content: string;
  significance: number;
  confidence: number;
  connections: ObservationLink[];
  metadata: ObservationMetadata;
  reflections: Reflection[];
}

export type ObservationType = 
  | 'pattern'        // Recognized pattern
  | 'anomaly'        // Deviation from expected
  | 'emergence'      // New phenomenon
  | 'transition'     // State change
  | 'milestone'      // Significant achievement
  | 'hypothesis'     // Predictive insight
  | 'synthesis'      // Combined understanding
  | 'question';      // Open inquiry

export interface ObservationLink {
  targetId: string;
  relationship: LinkType;
  strength: number;
}

export type LinkType = 
  | 'causes'
  | 'correlates'
  | 'contradicts'
  | 'reinforces'
  | 'questions'
  | 'explains';

export interface ObservationMetadata {
  modules: string[];
  schemas: string[];
  confidence: number;
  processingDepth: number;
  tags: string[];
}

// Deep reflection
export interface Reflection {
  depth: number; // How many layers deep
  insight: string;
  connections: string[]; // Connected observations
  implications: string[];
  uncertainty: number;
}

// Owl responses
export interface OwlResponse {
  observations: Observation[];
  activePlans: StrategicPlan[];
  schemaAlignments: SchemaAlignment[];
  recommendations: StrategicRecommendation[];
  reflections: ReflectionEntry[];
  predictions: Prediction[];
  metadata: ResponseMetadata;
}

export interface SchemaAlignment {
  schemaId: string;
  alignment: number;
  trajectory: TrajectoryPoint[];
  phase: string;
  momentum: number;
}

export interface Prediction {
  type: 'state' | 'event' | 'pattern' | 'milestone';
  description: string;
  timeframe: number; // ticks
  probability: number;
  confidence: number;
  assumptions: string[];
}

export interface ReflectionEntry {
  id: string;
  timestamp: number;
  depth: number;
  content: string;
  insights: Insight[];
  questions: string[];
  synthesis?: string;
  emotionalTone: EmotionalTone;
}

export interface Insight {
  id: string;
  type: InsightType;
  content: string;
  novelty: number; // How new/surprising
  confidence: number;
  actionable: boolean;
  implications: string[];
  relatedObservations: string[];
}

export type InsightType = 
  | 'pattern'
  | 'connection'
  | 'prediction'
  | 'warning'
  | 'opportunity'
  | 'understanding'
  | 'question';

export interface EmotionalTone {
  valence: number; // -1 to 1
  arousal: number; // 0 to 1
  dominance: number; // 0 to 1
  qualities: string[]; // descriptive terms
}

export interface ResponseMetadata {
  processingTime: number;
  reflectionDepth: number;
  confidenceLevel: number;
  unityScore: number;
  observationCount: number;
  insightNovelty: number;
}

// Strategic plans (simplified reference)
export interface StrategicPlan {
  id: string;
  name: string;
  description: string;
  horizon: number;
  confidence: number;
  status: 'conceptual' | 'proposed' | 'active' | 'suspended' | 'completed';
}

// Strategic recommendations (simplified reference)
export interface StrategicRecommendation {
  id: string;
  type: 'course_correction' | 'opportunity' | 'risk_mitigation' | 'optimization';
  urgency: number; // 0-10
  importance: number; // 0-10
  description: string;
  rationale: string;
  confidence: number;
} 