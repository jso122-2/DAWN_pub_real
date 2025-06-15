import { useState, useEffect, useCallback, useRef } from 'react';
import { ParticleSystem } from '@/types/visualization.types';
import { particlePhysics } from '@/utils/consciousness/particlePhysics';

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  systemUnity: number;
}

// Mock consciousness hook - replace with actual implementation
function useConsciousness(): ConsciousnessState {
  const [consciousness, setConsciousness] = useState<ConsciousnessState>({
    scup: 75,
    entropy: 0.5,
    mood: 'active',
    neuralActivity: 0.6,
    systemUnity: 0.7
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setConsciousness(prev => ({
        ...prev,
        scup: Math.max(0, Math.min(100, prev.scup + (Math.random() - 0.5) * 10)),
        entropy: Math.max(0, Math.min(1, prev.entropy + (Math.random() - 0.5) * 0.2)),
        neuralActivity: Math.max(0, Math.min(1, prev.neuralActivity + (Math.random() - 0.5) * 0.3)),
        systemUnity: Math.max(0, Math.min(1, prev.systemUnity + (Math.random() - 0.5) * 0.1))
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return consciousness;
}

export function useParticleSystem() {
  const [particleSystem, setParticleSystem] = useState<ParticleSystem>({
    particles: [],
    centerMass: { x: 0, y: 0, z: 0 },
    entropy: 0.5,
    unity: 0.5
  });

  const consciousness = useConsciousness();
  const animationFrameRef = useRef<number>();
  const lastTimeRef = useRef<number>(Date.now());

  const updateSystem = useCallback(() => {
    const currentTime = Date.now();
    const deltaTime = currentTime - lastTimeRef.current;
    lastTimeRef.current = currentTime;

    setParticleSystem(prevSystem => 
      particlePhysics.updateParticleSystem(
        prevSystem,
        consciousness,
        deltaTime
      )
    );

    animationFrameRef.current = requestAnimationFrame(updateSystem);
  }, [consciousness]);

  useEffect(() => {
    animationFrameRef.current = requestAnimationFrame(updateSystem);

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [updateSystem]);

  const resetSystem = useCallback(() => {
    setParticleSystem({
      particles: [],
      centerMass: { x: 0, y: 0, z: 0 },
      entropy: consciousness.entropy,
      unity: consciousness.systemUnity
    });
  }, [consciousness]);

  return {
    particleSystem,
    resetSystem,
    particleCount: particleSystem.particles.length
  };
} 