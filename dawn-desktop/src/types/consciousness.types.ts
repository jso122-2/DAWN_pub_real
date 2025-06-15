export interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  systemUnity: number;
  memoryPressure: number;
  timestamp: number;
  tick: number; // Added for Cairrn cache compatibility
}

export interface TickData {
  tick_number: number;
  timestamp: number;
  scup: number;
  entropy: number;
  mood: string;
  neural_activity: number;
  consciousness_unity: number;
  memory_pressure: number;
  active_processes: string[];
} 