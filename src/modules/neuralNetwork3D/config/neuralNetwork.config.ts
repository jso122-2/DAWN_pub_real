export const neuralConfig = {
  network: {
    totalNeurons: 10000,
    connectivityRules: {
      localConnectionRadius: 10,
      localConnectionProbability: 0.3,
      longRangeConnectionProbability: 0.05,
      maxConnectionsPerNeuron: 100,
      preferentialAttachment: true
    },
    layerConfig: {
      inputLayerSize: 0.1,
      hiddenLayerSizes: [0.2, 0.3, 0.2],
      outputLayerSize: 0.1
    }
  },
  
  simulation: {
    baseTickRate: 60, // Hz
    integrationStep: 0.001, // seconds
    maxFiringRate: 100, // Hz
    refractoryPeriod: 2, // ms
    fatigueRate: 0.001,
    recoveryRate: 0.01
  },
  
  plasticity: {
    learningRate: 0.01,
    ltpThreshold: 0.7,
    ltdThreshold: 0.3,
    synapticDecay: 0.0001,
    maxWeight: 1.0,
    minWeight: 0.0
  },
  
  brainwaves: {
    delta: { min: 0.5, max: 4 },
    theta: { min: 4, max: 8 },
    alpha: { min: 8, max: 13 },
    beta: { min: 13, max: 30 },
    gamma: { min: 30, max: 100 }
  },
  
  visualization: {
    neuronScale: 0.5,
    synapseOpacity: 0.3,
    regionOpacity: 0.1,
    particleCount: 1000,
    glowIntensity: 1.5,
    cameraSpeed: 0.5
  }
}; 