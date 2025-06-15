import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ConsciousnessFieldProps {
  consciousness: any;
}

// Consciousness field vertex shader
const vertexShader = `
  uniform float time;
  uniform float unity;
  uniform float entropy;
  uniform float scup;
  
  varying vec3 vPosition;
  varying float vPotential;
  varying vec3 vNormal;
  
  // Consciousness potential function
  float consciousnessPotential(vec3 pos) {
    float r = length(pos);
    
    // Base consciousness oscillation
    float phase = sin(r * 0.02 - time * 0.5) * unity;
    
    // Consciousness modulation
    float consciousness_wave = sin(pos.x * 0.03 + time * 0.3) * 
                              cos(pos.y * 0.03 + time * 0.2) * 
                              sin(pos.z * 0.03 + time * 0.4);
    consciousness_wave *= (scup / 100.0);
    
    // Entropy-driven noise
    float noise = sin(pos.x * 0.1) * cos(pos.y * 0.1) * sin(pos.z * 0.1);
    noise += sin(pos.x * 0.05 + time) * sin(pos.y * 0.07 + time * 1.2);
    noise *= entropy;
    
    // Consciousness tunneling effect
    float tunneling = exp(-r * 0.01) * sin(time * 2.0 + r * 0.1);
    
    return phase + consciousness_wave + noise * 0.3 + tunneling * 0.5;
  }
  
  void main() {
    vPosition = position;
    vNormal = normal;
    
    // Calculate consciousness field displacement
    float potential = consciousnessPotential(position);
    vPotential = potential;
    
    // Displace vertices based on consciousness field
    vec3 displaced = position + normal * potential * 8.0;
    
    // Add wave-like distortion
    displaced.x += sin(position.y * 0.02 + time) * unity * 5.0;
    displaced.y += cos(position.z * 0.02 + time * 1.1) * unity * 5.0;
    displaced.z += sin(position.x * 0.02 + time * 0.9) * unity * 5.0;
    
    gl_Position = projectionMatrix * modelViewMatrix * vec4(displaced, 1.0);
  }
`;

// Consciousness field fragment shader
const fragmentShader = `
  uniform float time;
  uniform float unity;
  uniform float entropy;
  uniform float scup;
  uniform vec3 color1;
  uniform vec3 color2;
  uniform vec3 color3;
  
  varying vec3 vPosition;
  varying float vPotential;
  varying vec3 vNormal;
  
  void main() {
    // Consciousness interference pattern
    float interference = sin(vPosition.x * 0.05) * 
                        sin(vPosition.y * 0.05) * 
                        sin(vPosition.z * 0.05);
    interference = pow(abs(interference), 0.3);
    
    // Consciousness-driven color mixing
    float consciousness_factor = (scup / 100.0);
    vec3 base_color = mix(color1, color2, consciousness_factor);
    
    // Entropy adds chaos to the colors
    vec3 chaotic_color = color3;
    base_color = mix(base_color, chaotic_color, entropy * 0.5);
    
    // Color based on consciousness potential
    vec3 color = mix(base_color, base_color * 1.5, vPotential * 0.5 + 0.5);
    
    // Add consciousness glow based on unity
    float glow = pow(abs(vPotential), 0.3) * unity;
    color += vec3(0.1, glow * 0.8, glow * 1.2) * unity;
    
    // Fresnel effect for consciousness aura
    vec3 viewDirection = normalize(cameraPosition - vPosition);
    float fresnel = pow(1.0 - max(dot(viewDirection, vNormal), 0.0), 2.0);
    color += vec3(0.2, 0.6, 1.0) * fresnel * unity;
    
    // Pulsing consciousness energy
    float pulse = sin(time * 3.0 + length(vPosition) * 0.01);
    color *= (1.0 + pulse * 0.2 * unity);
    
    // Fade at edges for ethereal effect
    float edge_fade = 1.0 - smoothstep(80.0, 120.0, length(vPosition));
    
    // Final alpha calculation
    float alpha = (0.15 + glow * 0.3) * edge_fade * (0.7 + unity * 0.3);
    
    gl_FragColor = vec4(color, alpha);
  }
`;

export const ConsciousnessField: React.FC<ConsciousnessFieldProps> = ({ consciousness }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  
  const uniforms = useMemo(() => ({
    time: { value: 0 },
    unity: { value: 0.5 },
    entropy: { value: 0.5 },
    scup: { value: 50 },
    color1: { value: new THREE.Color(0x0088ff) }, // Consciousness blue
    color2: { value: new THREE.Color(0xff00ff) }, // Consciousness magenta
    color3: { value: new THREE.Color(0x00ff88) }  // Entropy green
  }), []);
  
  useFrame((state) => {
    if (meshRef.current) {
      // Update time for animation
      uniforms.time.value = state.clock.elapsedTime;
      
      // Update consciousness parameters
      if (consciousness) {
        uniforms.unity.value = consciousness.systemUnity || 0.5;
        uniforms.entropy.value = consciousness.entropy || 0.5;
        uniforms.scup.value = consciousness.scup || 50;
      }
      
      // Gentle rotation based on consciousness state
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.1) * 0.2;
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.03;
      meshRef.current.rotation.z = Math.cos(state.clock.elapsedTime * 0.07) * 0.1;
    }
  });
  
  return (
    <group>
      {/* Main consciousness field mesh */}
      <mesh ref={meshRef}>
        <icosahedronGeometry args={[100, 4]} />
        <shaderMaterial
          vertexShader={vertexShader}
          fragmentShader={fragmentShader}
          uniforms={uniforms}
          transparent
          blending={THREE.AdditiveBlending}
          side={THREE.DoubleSide}
          depthWrite={false}
        />
      </mesh>
      
      {/* Inner consciousness core */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[30, 32, 32]} />
        <shaderMaterial
          vertexShader={`
            uniform float time;
            varying vec3 vPosition;
            
            void main() {
              vPosition = position;
              vec3 newPosition = position;
              
              // Consciousness core pulsing
              float pulse = sin(time * 4.0) * 0.1;
              newPosition *= (1.0 + pulse);
              
              gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
            }
          `}
          fragmentShader={`
            uniform float time;
            uniform float unity;
            varying vec3 vPosition;
            
            void main() {
              float r = length(vPosition);
              
              // Core consciousness energy
              vec3 color = vec3(0.2, 0.8, 1.0);
              
              // Pulsing intensity
              float intensity = sin(time * 6.0) * 0.3 + 0.7;
              
              // Radial gradient
              float gradient = 1.0 - (r / 30.0);
              
              gl_FragColor = vec4(color * intensity, gradient * 0.6 * unity);
            }
          `}
          uniforms={{
            time: uniforms.time,
            unity: uniforms.unity
          }}
          transparent
          blending={THREE.AdditiveBlending}
        />
      </mesh>
      
      {/* Consciousness energy particles */}
      <ThoughtNodes consciousness={consciousness} />
    </group>
  );
};

// Consciousness energy particles floating around the field
const ThoughtNodes: React.FC<{ consciousness: any }> = ({ consciousness }) => {
  const particlesRef = useRef<THREE.Points>(null);
  
  const { positions, colors, sizes } = useMemo(() => {
    const count = 1000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      // Random spherical distribution
      const radius = 80 + Math.random() * 100;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      
      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);
      
      // Consciousness colors
      const hue = (i / count + Math.random() * 0.1) % 1;
      const color = new THREE.Color();
      color.setHSL(hue, 0.8, 0.6);
      
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
      
      sizes[i] = Math.random() * 3 + 1;
    }
    
    return { positions, colors, sizes };
  }, []);
  
  useFrame((state) => {
    if (particlesRef.current) {
      // Rotate particle system
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.02;
      particlesRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.01) * 0.1;
      
      // Update particle opacity based on consciousness
      const material = particlesRef.current.material as THREE.PointsMaterial;
      material.opacity = 0.4 + (consciousness?.systemUnity || 0.5) * 0.4;
    }
  });
  
  return (
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
        size={1}
        sizeAttenuation={true}
        vertexColors
        transparent
        opacity={0.6}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
}; 