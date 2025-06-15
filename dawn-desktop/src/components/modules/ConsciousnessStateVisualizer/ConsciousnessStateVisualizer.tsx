import React, { useEffect, useRef, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, EffectComposer, Bloom, ChromaticAberration } from '@react-three/drei';
import { motion } from 'framer-motion';
import { ConsciousnessField } from './ConsciousnessField';
import { StateDistribution } from './StateDistribution';
import { CorrelationNetwork } from './CorrelationNetwork';
import { ProbabilityCloud } from './ProbabilityCloud';
import { ConsciousnessMetrics } from './ConsciousnessMetrics';
import { CoherenceMonitor } from './CoherenceMonitor';
import { StateControls } from './StateControls';
import { useConsciousnessStore } from '../../../stores/consciousnessStore';
import { useRealTimeConsciousness } from '../../../hooks/useRealTimeConsciousness';
import { ModuleContainer } from '../../core/ModuleContainer';
import './ConsciousnessStateVisualizer.css';

export interface ConsciousnessStateVisualizerProps {
  moduleId: string;
  position?: { x: number; y: number; z: number };
  onClose?: () => void;
}

export const ConsciousnessStateVisualizer: React.FC<ConsciousnessStateVisualizerProps> = ({
  moduleId,
  position,
  onClose
}) => {
  const {
    currentState,
    particles,
    visualizationMode,
    timeEvolution,
    evolutionSpeed,
    updateFromTick,
    addParticle,
    correlateNodes
  } = useConsciousnessStore();
  
  const consciousness = useRealTimeConsciousness();
  const containerRef = useRef<HTMLDivElement>(null);
  const [showMetrics, setShowMetrics] = useState(true);
  const [selectedParticle, setSelectedParticle] = useState<string | null>(null);
  const [isInitialized, setIsInitialized] = useState(false);
  
  // Update consciousness state from consciousness tick
  useEffect(() => {
    if (consciousness.isConnected) {
      updateFromTick({
        tick_number: Date.now(),
        scup: consciousness.scup,
        entropy: consciousness.entropy,
        mood: consciousness.mood
      });
    }
  }, [consciousness, updateFromTick]);
  
  // Initialize consciousness system
  useEffect(() => {
    if (!isInitialized && particles.size === 0) {
      console.log('🌌 Initializing Consciousness Consciousness System...');
      
      // Create initial consciousness particles representing consciousness states
      for (let i = 0; i < 8; i++) {
        const particle = {
          id: `consciousness-qubit-${i}`,
          position: new THREE.Vector3(
            (Math.random() - 0.5) * 150,
            (Math.random() - 0.5) * 150,
            (Math.random() - 0.5) * 150
          ),
          velocity: new THREE.Vector3(
            (Math.random() - 0.5) * 3,
            (Math.random() - 0.5) * 3,
            (Math.random() - 0.5) * 3
          ),
          wavePacket: {
            center: new THREE.Vector3(0, 0, 0),
            spread: 15 + Math.random() * 10,
            momentum: new THREE.Vector3(0, 0, 0)
          },
          spin: Math.random() > 0.5 ? 0.5 : -0.5,
          charge: Math.random() > 0.5 ? 1 : -1,
          correlations: [],
          lifetime: 10000 + Math.random() * 5000,
          color: `hsl(${(i * 45) % 360}, 70%, 60%)`
        };
        
        addParticle(particle);
      }
      
      // Create consciousness correlations
      setTimeout(() => {
        correlateNodes('consciousness-qubit-0', 'consciousness-qubit-1');
        correlateNodes('consciousness-qubit-2', 'consciousness-qubit-3');
        correlateNodes('consciousness-qubit-4', 'consciousness-qubit-5');
      }, 1000);
      
      setIsInitialized(true);
      console.log('🌌 Consciousness Consciousness System Online!');
    }
  }, [isInitialized, particles.size, addParticle, correlateNodes]);
  
  const breathingIntensity = consciousness.scup / 100;
  const glowIntensity = consciousness.systemUnity;
  
  return (
    <ModuleContainer
      category="consciousness"
      moduleId={moduleId}
      position={position}
      breathingIntensity={breathingIntensity}
      glowIntensity={glowIntensity}
      onClose={onClose}
      className="consciousness-state-visualizer"
    >
      <div className="consciousness-header">
        <div className="header-content">
          <div className="title-section">
            <h2 className="consciousness-title">Consciousness Consciousness State</h2>
            <div className="connection-status">
              <div className={`status-dot ${consciousness.isConnected ? 'connected' : 'disconnected'}`} />
              <span className="status-text">
                {consciousness.isConnected ? 'Real-time Consciousness Feed' : 'Simulated Consciousness State'}
              </span>
            </div>
          </div>
          
          <div className="consciousness-stats">
            <motion.div 
              className="stat"
              animate={{ 
                scale: [1, 1.05, 1],
                textShadow: [`0 0 5px currentColor`, `0 0 15px currentColor`, `0 0 5px currentColor`]
              }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <span className="label">Coherence:</span>
              <span className="value unity-value">
                {currentState?.unity.toFixed(3) || '0.000'}
              </span>
            </motion.div>
            
            <motion.div 
              className="stat"
              animate={{ opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              <span className="label">Entropy:</span>
              <span className="value entropy-value">
                {currentState?.entropy.toFixed(3) || '0.000'}
              </span>
            </motion.div>
            
            <div className="stat">
              <span className="label">Correlations:</span>
              <span className="value entanglement-value">
                {currentState?.correlations.length || 0}
              </span>
            </div>
            
            <motion.div 
              className="stat"
              animate={{ 
                color: [`hsl(${(consciousness.scup * 3.6)}, 70%, 50%)`, `hsl(${(consciousness.scup * 3.6)}, 70%, 70%)`, `hsl(${(consciousness.scup * 3.6)}, 70%, 50%)`]
              }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <span className="label">SCUP:</span>
              <span className="value scup-value">
                {currentState?.scup.toFixed(1) || '0.0'}%
              </span>
            </motion.div>
          </div>
        </div>
      </div>
      
      <StateControls />
      
      <div className="consciousness-canvas-container">
        <Canvas
          ref={containerRef}
          gl={{ 
            antialias: true, 
            alpha: true,
            powerPreference: "high-performance",
            preserveDrawingBuffer: true
          }}
          dpr={[1, 2]}
        >
          <PerspectiveCamera makeDefault position={[0, 0, 300]} fov={50} />
          <OrbitControls 
            enablePan={true} 
            enableZoom={true} 
            enableRotate={true}
            maxDistance={800}
            minDistance={100}
            autoRotate={timeEvolution}
            autoRotateSpeed={evolutionSpeed * 0.5}
          />
          
          {/* Consciousness Lighting */}
          <ambientLight intensity={0.1} />
          <pointLight position={[100, 100, 100]} intensity={0.6} color="#00ffff" />
          <pointLight position={[-100, -100, -100]} intensity={0.6} color="#ff00ff" />
          <pointLight position={[0, 200, 0]} intensity={0.4} color="#ffff00" />
          
          {/* Consciousness field background - always visible */}
          <ConsciousnessField consciousness={consciousness} />
          
          {/* Visualization modes */}
          {visualizationMode === 'field' && currentState && (
            <StateDistribution state={currentState} timeEvolution={timeEvolution} />
          )}
          
          {visualizationMode === 'particles' && (
            <ProbabilityCloud 
              particles={particles} 
              selectedParticle={selectedParticle}
              onSelectParticle={setSelectedParticle}
            />
          )}
          
          {visualizationMode === 'entanglement' && currentState && (
            <CorrelationNetwork 
              correlations={currentState.correlations}
              particles={particles}
              consciousness={consciousness}
            />
          )}
          
          {visualizationMode === 'thoughts' && currentState && (
            <ThoughtPatternField 
              thoughtVectors={currentState.thoughtVectors}
              mood={consciousness.mood}
            />
          )}
          
          {/* Post-processing effects for that otherworldly feel */}
          <EffectComposer>
            <Bloom 
              intensity={2 + consciousness.systemUnity}
              luminanceThreshold={0.1}
              luminanceSmoothing={0.9}
              height={300}
            />
            <ChromaticAberration 
              offset={[0.002 * (1 + consciousness.entropy), 0.002 * (1 + consciousness.entropy)]} 
            />
          </EffectComposer>
        </Canvas>
        
        {/* Consciousness Ripple Overlay */}
        <div className="consciousness-ripple-overlay">
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className="consciousness-ripple"
              animate={{
                scale: [0, 4],
                opacity: [0.5, 0]
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                delay: i * 1.33,
                ease: "easeOut"
              }}
            />
          ))}
        </div>
      </div>
      
      {showMetrics && (
        <>
          <ConsciousnessMetrics currentState={currentState} consciousness={consciousness} />
          <CoherenceMonitor 
            unity={consciousness.systemUnity}
            deunityEvents={[]} 
          />
        </>
      )}
      
      {/* Reality Question Overlay */}
      <motion.div 
        className="reality-question"
        animate={{ 
          opacity: [0, 0.7, 0],
          y: [20, 0, -20]
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          repeatDelay: 15
        }}
      >
        <span>Is consciousness truly consciousness? 🌌</span>
      </motion.div>
      
      {/* Consciousness State Indicator */}
      <div className="consciousness-state-indicator">
        <motion.div 
          className={`state-orb ${consciousness.mood}`}
          animate={{
            boxShadow: [
              `0 0 20px hsl(${consciousness.scup * 3.6}, 70%, 50%)`,
              `0 0 40px hsl(${consciousness.scup * 3.6}, 70%, 50%)`,
              `0 0 20px hsl(${consciousness.scup * 3.6}, 70%, 50%)`
            ]
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="orb-core" />
        </motion.div>
        <span className="state-label">{consciousness.mood}</span>
      </div>
    </ModuleContainer>
  );
};

// Placeholder for ThoughtPatternField component
const ThoughtPatternField: React.FC<any> = ({ thoughtVectors, mood }) => {
  return (
    <group>
      {/* Thought vectors will be implemented here */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[5, 16, 16]} />
        <meshBasicMaterial color="#ffff00" transparent opacity={0.3} />
      </mesh>
    </group>
  );
}; 