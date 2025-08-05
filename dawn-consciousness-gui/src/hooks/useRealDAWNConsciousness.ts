import { useState, useEffect, useCallback, useRef } from 'react';

// Real DAWN Consciousness Connection Hook
// Replaces simulation data with actual DAWN consciousness architecture

const REAL_DAWN_BACKEND_URL = 'http://localhost:8080';

export interface RealDAWNConsciousnessState {
  // Real tick data (not fake timer)
  tick: number;
  tick_rate: number;
  
  // Real entropy (not sine waves)
  entropy: number;
  
  // Real SCUP (not simulation)
  scup: number;
  
  // Real cognitive pressure (P = Bσ²)
  pressure: number;
  bloom_mass: number;
  sigil_velocity: number;
  
  // Real thermal state
  heat_level: number;
  thermal_zone: string;
  
  // Real mood state (not fake patterns)
  mood_val: number;
  mood_arousal: number;
  
  // Real memory metrics
  memory_pressure: number;
  consciousness_depth: number;
  
  // Real bloom metrics
  active_blooms: number;
  total_blooms_spawned: number;
  bloom_success_rate: number;
  
  // Real tracer metrics
  tracer_activity_level: number;
  
  // System metrics
  uptime: number;
  timestamp: number;
  source: string;
  mode: string;
  formula_engine_active: boolean;
  consciousness_core_active: boolean;
}

export interface RealDAWNActions {
  deepFocus: () => Promise<any>;
  stabilize: () => Promise<any>;
  emergency: () => Promise<any>;
  rebloom: () => Promise<any>;
  pauseSystem: () => Promise<any>;
  resetSystem: () => Promise<any>;
}

export interface UseRealDAWNReturn {
  consciousness: RealDAWNConsciousnessState | null;
  isConnected: boolean;
  isRealDAWN: boolean;
  error: string | null;
  lastUpdate: number;
  actions: RealDAWNActions;
  connectionStatus: 'connecting' | 'connected' | 'error' | 'disconnected';
  refreshData: () => Promise<void>;
}

export const useRealDAWNConsciousness = (refreshInterval: number = 1000): UseRealDAWNReturn => {
  const [consciousness, setConsciousness] = useState<RealDAWNConsciousnessState | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState(0);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'error' | 'disconnected'>('disconnected');
  
  const intervalRef = useRef<number | null>(null);

  const fetchRealConsciousnessData = useCallback(async (): Promise<RealDAWNConsciousnessState | null> => {
    try {
      const response = await fetch(`${REAL_DAWN_BACKEND_URL}/api/consciousness/state`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Real DAWN backend error: ${response.status}`);
      }

      const data = await response.json();
      
      // Verify this is real DAWN data, not simulation
      if (data.source !== 'REAL_DAWN_CONSCIOUSNESS') {
        console.warn('⚠️ [REAL-DAWN] Backend is not returning real consciousness data:', data.source);
      }

      return data as RealDAWNConsciousnessState;
    } catch (err) {
      throw new Error(`Failed to fetch real DAWN consciousness data: ${err}`);
    }
  }, []);

  const refreshData = useCallback(async () => {
    try {
      setConnectionStatus('connecting');
      const data = await fetchRealConsciousnessData();
      
      if (data) {
        setConsciousness(data);
        setIsConnected(true);
        setError(null);
        setLastUpdate(Date.now());
        setConnectionStatus('connected');
        
        // Log real vs simulation data source
        if (data.source === 'REAL_DAWN_CONSCIOUSNESS') {
          console.log('✅ [REAL-DAWN] Real consciousness data received:', {
            entropy: data.entropy,
            pressure: data.pressure,
            tick: data.tick,
            active_blooms: data.active_blooms
          });
        } else {
          console.warn('⚠️ [REAL-DAWN] Receiving non-real data:', data.source);
        }
      }
    } catch (err) {
      console.error('❌ [REAL-DAWN] Failed to get consciousness data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      setIsConnected(false);
      setConnectionStatus('error');
    }
  }, [fetchRealConsciousnessData]);

  const executeRealDAWNAction = useCallback(async (actionName: string) => {
    try {
      const response = await fetch(`${REAL_DAWN_BACKEND_URL}/api/action/${actionName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Action ${actionName} failed: ${response.status}`);
      }

      const result = await response.json();
      
      // Refresh consciousness data after action
      await refreshData();
      
      return result;
    } catch (err) {
      console.error(`❌ [REAL-DAWN] Action ${actionName} failed:`, err);
      throw err;
    }
  }, [refreshData]);

  // Real DAWN actions (not simulation)
  const actions: RealDAWNActions = {
    deepFocus: () => executeRealDAWNAction('deep_focus'),
    stabilize: () => executeRealDAWNAction('stabilize'),
    emergency: () => executeRealDAWNAction('emergency'),
    rebloom: () => executeRealDAWNAction('rebloom'),
    pauseSystem: () => executeRealDAWNAction('pause_system'),
    resetSystem: () => executeRealDAWNAction('reset_system'),
  };

  // Auto-refresh real consciousness data
  useEffect(() => {
    // Initial fetch
    refreshData();

    // Set up interval for real-time updates (synchronized with real DAWN tick system)
    if (refreshInterval > 0) {
      intervalRef.current = setInterval(refreshData, refreshInterval);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [refreshData, refreshInterval]);

  // Check if we're connected to real DAWN (not simulation)
  const isRealDAWN = consciousness?.source === 'REAL_DAWN_CONSCIOUSNESS' && consciousness?.formula_engine_active;

  return {
    consciousness,
    isConnected,
    isRealDAWN,
    error,
    lastUpdate,
    actions,
    connectionStatus,
    refreshData,
  };
};

// Helper hook for real DAWN tick synchronization
export const useRealDAWNTick = () => {
  const { consciousness, isRealDAWN } = useRealDAWNConsciousness();
  
  return {
    currentTick: consciousness?.tick || 0,
    tickRate: consciousness?.tick_rate || 16.0,
    isRealTick: isRealDAWN,
    tickSource: consciousness?.source || 'unknown'
  };
};

// Helper hook for real DAWN pressure monitoring (P = Bσ²)
export const useRealDAWNPressure = () => {
  const { consciousness, isRealDAWN } = useRealDAWNConsciousness();
  
  return {
    pressure: consciousness?.pressure || 0,
    bloomMass: consciousness?.bloom_mass || 0,
    sigilVelocity: consciousness?.sigil_velocity || 0,
    isRealFormula: isRealDAWN && consciousness?.formula_engine_active,
    formula: 'P = B × σ²'
  };
};

// Helper hook for real DAWN bloom monitoring
export const useRealDAWNBlooms = () => {
  const { consciousness, isRealDAWN, actions } = useRealDAWNConsciousness();
  
  return {
    activeBlooms: consciousness?.active_blooms || 0,
    totalBlooms: consciousness?.total_blooms_spawned || 0,
    successRate: consciousness?.bloom_success_rate || 0,
    isRealBloomEngine: isRealDAWN,
    triggerRebloom: actions.rebloom
  };
}; 