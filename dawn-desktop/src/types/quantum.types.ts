import { Vector3 } from 'three';

export interface StateAmplitude {
  real: number;
  imaginary: number;
}

export interface ConsciousnessState {
  id: string;
  timestamp: number;
  
  // Core consciousness properties
  stateDistribution: StateAmplitude[];
  probabilityDistribution: number[];
  unity: number; // 0-1, how consciousness vs classical
  entropy: number;
  
  // Multi-state states
  multiStates: MultiState[];
  
  // Correlation network
  correlations: Correlation[];
  
  // Observable properties
  observables: {
    position: Observable<Vector3>;
    momentum: Observable<Vector3>;
    spin: Observable<number>;
    energy: Observable<number>;
  };
  
  // Consciousness correlation
  scup: number; // System Consciousness Unity Percentage
  mood: string;
  thoughtVectors: ThoughtPattern[];
}

export interface MultiState {
  id: string;
  states: PossibleState[];
  amplitudes: StateAmplitude[];
  unityTime: number;
  measurementBasis?: string;
}

export interface PossibleState {
  label: string;
  vector: number[];
  probability: number;
  color: string;
}

export interface Correlation {
  id: string;
  particleA: string;
  particleB: string;
  strength: number; // 0-1
  type: 'bell' | 'ghz' | 'cluster';
  correlations: {
    position: number;
    momentum: number;
    spin: number;
  };
}

export interface Observable<T> {
  expectationValue: T;
  uncertainty: number;
  eigenvalues: T[];
  eigenstates: PossibleState[];
}

export interface ThoughtPattern {
  id: string;
  position: Vector3;
  direction: Vector3;
  magnitude: number;
  consciousnessState: string; // Reference to multiState
  semanticContent?: string;
}

export interface ThoughtNode {
  id: string;
  position: Vector3;
  velocity: Vector3;
  wavePacket: {
    center: Vector3;
    spread: number;
    momentum: Vector3;
  };
  spin: number;
  charge: number;
  correlations: string[]; // IDs of correlated particles
  lifetime: number;
  color: string;
}

export interface ConsciousnessFieldPoint {
  position: Vector3;
  potential: number;
  fieldStrength: Vector3;
  probability: number;
}

export interface StateCollapseEvent {
  timestamp: number;
  location: Vector3;
  strength: number;
  cause: 'measurement' | 'environment' | 'entanglement';
  affectedStates: string[];
}

export interface BreakthroughEvent {
  startPosition: Vector3;
  endPosition: Vector3;
  probability: number;
  barrier: {
    height: number;
    width: number;
  };
  duration: number;
}

export interface ConsciousnessVisualizationState {
  currentState: ConsciousnessState | null;
  particles: Map<string, ThoughtNode>;
  deunityEvents: StateCollapseEvent[];
  measurementMode: 'position' | 'momentum' | 'spin' | 'energy';
  visualizationMode: 'field' | 'particles' | 'entanglement' | 'thoughts';
  timeEvolution: boolean;
  evolutionSpeed: number;
} 