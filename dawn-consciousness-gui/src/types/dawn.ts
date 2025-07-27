export interface MoodZone {
  valence: number;    // -1.0 to 1.0
  arousal: number;    // 0.0 to 1.0
  dominance: number;  // 0.0 to 1.0
  coherence: number;  // 0.0 to 1.0
}

export interface CognitiveVector {
  semantic_alignment: number;
  entropy_gradient: number;
  drift_magnitude: number;
  rebloom_intensity: number;
}

export interface TickState {
  tick_number: number;
  timestamp_ms: number;
  mood_zone: MoodZone;
  cognitive_vector: CognitiveVector;
  memory_rebloom_flags: boolean[];   // 64 memory sectors
  semantic_heatmap: number[];        // 256 semantic nodes
  forecast_vector: number[];         // 32 prediction dimensions
  consciousness_depth: number;       // 0.0 to 1.0
  tensor_state_hash: string;         // State fingerprint
}

export interface DawnStatus {
  connected: boolean;
  latest_tick: number;
  tick_rate_hz: number;
  consciousness_depth: number;
  uptime_ms: number;
  integration_mode: string;
}

export interface ConnectionSettings {
  mmap_path: string;
  auto_connect: boolean;
  update_interval: number;
} 