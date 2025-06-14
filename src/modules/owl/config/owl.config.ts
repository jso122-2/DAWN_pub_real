export const owlConfig = {
  // Connection settings
  websocket: {
    url: 'ws://localhost:8000/owl',
    reconnectDelay: 5000,
    maxReconnectAttempts: 10,
    heartbeatInterval: 30000
  },

  // Analysis settings
  analysis: {
    deepAnalysisInterval: 50, // ticks
    activityThreshold: 10, // observations to trigger deep analysis
    maxObservationBuffer: 1000,
    confidenceThreshold: 0.7
  },

  // Focus management
  focus: {
    maxTicks: 1000, // Maximum ticks to stay on one focus
    shiftThreshold: 0.8, // Significance threshold for focus shift
    momentum: {
      decay: 0.95,
      threshold: 0.1
    }
  },

  // Schema detection
  schemas: {
    alignmentThreshold: 0.3, // Minimum alignment to be relevant
    transitionProbability: 0.1, // Base transition probability
    phaseStability: {
      minTicks: 50,
      maxTicks: 1000
    }
  },

  // Planning horizons
  planning: {
    horizons: {
      immediate: 10,   // 1-10 ticks
      near: 100,       // 10-100 ticks
      medium: 1000,    // 100-1000 ticks
      far: 10000,      // 1000-10000 ticks
      epochal: 100000  // 10000+ ticks
    },
    maxActivePlans: 5,
    planConfidenceThreshold: 0.6
  },

  // Visualization settings
  visualization: {
    maxDataPoints: 200,
    animationDuration: 300,
    colors: {
      primary: '#4f46e5',
      secondary: '#06b6d4',
      success: '#10b981',
      warning: '#f59e0b',
      danger: '#ef4444',
      insight: '#8b5cf6',
      observation: '#64748b'
    },
    opacity: {
      active: 1.0,
      inactive: 0.6,
      disabled: 0.3
    }
  },

  // Attention allocation
  attention: {
    totalCapacity: 1.0,
    moduleWeights: {
      neural: 0.3,
      quantum: 0.2,
      memory: 0.2,
      process: 0.2,
      self: 0.1
    },
    adaptiveThreshold: 0.1 // When to adjust attention
  },

  // Reflection depth settings
  reflection: {
    maxDepth: 10,
    defaultDepth: 5,
    depthIncrement: 1,
    timePerDepth: 100 // ms
  },

  // Pattern detection
  patterns: {
    oscillation: {
      minDataPoints: 10,
      signChangeThreshold: 0.5
    },
    trend: {
      minDataPoints: 5,
      strengthThreshold: 0.8,
      rSquaredThreshold: 0.7
    },
    anomaly: {
      zScoreThreshold: 3.0,
      windowSize: 50
    }
  },

  // Semantic space
  semantic: {
    dimensions: [
      'consciousness',
      'coherence', 
      'exploration',
      'stability',
      'emergence',
      'complexity'
    ],
    neighborhood: {
      maxDistance: 0.3,
      stabilityThreshold: 0.7
    }
  },

  // Logging and debugging
  debug: {
    enabled: process.env.NODE_ENV === 'development',
    logLevel: 'info', // 'debug' | 'info' | 'warn' | 'error'
    logObservations: true,
    logReflections: true,
    logPlanning: true
  }
}; 