import React from 'react';
import { Canvas } from '@react-three/fiber';

const SimpleBox: React.FC = () => {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshBasicMaterial color="orange" />
    </mesh>
  );
};

export const ThreeJSTest: React.FC = () => {
  return (
    <div style={{ width: '100%', height: '400px', background: '#000' }}>
      <Canvas>
        <ambientLight intensity={0.5} />
        <SimpleBox />
      </Canvas>
    </div>
  );
}; 