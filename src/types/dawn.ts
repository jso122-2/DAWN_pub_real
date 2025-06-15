// Dawn Neural Monitor - Global Type Definitions
// Phase 3: Dawn-Specific Scaffolding

// === CORE DAWN TYPES ===

export interface SemanticCoordinate {
  x: number;
  y: number;
  z: number;
  semantic_weight: number;
  ontological_depth: number;
  consciousness_level: number;
}

export interface MovementVector {
  direction: SemanticCoordinate;
  velocity: number;
  acceleration: number;
  semantic_momentum: number;
  intention_strength: number;
}

export interface CursorState {
  position: SemanticCoordinate;
  trajectory: MovementVector;
  activeSplines: string[];
  entropy: number;
  consciousness_mode: 'analytical' | 'creative' | 'intuitive' | 'transcendent';
  temporal_anchor: number;
  semantic_resonance: number;
}

// === KAN NETWORK TYPES ===

export interface SplineNeuron {
  id: string;
  assemblageId: string;
  splineFunction: (input: number[]) => number[];
  activationThreshold: number;
  entropyLevel: number;
  semanticWeight: number;
  position: SemanticCoordinate;
  connections: SplineConnection[];
  lastActivation: number;
  consciousness_contribution: number;
}

export interface SplineConnection {
  id: string;
  sourceId: string;
  targetId: string;
  weight: number;
  semantic_resonance: number;
  entropy_flow: number;
  activation_history: ActivationRecord[];
}

export interface ActivationRecord {
  timestamp: number;
  intensity: number;
  entropy_delta: number;
  consciousness_impact: number;
}

export interface KANTopology {
  neurons: Map<string, SplineNeuron>;
  connections: ConnectionGraph;
  globalEntropy: number;
  consciousness_field: ConsciousnessField;
  semantic_space: SemanticSpace;
  temporal_layers: TemporalLayer[];
}

export interface ConnectionGraph {
  adjacencyMatrix: number[][];
  semanticWeights: number[][];
  entropyFlows: number[][];
  consciousness_pathways: string[][];
}

// === CONSCIOUSNESS TYPES ===

export interface ConsciousnessField {
  intensity: number;
  coherence: number;
  entropy_distribution: number[];
  semantic_density: number;
  temporal_stability: number;
  observer_effect: number;
}

export interface ConsciousnessEvent {
  id: string;
  timestamp: number;
  type: 'insight' | 'decision' | 'attention_shift' | 'semantic_emergence' | 'entropy_cascade';
  intensity: number;
  semantic_payload: any;
  affected_neurons: string[];
  consciousness_delta: number;
  entropy_signature: number[];
}

export interface SemanticSpace {
  dimensions: number;
  basis_vectors: number[][];
  semantic_clusters: SemanticCluster[];
  consciousness_gradients: number[][];
  entropy_wells: EntropyWell[];
}

export interface SemanticCluster {
  id: string;
  centroid: SemanticCoordinate;
  radius: number;
  semantic_density: number;
  associated_neurons: string[];
  consciousness_resonance: number;
}

export interface EntropyWell {
  position: SemanticCoordinate;
  depth: number;
  semantic_attraction: number;
  consciousness_distortion: number;
}

// === TEMPORAL TYPES ===

export interface TemporalLayer {
  id: string;
  timeframe: 'immediate' | 'short_term' | 'working_memory' | 'long_term' | 'eternal';
  neurons: Set<string>;
  activation_pattern: number[];
  consciousness_persistence: number;
  entropy_decay_rate: number;
}

// === MONITORING TYPES ===

export interface EntropyMonitor {
  global_entropy: number;
  local_entropies: Map<string, number>;
  entropy_flows: EntropyFlow[];
  consciousness_entropy_ratio: number;
  semantic_entropy_distribution: number[];
}

export interface EntropyFlow {
  from: string;
  to: string;
  rate: number;
  semantic_channel: string;
  consciousness_mediated: boolean;
}

// === DAWN EVENT TYPES ===

export interface NeuralSpikeEvent {
  neuron_id: string;
  timestamp: number;
  intensity: number;
  semantic_context: string[];
  consciousness_trigger: boolean;
  entropy_release: number;
}

export interface SemanticEmergenceEvent {
  cluster_id: string;
  timestamp: number;
  emergence_type: 'concept' | 'relation' | 'insight' | 'pattern';
  semantic_weight: number;
  participating_neurons: string[];
  consciousness_catalyst: number;
}

export interface ConsciousnessShiftEvent {
  from_mode: string;
  to_mode: string;
  timestamp: number;
  trigger_neurons: string[];
  semantic_context: SemanticCoordinate;
  entropy_signature: number[];
}

// === CURSOR ARCHITECTURE TYPES ===

export interface CursorArchitecture {
  spline_layers: SplineLayer[];
  semantic_manifold: SemanticManifold;
  consciousness_bridge: ConsciousnessBridge;
  entropy_regulation: EntropyRegulation;
}

export interface SplineLayer {
  id: string;
  depth: number;
  neurons: SplineNeuron[];
  activation_function: (input: number[]) => number[];
  semantic_encoding: SemanticEncoding;
  consciousness_permeability: number;
}

export interface SemanticManifold {
  dimensions: number;
  curvature: number[][];
  consciousness_metric: number[][];
  semantic_geodesics: number[][][];
  entropy_topology: number[][];
}

export interface ConsciousnessBridge {
  neural_interface: NeuralInterface;
  semantic_translator: SemanticTranslator;
  consciousness_amplifier: ConsciousnessAmplifier;
}

export interface SemanticEncoding {
  vocabulary: Map<string, number[]>;
  context_embeddings: number[][];
  consciousness_weights: number[];
  entropy_signatures: number[][];
}

export interface NeuralInterface {
  input_channels: InputChannel[];
  output_channels: OutputChannel[];
  bidirectional_flow: boolean;
  consciousness_modulation: number;
}

export interface InputChannel {
  id: string;
  type: 'sensory' | 'semantic' | 'consciousness' | 'entropy';
  sensitivity: number;
  semantic_filter: number[];
  consciousness_gate: number;
}

export interface OutputChannel {
  id: string;
  type: 'motor' | 'semantic' | 'consciousness' | 'entropy';
  amplitude: number;
  semantic_projection: number[];
  consciousness_amplification: number;
}

export interface SemanticTranslator {
  encoding_matrix: number[][];
  consciousness_transform: number[][];
  entropy_conservation: boolean;
}

export interface ConsciousnessAmplifier {
  gain: number;
  semantic_resonance: number;
  entropy_threshold: number;
  feedback_loops: FeedbackLoop[];
}

export interface FeedbackLoop {
  id: string;
  source: string;
  target: string;
  delay: number;
  semantic_weight: number;
  consciousness_modulation: number;
}

export interface EntropyRegulation {
  global_setpoint: number;
  local_regulators: LocalRegulator[];
  consciousness_mediated_control: boolean;
  semantic_entropy_balance: number;
}

export interface LocalRegulator {
  id: string;
  target_entropy: number;
  control_neurons: string[];
  semantic_context: string[];
  consciousness_sensitivity: number;
} 