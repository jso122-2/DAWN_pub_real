import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { eventBus } from '../../utils/eventBus';

export const FrequencySpectrum: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const freqData = useRef<number[]>(new Array(32).fill(0));
  const nodeRefs = useRef<THREE.Mesh[]>([]);
  const animationRef = useRef<number>();

  useEffect(() => {
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#0a0f1b');
    const camera = new THREE.PerspectiveCamera(60, 2.5, 0.1, 100);
    camera.position.set(0, 0, 12);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x0a0f1b, 0.0);
    renderer.setSize(320, 120);
    if (mountRef.current) mountRef.current.appendChild(renderer.domElement);

    // Create pulsing nodes
    nodeRefs.current = [];
    for (let i = 0; i < 32; i++) {
      const geometry = new THREE.SphereGeometry(0.18, 24, 24);
      const material = new THREE.MeshStandardMaterial({
        color: '#00fff7',
        emissive: '#00fff7',
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.8,
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.x = -4.5 + (i / 31) * 9;
      mesh.position.y = 0;
      scene.add(mesh);
      nodeRefs.current.push(mesh);
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
      nodeRefs.current.forEach((mesh, i) => {
        const value = freqData.current[i] || 0;
        const pulse = 1 + Math.sin(frame * 0.08 + i) * 0.08 * (0.5 + value);
        mesh.scale.set(pulse, 0.7 + value * 1.2, pulse);
        (mesh.material as any).emissiveIntensity = 0.3 + value * 1.5;
        (mesh.material as any).opacity = 0.6 + value * 0.4;
      });
      renderer.render(scene, camera);
      animationRef.current = requestAnimationFrame(animate);
    }
    animate();

    // Event subscription
    const handler = (event: any) => {
      if (event.payload && typeof event.payload.value === 'number') {
        freqData.current = freqData.current.map((v, i) => i === 16 ? event.payload.value : v * 0.95);
      }
    };
    eventBus.on('neural:pulse', handler, 'FrequencySpectrum');
    eventBus.on('entropy:spike', handler, 'FrequencySpectrum');
    return () => {
      eventBus.off('neural:pulse', handler);
      eventBus.off('entropy:spike', handler);
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      renderer.dispose();
      if (mountRef.current) mountRef.current.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={mountRef} style={{ width: 320, height: 120, boxShadow: '0 0 24px #00fff7', borderRadius: 12, margin: 8, background: 'rgba(10,15,27,0.8)' }} />;
};

export default FrequencySpectrum; 