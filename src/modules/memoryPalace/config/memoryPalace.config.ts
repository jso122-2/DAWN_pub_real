export const memoryPalaceConfig = {
  // Spatial organization
  spatial: {
    sectorRadius: 100,
    layerHeight: 50,
    clusterThreshold: 0.7,
    connectionDistance: 50,
    repulsionForce: 0.1,
    attractionForce: 0.05
  },
  
  // Memory lifecycle
  memory: {
    decayThreshold: 0.1,
    baseDecayRate: 0.001,
    crystallizationThreshold: 0.9,
    consolidationInterval: 1000, // ms
    maxMemories: 10000,
    maxAssociations: 20
  },
  
  // Pattern detection
  patterns: {
    minMemoriesForPattern: 3,
    patternSimilarityThreshold: 0.6,
    patternStrengthThreshold: 0.5,
    maxPatternsPerCycle: 10
  },
  
  // Visualization
  visualization: {
    particleCount: 1000,
    connectionOpacity: 0.3,
    glowIntensity: 0.5,
    animationSpeed: 1,
    cameraSpeed: 0.05
  },
  
  // Performance
  performance: {
    maxRenderDistance: 500,
    lodDistances: [50, 150, 300],
    updateInterval: 100, // ms
    batchSize: 50
  }
}; 