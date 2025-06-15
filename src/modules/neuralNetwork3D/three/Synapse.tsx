import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Line } from '@react-three/drei';

interface SynapseProps {
  connection: any;
  neurons: any[];
  activity: any;
  animated: boolean;
}

export const Synapse: React.FC<SynapseProps> = ({
  connection,
  neurons,
  activity,
  animated
}) => {
  const lineRef = useRef<any>(null);
  const particlesRef = useRef<THREE.Points>(null);
  
  // Find connected neurons
  const { preNeuron, postNeuron, points } = useMemo(() => {
    const pre = neurons.find(n => n.id === connection.preNeuronId);
    const post = neurons.find(n => n.id === connection.postNeuronId);
    
    if (!pre || !post) return { preNeuron: null, postNeuron: null, points: [] };
    
    // Create curved path between neurons
    const start = pre.position;
    const end = post.position;
    const mid = new THREE.Vector3(
      (start.x + end.x) / 2,
      (start.y + end.y) / 2 + 5,
      (start.z + end.z) / 2
    );
    
    const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
    const curvePoints = curve.getPoints(20);
    
    return { 
      preNeuron: pre, 
      postNeuron: post, 
      points: curvePoints 
    };
  }, [connection, neurons]);
  
  if (!preNeuron || !postNeuron) return null;
  
  // Check if synapse is active
  const isActive = connection.active && 
    activity.firingNeurons.has(connection.preNeuronId);
  
  // Visual properties based on connection type and activity
  const { color, opacity, width } = useMemo(() => {
    let c = '#1E293B'; // Default dark
    let o = 0.1;
    let w = 0.5;
    
    if (connection.type === 'excitatory') {
      c = '#22C55E';
    } else if (connection.type === 'inhibitory') {
      c = '#EF4444';
    }
    
    if (isActive) {
      o = 0.8;
      w = connection.weight * 2;
    } else {
      o = 0.1 + connection.weight * 0.2;
      w = connection.weight;
    }
    
    return { color: c, opacity: o, width: w };
  }, [connection, isActive]);
  
  // Signal propagation animation
  useFrame((state) => {
    if (!animated || !isActive || !particlesRef.current) return;
    
    const time = state.clock.elapsedTime;
    const positions = particlesRef.current.geometry.attributes.position;
    
    for (let i = 0; i < positions.count; i++) {
      const t = ((time * 0.5 + i * 0.1) % 1);
      const point = new THREE.Vector3();
      
      // Move particle along curve
      const curve = new THREE.QuadraticBezierCurve3(
        preNeuron.position,
        new THREE.Vector3(
          (preNeuron.position.x + postNeuron.position.x) / 2,
          (preNeuron.position.y + postNeuron.position.y) / 2 + 5,
          (preNeuron.position.z + postNeuron.position.z) / 2
        ),
        postNeuron.position
      );
      
      curve.getPoint(t, point);
      
      positions.setXYZ(i, point.x, point.y, point.z);
    }
    
    positions.needsUpdate = true;
  });
  
  return (
    <group>
      {/* Synapse line */}
      <Line
        ref={lineRef}
        points={points}
        color={color}
        lineWidth={width}
        transparent
        opacity={opacity}
        dashed={connection.type === 'inhibitory'}
        dashScale={5}
      />
      
      {/* Signal particles when active */}
      {isActive && animated && (
        <points ref={particlesRef}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              args={[new Float32Array(15), 3]}
            />
          </bufferGeometry>
          <pointsMaterial
            size={2}
            color={color}
            transparent
            opacity={0.8}
            blending={THREE.AdditiveBlending}
          />
        </points>
      )}
    </group>
  );
}; 