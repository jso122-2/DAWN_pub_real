import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

interface NeuronProps {
  neuron: any;
  selected: boolean;
  onClick: () => void;
  viewMode: string;
  activity: any;
}

export const Neuron: React.FC<NeuronProps> = ({
  neuron,
  selected,
  onClick,
  viewMode,
  activity
}) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const glowRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  
  // Calculate if neuron is firing
  const isFiring = activity.firingNeurons.has(neuron.id);
  
  // Visual properties based on neuron state
  const { geometry, material, scale } = useMemo(() => {
    const geom = getNeuronGeometry(neuron.type);
    const mat = getNeuronMaterial(neuron, isFiring, viewMode);
    const s = getNeuronScale(neuron);
    
    return { geometry: geom, material: mat, scale: s };
  }, [neuron, isFiring, viewMode]);
  
  // Animation
  useFrame((state) => {
    if (!meshRef.current) return;
    
    // Pulse when firing
    if (isFiring) {
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 10) * 0.2;
      meshRef.current.scale.setScalar(scale * pulse);
      
      // Glow effect
      if (glowRef.current) {
        glowRef.current.scale.setScalar(scale * pulse * 1.5);
        (glowRef.current.material as THREE.MeshBasicMaterial).opacity = 
          0.5 + Math.sin(state.clock.elapsedTime * 20) * 0.3;
      }
    } else {
      // Gentle breathing when idle
      const breathe = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.05;
      meshRef.current.scale.setScalar(scale * breathe);
    }
    
    // Rotation based on type
    if (neuron.type === 'interneuron') {
      meshRef.current.rotation.y += 0.005;
    }
  });
  
  return (
    <group position={neuron.position}>
      {/* Firing glow */}
      {isFiring && (
        <mesh ref={glowRef} scale={scale * 1.5}>
          <sphereGeometry args={[1, 8, 8]} />
          <meshBasicMaterial
            color="#4FC3F7"
            transparent
            opacity={0.5}
            side={THREE.BackSide}
          />
        </mesh>
      )}
      
      {/* Neuron body */}
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
        <meshPhysicalMaterial
          color={material.color}
          emissive={material.emissive}
          emissiveIntensity={isFiring ? 1 : 0.2}
          metalness={0.3}
          roughness={0.7}
          clearcoat={0.3}
          clearcoatRoughness={0.7}
          transparent
          opacity={0.8}
        />
      </mesh>
      
      {/* Dendrites (simplified) */}
      <DendriteSystem neuron={neuron} scale={scale} />
      
      {/* Selection indicator */}
      {selected && (
        <mesh scale={scale * 1.8}>
          <ringGeometry args={[1.2, 1.4, 32]} />
          <meshBasicMaterial color="#FFD700" transparent opacity={0.8} />
        </mesh>
      )}
      
      {/* Label on hover */}
      {(hovered || selected) && (
        <Text
          position={[0, scale * 2, 0]}
          fontSize={0.5}
          color="white"
          anchorX="center"
          anchorY="bottom"
        >
          {neuron.type} • {neuron.layer.name}
        </Text>
      )}
    </group>
  );
};

// Dendrite visualization
const DendriteSystem: React.FC<{ neuron: any; scale: number }> = ({ neuron, scale }) => {
  const dendriteCount = neuron.type === 'pyramidal' ? 6 : 4;
  
  return (
    <group>
      {Array.from({ length: dendriteCount }).map((_, i) => {
        const angle = (i / dendriteCount) * Math.PI * 2;
        const length = scale * 2;
        
        return (
          <mesh
            key={i}
            position={[
              Math.cos(angle) * scale * 0.5,
              0,
              Math.sin(angle) * scale * 0.5
            ]}
            rotation={[0, angle, Math.PI / 4]}
          >
            <coneGeometry args={[0.1, length, 4]} />
            <meshStandardMaterial
              color={neuron.state.health > 0.5 ? '#334155' : '#991B1B'}
              transparent
              opacity={0.3}
            />
          </mesh>
        );
      })}
    </group>
  );
};

// Helper functions
function getNeuronGeometry(type: string): React.ReactElement {
  switch (type) {
    case 'pyramidal':
      return <coneGeometry args={[1, 2, 4]} />;
    case 'interneuron':
      return <octahedronGeometry args={[1, 0]} />;
    case 'sensory':
      return <sphereGeometry args={[1, 16, 12]} />;
    case 'motor':
      return <boxGeometry args={[1.5, 1.5, 1.5]} />;
    default:
      return <sphereGeometry args={[1, 12, 8]} />;
  }
}

function getNeuronMaterial(neuron: any, isFiring: boolean, viewMode: string): any {
  let color = '#4B5563'; // Default gray
  let emissive = '#000000';
  
  if (viewMode === 'activity') {
    if (isFiring) {
      color = '#4FC3F7'; // Cyan when firing
      emissive = '#4FC3F7';
    } else {
      const activityLevel = neuron.state.firingRate / 100;
      color = new THREE.Color().setHSL(0.6 - activityLevel * 0.6, 0.7, 0.5).getStyle();
    }
  } else if (viewMode === 'structure') {
    // Color by neuron type
    const typeColors: Record<string, string> = {
      'sensory': '#10B981',
      'motor': '#F59E0B',
      'interneuron': '#8B5CF6',
      'pyramidal': '#3B82F6'
    };
    color = typeColors[neuron.type] || '#6B7280';
  }
  
  // Health affects opacity
  const healthColor = neuron.state.health < 0.5 ? '#EF4444' : color;
  
  return {
    color: healthColor,
    emissive: isFiring ? emissive : '#000000'
  };
}

function getNeuronScale(neuron: any): number {
  const baseScale = 0.5;
  const typeScale = neuron.type === 'pyramidal' ? 1.5 : 1;
  const healthScale = 0.5 + neuron.state.health * 0.5;
  
  return baseScale * typeScale * healthScale;
} 