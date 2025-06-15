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
  RegionType,
  PlasticityEvent
} from './types/neural.types';
import { neuralConfig } from './config/neuralNetwork.config';

// Import consciousness types - we'll need to create this
interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  systemUnity: number;
}

export class NeuralNetworkCore extends EventEmitter {
  private state: NetworkState;
  
  // Simulation parameters
  private simulationSpeed = 1.0;
  private lastUpdate = Date.now();
  private tickCount = 0;
  private isRunning = false;
  
  constructor() {
    super();
    
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
    const neurons = this.generateNeurons(layers, regions, neuralConfig.network.totalNeurons);
    
    neurons.forEach(neuron => {
      this.state.topology.neurons.set(neuron.id, neuron);
    });
    
    // Create connections
    this.generateConnections();
    
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
    
    neuron.state.potential += strength * 20; // Strong stimulation
    this.emit('neuronStimulated', { neuronId, strength });
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
  
  private generateNeurons(layers: NetworkLayer[], regions: BrainRegion[], totalCount: number): Neuron[] {
    const neurons: Neuron[] = [];
    let neuronId = 0;
    
    layers.forEach(layer => {
      for (let i = 0; i < layer.neuronCount; i++) {
        // Generate position within layer
        const angle = (i / layer.neuronCount) * Math.PI * 2;
        const radius = layer.radius * (0.5 + Math.random() * 0.5);
        const height = (Math.random() - 0.5) * 10;
        
        const position = new THREE.Vector3(
          layer.position.x + Math.cos(angle) * radius,
          layer.position.y + height,
          layer.position.z + Math.sin(angle) * radius
        );
        
        // Assign to nearest region
        const nearestRegion = this.findNearestRegion(position, regions);
        
        // Determine neuron type based on layer
        let neuronType: NeuronType = 'interneuron';
        if (layer.type === 'input') neuronType = 'sensory';
        else if (layer.type === 'output') neuronType = 'motor';
        else if (Math.random() < 0.3) neuronType = 'pyramidal';
        
        const neuron: Neuron = {
          id: `neuron_${neuronId++}`,
          type: neuronType,
          position,
          layer,
          region: nearestRegion,
          state: {
            potential: -70, // Resting potential
            threshold: -55,
            firing: false,
            lastFired: 0,
            firingRate: 0,
            refractory: false,
            fatigue: 0,
            health: 1.0
          },
          connections: [],
          metadata: {
            birthTick: 0,
            totalFirings: 0,
            averageActivity: 0,
            preferredInput: '',
            receptiveField: {
              shape: 'circular',
              size: 10,
              selectivity: Math.random()
            },
            plasticityRate: 0.01
          }
        };
        
        neurons.push(neuron);
        nearestRegion.neurons.push(neuron.id);
      }
    });
    
    return neurons;
  }
  
  private findNearestRegion(position: THREE.Vector3, regions: BrainRegion[]): BrainRegion {
    let nearestRegion = regions[0];
    let minDistance = position.distanceTo(nearestRegion.center);
    
    regions.forEach(region => {
      const distance = position.distanceTo(region.center);
      if (distance < minDistance) {
        minDistance = distance;
        nearestRegion = region;
      }
    });
    
    return nearestRegion;
  }
  
  private generateConnections() {
    const neurons = Array.from(this.state.topology.neurons.values());
    const config = neuralConfig.network.connectivityRules;
    
    neurons.forEach(neuron => {
      const connections: SynapticConnection[] = [];
      let connectionCount = 0;
      
      // Local connections
      neurons.forEach(target => {
        if (target.id === neuron.id) return;
        if (connectionCount >= config.maxConnectionsPerNeuron) return;
        
        const distance = neuron.position.distanceTo(target.position);
        
        // Local connections
        if (distance < config.localConnectionRadius) {
          if (Math.random() < config.localConnectionProbability) {
            connections.push(this.createConnection(neuron.id, target.id, distance));
            connectionCount++;
          }
        }
        // Long-range connections
        else if (Math.random() < config.longRangeConnectionProbability) {
          connections.push(this.createConnection(neuron.id, target.id, distance));
          connectionCount++;
        }
      });
      
      neuron.connections = connections;
    });
  }
  
  private createConnection(preId: string, postId: string, distance: number): SynapticConnection {
    return {
      id: `synapse_${preId}_${postId}`,
      preNeuronId: preId,
      postNeuronId: postId,
      weight: Math.random() * 0.5 + 0.25, // 0.25-0.75
      type: Math.random() < 0.8 ? 'excitatory' : 'inhibitory',
      plasticity: 0.01,
      delay: Math.max(1, distance * 0.1), // Distance-based delay
      active: false,
      lastActivated: 0,
      metadata: {
        neurotransmitter: 'glutamate',
        receptorType: 'AMPA',
        strengthHistory: [],
        activityCount: 0
      }
    };
  }
  
  private updateNetworkMetrics() {
    const topology = this.state.topology;
    
    // Calculate connectivity
    let totalConnections = 0;
    topology.neurons.forEach(neuron => {
      totalConnections += neuron.connections.length;
    });
    
    topology.globalConnectivity = totalConnections / 
      (topology.neurons.size * topology.neurons.size);
    
    // TODO: Calculate other metrics
    topology.smallWorldness = 0.6 + Math.random() * 0.2;
    topology.modularity = 0.7 + Math.random() * 0.15;
  }
  
  /**
   * Main simulation loop
   */
  private startSimulation() {
    this.isRunning = true;
    const simulate = () => {
      if (!this.isRunning) return;
      
      const deltaTime = (Date.now() - this.lastUpdate) * this.simulationSpeed;
      this.lastUpdate = Date.now();
      
      this.update(deltaTime);
      
      setTimeout(() => requestAnimationFrame(simulate), 16); // ~60fps
    };
    
    requestAnimationFrame(simulate);
  }
  
  private update(deltaTime: number) {
    this.tickCount++;
    
    // Update neural activity
    this.simulateNeuralActivity(deltaTime);
    
    // Process firing patterns
    this.processFiringPatterns();
    
    // Update network health
    this.updateNetworkHealth();
    
    // Emit update event
    this.emit('networkUpdate', {
      activity: this.state.currentActivity,
      brainwaves: this.state.brainwaves,
      patterns: Array.from(this.state.firingPatterns.values())
    });
  }
  
  private simulateNeuralActivity(deltaTime: number) {
    const neurons = Array.from(this.state.topology.neurons.values());
    const firingNeurons = new Set<string>();
    let totalActivity = 0;
    
    // Update each neuron
    neurons.forEach(neuron => {
      // Add random noise
      const totalInput = (Math.random() - 0.5) * 2;
      
      // Update membrane potential
      neuron.state.potential += totalInput * deltaTime;
      
      // Check firing threshold
      if (neuron.state.potential > neuron.state.threshold) {
        neuron.state.firing = true;
        neuron.state.lastFired = Date.now();
        neuron.state.potential = -70; // Reset potential
        neuron.metadata.totalFirings++;
        
        firingNeurons.add(neuron.id);
        totalActivity += 1;
      } else {
        neuron.state.firing = false;
        // Passive decay
        neuron.state.potential += (-70 - neuron.state.potential) * 0.1 * deltaTime;
      }
    });
    
    // Update activity state
    this.state.currentActivity = {
      timestamp: Date.now(),
      tickNumber: this.tickCount,
      globalActivity: totalActivity / neurons.length,
      firingNeurons,
      propagationWaves: [],
      synchronyIndex: firingNeurons.size / neurons.length,
      dominantFrequency: 8 + Math.random() * 20,
      phaseCoherence: Math.random() * 0.5 + 0.5
    };
  }
  
  private processFiringPatterns() {
    // Clean old patterns
    const now = Date.now();
    this.state.firingPatterns.forEach((pattern, id) => {
      if (now - pattern.lastOccurrence > 10000) {
        this.state.firingPatterns.delete(id);
      }
    });
  }
  
  private updateNetworkHealth() {
    this.state.health.overallHealth = 1.0;
  }
  
  dispose() {
    this.isRunning = false;
    this.removeAllListeners();
  }
}

// Export singleton
export const neuralNetwork = new NeuralNetworkCore(); 