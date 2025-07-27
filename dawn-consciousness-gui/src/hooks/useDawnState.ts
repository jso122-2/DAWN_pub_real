// src/hooks/useDawnState.ts
//! React hook for DAWN consciousness state management
//! Handles the fixed Rust backend integration

import { useState, useEffect, useCallback } from 'react';
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';

// TypeScript interfaces matching Rust structs
export interface MoodZone {
  valence: number;     // -1.0 to 1.0  
  arousal: number;     // 0.0 to 1.0
  dominance: number;   // 0.0 to 1.0
  coherence: number;   // 0.0 to 1.0
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
  tensor_state_hash: string;         // TensorFlow state fingerprint
}

export interface DawnStatus {
  connected: boolean;
  latest_tick: number;
  tick_rate_hz: number;
  consciousness_depth: number;
  uptime_ms: number;
  integration_mode: string;
  mmap_path: string;
}

export interface UseDawnStateReturn {
  // State
  tickState: TickState | null;
  status: DawnStatus | null;
  connected: boolean;
  error: string | null;
  
  // Actions
  connect: (mmapPath: string) => Promise<void>;
  disconnect: () => void;
  
  // Computed values
  tickRate: number;
  uptime: number;
  lastUpdate: Date | null;
}

export const useDawnState = (autoConnectPath?: string): UseDawnStateReturn => {
  const [tickState, setTickState] = useState<TickState | null>(null);
  const [status, setStatus] = useState<DawnStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);

  // Connect to DAWN consciousness engine
  const connect = useCallback(async (mmapPath: string) => {
    try {
      setError(null);
      console.log('🧠 [DAWN] Connecting to:', mmapPath);
      
      const result = await invoke<string>('connect_dawn', { 
        mmapPath 
      });
      
      console.log('✅ [DAWN] Connected:', result);
      
      // Get initial status
      const initialStatus = await invoke<DawnStatus>('get_dawn_status');
      setStatus(initialStatus);
      
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      console.error('❌ [DAWN] Connection failed:', errorMsg);
      setError(errorMsg);
    }
  }, []);

  // Disconnect (cleanup)
  const disconnect = useCallback(() => {
    setTickState(null);
    setStatus(null);
    setError(null);
    setLastUpdate(null);
  }, []);

  // Set up event listeners
  useEffect(() => {
    let tickUnlisten: (() => void) | null = null;
    let statusUnlisten: (() => void) | null = null;

    const setupListeners = async () => {
      try {
        // Listen for consciousness tick updates
        tickUnlisten = await listen<TickState>('dawn:tick', (event) => {
          console.log('🧠 [DAWN] Tick received:', event.payload.tick_number);
          setTickState(event.payload);
          setLastUpdate(new Date());
          setError(null); // Clear errors on successful tick
        });

        // Listen for status updates
        statusUnlisten = await listen<DawnStatus>('dawn:status', (event) => {
          setStatus(event.payload);
        });

        console.log('👂 [DAWN] Event listeners set up');
        
      } catch (err) {
        console.error('❌ [DAWN] Failed to set up listeners:', err);
        setError('Failed to set up event listeners');
      }
    };

    setupListeners();

    // Cleanup function
    return () => {
      if (tickUnlisten) tickUnlisten();
      if (statusUnlisten) statusUnlisten();
    };
  }, []);

  // Auto-connect on mount if path provided
  useEffect(() => {
    if (autoConnectPath) {
      connect(autoConnectPath);
    }
  }, [autoConnectPath, connect]);

  // Periodic status polling as backup
  useEffect(() => {
    if (!status?.connected) return;

    const interval = setInterval(async () => {
      try {
        const currentStatus = await invoke<DawnStatus>('get_dawn_status');
        setStatus(currentStatus);
      } catch (err) {
        console.warn('⚠️ [DAWN] Status poll failed:', err);
      }
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, [status?.connected]);

  return {
    // State
    tickState,
    status,
    connected: status?.connected || false,
    error,
    
    // Actions
    connect,
    disconnect,
    
    // Computed values
    tickRate: status?.tick_rate_hz || 0,
    uptime: status?.uptime_ms || 0,
    lastUpdate,
  };
};

// Utility functions for consciousness state analysis
export const useDawnAnalytics = (tickState: TickState | null) => {
  return {
    // Mood analysis
    moodIntensity: tickState ? Math.sqrt(
      Math.pow(tickState.mood_zone.valence, 2) + 
      Math.pow(tickState.mood_zone.arousal, 2)
    ) : 0,
    
    // Cognitive load
    cognitiveLoad: tickState ? (
      tickState.cognitive_vector.semantic_alignment +
      tickState.cognitive_vector.entropy_gradient +
      tickState.cognitive_vector.drift_magnitude +
      tickState.cognitive_vector.rebloom_intensity
    ) / 4 : 0,
    
    // Memory activity
    memoryActivity: tickState ? 
      tickState.memory_rebloom_flags.filter(Boolean).length / 64 : 0,
    
    // Semantic heat
    semanticHeat: tickState ? 
      tickState.semantic_heatmap.reduce((sum, val) => sum + val, 0) / 256 : 0,
    
    // Prediction confidence
    predictionConfidence: tickState ? 
      tickState.forecast_vector.reduce((sum, val) => sum + Math.abs(val), 0) / 32 : 0,
  };
};