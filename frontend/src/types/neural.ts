export interface NeuralMetrics {
  neural_activity: number;
  quantum_coherence: number;
  chaos_factor: number;
  memory_utilization: number;
  pattern_recognition: number;
  entropy_distribution: number[];
  tick_number: number;
}

export interface RadarChartProps {
  data: NeuralMetrics | null;
}

export interface HistogramProps {
  data: number[];
  bins?: number;
  height?: number;
} 