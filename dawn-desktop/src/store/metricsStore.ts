import { create } from 'zustand';
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';

interface Metrics {
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
  timestamp: number;
  tick_count: number;
}

interface SubsystemInfo {
  id: string;
  name: string;
  status: string;
  state: Record<string, any>;
}

interface HealthResponse {
  status: string;
  booted: boolean;
  running: boolean;
  timestamp: number;
}

interface ConnectionStatus {
  backend: 'connected' | 'connecting' | 'disconnected' | 'error';
  websocket: boolean;
  lastUpdate: number;
}

interface MetricsState {
  // Data
  metrics: Metrics;
  subsystems: SubsystemInfo[];
  alertThresholds: Record<string, any>;
  
  // Status
  isLoading: boolean;
  error: string | null;
  connectionStatus: ConnectionStatus;
  
  // Actions
  fetchMetrics: () => Promise<void>;
  fetchSubsystems: () => Promise<void>;
  fetchSubsystemDetails: (id: string) => Promise<SubsystemInfo | null>;
  addSubsystem: (name: string, config?: Record<string, any>) => Promise<void>;
  removeSubsystem: (id: string) => Promise<void>;
  setAlertThreshold: (metric: string, threshold: number, direction?: string) => Promise<void>;
  fetchAlertThresholds: () => Promise<void>;
  checkBackendHealth: () => Promise<void>;
  subscribeToMetrics: () => Promise<void>;
  checkWebSocketConnection: () => Promise<void>;
  
  // Event listeners
  initializeEventListeners: () => () => void;
}

const useMetricsStore = create<MetricsState>((set, get) => ({
  // Initial state
  metrics: {
    scup: 0,
    entropy: 0,
    heat: 0,
    mood: 'initializing',
    timestamp: 0,
    tick_count: 0
  },
  subsystems: [],
  alertThresholds: {},
  isLoading: false,
  error: null,
  connectionStatus: {
    backend: 'disconnected',
    websocket: false,
    lastUpdate: 0
  },

  // Actions
  fetchMetrics: async () => {
    set({ isLoading: true, error: null });
    try {
      const metrics = await invoke<Metrics>('get_current_metrics');
      set({ 
        metrics, 
        isLoading: false,
        connectionStatus: { 
          ...get().connectionStatus, 
          backend: 'connected',
          lastUpdate: Date.now()
        }
      });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      set({ 
        error: errorMessage, 
        isLoading: false,
        connectionStatus: { 
          ...get().connectionStatus, 
          backend: 'error'
        }
      });
      console.error('Failed to fetch metrics:', error);
    }
  },

  fetchSubsystems: async () => {
    try {
      const subsystems = await invoke<SubsystemInfo[]>('get_subsystems');
      set({ subsystems });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      set({ error: errorMessage });
      console.error('Failed to fetch subsystems:', error);
    }
  },

  fetchSubsystemDetails: async (id: string) => {
    try {
      const subsystem = await invoke<SubsystemInfo>('get_subsystem_details', { subsystemId: id });
      return subsystem;
    } catch (error) {
      console.error(`Failed to fetch subsystem details for ${id}:`, error);
      return null;
    }
  },

  addSubsystem: async (name: string, config = {}) => {
    try {
      await invoke('add_subsystem', { name, config });
      // Refresh subsystems list
      await get().fetchSubsystems();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      set({ error: errorMessage });
      console.error('Failed to add subsystem:', error);
    }
  },

  removeSubsystem: async (id: string) => {
    try {
      await invoke('remove_subsystem', { subsystemId: id });
      // Refresh subsystems list
      await get().fetchSubsystems();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      set({ error: errorMessage });
      console.error('Failed to remove subsystem:', error);
    }
  },

  setAlertThreshold: async (metric: string, threshold: number, direction = 'above') => {
    try {
      await invoke('set_alert_threshold', { metric, threshold, direction });
      // Refresh thresholds
      await get().fetchAlertThresholds();
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      set({ error: errorMessage });
      console.error('Failed to set alert threshold:', error);
    }
  },

  fetchAlertThresholds: async () => {
    try {
      const thresholds = await invoke<Record<string, any>>('get_alert_thresholds');
      set({ alertThresholds: thresholds });
    } catch (error) {
      console.error('Failed to fetch alert thresholds:', error);
    }
  },

  checkBackendHealth: async () => {
    try {
      const health = await invoke<HealthResponse>('check_backend_health');
      set({
        connectionStatus: {
          ...get().connectionStatus,
          backend: health.status === 'healthy' ? 'connected' : 'error',
          lastUpdate: Date.now()
        }
      });
    } catch (error) {
      set({
        connectionStatus: {
          ...get().connectionStatus,
          backend: 'error'
        }
      });
      console.error('Backend health check failed:', error);
    }
  },

  subscribeToMetrics: async () => {
    try {
      await invoke('subscribe_to_metrics');
      console.log('WebSocket subscription started');
    } catch (error) {
      console.error('Failed to subscribe to metrics:', error);
    }
  },

  checkWebSocketConnection: async () => {
    try {
      const connected = await invoke<boolean>('is_websocket_connected');
      set({
        connectionStatus: {
          ...get().connectionStatus,
          websocket: connected
        }
      });
    } catch (error) {
      console.error('Failed to check WebSocket connection:', error);
    }
  },

  initializeEventListeners: () => {
    const unsubscribers: (() => void)[] = [];

    // Listen for metrics updates from WebSocket
    listen<Metrics>('metrics-update', (event) => {
      console.log('Received metrics update:', event.payload);
      set({ 
        metrics: event.payload,
        connectionStatus: {
          ...get().connectionStatus,
          websocket: true,
          lastUpdate: Date.now()
        }
      });
    }).then(unlisten => unsubscribers.push(unlisten));

    // Listen for backend connection events
    listen('backend-connecting', () => {
      console.log('Backend connecting...');
      set({
        connectionStatus: {
          ...get().connectionStatus,
          backend: 'connecting'
        }
      });
    }).then(unlisten => unsubscribers.push(unlisten));

    listen('backend-connected', () => {
      console.log('Backend connected!');
      set({
        connectionStatus: {
          ...get().connectionStatus,
          backend: 'connected'
        }
      });
    }).then(unlisten => unsubscribers.push(unlisten));

    listen<string>('backend-error', (event) => {
      console.error('Backend error:', event.payload);
      set({
        error: event.payload,
        connectionStatus: {
          ...get().connectionStatus,
          backend: 'error'
        }
      });
    }).then(unlisten => unsubscribers.push(unlisten));

    // Return cleanup function
    return () => {
      unsubscribers.forEach(unsubscribe => unsubscribe());
    };
  }
}));

export default useMetricsStore; 