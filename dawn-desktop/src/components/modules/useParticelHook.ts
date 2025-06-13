import { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import { useAnimation } from '../../contexts/AnimationContext';

export interface Particle {
  id: string;
  x: number;
  y: number;
  size: number;
  opacity: number;
  velocity: { x: number; y: number };
  glowIntensity: number;
  color: string;
  connectionDistance: number;
}

export interface ParticleConfig {
  count?: number;
  sizeRange?: { min: number; max: number };
  opacityRange?: { min: number; max: number };
  speedRange?: { min: number; max: number };
  colors?: string[];
  connectionPortRadius?: number;
  glowFalloff?: number;
  bounds?: { width: number; height: number };
  driftPattern?: 'random' | 'orbital' | 'flow' | 'swarm';
}

interface UseParticlesOptions {
  moduleId?: string;
  config?: ParticleConfig;
  activityLevel?: number; // 0-1, affects particle speed
  connectionPorts?: Array<{ x: number; y: number }>;
  isActive?: boolean;
}

interface UseParticlesReturn {
  particles: Particle[];
  updateActivity: (level: number) => void;
  updateConnectionPorts: (ports: Array<{ x: number; y: number }>) => void;
  particlePositions: Array<{ x: number; y: number; opacity: number }>;
}

const DEFAULT_CONFIG: ParticleConfig = {
  count: 12,
  sizeRange: { min: 2, max: 6 },
  opacityRange: { min: 0.3, max: 0.8 },
  speedRange: { min: 0.1, max: 0.5 },
  colors: ['#a855f7', '#06b6d4', '#ec4899', '#22c55e', '#ffffff'],
  connectionPortRadius: 50,
  glowFalloff: 0.02,
  bounds: { width: 300, height: 200 },
  driftPattern: 'random'
};

// Noise function for organic movement
function noise2D(x: number, y: number): number {
  const X = Math.floor(x) & 255;
  const Y = Math.floor(y) & 255;
  const xf = x - Math.floor(x);
  const yf = y - Math.floor(y);
  
  const u = fade(xf);
  const v = fade(yf);
  
  const n00 = grad2D(X + Y * 256, xf, yf);
  const n01 = grad2D(X + (Y + 1) * 256, xf, yf - 1);
  const n10 = grad2D((X + 1) + Y * 256, xf - 1, yf);
  const n11 = grad2D((X + 1) + (Y + 1) * 256, xf - 1, yf - 1);
  
  const x1 = lerp(n00, n10, u);
  const x2 = lerp(n01, n11, u);
  
  return lerp(x1, x2, v);
}

function fade(t: number): number {
  return t * t * t * (t * (t * 6 - 15) + 10);
}

function lerp(a: number, b: number, t: number): number {
  return a + t * (b - a);
}

function grad2D(hash: number, x: number, y: number): number {
  const h = hash & 3;
  const u = h < 2 ? x : y;
  const v = h < 2 ? y : x;
  return ((h & 1) === 0 ? u : -u) + ((h & 2) === 0 ? v : -v);
}

export function useParticles({
  moduleId = `particles-${Date.now()}`,
  config = {},
  activityLevel = 0.5,
  connectionPorts = [],
  isActive = true
}: UseParticlesOptions = {}): UseParticlesReturn {
  const { isAnimationsEnabled } = useAnimation();
  const mergedConfig = useMemo(() => ({ ...DEFAULT_CONFIG, ...config }), [config]);
  
  const [particles, setParticles] = useState<Particle[]>([]);
  const animationFrameRef = useRef<number>();
  const timeRef = useRef(0);
  const activityRef = useRef(activityLevel);
  const portsRef = useRef(connectionPorts);
  
  // Initialize particles
  useEffect(() => {
    const newParticles: Particle[] = [];
    for (let i = 0; i < mergedConfig.count!; i++) {
      newParticles.push({
        id: `${moduleId}-p${i}`,
        x: Math.random() * mergedConfig.bounds!.width,
        y: Math.random() * mergedConfig.bounds!.height,
        size: Math.random() * (mergedConfig.sizeRange!.max - mergedConfig.sizeRange!.min) + mergedConfig.sizeRange!.min,
        opacity: Math.random() * (mergedConfig.opacityRange!.max - mergedConfig.opacityRange!.min) + mergedConfig.opacityRange!.min,
        velocity: {
          x: (Math.random() - 0.5) * mergedConfig.speedRange!.max,
          y: (Math.random() - 0.5) * mergedConfig.speedRange!.max
        },
        glowIntensity: 0,
        color: mergedConfig.colors![Math.floor(Math.random() * mergedConfig.colors!.length)],
        connectionDistance: Infinity
      });
    }
    setParticles(newParticles);
  }, [moduleId, mergedConfig]);
  
  // Animation loop
  const animate = useCallback(() => {
    if (!isAnimationsEnabled || !isActive) return;
    
    timeRef.current += 0.016; // ~60fps
    const activity = activityRef.current;
    const ports = portsRef.current;
    
    setParticles(prevParticles => {
      return prevParticles.map((particle, index) => {
        let { x, y, velocity } = particle;
        const speedMultiplier = 0.5 + activity * 1.5;
        
        // Apply drift pattern
        switch (mergedConfig.driftPattern) {
          case 'orbital': {
            const centerX = mergedConfig.bounds!.width / 2;
            const centerY = mergedConfig.bounds!.height / 2;
            const angle = Math.atan2(y - centerY, x - centerX);
            const radius = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2);
            const orbitalSpeed = speedMultiplier * 0.02;
            
            x = centerX + Math.cos(angle + orbitalSpeed) * radius;
            y = centerY + Math.sin(angle + orbitalSpeed) * radius;
            break;
          }
          
          case 'flow': {
            const flowAngle = timeRef.current * 0.1;
            velocity.x += Math.cos(flowAngle) * 0.1 * speedMultiplier;
            velocity.y += Math.sin(flowAngle) * 0.05 * speedMultiplier;
            break;
          }
          
          case 'swarm': {
            // Particles attract to each other slightly
            prevParticles.forEach((other, otherIndex) => {
              if (index === otherIndex) return;
              const dx = other.x - x;
              const dy = other.y - y;
              const dist = Math.sqrt(dx * dx + dy * dy);
              if (dist < 50 && dist > 10) {
                velocity.x += (dx / dist) * 0.01 * speedMultiplier;
                velocity.y += (dy / dist) * 0.01 * speedMultiplier;
              }
            });
            break;
          }
          
          case 'random':
          default: {
            // Perlin noise for organic movement
            const noiseScale = 0.01;
            const noiseX = noise2D(x * noiseScale, timeRef.current * 0.1);
            const noiseY = noise2D(y * noiseScale + 100, timeRef.current * 0.1);
            
            velocity.x += noiseX * 0.2 * speedMultiplier;
            velocity.y += noiseY * 0.2 * speedMultiplier;
            break;
          }
        }
        
        // Apply velocity with damping
        x += velocity.x * speedMultiplier;
        y += velocity.y * speedMultiplier;
        velocity.x *= 0.98;
        velocity.y *= 0.98;
        
        // Boundary wrapping
        if (x < 0) x = mergedConfig.bounds!.width;
        if (x > mergedConfig.bounds!.width) x = 0;
        if (y < 0) y = mergedConfig.bounds!.height;
        if (y > mergedConfig.bounds!.height) y = 0;
        
        // Calculate glow based on proximity to connection ports
        let minDistance = Infinity;
        ports.forEach(port => {
          const dist = Math.sqrt((x - port.x) ** 2 + (y - port.y) ** 2);
          minDistance = Math.min(minDistance, dist);
        });
        
        const glowIntensity = minDistance < mergedConfig.connectionPortRadius!
          ? Math.max(0, 1 - (minDistance / mergedConfig.connectionPortRadius!))
          : 0;
        
        // Update opacity based on activity and glow
        const baseOpacity = particle.opacity;
        const activityOpacity = baseOpacity * (0.5 + activity * 0.5);
        const finalOpacity = Math.min(
          mergedConfig.opacityRange!.max,
          activityOpacity + glowIntensity * 0.3
        );
        
        return {
          ...particle,
          x,
          y,
          velocity,
          glowIntensity,
          opacity: finalOpacity,
          connectionDistance: minDistance
        };
      });
    });
    
    animationFrameRef.current = requestAnimationFrame(animate);
  }, [isAnimationsEnabled, isActive, mergedConfig]);
  
  // Start animation
  useEffect(() => {
    if (isAnimationsEnabled && isActive) {
      animate();
    }
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [animate, isAnimationsEnabled, isActive]);
  
  // Update activity level
  const updateActivity = useCallback((level: number) => {
    activityRef.current = Math.max(0, Math.min(1, level));
  }, []);
  
  // Update connection ports
  const updateConnectionPorts = useCallback((ports: Array<{ x: number; y: number }>) => {
    portsRef.current = ports;
  }, []);
  
  // Get simple position array for rendering
  const particlePositions = useMemo(() => {
    return particles.map(p => ({
      x: p.x,
      y: p.y,
      opacity: p.opacity
    }));
  }, [particles]);
  
  return {
    particles,
    updateActivity,
    updateConnectionPorts,
    particlePositions
  };
}