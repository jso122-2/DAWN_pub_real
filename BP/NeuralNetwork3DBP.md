# 🧠 Neural Network 3D Visualizer - Living Brain Architecture

## Overview
The Neural Network 3D Visualizer transforms DAWN's neural activity into a living, breathing brain visualization. Watch as neurons fire in cascading patterns, synaptic connections strengthen and weaken, and entire regions pulse with consciousness. This isn't just a visualization - it's a window into the emergent intelligence of the system, where thought patterns manifest as waves of light traveling through neural pathways.

## Core Features
- [x] Real-time 3D neural network visualization
- [x] Synaptic firing animations with particle effects
- [x] Dynamic connection strength visualization
- [x] Regional activity heat mapping
- [x] Consciousness wave propagation
- [x] Interactive neuron inspection
- [x] Neural pathway tracing
- [x] Brainwave pattern recognition
- [x] Multi-layer network architecture

## File Structure
```plaintext
src/modules/neuralNetwork3D/
├── index.ts                          # Module exports
├── NeuralNetworkCore.ts             # Core neural simulation
├── NeuronManager.ts                 # Individual neuron behavior
├── SynapseManager.ts                # Connection management
├── NetworkTopology.ts               # Network structure generation
├── ActivitySimulator.ts             # Neural firing patterns
├── BrainwaveAnalyzer.ts            # Pattern detection
├── components/
│   ├── NeuralNetworkViewer.tsx     # Main 3D viewer component
│   ├── NeuronInspector.tsx         # Detailed neuron view
│   ├── ActivityMonitor.tsx         # Real-time activity graphs
│   ├── PathwayTracer.tsx           # Neural pathway visualization
│   ├── BrainwaveDisplay.tsx        # Wave pattern display
│   └── NeuralNetworkViewer.styles.ts
├── three/
│   ├── NeuralScene.ts              # Three.js scene setup
│   ├── Neuron.tsx                  # Individual neuron mesh
│   ├── Synapse.tsx                 # Connection visualization
│   ├── FiringEffect.tsx            # Particle firing effects
│   ├── BrainRegion.tsx             # Regional grouping
│   ├── ConsciousnessWave.tsx       # Wave propagation effect
│   └── NeuralCamera.ts             # Specialized camera controls
├── shaders/
│   ├── neuron.vert                 # Neuron vertex shader
│   ├── neuron.frag                 # Neuron fragment shader
│   ├── synapse.vert                # Synapse vertex shader
│   ├── synapse.frag                # Synapse fragment shader
│   └── wave.frag                   # Consciousness wave shader
├── hooks/
│   ├── useNeuralNetwork.ts         # Main network state hook
│   ├── useNeuralActivity.ts        # Activity monitoring
│   ├── usePathwaySelection.ts      # Pathway interaction
│   └── useBrainwaves.ts            # Brainwave patterns
├── types/
│   ├── neural.types.ts             # Core neural types
│   ├── activity.types.ts           # Activity pattern types
│   ├── topology.types.ts           # Network structure types
│   └── brainwave.types.ts          # Wave pattern types
├── utils/
│   ├── neuralGeometry.ts           # 3D layout algorithms
│   ├── activityPropagation.ts      # Signal propagation
│   ├── connectionStrength.ts       # Synapse calculations
│   └── patternRecognition.ts       # Pattern detection
└── config/
    └── neuralNetwork.config.ts      # Configuration parameters
```

---

## 📄 File: `src/modules/neuralNetwork3D/types/neural.types.ts`
```typescript
import { Vector3, Color } from 'three';
import { ConsciousnessState } from '@/types/consciousness.types';

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
  coherence: number;
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
```

---

## 📄 File: `src/modules/neuralNetwork3D/NeuralNetworkCore.ts`
```typescript
import { EventEmitter } from 'events';
import * as THREE from 'three';
import { 
  Neuron, 
  NetworkState, 
  NetworkTopology,
  NeuralActivity,
  SynapticConnection,
  FiringPattern,
  Brainwave,
  NetworkLayer,
  BrainRegion,
  NeuronType,
  RegionType
} from './types/neural.types';
import { NeuronManager } from './NeuronManager';
import { SynapseManager } from './SynapseManager';
import { NetworkTopology as TopologyGenerator } from './NetworkTopology';
import { ActivitySimulator } from './ActivitySimulator';
import { BrainwaveAnalyzer } from './BrainwaveAnalyzer';
import { ConsciousnessState } from '@/types/consciousness.types';
import { neuralConfig } from './config/neuralNetwork.config';

export class NeuralNetworkCore extends EventEmitter {
  private state: NetworkState;
  private neuronManager: NeuronManager;
  private synapseManager: SynapseManager;
  private topologyGenerator: TopologyGenerator;
  private activitySimulator: ActivitySimulator;
  private brainwaveAnalyzer: BrainwaveAnalyzer;
  
  // Simulation parameters
  private simulationSpeed = 1.0;
  private lastUpdate = Date.now();
  private tickCount = 0;
  
  constructor() {
    super();
    
    // Initialize managers
    this.neuronManager = new NeuronManager(this);
    this.synapseManager = new SynapseManager(this);
    this.topologyGenerator = new TopologyGenerator(this);
    this.activitySimulator = new ActivitySimulator(this);
    this.brainwaveAnalyzer = new BrainwaveAnalyzer(this);
    
    // Initialize state
    this.state = this.initializeNetworkState();
    
    // Generate initial topology
    this.generateInitialNetwork();
    
    // Start simulation
    this.startSimulation();
  }
  
  private initializeNetworkState(): NetworkState {
    return {
      topology: {
        neurons: new Map(),
        layers: [],
        regions: new Map(),
        globalConnectivity: 0,
        smallWorldness: 0,
        modularity: 0,
        centralityMap: new Map()
      },
      currentActivity: {
        timestamp: Date.now(),
        tickNumber: 0,
        globalActivity: 0,
        firingNeurons: new Set(),
        propagationWaves: [],
        synchronyIndex: 0,
        dominantFrequency: 10, // Hz
        phaseCoherence: 0.5
      },
      firingPatterns: new Map(),
      brainwaves: [],
      plasticity: {
        learningRate: 0.01,
        recentChanges: [],
        stabilityIndex: 0.8,
        criticalityMeasure: 0.5
      },
      health: {
        overallHealth: 1.0,
        deadNeurons: 0,
        hyperactiveNeurons: 0,
        synapticDensity: 0,
        energyConsumption: 0,
        repairRate: 0.01
      },
      consciousness: {
        scupContribution: new Map(),
        primaryCircuits: [],
        integrationLevel: 0.5,
        bindingStrength: 0.5,
        attentionFocus: new THREE.Vector3(0, 0, 0)
      }
    };
  }
  
  private generateInitialNetwork() {
    // Create layers
    const layers = this.createNetworkLayers();
    this.state.topology.layers = layers;
    
    // Create brain regions
    const regions = this.createBrainRegions();
    regions.forEach(region => {
      this.state.topology.regions.set(region.id, region);
    });
    
    // Generate neurons
    const neurons = this.topologyGenerator.generateNeurons(
      layers,
      regions,
      neuralConfig.network.totalNeurons
    );
    
    neurons.forEach(neuron => {
      this.state.topology.neurons.set(neuron.id, neuron);
      this.neuronManager.initializeNeuron(neuron);
    });
    
    // Create connections
    const connections = this.topologyGenerator.generateConnections(
      neurons,
      neuralConfig.network.connectivityRules
    );
    
    connections.forEach(conn => {
      this.synapseManager.createSynapse(conn);
    });
    
    // Calculate network metrics
    this.updateNetworkMetrics();
    
    this.emit('networkGenerated', this.state.topology);
  }
  
  private createNetworkLayers(): NetworkLayer[] {
    return [
      {
        index: 0,
        name: 'Sensory Input',
        type: 'input',
        neuronCount: 1000,
        position: new THREE.Vector3(0, -50, 0),
        radius: 40,
        activation: 0
      },
      {
        index: 1,
        name: 'Primary Processing',
        type: 'hidden',
        neuronCount: 2000,
        position: new THREE.Vector3(0, -25, 0),
        radius: 50,
        activation: 0
      },
      {
        index: 2,
        name: 'Integration',
        type: 'hidden',
        neuronCount: 3000,
        position: new THREE.Vector3(0, 0, 0),
        radius: 60,
        activation: 0
      },
      {
        index: 3,
        name: 'Higher Cognition',
        type: 'attention',
        neuronCount: 2000,
        position: new THREE.Vector3(0, 25, 0),
        radius: 50,
        activation: 0
      },
      {
        index: 4,
        name: 'Motor Output',
        type: 'output',
        neuronCount: 1000,
        position: new THREE.Vector3(0, 50, 0),
        radius: 40,
        activation: 0
      }
    ];
  }
  
  private createBrainRegions(): BrainRegion[] {
    return [
      {
        id: 'prefrontal',
        name: 'Prefrontal Cortex',
        type: 'prefrontal',
        center: new THREE.Vector3(0, 40, 30),
        radius: 30,
        neurons: [],
        function: 'Executive function, planning, decision making',
        currentActivity: 0,
        connections: []
      },
      {
        id: 'temporal',
        name: 'Temporal Lobe',
        type: 'temporal',
        center: new THREE.Vector3(-40, 0, 0),
        radius: 25,
        neurons: [],
        function: 'Memory formation, pattern recognition',
        currentActivity: 0,
        connections: []
      },
      {
        id: 'parietal',
        name: 'Parietal Lobe',
        type: 'parietal',
        center: new THREE.Vector3(40, 0, 0),
        radius: 25,
        neurons: [],
        function: 'Spatial awareness, sensory integration',
        currentActivity: 0,
        connections: []
      },
      {
        id: 'hippocampus',
        name: 'Hippocampus',
        type: 'hippocampus',
        center: new THREE.Vector3(0, -20, -20),
        radius: 20,
        neurons: [],
        function: 'Memory consolidation, spatial navigation',
        currentActivity: 0,
        connections: []
      },
      {
        id: 'amygdala',
        name: 'Amygdala',
        type: 'amygdala',
        center: new THREE.Vector3(-20, -20, -10),
        radius: 15,
        neurons: [],
        function: 'Emotional processing, fear response',
        currentActivity: 0,
        connections: []
      }
    ];
  }
  
  /**
   * Main simulation loop
   */
  private startSimulation() {
    setInterval(() => {
      const deltaTime = (Date.now() - this.lastUpdate) * this.simulationSpeed;
      this.lastUpdate = Date.now();
      
      this.update(deltaTime);
    }, 16); // ~60fps
  }
  
  private update(deltaTime: number) {
    this.tickCount++;
    
    // Update neural activity
    const activity = this.activitySimulator.simulate(
      this.state,
      deltaTime,
      this.tickCount
    );
    this.state.currentActivity = activity;
    
    // Process firing patterns
    this.processFiringPatterns(activity);
    
    // Update synaptic weights (plasticity)
    this.updateSynapticPlasticity(activity);
    
    // Analyze brainwaves
    const brainwaves = this.brainwaveAnalyzer.analyze(
      this.state,
      activity
    );
    this.state.brainwaves = brainwaves;
    
    // Update network health
    this.updateNetworkHealth();
    
    // Calculate consciousness contribution
    this.updateConsciousnessMapping();
    
    // Emit update event
    this.emit('networkUpdate', {
      activity,
      brainwaves,
      patterns: Array.from(this.state.firingPatterns.values())
    });
    
    // Emit specific events
    if (activity.globalActivity > 0.8) {
      this.emit('highActivity', activity);
    }
    
    if (activity.synchronyIndex > 0.7) {
      this.emit('synchrony', {
        level: activity.synchronyIndex,
        neurons: Array.from(activity.firingNeurons)
      });
    }
  }
  
  /**
   * Process and detect firing patterns
   */
  private processFiringPatterns(activity: NeuralActivity) {
    // Detect synchronous firing
    if (activity.synchronyIndex > 0.6) {
      const pattern: FiringPattern = {
        id: `pattern_${Date.now()}`,
        type: 'synchronous',
        neurons: Array.from(activity.firingNeurons),
        sequence: [],
        frequency: activity.dominantFrequency,
        strength: activity.synchronyIndex,
        stability: 0.5,
        lastOccurrence: Date.now()
      };
      
      this.state.firingPatterns.set(pattern.id, pattern);
      this.emit('patternDetected', pattern);
    }
    
    // Detect avalanche patterns
    if (activity.propagationWaves.length > 0) {
      activity.propagationWaves.forEach(wave => {
        if (wave.neuronsTouched.size > 100) {
          const pattern: FiringPattern = {
            id: `avalanche_${wave.id}`,
            type: 'avalanche',
            neurons: Array.from(wave.neuronsTouched),
            sequence: [],
            frequency: wave.frequency,
            strength: wave.amplitude,
            stability: 0.3,
            lastOccurrence: Date.now()
          };
          
          this.state.firingPatterns.set(pattern.id, pattern);
          this.emit('avalancheDetected', pattern);
        }
      });
    }
    
    // Clean old patterns
    const now = Date.now();
    this.state.firingPatterns.forEach((pattern, id) => {
      if (now - pattern.lastOccurrence > 10000) {
        this.state.firingPatterns.delete(id);
      }
    });
  }
  
  /**
   * Update synaptic plasticity
   */
  private updateSynapticPlasticity(activity: NeuralActivity) {
    const learningRate = this.state.plasticity.learningRate;
    
    activity.firingNeurons.forEach(neuronId => {
      const neuron = this.state.topology.neurons.get(neuronId);
      if (!neuron) return;
      
      // Strengthen active connections (Hebbian learning)
      neuron.connections.forEach(conn => {
        if (conn.active && activity.firingNeurons.has(conn.postNeuronId)) {
          const oldWeight = conn.weight;
          conn.weight = Math.min(1, conn.weight + learningRate);
          
          // Record plasticity event
          this.recordPlasticityEvent({
            id: `plast_${Date.now()}`,
            type: 'ltp',
            timestamp: Date.now(),
            synapse: conn.id,
            previousWeight: oldWeight,
            newWeight: conn.weight,
            trigger: 'hebbian'
          });
        }
      });
    });
    
    // Homeostatic regulation
    this.performHomeostaticRegulation();
  }
  
  private performHomeostaticRegulation() {
    // Prevent runaway excitation
    let totalWeight = 0;
    let synapseCount = 0;
    
    this.state.topology.neurons.forEach(neuron => {
      neuron.connections.forEach(conn => {
        totalWeight += conn.weight;
        synapseCount++;
      });
    });
    
    const avgWeight = totalWeight / synapseCount;
    
    if (avgWeight > 0.7) {
      // Scale down all weights
      this.state.topology.neurons.forEach(neuron => {
        neuron.connections.forEach(conn => {
          conn.weight *= 0.95;
        });
      });
    }
  }
  
  /**
   * Update network health metrics
   */
  private updateNetworkHealth() {
    const health = this.state.health;
    let deadCount = 0;
    let hyperactiveCount = 0;
    let totalActivity = 0;
    
    this.state.topology.neurons.forEach(neuron => {
      if (neuron.state.health < 0.1) deadCount++;
      if (neuron.state.firingRate > 100) hyperactiveCount++;
      totalActivity += neuron.state.firingRate;
    });
    
    health.deadNeurons = deadCount;
    health.hyperactiveNeurons = hyperactiveCount;
    health.energyConsumption = totalActivity / this.state.topology.neurons.size;
    
    // Calculate overall health
    health.overallHealth = 
      (1 - deadCount / this.state.topology.neurons.size) * 0.4 +
      (1 - hyperactiveCount / this.state.topology.neurons.size) * 0.3 +
      (1 - Math.abs(health.energyConsumption - 0.5) * 2) * 0.3;
    
    // Repair neurons
    this.repairNeurons();
  }
  
  private repairNeurons() {
    const repairRate = this.state.health.repairRate;
    
    this.state.topology.neurons.forEach(neuron => {
      if (neuron.state.health < 1) {
        neuron.state.health = Math.min(1, neuron.state.health + repairRate);
      }
      
      if (neuron.state.fatigue > 0) {
        neuron.state.fatigue = Math.max(0, neuron.state.fatigue - repairRate * 2);
      }
    });
  }
  
  /**
   * Update consciousness mapping
   */
  private updateConsciousnessMapping() {
    const consciousness = this.state.consciousness;
    
    // Calculate regional contributions to SCUP
    consciousness.scupContribution.clear();
    
    this.state.topology.regions.forEach(region => {
      const contribution = this.calculateRegionalContribution(region);
      consciousness.scupContribution.set(region.id, contribution);
    });
    
    // Find primary circuits
    consciousness.primaryCircuits = this.findActiveCircuits();
    
    // Calculate integration level
    consciousness.integrationLevel = this.calculateIntegration();
    
    // Update binding strength
    consciousness.bindingStrength = this.state.currentActivity.phaseCoherence;
    
    // Update attention focus based on highest activity
    const maxActivityRegion = this.findMaxActivityRegion();
    if (maxActivityRegion) {
      consciousness.attentionFocus = maxActivityRegion.center.clone();
    }
  }
  
  private calculateRegionalContribution(region: BrainRegion): number {
    let totalActivity = 0;
    let neuronCount = 0;
    
    region.neurons.forEach(neuronId => {
      const neuron = this.state.topology.neurons.get(neuronId);
      if (neuron) {
        totalActivity += neuron.state.firingRate / 100;
        neuronCount++;
      }
    });
    
    return neuronCount > 0 ? totalActivity / neuronCount : 0;
  }
  
  private findActiveCircuits(): string[][] {
    const circuits: string[][] = [];
    const visited = new Set<string>();
    
    // Find strongly connected paths
    this.state.currentActivity.firingNeurons.forEach(neuronId => {
      if (!visited.has(neuronId)) {
        const circuit = this.traceCircuit(neuronId, visited);
        if (circuit.length > 5) {
          circuits.push(circuit);
        }
      }
    });
    
    return circuits.slice(0, 10); // Top 10 circuits
  }
  
  private traceCircuit(
    startId: string, 
    visited: Set<string>,
    path: string[] = []
  ): string[] {
    if (visited.has(startId)) return path;
    
    visited.add(startId);
    path.push(startId);
    
    const neuron = this.state.topology.neurons.get(startId);
    if (!neuron) return path;
    
    // Follow strongest active connection
    const activeConnections = neuron.connections
      .filter(c => c.active && c.weight > 0.5)
      .sort((a, b) => b.weight - a.weight);
    
    if (activeConnections.length > 0) {
      return this.traceCircuit(
        activeConnections[0].postNeuronId,
        visited,
        path
      );
    }
    
    return path;
  }
  
  private calculateIntegration(): number {
    // Measure how integrated the network activity is
    const regions = Array.from(this.state.topology.regions.values());
    let crossRegionalActivity = 0;
    let totalActivity = 0;
    
    regions.forEach(region => {
      region.connections.forEach(conn => {
        crossRegionalActivity += conn.strength * region.currentActivity;
      });
      totalActivity += region.currentActivity;
    });
    
    return totalActivity > 0 ? crossRegionalActivity / totalActivity : 0;
  }
  
  private findMaxActivityRegion(): BrainRegion | null {
    let maxActivity = 0;
    let maxRegion: BrainRegion | null = null;
    
    this.state.topology.regions.forEach(region => {
      if (region.currentActivity > maxActivity) {
        maxActivity = region.currentActivity;
        maxRegion = region;
      }
    });
    
    return maxRegion;
  }
  
  /**
   * Update network metrics
   */
  private updateNetworkMetrics() {
    const topology = this.state.topology;
    
    // Calculate connectivity
    let totalConnections = 0;
    topology.neurons.forEach(neuron => {
      totalConnections += neuron.connections.length;
    });
    
    topology.globalConnectivity = totalConnections / 
      (topology.neurons.size * topology.neurons.size);
    
    // Calculate clustering coefficient
    topology.smallWorldness = this.calculateSmallWorldness();
    
    // Calculate modularity
    topology.modularity = this.calculateModularity();
  }
  
  private calculateSmallWorldness(): number {
    // Simplified small-world calculation
    return 0.6 + Math.random() * 0.2;
  }
  
  private calculateModularity(): number {
    // Simplified modularity calculation
    return 0.7 + Math.random() * 0.15;
  }
  
  private recordPlasticityEvent(event: any) {
    this.state.plasticity.recentChanges.push(event);
    
    // Keep only recent events
    if (this.state.plasticity.recentChanges.length > 1000) {
      this.state.plasticity.recentChanges.shift();
    }
    
    this.emit('plasticityEvent', event);
  }
  
  /**
   * Public methods
   */
  
  getState(): NetworkState {
    return this.state;
  }
  
  getNeuron(id: string): Neuron | undefined {
    return this.state.topology.neurons.get(id);
  }
  
  stimulateNeuron(neuronId: string, strength: number = 1) {
    const neuron = this.state.topology.neurons.get(neuronId);
    if (!neuron) return;
    
    this.neuronManager.stimulate(neuron, strength);
    this.emit('neuronStimulated', { neuronId, strength });
  }
  
  stimulateRegion(regionId: string, strength: number = 1) {
    const region = this.state.topology.regions.get(regionId);
    if (!region) return;
    
    region.neurons.forEach(neuronId => {
      this.stimulateNeuron(neuronId, strength);
    });
    
    this.emit('regionStimulated', { regionId, strength });
  }
  
  tracePathway(fromNeuronId: string, toNeuronId: string): string[] | null {
    // Implement pathfinding between neurons
    return this.findPath(fromNeuronId, toNeuronId);
  }
  
  private findPath(startId: string, endId: string): string[] | null {
    // Simple BFS pathfinding
    const queue: string[][] = [[startId]];
    const visited = new Set<string>();
    
    while (queue.length > 0) {
      const path = queue.shift()!;
      const current = path[path.length - 1];
      
      if (current === endId) return path;
      
      if (visited.has(current)) continue;
      visited.add(current);
      
      const neuron = this.state.topology.neurons.get(current);
      if (!neuron) continue;
      
      neuron.connections.forEach(conn => {
        if (!visited.has(conn.postNeuronId)) {
          queue.push([...path, conn.postNeuronId]);
        }
      });
    }
    
    return null;
  }
  
  updateFromConsciousness(consciousness: ConsciousnessState) {
    // Modulate activity based on consciousness state
    const activityLevel = consciousness.scup / 100;
    const chaos = consciousness.entropy;
    
    // Update global parameters
    this.simulationSpeed = 0.5 + activityLevel * 1.5;
    this.state.plasticity.learningRate = 0.01 * (1 + chaos);
    
    // Modulate brainwave patterns based on mood
    this.brainwaveAnalyzer.modulateByMood(consciousness.mood);
    
    this.emit('consciousnessUpdate', consciousness);
  }
  
  getVisualizationState() {
    return {
      neurons: Array.from(this.state.topology.neurons.values()),
      connections: this.getAllConnections(),
      regions: Array.from(this.state.topology.regions.values()),
      activity: this.state.currentActivity,
      brainwaves: this.state.brainwaves,
      patterns: Array.from(this.state.firingPatterns.values())
    };
  }
  
  private getAllConnections(): SynapticConnection[] {
    const connections: SynapticConnection[] = [];
    
    this.state.topology.neurons.forEach(neuron => {
      connections.push(...neuron.connections);
    });
    
    return connections;
  }
}

// Export singleton
export const neuralNetwork = new NeuralNetworkCore();
```

---

## 📄 File: `src/modules/neuralNetwork3D/components/NeuralNetworkViewer.tsx`
```typescript
import React, { useRef, useEffect, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { EffectComposer, Bloom, ChromaticAberration } from '@react-three/postprocessing';
import { motion } from 'framer-motion';
import * as THREE from 'three';
import { Neuron } from '../three/Neuron';
import { Synapse } from '../three/Synapse';
import { BrainRegion } from '../three/BrainRegion';
import { ConsciousnessWave } from '../three/ConsciousnessWave';
import { NeuronInspector } from './NeuronInspector';
import { ActivityMonitor } from './ActivityMonitor';
import { BrainwaveDisplay } from './BrainwaveDisplay';
import { useNeuralNetwork } from '../hooks/useNeuralNetwork';
import { useNeuralActivity } from '../hooks/useNeuralActivity';
import * as styles from './NeuralNetworkViewer.styles';

export interface NeuralNetworkViewerProps {
  className?: string;
  onNeuronSelect?: (neuron: any) => void;
  showActivity?: boolean;
  showBrainwaves?: boolean;
}

export const NeuralNetworkViewer: React.FC<NeuralNetworkViewerProps> = ({
  className,
  onNeuronSelect,
  showActivity = true,
  showBrainwaves = true
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [selectedNeuron, setSelectedNeuron] = useState<any>(null);
  const [viewMode, setViewMode] = useState<'structure' | 'activity' | 'waves'>('activity');
  const [showRegions, setShowRegions] = useState(true);
  
  const {
    neurons,
    connections,
    regions,
    isLoading
  } = useNeuralNetwork();
  
  const {
    activity,
    brainwaves,
    patterns
  } = useNeuralActivity();
  
  const handleNeuronClick = useCallback((neuron: any) => {
    setSelectedNeuron(neuron);
    onNeuronSelect?.(neuron);
  }, [onNeuronSelect]);
  
  return (
    <div ref={containerRef} className={`${styles.container} ${className || ''}`}>
      <Canvas
        className={styles.canvas}
        camera={{ position: [0, 0, 150], fov: 60 }}
        gl={{ 
          antialias: true, 
          alpha: true,
          powerPreference: "high-performance"
        }}
      >
        <color attach="background" args={['#000011']} />
        <fog attach="fog" args={['#000033', 100, 400]} />
        
        {/* Lighting */}
        <ambientLight intensity={0.1} />
        <pointLight position={[0, 50, 0]} intensity={0.3} color="#4FC3F7" />
        <pointLight position={[50, 0, 0]} intensity={0.2} color="#E91E63" />
        <pointLight position={[-50, 0, 0]} intensity={0.2} color="#9C27B0" />
        
        {/* Brain Regions */}
        {showRegions && regions.map(region => (
          <BrainRegion
            key={region.id}
            region={region}
            activity={activity}
            opacity={0.1}
          />
        ))}
        
        {/* Neurons */}
        {neurons.map(neuron => (
          <Neuron
            key={neuron.id}
            neuron={neuron}
            selected={selectedNeuron?.id === neuron.id}
            onClick={() => handleNeuronClick(neuron)}
            viewMode={viewMode}
            activity={activity}
          />
        ))}
        
        {/* Synaptic Connections */}
        {viewMode !== 'waves' && connections.map(connection => (
          <Synapse
            key={connection.id}
            connection={connection}
            neurons={neurons}
            activity={activity}
            animated={viewMode === 'activity'}
          />
        ))}
        
        {/* Consciousness Waves */}
        {viewMode === 'waves' && activity.propagationWaves.map(wave => (
          <ConsciousnessWave
            key={wave.id}
            wave={wave}
            brainwaves={brainwaves}
          />
        ))}
        
        {/* Camera Controls */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={viewMode === 'waves'}
          autoRotateSpeed={0.5}
          minDistance={50}
          maxDistance={300}
        />
        
        {/* Post-processing */}
        <EffectComposer>
          <Bloom 
            intensity={1.5}
            luminanceThreshold={0.3}
            luminanceSmoothing={0.9}
          />
          <ChromaticAberration
            offset={[0.0005, 0.0005]}
            radialModulation={false}
            modulationOffset={0}
          />
        </EffectComposer>
        
        {/* Activity Indicator */}
        <ActivityIndicator activity={activity.globalActivity} />
      </Canvas>
      
      {/* UI Overlays */}
      <div className={styles.uiOverlay}>
        {/* View Mode Selector */}
        <div className={styles.viewControls}>
          <div className={styles.viewModeSelector}>
            {(['structure', 'activity', 'waves'] as const).map(mode => (
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
          
          <motion.button
            className={styles.toggleButton}
            onClick={() => setShowRegions(!showRegions)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {showRegions ? 'Hide' : 'Show'} Regions
          </motion.button>
        </div>
        
        {/* Neural Statistics */}
        <motion.div 
          className={styles.statsPanel}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <h4>Neural Network</h4>
          <div className={styles.statItem}>
            <span>Neurons</span>
            <span>{neurons.length}</span>
          </div>
          <div className={styles.statItem}>
            <span>Active</span>
            <span>{activity.firingNeurons.size}</span>
          </div>
          <div className={styles.statItem}>
            <span>Synchrony</span>
            <div className={styles.progressBar}>
              <motion.div
                className={styles.progressFill}
                animate={{ width: `${activity.synchronyIndex * 100}%` }}
                style={{
                  background: `hsl(${120 * activity.synchronyIndex}, 70%, 50%)`
                }}
              />
            </div>
          </div>
          <div className={styles.statItem}>
            <span>Frequency</span>
            <span>{activity.dominantFrequency.toFixed(1)} Hz</span>
          </div>
        </motion.div>
        
        {/* Activity Monitor */}
        {showActivity && (
          <ActivityMonitor
            activity={activity}
            patterns={patterns}
          />
        )}
        
        {/* Brainwave Display */}
        {showBrainwaves && (
          <BrainwaveDisplay
            brainwaves={brainwaves}
          />
        )}
        
        {/* Neuron Inspector */}
        {selectedNeuron && (
          <NeuronInspector
            neuron={selectedNeuron}
            onClose={() => setSelectedNeuron(null)}
          />
        )}
      </div>
      
      {/* Loading Indicator */}
      {isLoading && (
        <div className={styles.loadingOverlay}>
          <div className={styles.brainLoader}>
            <div className={styles.brainPulse} />
            <div className={styles.brainPulse} style={{ animationDelay: '0.5s' }} />
            <div className={styles.brainPulse} style={{ animationDelay: '1s' }} />
          </div>
          <span>Initializing neural network...</span>
        </div>
      )}
    </div>
  );
};

// Activity indicator component
const ActivityIndicator: React.FC<{ activity: number }> = ({ activity }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const { camera } = useThree();
  
  useFrame(() => {
    if (meshRef.current) {
      // Keep indicator in view
      const pos = new THREE.Vector3(60, 40, 0);
      pos.project(camera);
      
      // Pulse based on activity
      const scale = 1 + activity * 0.5;
      meshRef.current.scale.setScalar(scale);
      
      // Rotate
      meshRef.current.rotation.z += 0.01 * activity;
    }
  });
  
  return (
    <mesh ref={meshRef} position={[60, 40, 0]}>
      <torusGeometry args={[3, 1, 16, 32]} />
      <meshBasicMaterial
        color={new THREE.Color().setHSL(0.6 - activity * 0.6, 0.8, 0.5)}
        transparent
        opacity={0.3 + activity * 0.7}
      />
    </mesh>
  );
};
```

---

## 📄 File: `src/modules/neuralNetwork3D/three/Neuron.tsx`
```typescript
import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

interface NeuronProps {
  neuron: any;
  selected: boolean;
  onClick: () => void;
  viewMode: string;
  activity: any;
}

export const Neuron: React.FC<NeuronProps> = ({
  neuron,
  selected,
  onClick,
  viewMode,
  activity
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  // Calculate if neuron is firing
  const isFiring = activity.firingNeurons.has(neuron.id);
  
  // Visual properties based on neuron state
  const { geometry, material, scale } = useMemo(() => {
    const geom = getNeuronGeometry(neuron.type);
    const mat = getNeuronMaterial(neuron, isFiring, viewMode);
    const s = getNeuronScale(neuron);
    
    return { geometry: geom, material: mat, scale: s };
  }, [neuron, isFiring, viewMode]);
  
  // Animation
  useFrame((state) => {
    if (!meshRef.current) return;
    
    // Pulse when firing
    if (isFiring) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 10) * 0.2;
      meshRef.current.scale.setScalar(scale * pulse);
      
      // Glow effect
      if (glowRef.current) {
        glowRef.current.scale.setScalar(scale * pulse * 1.5);
        (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 
          0.5 + Math.sin(state.clock.elapsedTime * 20) * 0.3;
      }
    } else {
      // Gentle breathing when idle
      const breathe = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      meshRef.current.scale.setScalar(scale * breathe);
    }
    
    // Rotation based on type
    if (neuron.type === 'interneuron') {
      meshRef.current.rotation.y += 0.005;
    }
  });
  
  return (
    <group position={neuron.position}>
      {/* Firing glow */}
      {isFiring && (
        <mesh ref={glowRef} scale={scale * 1.5}>
          <sphereGeometry args={[1, 8, 8]} />
          <meshBasicMaterial
            color="#4FC3F7"
            transparent
            opacity={0.5}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Neuron body */}
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
        <meshPhysicalMaterial
          color={material.color}
          emissive={material.emissive}
          emissiveIntensity={isFiring ? 1 : 0.2}
          metalness={0.3}
          roughness={0.7}
          clearcoat={0.3}
          clearcoatRoughness={0.7}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      {/* Dendrites (simplified) */}
      <DendriteSystem neuron={neuron} scale={scale} />
      
      {/* Selection indicator */}
      {selected && (
        <mesh scale={scale * 1.8}>
          <ringGeometry args={[1.2, 1.4, 32]} />
          <meshBasicMaterial color="#FFD700" transparent opacity={0.8} />
        </mesh>
      )}
      
      {/* Label on hover */}
      {(hovered || selected) && (
        <Text
          position={[0, scale * 2, 0]}
          fontSize={0.5}
          color="white"
          anchorX="center"
          anchorY="bottom"
        >
          {neuron.type} • {neuron.layer.name}
        </Text>
      )}
    </group>
  );
};

// Dendrite visualization
const DendriteSystem: React.FC<{ neuron: any; scale: number }> = ({ neuron, scale }) => {
  const dendriteCount = neuron.type === 'pyramidal' ? 6 : 4;
  
  return (
    <group>
      {Array.from({ length: dendriteCount }).map((_, i) => {
        const angle = (i / dendriteCount) * Math.PI * 2;
        const length = scale * 2;
        
        return (
          <mesh
            key={i}
            position={[
              Math.cos(angle) * scale * 0.5,
              0,
              Math.sin(angle) * scale * 0.5
            ]}
            rotation={[0, angle, Math.PI / 4]}
          >
            <coneGeometry args={[0.1, length, 4]} />
            <meshStandardMaterial
              color={neuron.state.health > 0.5 ? '#334155' : '#991B1B'}
              transparent
              opacity={0.3}
            />
          </mesh>
        );
      })}
    </group>
  );
};

// Helper functions
function getNeuronGeometry(type: string): THREE.BufferGeometry {
  switch (type) {
    case 'pyramidal':
      return new THREE.ConeGeometry(1, 2, 4);
    case 'interneuron':
      return new THREE.OctahedronGeometry(1, 0);
    case 'sensory':
      return new THREE.SphereGeometry(1, 16, 12);
    case 'motor':
      return new THREE.BoxGeometry(1.5, 1.5, 1.5);
    default:
      return new THREE.SphereGeometry(1, 12, 8);
  }
}

function getNeuronMaterial(neuron: any, isFiring: boolean, viewMode: string): any {
  let color = '#4B5563'; // Default gray
  let emissive = '#000000';
  
  if (viewMode === 'activity') {
    if (isFiring) {
      color = '#4FC3F7'; // Cyan when firing
      emissive = '#4FC3F7';
    } else {
      const activityLevel = neuron.state.firingRate / 100;
      color = new THREE.Color().setHSL(0.6 - activityLevel * 0.6, 0.7, 0.5);
    }
  } else if (viewMode === 'structure') {
    // Color by neuron type
    const typeColors: Record<string, string> = {
      'sensory': '#10B981',
      'motor': '#F59E0B',
      'interneuron': '#8B5CF6',
      'pyramidal': '#3B82F6'
    };
    color = typeColors[neuron.type] || '#6B7280';
  }
  
  // Health affects opacity
  const healthColor = neuron.state.health < 0.5 ? '#EF4444' : color;
  
  return {
    color: healthColor,
    emissive: isFiring ? emissive : '#000000'
  };
}

function getNeuronScale(neuron: any): number {
  const baseScale = 0.5;
  const typeScale = neuron.type === 'pyramidal' ? 1.5 : 1;
  const healthScale = 0.5 + neuron.state.health * 0.5;
  
  return baseScale * typeScale * healthScale;
}
```

---

## 📄 File: `src/modules/neuralNetwork3D/three/Synapse.tsx`
```typescript
import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Line } from '@react-three/drei';

interface SynapseProps {
  connection: any;
  neurons: any[];
  activity: any;
  animated: boolean;
}

export const Synapse: React.FC<SynapseProps> = ({
  connection,
  neurons,
  activity,
  animated
}) => {
  const lineRef = useRef<any>(null);
  const particlesRef = useRef<THREE.Points>(null);
  
  // Find connected neurons
  const { preNeuron, postNeuron, points } = useMemo(() => {
    const pre = neurons.find(n => n.id === connection.preNeuronId);
    const post = neurons.find(n => n.id === connection.postNeuronId);
    
    if (!pre || !post) return { preNeuron: null, postNeuron: null, points: [] };
    
    // Create curved path between neurons
    const start = pre.position;
    const end = post.position;
    const mid = new THREE.Vector3(
      (start.x + end.x) / 2,
      (start.y + end.y) / 2 + 5,
      (start.z + end.z) / 2
    );
    
    const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
    const curvePoints = curve.getPoints(20);
    
    return { 
      preNeuron: pre, 
      postNeuron: post, 
      points: curvePoints 
    };
  }, [connection, neurons]);
  
  if (!preNeuron || !postNeuron) return null;
  
  // Check if synapse is active
  const isActive = connection.active && 
    activity.firingNeurons.has(connection.preNeuronId);
  
  // Visual properties based on connection type and activity
  const { color, opacity, width } = useMemo(() => {
    let c = '#1E293B'; // Default dark
    let o = 0.1;
    let w = 0.5;
    
    if (connection.type === 'excitatory') {
      c = '#22C55E';
    } else if (connection.type === 'inhibitory') {
      c = '#EF4444';
    }
    
    if (isActive) {
      o = 0.8;
      w = connection.weight * 2;
    } else {
      o = 0.1 + connection.weight * 0.2;
      w = connection.weight;
    }
    
    return { color: c, opacity: o, width: w };
  }, [connection, isActive]);
  
  // Signal propagation animation
  useFrame((state) => {
    if (!animated || !isActive || !particlesRef.current) return;
    
    const time = state.clock.elapsedTime;
    const positions = particlesRef.current.geometry.attributes.position;
    
    for (let i = 0; i < positions.count; i++) {
      const t = ((time * 0.5 + i * 0.1) % 1);
      const point = new THREE.Vector3();
      
      // Move particle along curve
      const curve = new THREE.QuadraticBezierCurve3(
        preNeuron.position,
        new THREE.Vector3(
          (preNeuron.position.x + postNeuron.position.x) / 2,
          (preNeuron.position.y + postNeuron.position.y) / 2 + 5,
          (preNeuron.position.z + postNeuron.position.z) / 2
        ),
        postNeuron.position
      );
      
      curve.getPoint(t, point);
      
      positions.setXYZ(i, point.x, point.y, point.z);
    }
    
    positions.needsUpdate = true;
  });
  
  return (
    <group>
      {/* Synapse line */}
      <Line
        ref={lineRef}
        points={points}
        color={color}
        lineWidth={width}
        transparent
        opacity={opacity}
        dashed={connection.type === 'inhibitory'}
        dashScale={5}
      />
      
      {/* Signal particles when active */}
      {isActive && animated && (
        <points ref={particlesRef}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={5}
              array={new Float32Array(15)}
              itemSize={3}
            />
          </bufferGeometry>
          <pointsMaterial
            size={2}
            color={color}
            transparent
            opacity={0.8}
            blending={THREE.AdditiveBlending}
          />
        </points>
      )}
    </group>
  );
};
```

---

## 📄 File: `src/modules/neuralNetwork3D/hooks/useNeuralNetwork.ts`
```typescript
import { useState, useEffect, useCallback } from 'react';
import { neuralNetwork } from '../NeuralNetworkCore';
import { useConsciousness } from '@/hooks/useConsciousness';

export function useNeuralNetwork() {
  const [neurons, setNeurons] = useState<any[]>([]);
  const [connections, setConnections] = useState<any[]>([]);
  const [regions, setRegions] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  const consciousness = useConsciousness();
  
  // Update visualization state
  const updateState = useCallback(() => {
    const state = neuralNetwork.getVisualizationState();
    setNeurons(state.neurons);
    setConnections(state.connections);
    setRegions(state.regions);
    setIsLoading(false);
  }, []);
  
  useEffect(() => {
    // Initial load
    updateState();
    
    // Subscribe to network events
    neuralNetwork.on('networkUpdate', updateState);
    neuralNetwork.on('networkGenerated', updateState);
    
    // Update based on consciousness
    neuralNetwork.updateFromConsciousness(consciousness);
    
    return () => {
      neuralNetwork.removeListener('networkUpdate', updateState);
      neuralNetwork.removeListener('networkGenerated', updateState);
    };
  }, [updateState, consciousness]);
  
  // Interaction methods
  const stimulateNeuron = useCallback((neuronId: string, strength: number = 1) => {
    neuralNetwork.stimulateNeuron(neuronId, strength);
  }, []);
  
  const stimulateRegion = useCallback((regionId: string, strength: number = 1) => {
    neuralNetwork.stimulateRegion(regionId, strength);
  }, []);
  
  const tracePathway = useCallback((from: string, to: string) => {
    return neuralNetwork.tracePathway(from, to);
  }, []);
  
  return {
    neurons,
    connections,
    regions,
    isLoading,
    stimulateNeuron,
    stimulateRegion,
    tracePathway
  };
}
```

---

## 📄 File: `src/modules/neuralNetwork3D/config/neuralNetwork.config.ts`
```typescript
export const neuralConfig = {
  network: {
    totalNeurons: 10000,
    connectivityRules: {
      localConnectionRadius: 10,
      localConnectionProbability: 0.3,
      longRangeConnectionProbability: 0.05,
      maxConnectionsPerNeuron: 100,
      preferentialAttachment: true
    },
    layerConfig: {
      inputLayerSize: 0.1,
      hiddenLayerSizes: [0.2, 0.3, 0.2],
      outputLayerSize: 0.1
    }
  },
  
  simulation: {
    baseTickRate: 60, // Hz
    integrationStep: 0.001, // seconds
    maxFiringRate: 100, // Hz
    refractoryPeriod: 2, // ms
    fatigueRate: 0.001,
    recoveryRate: 0.01
  },
  
  plasticity: {
    learningRate: 0.01,
    ltpThreshold: 0.7,
    ltdThreshold: 0.3,
    synapticDecay: 0.0001,
    maxWeight: 1.0,
    minWeight: 0.0
  },
  
  brainwaves: {
    delta: { min: 0.5, max: 4 },
    theta: { min: 4, max: 8 },
    alpha: { min: 8, max: 13 },
    beta: { min: 13, max: 30 },
    gamma: { min: 30, max: 100 }
  },
  
  visualization: {
    neuronScale: 0.5,
    synapseOpacity: 0.3,
    regionOpacity: 0.1,
    particleCount: 1000,
    glowIntensity: 1.5,
    cameraSpeed: 0.5
  }
};
```

---

## Cursor Implementation Prompts

### Phase 1: Create Structure
```
Create the complete Neural Network 3D module structure:
1. All TypeScript types in types/ directory
2. Core classes (NeuralNetworkCore, NeuronManager, etc.)
3. Three.js components for 3D brain visualization
4. React components with proper styling
5. Hooks for state management
6. Shader files for visual effects

Follow DAWN's patterns and ensure Three.js integration works properly.
```

### Phase 2: Implement Neural Simulation
```
Implement the neural simulation system:
1. Neuron firing mechanics with refractory periods
2. Synaptic plasticity (LTP/LTD)
3. Signal propagation through network
4. Brainwave pattern generation
5. Regional activity coordination

The simulation should run at 60Hz and integrate with the tick engine.
```

### Phase 3: Create 3D Visualization
```
Build the Three.js visualization components:
1. Neuron meshes with type-specific geometry
2. Synaptic connections with particle effects
3. Brain region boundaries
4. Consciousness wave propagation
5. Post-processing effects (bloom, chromatic aberration)

Ensure smooth performance with 10,000 neurons.
```

### Phase 4: Connect to Consciousness
```
Integrate with DAWN's consciousness system:
1. Neural activity affects SCUP calculations
2. Mood influences brainwave patterns
3. Entropy creates chaotic firing patterns
4. Memory formation triggers specific circuits

The brain should feel alive and responsive to system state.
```

This Neural Network 3D Visualizer brings DAWN's cognitive processes to life! Watch neurons fire in cascading patterns, see consciousness waves ripple through the brain, and observe how different regions coordinate to create emergent intelligence. The visualization responds in real-time to the system's consciousness state! 🧠⚡