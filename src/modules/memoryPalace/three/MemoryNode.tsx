import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Text } from '@react-three/drei';
import { Memory } from '../types/memory.types';

interface MemoryNodeProps {
  memory: Memory;
  selected: boolean;
  onClick: () => void;
  viewMode: 'spatial' | 'temporal' | 'emotional';
}

export const MemoryNode: React.FC<MemoryNodeProps> = ({
  memory,
  selected,
  onClick,
  viewMode
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  // Calculate visual properties
  const { geometry, material, scale, glowMaterial } = useMemo(() => {
    const geom = getMemoryGeometry(memory);
    const mat = getMemoryMaterial(memory, viewMode);
    const s = getMemoryScale(memory);
    const glow = getGlowMaterial(memory);
    
    return { geometry: geom, material: mat, scale: s, glowMaterial: glow };
  }, [memory, viewMode]);
  
  // Animation
  useFrame((state) => {
    if (!meshRef.current) return;
    
    // Breathing effect
    const breathingScale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05 * memory.strength;
    meshRef.current.scale.setScalar(scale * breathingScale);
    
    // Rotation based on type
    if (memory.type === 'insight' || memory.type === 'revelation') {
      meshRef.current.rotation.y += 0.01;
    }
    
    // Pulse when selected
    if (selected && glowRef.current) {
      glowRef.current.scale.setScalar(scale * breathingScale * 1.3);
      (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 
        0.3 + Math.sin(state.clock.elapsedTime * 4) * 0.2;
    }
    
    // Float effect
    const originalY = memory.spatialPosition.position.y;
    meshRef.current.position.y = originalY + 
      Math.sin(state.clock.elapsedTime + memory.timestamp * 0.001) * 0.5;
  });
  
  // Position based on view mode
  const position = useMemo(() => {
    switch (viewMode) {
      case 'temporal':
        return new THREE.Vector3(
          (memory.tickNumber % 100) * 2 - 100,
          memory.temporalLayer * 20,
          Math.floor(memory.tickNumber / 100) * 10
        );
      case 'emotional':
        return new THREE.Vector3(
          memory.emotionalValence.valence * 100,
          memory.emotionalValence.arousal * 100,
          memory.emotionalValence.dominance * 100
        );
      default:
        return memory.spatialPosition.position;
    }
  }, [memory, viewMode]);
  
  return (
    <group position={position}>
      {/* Glow effect */}
      {(selected || hovered) && (
        <mesh ref={glowRef} scale={scale * 1.2}>
          <sphereGeometry args={[1, 16, 16]} />
          <meshBasicMaterial
            color={memory.content.sensory.color}
            transparent
            opacity={0.3}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Main memory geometry */}
      <mesh
        ref={meshRef}
        scale={scale}
        onClick={(e) => {
          e.stopPropagation();
          onClick();
        }}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        {geometry}
        {material}
      </mesh>
      
      {/* Label */}
      {(selected || hovered) && (
        <Text
          position={[0, scale + 2, 0]}
          fontSize={1}
          color="white"
          anchorX="center"
          anchorY="bottom"
        >
          {memory.content.primary.substring(0, 30)}...
        </Text>
      )}
      
      {/* Crystallized indicator */}
      {memory.metadata.crystallized && (
        <mesh position={[0, scale + 1, 0]} scale={0.5}>
          <octahedronGeometry args={[1, 0]} />
          <meshStandardMaterial
            color="#FFD700"
            emissive="#FFD700"
            emissiveIntensity={0.5}
            metalness={1}
            roughness={0}
          />
        </mesh>
      )}
    </group>
  );
};

// Helper functions
function getMemoryGeometry(memory: Memory): JSX.Element {
  switch (memory.type) {
    case 'milestone':
      return <octahedronGeometry args={[1, 0]} />;
    case 'pattern':
      return <tetrahedronGeometry args={[1, 0]} />;
    case 'insight':
    case 'revelation':
      return <icosahedronGeometry args={[1, 0]} />;
    case 'dream':
      return <sphereGeometry args={[1, 8, 6]} />;
    default:
      return <boxGeometry args={[1, 1, 1]} />;
  }
}

function getMemoryMaterial(memory: Memory, viewMode: string): JSX.Element {
  const color = new THREE.Color(memory.content.sensory.color);
  
  if (memory.metadata.crystallized) {
    return (
      <meshPhysicalMaterial
        color={color}
        metalness={0.9}
        roughness={0.1}
        clearcoat={1}
        clearcoatRoughness={0}
        reflectivity={1}
        transparent={true}
        opacity={0.9}
        side={THREE.DoubleSide}
      />
    );
  }
  
  return (
    <meshStandardMaterial
      color={color}
      emissive={color}
      emissiveIntensity={memory.strength * 0.3}
      metalness={memory.consolidation * 0.5}
      roughness={1 - memory.consolidation * 0.5}
      transparent={true}
      opacity={0.3 + memory.strength * 0.7}
      side={THREE.DoubleSide}
    />
  );
}

function getMemoryScale(memory: Memory): number {
  const baseScale = 1;
  const importanceScale = memory.metadata.importance * 2;
  const strengthScale = memory.strength;
  const consolidationScale = memory.consolidation * 0.5;
  
  return baseScale + importanceScale + strengthScale + consolidationScale;
}

function getGlowMaterial(memory: Memory): JSX.Element {
  const color = new THREE.Color(memory.content.sensory.color);
  
  return (
    <meshBasicMaterial
      color={color}
      transparent={true}
      opacity={0.3}
      side={THREE.BackSide}
    />
  );
} 