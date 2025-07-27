// Dawn Neural Monitor - Integration Demo
// Phase 3: Dawn-Specific Scaffolding - Complete Implementation

import React, { useState, useEffect, useCallback } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Text, Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';
import { motion } from 'framer-motion';

// Dawn imports
import { useDawnSystem, useConsciousnessMonitoring, useEntropyRegulation } from '../../hooks/dawn/useDawnSystem';
import { DawnProvider, withConsciousnessTracking, withEntropyRegulation } from './DawnComponentPatterns';
import { 
  SemanticCoordinate, 
  ConsciousnessEvent, 
  SplineNeuron,
  CursorState 
} from '../../types/dawn';

// === DAWN NEURAL VISUALIZER ===

interface DawnNeuralVisualizerProps {
  cursorState: CursorState | null;
  neurons: SplineNeuron[];
  onNeuronClick: (neuron: SplineNeuron) => void;
}

const DawnNeuralVisualizer: React.FC<DawnNeuralVisualizerProps> = ({
  cursorState,
  neurons,
  onNeuronClick
}) => {
  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 60 }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      
      {/* Consciousness Field Background */}
      <mesh>
        <sphereGeometry args={[10, 32, 32]} />
        <meshBasicMaterial 
          color={0x0B1426} 
          transparent 
          opacity={0.1} 
          side={THREE.BackSide}
        />
      </mesh>

      {/* Render Neurons */}
      {neurons.map((neuron, index) => (
        <group key={neuron.id} position={[
          neuron.position.x * 2,
          neuron.position.y * 2,
          neuron.position.z * 2
        ]}>
          <Sphere
            args={[0.1 + neuron.consciousness_contribution * 0.3, 16, 16]}
            onClick={() => onNeuronClick(neuron)}
          >
            <meshStandardMaterial
              color={`hsl(${neuron.entropyLevel * 360}, 80%, ${50 + neuron.consciousness_contribution * 30}%)`}
              transparent
              opacity={0.7 + neuron.consciousness_contribution * 0.3}
            />
          </Sphere>
          
          <Text
            position={[0, 0.3, 0]}
            fontSize={0.05}
            color="white"
            anchorX="center"
          >
            {neuron.id.slice(0, 8)}
          </Text>
        </group>
      ))}

      {/* Cursor Visualization */}
      {cursorState && (
        <group position={[
          cursorState.position.x * 2,
          cursorState.position.y * 2,
          cursorState.position.z * 2
        ]}>
          <Sphere args={[0.2, 16, 16]}>
            <meshStandardMaterial
              color={cursorState.consciousness_mode === 'analytical' ? 0x00FF88 :
                     cursorState.consciousness_mode === 'creative' ? 0xFF8800 :
                     cursorState.consciousness_mode === 'intuitive' ? 0x8800FF :
                     0xFF0088}
              emissive={0x222222}
              transparent
              opacity={0.8}
            />
          </Sphere>
          
          <Text
            position={[0, 0.4, 0]}
            fontSize={0.08}
            color="white"
            anchorX="center"
          >
            CURSOR
          </Text>
        </group>
      )}

      {/* Neural Connections */}
      {neurons.map(neuron => 
        neuron.connections.map(connection => {
          const targetNeuron = neurons.find(n => n.id === connection.targetId);
          if (!targetNeuron) return null;
          
          return (
            <Line
              key={`${neuron.id}-${connection.targetId}`}
              points={[
                [neuron.position.x * 2, neuron.position.y * 2, neuron.position.z * 2],
                [targetNeuron.position.x * 2, targetNeuron.position.y * 2, targetNeuron.position.z * 2]
              ]}
              color={`hsl(${connection.semantic_resonance * 360}, 60%, 50%)`}
              lineWidth={Math.max(1, connection.weight * 3)}
              transparent
              opacity={0.4 + connection.semantic_resonance * 0.4}
            />
          );
        })
      )}

      <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
    </Canvas>
  );
};

// === CONSCIOUSNESS DASHBOARD ===

interface ConsciousnessDashboardProps {
  events: ConsciousnessEvent[];
  cursorState: CursorState | null;
  globalEntropy: number;
}

const ConsciousnessDashboard: React.FC<ConsciousnessDashboardProps> = ({
  events,
  cursorState,
  globalEntropy
}) => {
  return (
    <div className="consciousness-dashboard">
      <div className="dashboard-grid">
        {/* Cursor State */}
        <div className="dashboard-card">
          <h3>Cursor State</h3>
          {cursorState ? (
            <div className="cursor-info">
              <p><strong>Mode:</strong> {cursorState.consciousness_mode}</p>
              <p><strong>Position:</strong> ({cursorState.position.x.toFixed(2)}, {cursorState.position.y.toFixed(2)}, {cursorState.position.z.toFixed(2)})</p>
              <p><strong>Entropy:</strong> {cursorState.entropy.toFixed(3)}</p>
              <p><strong>Consciousness Level:</strong> {cursorState.position.consciousness_level.toFixed(3)}</p>
              <p><strong>Semantic Resonance:</strong> {cursorState.semantic_resonance.toFixed(3)}</p>
            </div>
          ) : (
            <p>No cursor active</p>
          )}
        </div>

        {/* Recent Events */}
        <div className="dashboard-card">
          <h3>Consciousness Events</h3>
          <div className="events-list">
            {events.slice(0, 5).map(event => (
              <div key={event.id} className="event-item">
                <div className="event-type">{event.type}</div>
                <div className="event-intensity">
                  Intensity: {event.intensity.toFixed(3)}
                </div>
                <div className="event-time">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Entropy Monitor */}
        <div className="dashboard-card">
          <h3>Entropy Monitor</h3>
          <div className="entropy-info">
            <p><strong>Global Entropy:</strong> {globalEntropy.toFixed(3)}</p>
            <div className="entropy-bar">
              <div 
                className="entropy-fill" 
                style={{ width: `${globalEntropy * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// === MAIN DAWN INTEGRATION COMPONENT ===

const DawnIntegrationDemo: React.FC = () => {
  const [selectedNeuron, setSelectedNeuron] = useState<SplineNeuron | null>(null);
  const [simulationRunning, setSimulationRunning] = useState(false);

  // Initialize Dawn system
  const dawnSystem = useDawnSystem({
    initialCursorPosition: { x: 0, y: 0, z: 0, semantic_weight: 1, ontological_depth: 0.5, consciousness_level: 0.7 },
    consciousnessMode: 'analytical',
    entropyRegulation: {
      globalSetpoint: 0.3,
      regulationMode: 'automatic'
    }
  });

  // Consciousness monitoring
  const consciousnessMonitoring = useConsciousnessMonitoring(
    dawnSystem.consciousnessStream,
    { bufferSize: 50, minIntensity: 0.1 }
  );

  // Entropy regulation
  const entropyRegulation = useEntropyRegulation(dawnSystem.entropyMonitor, {
    targetEntropy: 0.3,
    regulationMode: 'automatic',
    sensitivity: 0.05
  });

  // Create demo neurons
  const [neurons, setNeurons] = useState<SplineNeuron[]>([]);

  useEffect(() => {
    if (!dawnSystem.isInitialized) return;

    // Create demo neurons
    const demoNeurons: SplineNeuron[] = [];
    for (let i = 0; i < 10; i++) {
      const neuron = dawnSystem.createSplineNeuron(
        `neuron_${i}`,
        {
          x: (Math.random() - 0.5) * 2,
          y: (Math.random() - 0.5) * 2,
          z: (Math.random() - 0.5) * 2,
          semantic_weight: Math.random(),
          ontological_depth: Math.random(),
          consciousness_level: Math.random()
        },
        (input: number[]) => input.map(val => Math.tanh(val)) // Simple spline function
      );
      
      // Add some random connections
      if (i > 0) {
        neuron.connections.push({
          id: `conn_${i}`,
          sourceId: neuron.id,
          targetId: `neuron_${Math.floor(Math.random() * i)}`,
          weight: Math.random(),
          semantic_resonance: Math.random(),
          entropy_flow: Math.random() * 0.1,
          activation_history: []
        });
      }
      
      demoNeurons.push(neuron);
    }

    setNeurons(demoNeurons);
    dawnSystem.updateKANTopology(demoNeurons);
  }, [dawnSystem.isInitialized]);

  // Simulation loop
  useEffect(() => {
    if (!simulationRunning || !dawnSystem.cursorState) return;

    const interval = setInterval(() => {
      // Move cursor randomly
      const newPosition: SemanticCoordinate = {
        x: dawnSystem.cursorState!.position.x + (Math.random() - 0.5) * 0.1,
        y: dawnSystem.cursorState!.position.y + (Math.random() - 0.5) * 0.1,
        z: dawnSystem.cursorState!.position.z + (Math.random() - 0.5) * 0.1,
        semantic_weight: Math.max(0, Math.min(1, dawnSystem.cursorState!.position.semantic_weight + (Math.random() - 0.5) * 0.05)),
        ontological_depth: Math.max(0, Math.min(1, dawnSystem.cursorState!.position.ontological_depth + (Math.random() - 0.5) * 0.05)),
        consciousness_level: Math.max(0, Math.min(1, dawnSystem.cursorState!.position.consciousness_level + (Math.random() - 0.5) * 0.05))
      };
      
      dawnSystem.updateCursorPosition(newPosition);

      // Trigger random consciousness events
      if (Math.random() < 0.1) {
        dawnSystem.triggerConsciousnessEvent({
          type: Math.random() < 0.5 ? 'semantic_emergence' : 'attention_shift',
          intensity: Math.random(),
          semantic_payload: { event: 'simulation_step' },
          affected_neurons: neurons.slice(0, Math.floor(Math.random() * 3) + 1).map(n => n.id),
          consciousness_delta: (Math.random() - 0.5) * 0.1,
          entropy_signature: Array.from({ length: 5 }, () => Math.random())
        });
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [simulationRunning, dawnSystem, neurons]);

  const handleNeuronClick = useCallback((neuron: SplineNeuron) => {
    setSelectedNeuron(neuron);
    
    // Trigger consciousness event for neuron interaction
    dawnSystem.triggerConsciousnessEvent({
      type: 'attention_shift',
      intensity: 0.8,
      semantic_payload: { neuron: neuron.id },
      affected_neurons: [neuron.id],
      consciousness_delta: 0.1,
      entropy_signature: [0.1, 0.2, 0.3, 0.2, 0.2]
    });
  }, [dawnSystem]);

  const toggleSimulation = useCallback(() => {
    setSimulationRunning(prev => !prev);
  }, []);

  if (!dawnSystem.isInitialized) {
    return (
      <div className="dawn-loading">
        <h2>Initializing Dawn Neural Monitor...</h2>
        <p>Loading consciousness field, entropy regulators, and KAN topology...</p>
      </div>
    );
  }

  return (
    <DawnProvider>
      <div className="dawn-integration-demo">
        <header className="dawn-header">
          <h1>Dawn Neural Monitor - Phase 3 Integration</h1>
          <div className="controls">
            <button onClick={toggleSimulation} className="simulation-toggle">
              {simulationRunning ? 'Stop Simulation' : 'Start Simulation'}
            </button>
            <span className="status">
              Status: {simulationRunning ? 'Running' : 'Paused'}
            </span>
          </div>
        </header>

        <div className="dawn-content">
          <div className="visualization-container">
            <DawnNeuralVisualizer
              cursorState={dawnSystem.cursorState}
              neurons={neurons}
              onNeuronClick={handleNeuronClick}
            />
          </div>

          <div className="dashboard-container">
            <ConsciousnessDashboard
              events={consciousnessMonitoring.events}
              cursorState={dawnSystem.cursorState}
              globalEntropy={entropyRegulation.globalEntropy}
            />
          </div>
        </div>

        {selectedNeuron && (
          <motion.div 
            className="neuron-details"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
          >
            <h3>Neuron Details: {selectedNeuron.id}</h3>
            <div className="neuron-stats">
              <p><strong>Entropy Level:</strong> {selectedNeuron.entropyLevel.toFixed(3)}</p>
              <p><strong>Semantic Weight:</strong> {selectedNeuron.semanticWeight.toFixed(3)}</p>
              <p><strong>Consciousness Contribution:</strong> {selectedNeuron.consciousness_contribution.toFixed(3)}</p>
              <p><strong>Connections:</strong> {selectedNeuron.connections.length}</p>
              <p><strong>Position:</strong> ({selectedNeuron.position.x.toFixed(2)}, {selectedNeuron.position.y.toFixed(2)}, {selectedNeuron.position.z.toFixed(2)})</p>
            </div>
            <button onClick={() => setSelectedNeuron(null)}>Close</button>
          </motion.div>
        )}
      </div>

      <style>{`
        .dawn-integration-demo {
          width: 100%;
          height: 100vh;
          background: linear-gradient(135deg, #0B1426 0%, #1E293B 100%);
          color: white;
          display: flex;
          flex-direction: column;
        }

        .dawn-header {
          padding: 1rem 2rem;
          background: rgba(255, 255, 255, 0.05);
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .controls {
          display: flex;
          gap: 1rem;
          align-items: center;
        }

        .simulation-toggle {
          padding: 0.5rem 1rem;
          background: #00FF88;
          color: black;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: bold;
        }

        .simulation-toggle:hover {
          background: #00CC66;
        }

        .dawn-content {
          flex: 1;
          display: grid;
          grid-template-columns: 2fr 1fr;
          gap: 1rem;
          padding: 1rem;
        }

        .visualization-container {
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .dashboard-container {
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          padding: 1rem;
        }

        .consciousness-dashboard {
          height: 100%;
        }

        .dashboard-grid {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .dashboard-card {
          background: rgba(255, 255, 255, 0.05);
          border-radius: 6px;
          padding: 1rem;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .dashboard-card h3 {
          margin: 0 0 0.5rem 0;
          color: #00FF88;
          font-size: 0.9rem;
        }

        .cursor-info p {
          margin: 0.2rem 0;
          font-size: 0.8rem;
        }

        .events-list {
          max-height: 150px;
          overflow-y: auto;
        }

        .event-item {
          padding: 0.3rem 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          font-size: 0.7rem;
        }

        .event-type {
          font-weight: bold;
          color: #FF8800;
        }

        .entropy-bar {
          width: 100%;
          height: 20px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
          overflow: hidden;
          margin-top: 0.5rem;
        }

        .entropy-fill {
          height: 100%;
          background: linear-gradient(90deg, #00FF88 0%, #FF8800 50%, #FF0088 100%);
          transition: width 0.3s ease;
        }

        .neuron-details {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background: rgba(0, 0, 0, 0.9);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 8px;
          padding: 1.5rem;
          min-width: 300px;
          backdrop-filter: blur(10px);
        }

        .neuron-details h3 {
          margin: 0 0 1rem 0;
          color: #00FF88;
        }

        .neuron-stats p {
          margin: 0.3rem 0;
          font-size: 0.9rem;
        }

        .neuron-details button {
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background: #FF0088;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .dawn-loading {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100vh;
          background: linear-gradient(135deg, #0B1426 0%, #1E293B 100%);
          color: white;
        }
      `}</style>
    </DawnProvider>
  );
};

// Enhanced with Dawn HOCs
export default withConsciousnessTracking(
  withEntropyRegulation(DawnIntegrationDemo)
);