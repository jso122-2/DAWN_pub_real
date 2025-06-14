export interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  quantumCoherence: number;
  memoryPressure: number;
  timestamp: number;
}

export interface TickData {
  tick_number: number;
  timestamp: number;
  scup: number;
  entropy: number;
  mood: string;
  neural_activity: number;
  quantum_coherence: number;
  memory_pressure: number;
  active_processes: string[];
} 