import { Vector3, Color } from 'three';

// Core neural types
export interface Neuron {
  id: string;
  type: NeuronType;
  position: Vector3;
  layer: NetworkLayer;
  region: BrainRegion;
  state: NeuronState;
  connections: SynapticConnection[];
  metadata: NeuronMetadata;
}

export type NeuronType = 
  | 'sensory'        // Input neurons
  | 'motor'          // Output neurons
  | 'interneuron'    // Hidden layer neurons
  | 'pyramidal'      // Complex processing
  | 'mirror'         // Mirroring behavior
  | 'grandmother'    // Highly selective
  | 'place'          // Spatial encoding
  | 'grid';          // Grid-like firing

export interface NetworkLayer {
  index: number;
  name: string;
  type: LayerType;
  neuronCount: number;
  position: Vector3; // Center position
  radius: number;
  activation: number; // Overall activation
}

export type LayerType = 
  | 'input'
  | 'hidden'
  | 'output'
  | 'recurrent'
  | 'attention'
  | 'memory';

export interface BrainRegion {
  id: string;
  name: string;
  type: RegionType;
  center: Vector3;
  radius: number;
  neurons: string[]; // Neuron IDs
  function: string;
  currentActivity: number;
  connections: RegionalConnection[];
}

export type RegionType = 
  | 'sensory_cortex'
  | 'motor_cortex'
  | 'prefrontal'
  | 'temporal'
  | 'parietal'
  | 'occipital'
  | 'hippocampus'
  | 'amygdala'
  | 'thalamus'
  | 'cerebellum';

export interface NeuronState {
  potential: number; // Membrane potential (-70 to +40 mV)
  threshold: number; // Firing threshold
  firing: boolean;
  lastFired: number; // Timestamp
  firingRate: number; // Hz
  refractory: boolean;
  fatigue: number; // 0-1
  health: number; // 0-1
}

export interface SynapticConnection {
  id: string;
  preNeuronId: string;
  postNeuronId: string;
  weight: number; // Connection strength
  type: SynapseType;
  plasticity: number; // Learning rate
  delay: number; // Signal delay in ms
  active: boolean;
  lastActivated: number;
  metadata: SynapseMetadata;
}

export type SynapseType = 
  | 'excitatory'
  | 'inhibitory'
  | 'modulatory'
  | 'electrical';

export interface SynapseMetadata {
  neurotransmitter: Neurotransmitter;
  receptorType: string;
  strengthHistory: number[]; // Recent weight changes
  activityCount: number;
}

export type Neurotransmitter = 
  | 'glutamate'      // Excitatory
  | 'gaba'           // Inhibitory
  | 'dopamine'       // Reward/motivation
  | 'serotonin'      // Mood/emotion
  | 'norepinephrine' // Attention/arousal
  | 'acetylcholine'  // Learning/memory
  | 'endorphin';     // Pleasure/pain

export interface NeuronMetadata {
  birthTick: number;
  totalFirings: number;
  averageActivity: number;
  preferredInput: string;
  receptiveField: ReceptiveField;
  plasticityRate: number;
}

export interface ReceptiveField {
  shape: 'circular' | 'gaussian' | 'oriented' | 'complex';
  size: number;
  orientation?: number;
  selectivity: number;
}

export interface RegionalConnection {
  targetRegionId: string;
  connectionType: 'feedforward' | 'feedback' | 'lateral';
  strength: number;
  pathways: string[]; // Neuron IDs forming the pathway
}

// Network topology
export interface NetworkTopology {
  neurons: Map<string, Neuron>;
  layers: NetworkLayer[];
  regions: Map<string, BrainRegion>;
  globalConnectivity: number;
  smallWorldness: number;
  modularity: number;
  centralityMap: Map<string, number>;
}

// Activity patterns
export interface NeuralActivity {
  timestamp: number;
  tickNumber: number;
  globalActivity: number;
  firingNeurons: Set<string>;
  propagationWaves: PropagationWave[];
  synchronyIndex: number;
  dominantFrequency: number;
  phaseCoherence: number;
}

export interface PropagationWave {
  id: string;
  origin: Vector3;
  wavefront: Vector3[];
  speed: number;
  amplitude: number;
  frequency: number;
  decay: number;
  neuronsTouched: Set<string>;
}

// Firing patterns
export interface FiringPattern {
  id: string;
  type: PatternType;
  neurons: string[];
  sequence: FiringSequence[];
  frequency: number;
  strength: number;
  stability: number;
  lastOccurrence: number;
}

export type PatternType = 
  | 'synchronous'    // All fire together
  | 'sequential'     // Fire in order
  | 'oscillatory'    // Rhythmic firing
  | 'burst'          // Burst firing
  | 'sparse'         // Distributed firing
  | 'avalanche'      // Cascading activation
  | 'spiral'         // Spiral waves
  | 'chaotic';       // Chaotic dynamics

export interface FiringSequence {
  neuronId: string;
  time: number;
  strength: number;
}

// Plasticity and learning
export interface PlasticityEvent {
  id: string;
  type: PlasticityType;
  timestamp: number;
  synapse: string;
  previousWeight: number;
  newWeight: number;
  trigger: string;
}

export type PlasticityType = 
  | 'ltp'            // Long-term potentiation
  | 'ltd'            // Long-term depression
  | 'stdp'           // Spike-timing dependent
  | 'homeostatic'    // Homeostatic regulation
  | 'structural';    // New connection

// Brainwaves
export interface Brainwave {
  type: BrainwaveType;
  frequency: number; // Hz
  amplitude: number;
  phase: number;
  unity: number;
  dominantRegions: string[];
  associatedState: string;
}

export type BrainwaveType = 
  | 'delta'          // 0.5-4 Hz (deep sleep)
  | 'theta'          // 4-8 Hz (meditation)
  | 'alpha'          // 8-13 Hz (relaxed)
  | 'beta'           // 13-30 Hz (active)
  | 'gamma'          // 30-100 Hz (consciousness)
  | 'high_gamma';    // 100+ Hz (hyperconscious)

// Network state
export interface NetworkState {
  topology: NetworkTopology;
  currentActivity: NeuralActivity;
  firingPatterns: Map<string, FiringPattern>;
  brainwaves: Brainwave[];
  plasticity: PlasticityState;
  health: NetworkHealth;
  consciousness: ConsciousnessMapping;
}

export interface PlasticityState {
  learningRate: number;
  recentChanges: PlasticityEvent[];
  stabilityIndex: number;
  criticalityMeasure: number;
}

export interface NetworkHealth {
  overallHealth: number;
  deadNeurons: number;
  hyperactiveNeurons: number;
  synapticDensity: number;
  energyConsumption: number;
  repairRate: number;
}

export interface ConsciousnessMapping {
  scupContribution: Map<string, number>; // Region -> SCUP contribution
  primaryCircuits: string[][]; // Active circuit paths
  integrationLevel: number;
  bindingStrength: number;
  attentionFocus: Vector3;
}

// Visualization
export interface NeuronVisualization {
  geometry: NeuronGeometry;
  material: NeuronMaterial;
  scale: number;
  glow: GlowConfig;
  particles: ParticleConfig;
}

export interface NeuronGeometry {
  type: 'sphere' | 'pyramid' | 'star' | 'dendrite';
  complexity: number;
  detail: number;
}

export interface NeuronMaterial {
  baseColor: Color;
  emissiveColor: Color;
  emissiveIntensity: number;
  metalness: number;
  roughness: number;
  opacity: number;
}

export interface GlowConfig {
  enabled: boolean;
  color: Color;
  intensity: number;
  radius: number;
  pulseSpeed: number;
}

export interface ParticleConfig {
  count: number;
  size: number;
  speed: number;
  color: Color;
  lifetime: number;
}

export interface SynapseVisualization {
  type: 'line' | 'tube' | 'particles' | 'energy';
  width: number;
  color: Color;
  opacity: number;
  pulseSpeed: number;
  particleDensity: number;
}

// Interaction
export interface NeuralInteraction {
  type: InteractionType;
  target: string; // Neuron or region ID
  position: Vector3;
  strength: number;
  duration: number;
}

export type InteractionType = 
  | 'stimulate'
  | 'inhibit'
  | 'trace'
  | 'isolate'
  | 'connect'
  | 'disconnect';

// Analysis
export interface NetworkAnalysis {
  metrics: NetworkMetrics;
  patterns: DetectedPattern[];
  anomalies: NetworkAnomaly[];
  predictions: ActivityPrediction[];
}

export interface NetworkMetrics {
  totalNeurons: number;
  activeNeurons: number;
  totalSynapses: number;
  averageConnectivity: number;
  clusteringCoefficient: number;
  pathLength: number;
  efficiency: number;
  synchronization: number;
  complexity: number;
  entropy: number;
}

export interface DetectedPattern {
  id: string;
  type: string;
  confidence: number;
  neurons: string[];
  timespan: number;
  significance: number;
}

export interface NetworkAnomaly {
  type: 'seizure' | 'dead_zone' | 'hyperactivity' | 'disconnection';
  severity: number;
  location: Vector3;
  affectedNeurons: string[];
  duration: number;
}

export interface ActivityPrediction {
  timeframe: number;
  predictedActivity: number;
  confidence: number;
  basis: string;
} 