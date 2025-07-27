import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { CatmullRomCurve3, TubeGeometry, Vector3 } from 'three';
import * as THREE from 'three';
import { DataFlow as DataFlowType, PythonProcess } from './types';
import { useProcessFlowStore } from '../../store/processFlowStore';

interface DataFlowProps {
  flow: DataFlowType;
  processes: Map<string, PythonProcess>;
}

export const DataFlow: React.FC<DataFlowProps> = ({ flow, processes }) => {
  const particlesRef = useRef<THREE.InstancedMesh>(null);
  const tubeRef = useRef<THREE.Mesh>(null);
  const { flowSpeed } = useProcessFlowStore();
  
  const source = processes.get(flow.sourceProcessId);
  const target = processes.get(flow.targetProcessId);
  
  // Create flow path
  const curve = useMemo(() => {
    if (!source || !target) return null;
    
    const start = new Vector3(source.position.x + 50, source.position.y, source.position.z);
    const end = new Vector3(target.position.x - 50, target.position.y, target.position.z);
    
    // Create a curved path
    const distance = start.distanceTo(end);
    const midPoint = new Vector3(
      (start.x + end.x) / 2,
      (start.y + end.y) / 2 + Math.max(50, distance * 0.2),
      (start.z + end.z) / 2
    );
    
    return new CatmullRomCurve3([start, midPoint, end]);
  }, [source, target]);
  
  // Create tube geometry
  const tubeGeometry = useMemo(() => {
    if (!curve) return null;
    return new TubeGeometry(curve, 64, 2, 8, false);
  }, [curve]);
  
  // Animate particles along the flow
  useFrame((state) => {
    if (!particlesRef.current || !curve) return;
    
    const time = state.clock.elapsedTime * flowSpeed;
    const particleCount = 15;
    
    for (let i = 0; i < particleCount; i++) {
      const t = ((time * 0.5 + i / particleCount) % 1);
      const position = curve.getPoint(t);
      
      // Get tangent for rotation
      const tangent = curve.getTangent(t);
      
      const matrix = new THREE.Matrix4();
      matrix.setPosition(position.x, position.y, position.z);
      
      // Add some random variation
      const variation = Math.sin(time + i * 2) * 2;
      matrix.setPosition(
        position.x + variation,
        position.y + variation * 0.5,
        position.z + variation * 0.3
      );
      
      particlesRef.current.setMatrixAt(i, matrix);
    }
    
    particlesRef.current.instanceMatrix.needsUpdate = true;
    
    // Animate tube opacity based on flow rate
    if (tubeRef.current && tubeRef.current.material) {
      const material = tubeRef.current.material as THREE.MeshBasicMaterial;
      material.opacity = 0.2 + Math.sin(time * 2) * 0.1;
    }
  });
  
  if (!curve || !tubeGeometry) return null;
  
  return (
    <group>
      {/* Flow tube */}
      <mesh ref={tubeRef} geometry={tubeGeometry}>
        <meshBasicMaterial
          color={flow.color}
          transparent
          opacity={0.3}
          wireframe={false}
        />
      </mesh>
      
      {/* Animated particles */}
      <instancedMesh ref={particlesRef} args={[undefined, undefined, 15]}>
        <sphereGeometry args={[1.5]} />
        <meshStandardMaterial 
          color={flow.color} 
          emissive={flow.color} 
          emissiveIntensity={1.2}
          transparent
          opacity={0.9}
        />
      </instancedMesh>
      
      {/* Data type indicator */}
      <mesh position={[
        curve.getPoint(0.5).x,
        curve.getPoint(0.5).y + 10,
        curve.getPoint(0.5).z
      ]}>
        <sphereGeometry args={[3]} />
        <meshStandardMaterial
          color={flow.color}
          emissive={flow.color}
          emissiveIntensity={0.5}
          transparent
          opacity={0.7}
        />
      </mesh>
    </group>
  );
}; 