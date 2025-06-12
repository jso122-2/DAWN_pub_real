import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { usePerformanceMonitor } from '../../hooks/usePerformanceMonitor';

interface PerformanceHUDProps {
  isVisible: boolean;
  onToggle: () => void;
}

const NODE_METRICS = [
  { key: 'fps', label: 'FPS', color: '#10b981', position: [1.5, 0, 0] },
  { key: 'cpu', label: 'CPU', color: '#f59e0b', position: [-1.5, 0, 0] },
  { key: 'gpu', label: 'GPU', color: '#8b5cf6', position: [0, 1.5, 0] },
  { key: 'memory', label: 'Memory', color: '#3b82f6', position: [0, -1.5, 0] },
  { key: 'network', label: 'Network', color: '#ec4899', position: [0, 0, 1.5] },
];

export const PerformanceHUD: React.FC<PerformanceHUDProps> = ({ isVisible, onToggle }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const { metrics } = usePerformanceMonitor();
  const animationRef = useRef<number>();
  const nodeRefs = useRef<THREE.Mesh[]>([]);
  const lineRefs = useRef<THREE.Line[]>([]);

  useEffect(() => {
    if (!isVisible) return;
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('rgba(10,15,27,0.95)');
    const camera = new THREE.PerspectiveCamera(60, 1.6, 0.1, 100);
    camera.position.set(0, 0, 7);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x0a0f1b, 0.0);
    renderer.setSize(480, 300);
    mountRef.current!.appendChild(renderer.domElement);

    // Create neural nodes
    nodeRefs.current = [];
    NODE_METRICS.forEach((metric, i) => {
      const geometry = new THREE.SphereGeometry(0.45, 32, 32);
      const material = new THREE.MeshStandardMaterial({
        color: metric.color,
        emissive: metric.color,
        emissiveIntensity: 0.3,
        transparent: true,
        opacity: 0.85,
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.set(...metric.position);
      mesh.name = metric.key;
      scene.add(mesh);
      nodeRefs.current.push(mesh);
    });

    // Connect nodes with animated glowing lines
    lineRefs.current = [];
    for (let i = 0; i < NODE_METRICS.length; i++) {
      for (let j = i + 1; j < NODE_METRICS.length; j++) {
        const mat = new THREE.LineBasicMaterial({
          color: '#00fff7',
          linewidth: 2,
          transparent: true,
          opacity: 0.5,
        });
        const points = [
          new THREE.Vector3(...NODE_METRICS[i].position),
          new THREE.Vector3(...NODE_METRICS[j].position),
        ];
        const geo = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geo, mat);
        scene.add(line);
        lineRefs.current.push(line);
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
      // Animate nodes: pulse and glow based on metric value
      nodeRefs.current.forEach((mesh, idx) => {
        const metric = NODE_METRICS[idx];
        let value = 0.5;
        if (metrics[metric.key]) {
          if (metric.key === 'fps') value = Math.min(metrics.fps[metrics.fps.length - 1] / 60, 1);
          else if (metric.key === 'memory') value = metrics.memory.used / metrics.memory.total;
          else if (metric.key === 'cpu') value = metrics.cpu / 100;
          else if (metric.key === 'gpu') value = metrics.gpu / 100;
          else if (metric.key === 'network') value = metrics.network / 100;
        }
        // Pulse effect
        const pulse = 1 + Math.sin(frame * 0.05 + idx) * 0.08 * (0.5 + value);
        mesh.scale.set(pulse, pulse, pulse);
        // Glow intensity
        (mesh.material as any).emissiveIntensity = 0.3 + value * 1.2;
        (mesh.material as any).opacity = 0.7 + value * 0.3;
      });
      // Animate lines: opacity pulses
      lineRefs.current.forEach((line, i) => {
        (line.material as any).opacity = 0.3 + 0.2 * Math.abs(Math.sin(frame * 0.02 + i));
      });
      // Rotate the whole network slowly
      scene.rotation.y += 0.003;
      renderer.render(scene, camera);
      animationRef.current = requestAnimationFrame(animate);
    }
    animate();

    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      renderer.dispose();
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, [isVisible, metrics]);

  if (!isVisible) return null;

  return (
    <div style={{ position: 'relative', width: 480, height: 300, background: 'rgba(10,15,27,0.95)', borderRadius: 24, boxShadow: '0 0 48px #00fff7', overflow: 'hidden' }}>
      <div ref={mountRef} style={{ width: 480, height: 300 }} />
      <button onClick={onToggle} style={{ position: 'absolute', top: 12, right: 16, zIndex: 2, background: '#0a0f1b', color: '#fff', border: 'none', borderRadius: 8, padding: '4px 12px', cursor: 'pointer', fontWeight: 600 }}>Close</button>
      {/* Node labels */}
      {NODE_METRICS.map((metric, idx) => (
        <div key={metric.key} style={{
          position: 'absolute',
          left: 240 + metric.position[0] * 70 - 32,
          top: 150 - metric.position[1] * 70 - 16,
          color: metric.color,
          fontWeight: 700,
          textShadow: '0 0 8px #fff, 0 0 16px ' + metric.color,
          pointerEvents: 'none',
          fontSize: 16,
        }}>{metric.label}</div>
      ))}
    </div>
  );
};

export default PerformanceHUD;