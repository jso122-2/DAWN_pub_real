import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { eventBus } from '../../utils/eventBus';

const components = ['A', 'B', 'C', 'D', 'E', 'F'];

export const CorrelationMatrix: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [matrix, setMatrix] = useState<number[][]>(Array.from({ length: components.length }, () => Array(components.length).fill(0)));
  const cubeRefs = useRef<THREE.Mesh[][]>([]);
  const animationRef = useRef<number>();

  useEffect(() => {
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#0a0f1b');
    const camera = new THREE.PerspectiveCamera(60, 1.45, 0.1, 100);
    camera.position.set(0, 0, 10);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x0a0f1b, 0.0);
    renderer.setSize(320, 220);
    if (mountRef.current) mountRef.current.appendChild(renderer.domElement);

    // Create grid of cubes
    cubeRefs.current = [];
    for (let i = 0; i < components.length; i++) {
      cubeRefs.current[i] = [];
      for (let j = 0; j < components.length; j++) {
        const geometry = new THREE.BoxGeometry(0.7, 0.5, 0.7);
        const material = new THREE.MeshStandardMaterial({
          color: '#ff00ea',
          emissive: '#ff00ea',
          emissiveIntensity: 0.3,
          transparent: true,
          opacity: 0.7,
        });
        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.x = -2 + j * 0.8;
        mesh.position.y = 2 - i * 0.7;
        scene.add(mesh);
        cubeRefs.current[i][j] = mesh;
      }
    }

    // Lighting
    const ambient = new THREE.AmbientLight('#ffffff', 0.7);
    scene.add(ambient);
    const point = new THREE.PointLight('#a78bfa', 1.2, 20);
    point.position.set(2, 2, 6);
    scene.add(point);

    // Animation loop
    let frame = 0;
    function animate() {
      frame++;
      for (let i = 0; i < components.length; i++) {
        for (let j = 0; j < components.length; j++) {
          const value = matrix[i][j];
          const pulse = 1 + Math.sin(frame * 0.07 + i + j) * 0.08 * (0.5 + value);
          cubeRefs.current[i][j].scale.set(pulse, pulse, pulse);
          (cubeRefs.current[i][j].material as any).emissiveIntensity = 0.3 + value * 1.2;
          (cubeRefs.current[i][j].material as any).opacity = 0.5 + value * 0.5;
        }
      }
      // Subtle rotation
      scene.rotation.y += 0.002;
      renderer.render(scene, camera);
      animationRef.current = requestAnimationFrame(animate);
    }
    animate();

    // Event subscription
    const handler = (event: any) => {
      setMatrix(m => m.map(row => row.map(val => Math.max(0, Math.min(1, val + (Math.random() - 0.5) * 0.1)))));
    };
    eventBus.on('memory:overflow', handler, 'CorrelationMatrix');
    eventBus.on('entropy:spike', handler, 'CorrelationMatrix');
    return () => {
      eventBus.off('memory:overflow', handler);
      eventBus.off('entropy:spike', handler);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      renderer.dispose();
      if (mountRef.current) mountRef.current.removeChild(renderer.domElement);
    };
  }, [matrix]);

  return <div ref={mountRef} style={{ width: 320, height: 220, background: 'rgba(10,15,27,0.8)', borderRadius: 16, boxShadow: '0 0 24px #ff00ea', margin: 8 }} />;
};

export default CorrelationMatrix; 