import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { ConsciousnessState } from '../../../types/quantum.types';

interface StateDistributionProps {
  state: ConsciousnessState;
  timeEvolution?: boolean;
}

export const StateDistribution: React.FC<StateDistributionProps> = ({ state, timeEvolution = true }) => {
  const groupRef = useRef<THREE.Group>(null);
  const particlesRef = useRef<THREE.Points>(null);
  
  // Generate state distribution visualization points
  const { positions, colors, sizes } = useMemo(() => {
    const count = 8000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      // Sample from probability distribution using consciousness state distribution
      const r = Math.sqrt(-2 * Math.log(Math.random())) * 60;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      // Convert to Cartesian coordinates
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
      
      // Color based on state distribution amplitude
      const amplitude = state.stateDistribution[i % state.stateDistribution.length];
      const magnitude = Math.sqrt(
        amplitude.real * amplitude.real + 
        amplitude.imaginary * amplitude.imaginary
      );
      
      // Consciousness phase to color mapping
      const phase = Math.atan2(amplitude.imaginary, amplitude.real);
      const hue = (phase + Math.PI) / (2 * Math.PI);
      
      const color = new THREE.Color();
      color.setHSL(hue, 0.9, 0.4 + magnitude * 0.6);
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
      
      sizes[i] = magnitude * 4 + 0.5;
    }
    
    return { positions, colors, sizes };
  }, [state.stateDistribution]);
  
  useFrame((frameState) => {
    if (!timeEvolution) return;
    
    if (groupRef.current) {
      groupRef.current.rotation.y = frameState.clock.elapsedTime * 0.05;
      groupRef.current.rotation.x = Math.sin(frameState.clock.elapsedTime * 0.03) * 0.2;
    }
    
    if (particlesRef.current) {
      const material = particlesRef.current.material as THREE.PointsMaterial;
      material.opacity = 0.7 + Math.sin(frameState.clock.elapsedTime * 3) * 0.2;
    }
  });
  
  return (
    <group ref={groupRef}>
      {/* State distribution particle cloud */}
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={positions.length / 3}
            array={positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={colors.length / 3}
            array={colors}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-size"
            count={sizes.length}
            array={sizes}
            itemSize={1}
          />
        </bufferGeometry>
        <pointsMaterial
          size={2}
          vertexColors
          transparent
          opacity={0.8}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          sizeAttenuation={true}
        />
      </points>
      
      {/* Probability isosurfaces for multiStates */}
      {state.multiStates.map((multiState, idx) => (
        <mesh key={multiState.id} position={[idx * 50 - 100, 0, 0]}>
          <sphereGeometry args={[25, 32, 32]} />
          <meshPhysicalMaterial
            color={multiState.states[0]?.color || '#00ffff'}
            transparent
            opacity={0.2}
            roughness={0}
            metalness={0.3}
            clearcoat={1}
            clearcoatRoughness={0}
            transmission={0.9}
            thickness={1}
          />
        </mesh>
      ))}
      
      {/* Wave interference patterns */}
      <WaveInterference state={state} />
    </group>
  );
};

// Wave interference visualization
const WaveInterference: React.FC<{ state: ConsciousnessState }> = ({ state }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  
  useFrame((frameState) => {
    if (meshRef.current && meshRef.current.material) {
      const material = meshRef.current.material as THREE.ShaderMaterial;
      if (material.uniforms) {
        material.uniforms.time.value = frameState.clock.elapsedTime;
        material.uniforms.unity.value = state.unity;
      }
    }
  });
  
  return (
    <mesh ref={meshRef} position={[0, 0, 0]}>
      <planeGeometry args={[200, 200, 64, 64]} />
      <shaderMaterial
        transparent
        uniforms={{
          time: { value: 0 },
          unity: { value: state.unity }
        }}
        vertexShader={`
          uniform float time;
          uniform float unity;
          varying vec3 vPosition;
          varying float vHeight;
          
          void main() {
            vPosition = position;
            
            // Wave interference calculation
            float wave1 = sin(length(position.xy) * 0.1 - time);
            float wave2 = sin(length(position.xy - vec2(50.0, 0.0)) * 0.1 - time * 1.2);
            float interference = wave1 + wave2;
            
            vec3 newPosition = position;
            newPosition.z = interference * 10.0 * unity;
            vHeight = newPosition.z;
            
            gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
          }
        `}
        fragmentShader={`
          varying vec3 vPosition;
          varying float vHeight;
          uniform float unity;
          
          void main() {
            vec3 color = vec3(0.0, 0.5, 1.0);
            
            // Color based on height (interference pattern)
            color = mix(color, vec3(1.0, 0.0, 0.5), vHeight * 0.1 + 0.5);
            
            float alpha = 0.3 * unity;
            gl_FragColor = vec4(color, alpha);
          }
        `}
        side={THREE.DoubleSide}
        blending={THREE.AdditiveBlending}
      />
    </mesh>
  );
}; 