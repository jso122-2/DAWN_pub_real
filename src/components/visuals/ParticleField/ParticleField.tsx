import React, { useRef, useMemo, useEffect, Suspense } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useConsciousnessStore } from '../../../stores/consciousnessStore';
import { useCanvasGuard, canvasMonitor } from '../../../hooks/useCanvasGuard';
import { SafeCanvas } from '../../SafeCanvas';
import './ParticleField.css';

const ParticleSystem: React.FC = () => {
  const pointsRef = useRef<THREE.Points>(null);
  const { tickData, isConnected } = useConsciousnessStore();
  const mountedRef = useRef(true);
  
  const particleConfig = useMemo(() => {
    const count = 5000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const velocities = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      
      // Position: spread across a large area
      positions[i3] = (Math.random() - 0.5) * 40;
      positions[i3 + 1] = (Math.random() - 0.5) * 40;
      positions[i3 + 2] = (Math.random() - 0.5) * 40;
      
      // Initial velocities
      velocities[i3] = (Math.random() - 0.5) * 0.02;
      velocities[i3 + 1] = (Math.random() - 0.5) * 0.02;
      velocities[i3 + 2] = (Math.random() - 0.5) * 0.02;
      
      // Colors: consciousness-inspired palette
      const hue = Math.random();
      const color = new THREE.Color();
      color.setHSL(hue, 0.8, 0.6);
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;
      
      // Random sizes
      sizes[i] = Math.random() * 2 + 0.5;
    }
    
    return { positions, colors, velocities, sizes, count };
  }, []);
  
  useEffect(() => {
    if (pointsRef.current && mountedRef.current) {
      const geometry = pointsRef.current.geometry;
      geometry.setAttribute('position', new THREE.BufferAttribute(particleConfig.positions, 3));
      geometry.setAttribute('color', new THREE.BufferAttribute(particleConfig.colors, 3));
      geometry.setAttribute('size', new THREE.BufferAttribute(particleConfig.sizes, 1));
    }
  }, [particleConfig]);

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
      const colors = pointsRef.current.geometry.attributes.color;
      
      // Consciousness-driven parameters
      const scupIntensity = tickData.scup;
      const entropyLevel = tickData.entropy;
      const heatLevel = tickData.heat;
      
      for (let i = 0; i < particleConfig.count; i++) {
        const i3 = i * 3;
        
        // Get current position
        const x = positions.getX(i);
        const y = positions.getY(i);
        const z = positions.getZ(i);
        
        // Flow motion based on consciousness
        const flowX = Math.sin(time * 0.5 + x * 0.1) * scupIntensity * 0.01;
        const flowY = Math.cos(time * 0.3 + y * 0.1) * scupIntensity * 0.01;
        const flowZ = Math.sin(time * 0.4 + z * 0.1) * scupIntensity * 0.01;
        
        // Entropy-based chaos
        const chaosX = (Math.random() - 0.5) * entropyLevel * 0.05;
        const chaosY = (Math.random() - 0.5) * entropyLevel * 0.05;
        const chaosZ = (Math.random() - 0.5) * entropyLevel * 0.05;
        
        // Heat-based expansion
        const distance = Math.sqrt(x*x + y*y + z*z);
        const expansion = heatLevel * 0.002;
        const expandX = (x / distance) * expansion;
        const expandY = (y / distance) * expansion;
        const expandZ = (z / distance) * expansion;
        
        // Combined movement
        const newX = x + flowX + chaosX + expandX + particleConfig.velocities[i3];
        const newY = y + flowY + chaosY + expandY + particleConfig.velocities[i3 + 1];
        const newZ = z + flowZ + chaosZ + expandZ + particleConfig.velocities[i3 + 2];
        
        // Boundary wrapping
        const wrapCoord = (coord: number) => {
          if (coord > 20) return -20;
          if (coord < -20) return 20;
          return coord;
        };
        
        positions.setXYZ(i, wrapCoord(newX), wrapCoord(newY), wrapCoord(newZ));
        
        // Dynamic colors based on mood
        const colorIntensity = 0.5 + Math.sin(time + i * 0.1) * 0.3;
        switch (tickData.mood) {
          case 'analytical':
            colors.setXYZ(i, 0.3 * colorIntensity, 0.7 * colorIntensity, 1.0 * colorIntensity);
            break;
          case 'confident':
            colors.setXYZ(i, 0.2 * colorIntensity, 1.0 * colorIntensity, 0.3 * colorIntensity);
            break;
          case 'focused':
            colors.setXYZ(i, 1.0 * colorIntensity, 0.6 * colorIntensity, 0.2 * colorIntensity);
            break;
          case 'creative':
            colors.setXYZ(i, 0.8 * colorIntensity, 0.3 * colorIntensity, 1.0 * colorIntensity);
            break;
          default:
            colors.setXYZ(i, 0.2 * colorIntensity, 1.0 * colorIntensity, 0.5 * colorIntensity);
        }
      }
      
      positions.needsUpdate = true;
      colors.needsUpdate = true;
    } catch (error) {
      console.warn('Particle frame update error:', error);
    }
  });
  
  return (
    <points ref={pointsRef}>
      <bufferGeometry />
      <pointsMaterial
        size={0.8}
        vertexColors
        transparent
        opacity={0.8}
        blending={THREE.AdditiveBlending}
        sizeAttenuation={false}
      />
    </points>
  );
};

// Loading fallback component
const ParticleLoadingFallback: React.FC = () => (
  <mesh>
    <boxGeometry args={[1, 1, 1]} />
    <meshBasicMaterial color="#00ff88" wireframe />
  </mesh>
);

const ParticleBackground: React.FC = () => {
  const { isConnected } = useConsciousnessStore();
  const { isReady } = useCanvasGuard();
  
  useEffect(() => {
    // Canvas monitoring is handled by useCanvasGuard hook
  }, []);

  // Don't render Canvas until component is stable
  if (!isReady) {
    return (
      <div className={`particle-background loading ${isConnected ? 'active' : 'dormant'}`}>
        <div style={{ 
          width: '100%', 
          height: '100%', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: '#00ff88'
        }}>
          <div>Loading Neural Interface...</div>
        </div>
      </div>
    );
  }
  
  return (
    <div className={`particle-background ${isConnected ? 'active' : 'dormant'}`}>
      <SafeCanvas id="particle-background">
        <Canvas
          camera={{ position: [0, 0, 15], fov: 60 }}
          style={{ background: 'transparent' }}
          gl={{ 
            antialias: true,
            alpha: true,
            preserveDrawingBuffer: false,
            powerPreference: "high-performance"
          }}
          onCreated={(state) => {
            console.log('Particle Canvas created successfully', state);
          }}
          onError={(error) => {
            console.error('Particle Canvas creation error:', error);
          }}
        >
          <Suspense fallback={<ParticleLoadingFallback />}>
            {/* Subtle lighting */}
            <ambientLight intensity={0.2} />
            
            {/* Particle system */}
            <ParticleSystem />
          </Suspense>
        </Canvas>
      </SafeCanvas>
    </div>
  );
};

export const ParticleField: React.FC<{
  className?: string;
  intensity?: number;
}> = ({ 
  className = '',
  intensity = 1
}) => {
  const { tickData, isConnected } = useConsciousnessStore();
  
  return (
    <div className={`particle-field ${className}`}>
      <ParticleBackground />
      
      {/* Overlay effects */}
      <div className="particle-overlay">
        {/* Connection glow */}
        <div className={`connection-glow ${isConnected ? 'connected' : 'disconnected'}`} />
        
        {/* Consciousness waves */}
        {tickData && (
          <div 
            className="consciousness-wave"
            style={{
              '--scup-intensity': tickData.scup,
              '--entropy-level': tickData.entropy,
              '--heat-level': tickData.heat
            } as React.CSSProperties}
          />
        )}
      </div>
      
      {/* Debug info */}
      {process.env.NODE_ENV === 'development' && tickData && (
        <div className="particle-debug">
          <div>Particles: 5000</div>
          <div>SCUP: {(tickData.scup * 100).toFixed(1)}%</div>
          <div>Entropy: {tickData.entropy.toFixed(3)}</div>
          <div>Mood: {tickData.mood}</div>
        </div>
      )}
    </div>
  );
}; 