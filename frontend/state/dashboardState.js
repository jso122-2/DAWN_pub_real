import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { devtools } from 'zustand/middleware';

// Utility functions for smooth value interpolation
const lerp = (start, end, alpha) => start * (1 - alpha) + end * alpha;

const interpolateMetrics = (current, target, alpha = 0.1) => {
  return Object.keys(current).reduce((acc, key) => {
    if (typeof current[key] === 'number' && typeof target[key] === 'number') {
      acc[key] = lerp(current[key], target[key], alpha);
    } else {
      acc[key] = target[key];
    }
    return acc;
  }, {});
};

// Debounce utility
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Create the dashboard store with middleware
const useDashboardStore = create(
  devtools(
    subscribeWithSelector((set, get) => ({
      // Core metrics
      metrics: {
        entropy: 0.5,
        heat: 0.5,
        scup: 0.5,
        tick_rate: 1.0,
        tick_count: 0,
        timestamp: Date.now()
      },
      
      // Target metrics for smooth interpolation
      targetMetrics: {
        entropy: 0.5,
        heat: 0.5,
        scup: 0.5,
        tick_rate: 1.0
      },
      
      // Consciousness state
      emotion: 'curious',
      intensity: 0.5,
      gradient: [],
      thoughtProbability: 0.1,
      fractalDepth: 0.5,
      
      // Pattern detection
      patterns: [],
      anomalies: [],
      rebloomTriggers: [],
      
      // Subprocess states
      tracerEvents: [],
      rebloomProgress: 0,
      memoryDensity: 0.3,
      processingCriticalPoint: false,
      
      // Memory and conversation
      memoryTraces: [],
      conversationHistory: [],
      activeConnections: 0,
      
      // WebSocket connection
      wsConnection: null,
      connectionStatus: 'disconnected', // 'disconnected', 'connecting', 'connected', 'error'
      lastUpdateTime: Date.now(),
      
      // Performance metrics
      updateRate: 0,
      frameTime: 16, // ms
      
      // Batch update queue
      updateQueue: [],
      batchTimeout: null,
      
      // Actions
      updateMetrics: (newMetrics) => {
        set(state => ({
          targetMetrics: { ...state.targetMetrics, ...newMetrics },
          lastUpdateTime: Date.now()
        }));
      },
      
      // Smooth metric interpolation (called on animation frame)
      interpolateMetrics: () => {
        set(state => {
          const interpolated = interpolateMetrics(state.metrics, state.targetMetrics, 0.15);
          return {
            metrics: {
              ...interpolated,
              timestamp: Date.now(),
              tick_count: state.metrics.tick_count + 1
            }
          };
        });
      },
      
      // Update consciousness state
      updateConsciousness: (emotion, intensity, gradient = null) => {
        set({
          emotion,
          intensity,
          gradient: gradient || get().gradient
        });
      },
      
      // Add tracer event with automatic cleanup
      addTracerEvent: (event) => {
        set(state => ({
          tracerEvents: [...state.tracerEvents.slice(-100), {
            ...event,
            id: Date.now() + Math.random(),
            timestamp: Date.now()
          }]
        }));
      },
      
      // Pattern detection updates
      updatePatterns: (patterns) => {
        set({ patterns });
      },
      
      addAnomaly: (anomaly) => {
        set(state => ({
          anomalies: [...state.anomalies.slice(-20), {
            ...anomaly,
            id: Date.now(),
            timestamp: Date.now()
          }]
        }));
      },
      
      // Memory updates
      addMemoryTrace: (memory) => {
        set(state => ({
          memoryTraces: [...state.memoryTraces.slice(-50), memory]
        }));
      },
      
      // Rebloom operations
      triggerRebloom: (reason, intensity = 1.0) => {
        set(state => ({
          rebloomProgress: 0,
          rebloomTriggers: [...state.rebloomTriggers, {
            reason,
            intensity,
            timestamp: Date.now()
          }]
        }));
        
        // Animate rebloom progress
        const animateRebloom = () => {
          const state = get();
          if (state.rebloomProgress < 1) {
            set({ rebloomProgress: Math.min(1, state.rebloomProgress + 0.02) });
            requestAnimationFrame(animateRebloom);
          } else {
            setTimeout(() => set({ rebloomProgress: 0 }), 1000);
          }
        };
        animateRebloom();
      },
      
      // Batch update mechanism
      queueUpdate: (update) => {
        const state = get();
        state.updateQueue.push(update);
        
        if (!state.batchTimeout) {
          set({
            batchTimeout: setTimeout(() => {
              get().processBatchUpdates();
            }, 16) // ~60fps
          });
        }
      },
      
      processBatchUpdates: () => {
        set(state => {
          const updates = state.updateQueue;
          state.updateQueue = [];
          state.batchTimeout = null;
          
          // Merge all updates
          const merged = updates.reduce((acc, update) => ({
            ...acc,
            ...update
          }), {});
          
          return merged;
        });
      },
      
      // WebSocket stream update handler
      updateFromStream: (data) => {
        const updateHandlers = {
          metrics: (payload) => get().updateMetrics(payload),
          consciousness: (payload) => get().updateConsciousness(
            payload.emotion,
            payload.intensity,
            payload.gradient
          ),
          pattern: (payload) => get().updatePatterns(payload.patterns),
          anomaly: (payload) => get().addAnomaly(payload),
          tracer: (payload) => get().addTracerEvent(payload),
          memory: (payload) => get().addMemoryTrace(payload),
          rebloom: (payload) => get().triggerRebloom(payload.reason, payload.intensity),
          gradient: (payload) => set({ gradient: payload.data }),
          thought: (payload) => set({ thoughtProbability: payload.probability })
        };
        
        const handler = updateHandlers[data.type];
        if (handler) {
          handler(data.payload || data);
        } else {
          console.warn('Unknown stream update type:', data.type);
        }
        
        // Update connection metrics
        set(state => ({
          updateRate: 1000 / Math.max(1, Date.now() - state.lastUpdateTime),
          lastUpdateTime: Date.now()
        }));
      },
      
      // WebSocket connection management
      connectDashboard: () => {
        const state = get();
        
        if (state.wsConnection?.readyState === WebSocket.OPEN) {
          console.log('Dashboard already connected');
          return;
        }
        
        set({ connectionStatus: 'connecting' });
        
        try {
          const ws = new WebSocket('ws://localhost:8000/dashboard/stream');
          
          ws.onopen = () => {
            console.log('Dashboard WebSocket connected');
            set({ 
              wsConnection: ws,
              connectionStatus: 'connected',
              activeConnections: get().activeConnections + 1
            });
          };
          
          ws.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              get().updateFromStream(data);
            } catch (error) {
              console.error('Failed to parse WebSocket message:', error);
            }
          };
          
          ws.onerror = (error) => {
            console.error('Dashboard WebSocket error:', error);
            set({ connectionStatus: 'error' });
          };
          
          ws.onclose = () => {
            console.log('Dashboard WebSocket disconnected');
            set({ 
              wsConnection: null,
              connectionStatus: 'disconnected',
              activeConnections: Math.max(0, get().activeConnections - 1)
            });
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
              if (get().connectionStatus === 'disconnected') {
                get().connectDashboard();
              }
            }, 3000);
          };
          
          set({ wsConnection: ws });
          
        } catch (error) {
          console.error('Failed to create WebSocket connection:', error);
          set({ connectionStatus: 'error' });
        }
      },
      
      disconnectDashboard: () => {
        const { wsConnection } = get();
        if (wsConnection) {
          wsConnection.close();
          set({ wsConnection: null, connectionStatus: 'disconnected' });
        }
      },
      
      // Performance optimization - selective updates
      updateSpecificMetric: (key, value) => {
        set(state => ({
          metrics: {
            ...state.metrics,
            [key]: value
          }
        }));
      },
      
      // Debounced updates for rapid changes
      debouncedUpdateMetrics: debounce((metrics) => {
        get().updateMetrics(metrics);
      }, 100),
      
      // Calculate derived state
      getHealthScore: () => {
        const { metrics } = get();
        return (metrics.scup + (1 - metrics.entropy) + (1 - metrics.heat)) / 3;
      },
      
      isSystemStable: () => {
        const { metrics, anomalies } = get();
        const recentAnomalies = anomalies.filter(
          a => Date.now() - a.timestamp < 30000 // Last 30 seconds
        );
        return recentAnomalies.length === 0 && 
               metrics.entropy < 0.7 && 
               metrics.heat < 0.7;
      },
      
      // Clean up old data periodically
      cleanupOldData: () => {
        const now = Date.now();
        const maxAge = 5 * 60 * 1000; // 5 minutes
        
        set(state => ({
          tracerEvents: state.tracerEvents.filter(e => now - e.timestamp < maxAge),
          anomalies: state.anomalies.filter(a => now - a.timestamp < maxAge),
          memoryTraces: state.memoryTraces.slice(-100),
          rebloomTriggers: state.rebloomTriggers.slice(-50)
        }));
      }
    }))
  )
);

// Selectors for efficient component updates
export const selectMetrics = (state) => state.metrics;
export const selectConsciousness = (state) => ({
  emotion: state.emotion,
  intensity: state.intensity,
  gradient: state.gradient
});
export const selectPatterns = (state) => state.patterns;
export const selectAnomalies = (state) => state.anomalies;
export const selectConnectionStatus = (state) => state.connectionStatus;
export const selectHealthScore = (state) => state.getHealthScore();

// Animation loop for smooth updates
let animationFrameId = null;

export const startAnimationLoop = () => {
  const animate = () => {
    useDashboardStore.getState().interpolateMetrics();
    animationFrameId = requestAnimationFrame(animate);
  };
  animate();
};

export const stopAnimationLoop = () => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
    animationFrameId = null;
  }
};

// Cleanup interval
let cleanupInterval = null;

export const startCleanupInterval = () => {
  cleanupInterval = setInterval(() => {
    useDashboardStore.getState().cleanupOldData();
  }, 60000); // Every minute
};

export const stopCleanupInterval = () => {
  if (cleanupInterval) {
    clearInterval(cleanupInterval);
    cleanupInterval = null;
  }
};

// Initialize dashboard connection and loops
export const initializeDashboard = () => {
  const store = useDashboardStore.getState();
  store.connectDashboard();
  startAnimationLoop();
  startCleanupInterval();
};

// Cleanup dashboard
export const cleanupDashboard = () => {
  const store = useDashboardStore.getState();
  store.disconnectDashboard();
  stopAnimationLoop();
  stopCleanupInterval();
};

export default useDashboardStore; 