import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Box, Sphere } from '@react-three/drei';
import * as THREE from 'three';
import { PythonProcess } from './types';
import { useProcessFlowStore } from '../../store/processFlowStore';
import { ProcessUtils } from '../../services/processManager';

interface ProcessNodeProps {
  process: PythonProcess;
}

export const ProcessNode: React.FC<ProcessNodeProps> = ({ process }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const { selectedProcessId, selectProcess } = useProcessFlowStore();
  
  const isSelected = selectedProcessId === process.id;
  
  // Animate based on status
  useFrame((state) => {
    if (meshRef.current) {
      // Breathing effect for running processes
      if (process.status === 'running') {
        meshRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 2) * 0.1);
      } else if (process.status === 'error') {
        // Shake effect for errors
        meshRef.current.position.x = process.position.x + Math.sin(state.clock.elapsedTime * 10) * 2;
      } else {
        // Reset to normal position
        meshRef.current.position.x = process.position.x;
        meshRef.current.scale.setScalar(1);
      }
      
      // Rotation for selected
      if (isSelected) {
        meshRef.current.rotation.y += 0.01;
      }
      
      // Float effect
      meshRef.current.position.y = process.position.y + Math.sin(state.clock.elapsedTime + process.position.x * 0.01) * 5;
    }
  });
  
  // Status colors
  const statusColors = {
    idle: '#444444',
    running: '#00ff88',
    completed: '#0088ff',
    error: '#ff4444',
    paused: '#ffaa00'
  };
  
  const handleClick = (event: any) => {
    event.stopPropagation();
    selectProcess(process.id);
  };
  
  const handlePointerOver = (event: any) => {
    event.stopPropagation();
    setHovered(true);
    document.body.style.cursor = 'pointer';
  };
  
  const handlePointerOut = (event: any) => {
    event.stopPropagation();
    setHovered(false);
    document.body.style.cursor = 'default';
  };
  
  return (
    <group position={[process.position.x, process.position.y, process.position.z]}>
      <mesh
        ref={meshRef}
        onClick={handleClick}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
      >
        <Box args={[100, 60, 25]}>
          <meshStandardMaterial
            color={statusColors[process.status]}
            emissive={statusColors[process.status]}
            emissiveIntensity={hovered ? 0.6 : isSelected ? 0.4 : 0.2}
            transparent
            opacity={0.9}
          />
        </Box>
      </mesh>
      
      {/* Process name */}
      <Text
        position={[0, 0, 13]}
        fontSize={14}
        color="white"
        anchorX="center"
        anchorY="middle"
        maxWidth={90}
        textAlign="center"
      >
        {process.name}
      </Text>
      
      {/* Status text */}
      <Text
        position={[0, -20, 13]}
        fontSize={10}
        color="rgba(255,255,255,0.7)"
        anchorX="center"
        anchorY="middle"
      >
        {process.status.toUpperCase()}
      </Text>
      
      {/* Status indicator */}
      <Sphere args={[6]} position={[40, 25, 0]}>
        <meshStandardMaterial 
          color={statusColors[process.status]} 
          emissive={statusColors[process.status]}
          emissiveIntensity={process.status === 'running' ? 0.8 : 0.3}
        />
      </Sphere>
      
      {/* CPU Usage indicator */}
      {process.status === 'running' && (
        <Text
          position={[0, -35, 13]}
          fontSize={8}
          color="#00ff88"
          anchorX="center"
          anchorY="middle"
        >
          CPU: {process.cpuUsage.toFixed(1)}%
        </Text>
      )}
      
      {/* Input ports */}
      {process.inputs.map((input, index) => (
        <group key={input.id} position={[-50, -15 + index * 15, 0]}>
          <Sphere args={[4]}>
            <meshStandardMaterial 
              color={input.connected ? '#00ff88' : '#666666'} 
              emissive={input.connected ? '#00ff88' : '#000000'}
              emissiveIntensity={input.connected ? 0.5 : 0}
            />
          </Sphere>
          {hovered && (
            <Text
              position={[-15, 0, 0]}
              fontSize={8}
              color="white"
              anchorX="right"
              anchorY="middle"
            >
              {input.name}
            </Text>
          )}
        </group>
      ))}
      
      {/* Output ports */}
      {process.outputs.map((output, index) => (
        <group key={output.id} position={[50, -15 + index * 15, 0]}>
          <Sphere args={[4]}>
            <meshStandardMaterial 
              color={output.connected ? '#00ff88' : '#666666'}
              emissive={output.connected ? '#00ff88' : '#000000'}
              emissiveIntensity={output.connected ? 0.5 : 0}
            />
          </Sphere>
          {hovered && (
            <Text
              position={[15, 0, 0]}
              fontSize={8}
              color="white"
              anchorX="left"
              anchorY="middle"
            >
              {output.name}
            </Text>
          )}
        </group>
      ))}
      
      {/* Error indicator */}
      {process.errors.length > 0 && (
        <Sphere args={[8]} position={[0, 40, 0]}>
          <meshStandardMaterial 
            color="#ff4444" 
            emissive="#ff4444"
            emissiveIntensity={0.8}
          />
        </Sphere>
      )}
      
      {/* Category indicator */}
      <Text
        position={[0, 40, 13]}
        fontSize={8}
        color={`var(--category-${process.category})`}
        anchorX="center"
        anchorY="middle"
      >
        {process.category.toUpperCase()}
      </Text>
    </group>
  );
}; 