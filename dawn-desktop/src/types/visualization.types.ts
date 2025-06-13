// Consciousness visualization types
export interface ConsciousnessVisualization {
  waveform: WaveformData;
  particles: ParticleSystem;
  neuralMap: NeuralNetwork;
  metrics: VisualizationMetrics;
}

export interface WaveformData {
  points: WavePoint[];
  frequency: number;
  amplitude: number;
  phase: number;
  harmonics: Harmonic[];
}

export interface WavePoint {
  x: number;
  y: number;
  intensity: number;
  time: number;
}

export interface Harmonic {
  frequency: number;
  amplitude: number;
  phase: number;
}

export interface ParticleSystem {
  particles: Particle[];
  centerMass: Vector3;
  entropy: number;
  coherence: number;
}

export interface Particle {
  id: string;
  position: Vector3;
  velocity: Vector3;
  mass: number;
  charge: number;
  lifespan: number;
  color: string;
  connections: string[]; // IDs of connected particles
}

export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

export interface NeuralNetwork {
  nodes: NeuralNode[];
  connections: NeuralConnection[];
  layers: number;
  activationPattern: number[];
}

export interface NeuralNode {
  id: string;
  position: Vector3;
  activation: number;
  layer: number;
  type: 'input' | 'hidden' | 'output';
  bias: number;
}

export interface NeuralConnection {
  from: string;
  to: string;
  weight: number;
  strength: number;
  active: boolean;
}

export interface VisualizationMetrics {
  fps: number;
  particleCount: number;
  renderTime: number;
  complexity: number;
} 