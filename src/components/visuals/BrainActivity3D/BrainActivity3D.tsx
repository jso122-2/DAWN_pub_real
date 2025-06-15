import React, { useRef, useEffect, useState, Suspense } from 'react';
import { Canvas, useFrame, ThreeElements } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import { useConsciousnessStore } from '../../../stores/consciousnessStore';
import { useCanvasGuard, canvasMonitor } from '../../../hooks/useCanvasGuard';
import { SafeCanvas } from '../../SafeCanvas';
import './BrainActivity3D.css';

const BrainSphere: React.FC = () => {
  const meshRef = useRef<THREE.Mesh>(null);
  const { tickData } = useConsciousnessStore();
  const mountedRef = useRef(true);

  // Safe cleanup on unmount
  useEffect(() => {
    return () => {
      mountedRef.current = false;
      
      // Clean up Three.js resources
      if (meshRef.current) {
        if (meshRef.current.geometry) {
          meshRef.current.geometry.dispose();
        }
        if (meshRef.current.material) {
          if (Array.isArray(meshRef.current.material)) {
            meshRef.current.material.forEach(mat => mat.dispose());
          } else {
            meshRef.current.material.dispose();
          }
        }
      }
    };
  }, []);

  useFrame((state) => {
    if (!mountedRef.current || !meshRef.current || !tickData) return;
    
    try {
      // Rotate based on consciousness level
      const rotationSpeed = 0.002 + (tickData.scup * 0.008);
      meshRef.current.rotation.y += rotationSpeed;
      meshRef.current.rotation.x += rotationSpeed * 0.3;

      // Pulse effect
      const time = state.clock.elapsedTime;
      const pulseIntensity = 0.8 + Math.sin(time * (2 + tickData.scup * 3)) * 0.3 * tickData.scup;
      meshRef.current.scale.setScalar(pulseIntensity);

      // Color based on mood
      const material = meshRef.current.material as THREE.MeshPhysicalMaterial;
      if (material) {
        switch (tickData.mood) {
          case 'analytical':
            material.color.setHex(0x4FC3F7); // Blue
            break;
          case 'confident':
            material.color.setHex(0x66BB6A); // Green
            break;
          case 'focused':
            material.color.setHex(0xFFB74D); // Orange
            break;
          case 'creative':
            material.color.setHex(0xBA68C8); // Purple
            break;
          default:
            material.color.setHex(0x00ff88); // Default
        }
      }
    } catch (error) {
      console.warn('Brain sphere frame update error:', error);
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[2, 64, 64]} />
      <meshPhysicalMaterial
        color="#00ff88"
        roughness={0.1}
        metalness={0.8}
        transparent
        opacity={0.9}
        clearcoat={1}
        clearcoatRoughness={0.1}
      />
    </mesh>
  );
};

const NeuralParticles: React.FC = () => {
  const pointsRef = useRef<THREE.Points>(null);
  const { tickData } = useConsciousnessStore();
  const mountedRef = useRef(true);

  useEffect(() => {
    if (pointsRef.current && mountedRef.current) {
      const particleCount = 200;
      const positions = new Float32Array(particleCount * 3);
      const colors = new Float32Array(particleCount * 3);

      for (let i = 0; i < particleCount * 3; i += 3) {
        const radius = 3 + Math.random() * 2;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.random() * Math.PI;

        positions[i] = radius * Math.sin(phi) * Math.cos(theta);
        positions[i + 1] = radius * Math.cos(phi);
        positions[i + 2] = radius * Math.sin(phi) * Math.sin(theta);

        colors[i] = 0.2 + Math.random() * 0.8;
        colors[i + 1] = 0.8 + Math.random() * 0.2;
        colors[i + 2] = 0.4 + Math.random() * 0.6;
      }

      pointsRef.current.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      pointsRef.current.geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    }
  }, []);

  // Safe cleanup on unmount
  useEffect(() => {
    return () => {
      mountedRef.current = false;
      
      // Clean up Three.js resources
      if (pointsRef.current) {
        if (pointsRef.current.geometry) {
          pointsRef.current.geometry.dispose();
        }
        if (pointsRef.current.material) {
          if (Array.isArray(pointsRef.current.material)) {
            pointsRef.current.material.forEach(mat => mat.dispose());
          } else {
            pointsRef.current.material.dispose();
          }
        }
      }
    };
  }, []);

  useFrame((state) => {
    if (!mountedRef.current || !pointsRef.current || !tickData) return;
    
    try {
      const time = state.clock.elapsedTime;
      const positions = pointsRef.current.geometry.attributes.position;

      for (let i = 0; i < positions.count; i++) {
        const x = positions.getX(i);
        const y = positions.getY(i);
        const z = positions.getZ(i);

        // Simple orbital motion
        const angle = time * 0.1;
        const newX = x * Math.cos(angle) - z * Math.sin(angle);
        const newZ = x * Math.sin(angle) + z * Math.cos(angle);
        const newY = y + Math.sin(time + i) * 0.01 * tickData.scup;

        positions.setXYZ(i, newX, newY, newZ);
      }

      positions.needsUpdate = true;
    } catch (error) {
      console.warn('Neural particles frame update error:', error);
    }
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry />
      <pointsMaterial
        size={0.05}
        vertexColors
        transparent
        opacity={0.8}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
};

// Loading fallback component
const BrainLoadingFallback: React.FC = () => (
  <mesh>
    <sphereGeometry args={[1, 16, 16]} />
    <meshBasicMaterial color="#00ff88" wireframe />
  </mesh>
);

export const BrainActivity3D: React.FC<{
  className?: string;
  showMetrics?: boolean;
  autoRotate?: boolean;
}> = ({
  className = '',
  showMetrics = true,
  autoRotate = true
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const { tickData, isConnected } = useConsciousnessStore();
  const { isReady } = useCanvasGuard();

  useEffect(() => {
    canvasMonitor.onCanvasCreate('brain-activity-3d');
    return () => {
      canvasMonitor.onCanvasDestroy('brain-activity-3d');
    };
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => setIsLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  // Don't render Canvas until both component is stable and loaded
  if (!isReady || !isLoaded) {
    return (
      <div className={`brain-activity-3d loading ${className}`}>
        <div className="loading-brain">
          <div className="brain-pulse"></div>
          <div className="loading-text">
            {!isReady ? 'Initializing Canvas...' : 'Initializing Neural Matrix...'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`brain-activity-3d ${className} ${isConnected ? 'connected' : 'disconnected'}`}>
      <SafeCanvas id="brain-activity-3d">
        <Canvas
          camera={{ position: [0, 0, 8], fov: 45 }}
          style={{ background: 'transparent' }}
          gl={{ 
            antialias: true,
            alpha: true,
            preserveDrawingBuffer: false,
            powerPreference: "high-performance"
          }}
          onCreated={(state) => {
            console.log('Brain Canvas created successfully', state);
          }}
          onError={(error) => {
            console.error('Brain Canvas creation error:', error);
          }}
        >
          <Suspense fallback={<BrainLoadingFallback />}>
            {/* Lighting */}
            <ambientLight intensity={0.4} />
            <pointLight position={[10, 10, 10]} intensity={1} color="#00ff88" />
            <pointLight position={[-10, -10, -10]} intensity={0.5} color="#ff00aa" />
            <spotLight position={[0, 10, 0]} intensity={0.8} color="#ffffff" />

            {/* Main brain sphere */}
            <BrainSphere />

            {/* Neural particles */}
            <NeuralParticles />

            {/* Controls */}
            <OrbitControls
              enableZoom={true}
              enablePan={false}
              autoRotate={autoRotate}
              autoRotateSpeed={0.5}
              maxDistance={15}
              minDistance={5}
            />
          </Suspense>
        </Canvas>
      </SafeCanvas>

      {/* Status overlay */}
      <div className="brain-status">
        <div className={`connection-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
          <span className="status-dot"></span>
          {isConnected ? 'Neural Network Online' : 'Awaiting Connection...'}
        </div>

        {tickData && (
          <div className="live-stats">
            <div className="stat">
              <span className="label">SCUP:</span>
              <span className="value">{(tickData.scup * 100).toFixed(1)}%</span>
            </div>
            <div className="stat">
              <span className="label">Entropy:</span>
              <span className="value">{tickData.entropy.toFixed(3)}</span>
            </div>
            <div className="stat">
              <span className="label">Mood:</span>
              <span className="value">{tickData.mood}</span>
            </div>
            <div className="stat">
              <span className="label">Tick:</span>
              <span className="value">#{tickData.tick_count}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}; 