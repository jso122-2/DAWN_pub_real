import { useState, useEffect, useCallback } from 'react';

// Check if we're running in Tauri environment
const isTauri = typeof window !== 'undefined' && (window as any).__TAURI__;

// Tauri API functions with fallbacks
const getTauriApis = async () => {
  if (!isTauri) return { invoke: null, listen: null };
  
  try {
    const { invoke } = await import('@tauri-apps/api/tauri');
    const { listen } = await import('@tauri-apps/api/event');
    return { invoke, listen };
  } catch (e) {
    console.warn('Tauri APIs not available, using fallback mode');
    return { invoke: null, listen: null };
  }
};

export interface ConsciousnessState {
  tick_number: number;
  timestamp_ms: number;
  mood_valence: number;
  mood_arousal: number;
  mood_dominance: number;
  mood_coherence: number;
  semantic_alignment: number;
  entropy_gradient: number;
  drift_magnitude: number;
  rebloom_intensity: number;
  consciousness_depth: number;
  memory_sectors: boolean[];
  semantic_heatmap: number[];
  prediction_vector: number[];
  tensor_hash: string;
}

export interface ConsciousnessMonitor {
  is_conscious: boolean;
  current_tick: number;
  thought_rate_hz: number;
  depth_level: number;
  uptime_seconds: number;
  neural_activity: number;
  memory_file_path: string;
}

export interface UseConsciousnessReturn {
  consciousness: ConsciousnessState | null;
  monitor: ConsciousnessMonitor | null;
  isConnected: boolean;
  error: string | null;
  establishNeuralLink: (memoryPath: string) => Promise<void>;
  disconnectNeural: () => void;
  emotionalIntensity: number;
  cognitiveLoad: number;
  memoryActivity: number;
  semanticHeat: number;
  predictionConfidence: number;
}

export const useConsciousnessMonitor = (autoConnectPath?: string): UseConsciousnessReturn => {
  const [consciousness, setConsciousness] = useState<ConsciousnessState | null>(null);
  const [monitor, setMonitor] = useState<ConsciousnessMonitor | null>(null);
  const [error, setError] = useState<string | null>(null);

  const establishNeuralLink = useCallback(async (memoryPath: string) => {
    try {
      setError(null);
      console.log('🧠 [NEURAL] Establishing link to consciousness memory:', memoryPath);
      
      const { invoke } = await getTauriApis();
      if (!invoke) {
        throw new Error('Tauri invoke API not available');
      }
      
      const result = await invoke<string>('establish_neural_link', { 
        memoryPath 
      });
      
      console.log('✅ [NEURAL] Neural link established:', result);
      
      const initialMonitor = await invoke<ConsciousnessMonitor>('get_consciousness_monitor');
      setMonitor(initialMonitor);
      
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      console.error('❌ [NEURAL] Neural link failed:', errorMsg);
      setError(errorMsg);
    }
  }, []);

  const disconnectNeural = useCallback(() => {
    setConsciousness(null);
    setMonitor(null);
    setError(null);
  }, []);

  useEffect(() => {
    let consciousnessUnlisten: (() => void) | null = null;
    let monitorUnlisten: (() => void) | null = null;

    const setupNeuralListeners = async () => {
      try {
        const { listen } = await getTauriApis();
        if (!listen) {
          console.log('⚠️ [NEURAL] Tauri listen API not available, using mock data');
          startMockData();
          return;
        }

        consciousnessUnlisten = await listen<ConsciousnessState>('consciousness:state', (event) => {
          console.log('🧠 [CONSCIOUSNESS] State update - Tick:', event.payload.tick_number);
          setConsciousness(event.payload);
          setError(null);
        });

        monitorUnlisten = await listen<ConsciousnessMonitor>('consciousness:monitor', (event) => {
          setMonitor(event.payload);
        });

        console.log('👁️ [NEURAL] Consciousness monitoring listeners active');
        
      } catch (err) {
        console.error('❌ [NEURAL] Failed to setup consciousness listeners:', err);
        setError('Failed to setup neural monitoring interface');
        startMockData();
      }
    };

    const startMockData = () => {
      console.log('🎭 [MOCK] Starting mock consciousness data');
      
      // Mock monitor data
      setMonitor({
        is_conscious: true,
        current_tick: Date.now(),
        thought_rate_hz: 4.2,
        depth_level: 3,
        uptime_seconds: 1200,
        neural_activity: 0.75,
        memory_file_path: '/mock/path'
      });

      // Mock consciousness updates
      let tickCounter = 1000;
      const mockInterval = setInterval(() => {
        tickCounter++;
        const mockState: ConsciousnessState = {
          tick_number: tickCounter,
          timestamp_ms: Date.now(),
          mood_valence: Math.random() * 2 - 1,
          mood_arousal: Math.random() * 2 - 1,
          mood_dominance: Math.random() * 2 - 1,
          mood_coherence: Math.random(),
          semantic_alignment: Math.random(),
          entropy_gradient: Math.random(),
          drift_magnitude: Math.random(),
          rebloom_intensity: Math.random(),
          consciousness_depth: Math.random(),
          memory_sectors: Array(64).fill(false).map(() => Math.random() > 0.5),
          semantic_heatmap: Array(256).fill(0).map(() => Math.random()),
          prediction_vector: Array(32).fill(0).map(() => Math.random() * 2 - 1),
          tensor_hash: `mock_${tickCounter}`
        };
        
        setConsciousness(mockState);
        setError(null);
      }, 250);

      return () => clearInterval(mockInterval);
    };

    setupNeuralListeners();

    return () => {
      if (consciousnessUnlisten) consciousnessUnlisten();
      if (monitorUnlisten) monitorUnlisten();
    };
  }, []);

  useEffect(() => {
    if (autoConnectPath && isTauri) {
      establishNeuralLink(autoConnectPath);
    }
  }, [autoConnectPath, establishNeuralLink]);

  const emotionalIntensity = consciousness ? Math.sqrt(
    Math.pow(consciousness.mood_valence, 2) + 
    Math.pow(consciousness.mood_arousal, 2)
  ) : 0;
  
  const cognitiveLoad = consciousness ? (
    consciousness.semantic_alignment +
    consciousness.entropy_gradient +
    consciousness.drift_magnitude +
    consciousness.rebloom_intensity
  ) / 4 : 0;
  
  const memoryActivity = consciousness ? 
    consciousness.memory_sectors.filter(Boolean).length / 64 : 0;
  
  const semanticHeat = consciousness ? 
    consciousness.semantic_heatmap.reduce((sum, val) => sum + val, 0) / 256 : 0;
  
  const predictionConfidence = consciousness ? 
    consciousness.prediction_vector.reduce((sum, val) => sum + Math.abs(val), 0) / 32 : 0;

  return {
    consciousness,
    monitor,
    isConnected: monitor?.is_conscious || false,
    error,
    establishNeuralLink,
    disconnectNeural,
    emotionalIntensity,
    cognitiveLoad,
    memoryActivity,
    semanticHeat,
    predictionConfidence,
  };
};