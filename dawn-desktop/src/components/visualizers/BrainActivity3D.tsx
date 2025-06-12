import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { eventBus } from '../../utils/eventBus';

const regionColors: Record<string, string> = {
  frontal: '#00fff7',
  parietal: '#a78bfa',
  occipital: '#ff00ea',
  temporal: '#fff600',
  default: '#3b82f6',
};

export const BrainActivity3D: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const activityRef = useRef<{ region: string; intensity: number }[]>([]);
  const connectionRefs = useRef<THREE.Line[]>([]);
  const particleRefs = useRef<THREE.Mesh[]>([]);

  useEffect(() => {
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color('#0a0f1b');
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
    camera.position.z = 4;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setClearColor(0x0a0f1b, 0.0);
    renderer.setSize(320, 320);
    mountRef.current!.appendChild(renderer.domElement);

    // Brain geometry (sphere clusters for demo)
    const brain = new THREE.Group();
    const regions = ['frontal', 'parietal', 'occipital', 'temporal'];
    const regionMeshes: Record<string, THREE.Mesh> = {};
    regions.forEach((region, i) => {
      const geometry = new THREE.SphereGeometry(0.7, 32, 32);
      const material = new THREE.MeshStandardMaterial({
        color: regionColors[region],
        emissive: regionColors[region],
        emissiveIntensity: 0.2,
        transparent: true,
        opacity: 0.7,
      });
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.x = Math.cos((i / 4) * Math.PI * 2) * 0.8;
      mesh.position.y = Math.sin((i / 4) * Math.PI * 2) * 0.5;
      mesh.name = region;
      brain.add(mesh);
      regionMeshes[region] = mesh;
    });
    scene.add(brain);

    // Add neural connections (animated energy streams)
    connectionRefs.current = [];
    particleRefs.current = [];
    for (let i = 0; i < regions.length; i++) {
      for (let j = i + 1; j < regions.length; j++) {
        const start = regionMeshes[regions[i]].position;
        const end = regionMeshes[regions[j]].position;
        // Glowing line
        const mat = new THREE.LineBasicMaterial({
          color: '#fff600',
          linewidth: 2,
          transparent: true,
          opacity: 0.5,
        });
        const points = [start.clone(), end.clone()];
        const geo = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geo, mat);
        brain.add(line);
        connectionRefs.current.push(line);
        // Particle (energy pulse)
        const particleGeo = new THREE.SphereGeometry(0.11, 12, 12);
        const particleMat = new THREE.MeshStandardMaterial({
          color: '#fff600',
          emissive: '#fff600',
          emissiveIntensity: 1.2,
          transparent: true,
          opacity: 0.8,
        });
        const particle = new THREE.Mesh(particleGeo, particleMat);
        brain.add(particle);
        particleRefs.current.push(particle);
      }
    }

    // Lighting
    const ambient = new THREE.AmbientLight('#ffffff', 0.5);
    scene.add(ambient);
    const point = new THREE.PointLight('#a78bfa', 1, 10);
    point.position.set(2, 2, 4);
    scene.add(point);

    // Animation
    let frame = 0;
    function animate() {
      frame++;
      brain.rotation.y += 0.01;
      // Animate activity
      activityRef.current.forEach(({ region, intensity }) => {
        const mesh = regionMeshes[region];
        if (mesh) {
          (mesh.material as any).emissiveIntensity = 0.2 + intensity * 1.2;
          (mesh.material as any).opacity = 0.7 + intensity * 0.3;
        }
      });
      // Animate connections (energy pulses)
      let particleIdx = 0;
      for (let i = 0; i < regions.length; i++) {
        for (let j = i + 1; j < regions.length; j++) {
          const start = regionMeshes[regions[i]].position;
          const end = regionMeshes[regions[j]].position;
          const t = (Math.sin(frame * 0.03 + i + j) + 1) / 2; // 0..1
          const px = start.x + (end.x - start.x) * t;
          const py = start.y + (end.y - start.y) * t;
          const pz = start.z + (end.z - start.z) * t;
          const particle = particleRefs.current[particleIdx++];
          if (particle) {
            particle.position.set(px, py, pz);
            (particle.material as any).emissiveIntensity = 1.2 + 0.8 * Math.abs(Math.sin(frame * 0.03 + i + j));
            (particle.material as any).opacity = 0.7 + 0.3 * Math.abs(Math.sin(frame * 0.03 + i + j));
          }
        }
      }
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }
    animate();

    // Event subscription
    const handler = (event: any) => {
      if (event.payload && event.payload.region) {
        activityRef.current = [{ region: event.payload.region, intensity: event.payload.intensity }];
        setTimeout(() => {
          activityRef.current = [];
        }, 600);
      }
    };
    eventBus.on('neural:pulse', handler, 'BrainActivity3D');

    return () => {
      eventBus.off('neural:pulse', handler);
      renderer.dispose();
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={mountRef} style={{ width: 320, height: 320, borderRadius: 24, boxShadow: '0 0 32px #00fff7', background: 'rgba(10,15,27,0.8)' }} />;
};

export default BrainActivity3D; 