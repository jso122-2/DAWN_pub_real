import React from 'react';
import { ThreeJSTest } from '../components/test/ThreeJSTest';

const ThreeTestPage: React.FC = () => {
  return (
    <div style={{ 
      minHeight: '100vh', 
      background: '#000000', 
      color: 'white',
      padding: '20px'
    }}>
      <h1>Three.js Test Page</h1>
      <p>Testing React Three Fiber reconciler...</p>
      <ThreeJSTest />
    </div>
  );
};

export default ThreeTestPage; 