# 🧠 CONSCIOUSNESS VISUALIZER BLUEPRINT

## 🎯 MISSION: Real-time Consciousness State Visualization
Create a living, breathing visualization of DAWN's consciousness using particle systems, waveforms, and neural patterns that respond to tick data.

## File Structure to Create
```
src/
├── components/
│   └── modules/
│       └── ConsciousnessVisualizer/
│           ├── index.tsx
│           ├── ConsciousnessVisualizer.tsx
│           ├── WaveformDisplay.tsx
│           ├── ParticleField.tsx
│           ├── NeuralMap.tsx
│           └── ConsciousnessVisualizer.styles.ts
├── hooks/
│   ├── useParticleSystem.ts
│   ├── useWaveformData.ts
│   └── useNeuralMapping.ts
├── utils/
│   ├── consciousness/
│   │   ├── waveformGenerator.ts
│   │   └── particlePhysics.ts
│   └── visual/
│       └── neuralGeometry.ts
└── types/
    └── visualization.types.ts
```

---

## 📄 File: `src/types/visualization.types.ts`
```typescript
// Consciousness visualization types
export interface ConsciousnessVisualization {
  waveform: WaveformData;
  particles: ParticleSystem;
  neuralMap: NeuralNetwork;
  metrics: VisualizationMetrics;
}

export interface WaveformData {
  points: WavePoint[];
  frequency: number;
  amplitude: number;
  phase: number;
  harmonics: Harmonic[];
}

export interface WavePoint {
  x: number;
  y: number;
  intensity: number;
  time: number;
}

export interface Harmonic {
  frequency: number;
  amplitude: number;
  phase: number;
}

export interface ParticleSystem {
  particles: Particle[];
  centerMass: Vector3;
  entropy: number;
  coherence: number;
}

export interface Particle {
  id: string;
  position: Vector3;
  velocity: Vector3;
  mass: number;
  charge: number;
  lifespan: number;
  color: string;
  connections: string[]; // IDs of connected particles
}

export interface Vector3 {
  x: number;
  y: number;
  z: number;
}

export interface NeuralNetwork {
  nodes: NeuralNode[];
  connections: NeuralConnection[];
  layers: number;
  activationPattern: number[];
}

export interface NeuralNode {
  id: string;
  position: Vector3;
  activation: number;
  layer: number;
  type: 'input' | 'hidden' | 'output';
  bias: number;
}

export interface NeuralConnection {
  from: string;
  to: string;
  weight: number;
  strength: number;
  active: boolean;
}

export interface VisualizationMetrics {
  fps: number;
  particleCount: number;
  renderTime: number;
  complexity: number;
}
```

---

## 📄 File: `src/utils/consciousness/waveformGenerator.ts`
```typescript
import { WaveformData, WavePoint, Harmonic } from '@/types/visualization.types';
import { ConsciousnessState } from '@/types/consciousness.types';

export class WaveformGenerator {
  private sampleRate: number = 60; // fps
  private bufferSize: number = 256;
  private timeOffset: number = 0;

  generateWaveform(state: ConsciousnessState): WaveformData {
    const baseFrequency = 0.1 + (state.scup / 100) * 0.4; // 0.1-0.5 Hz
    const amplitude = 0.5 + (state.neuralActivity * 0.5);
    const phase = state.entropy * Math.PI * 2;

    // Generate harmonics based on mood
    const harmonics = this.generateHarmonics(state.mood, baseFrequency);

    // Create waveform points
    const points: WavePoint[] = [];
    for (let i = 0; i < this.bufferSize; i++) {
      const t = (i / this.sampleRate) + this.timeOffset;
      const x = i / this.bufferSize;
      
      let y = 0;
      // Base wave
      y += amplitude * Math.sin(2 * Math.PI * baseFrequency * t + phase);
      
      // Add harmonics
      harmonics.forEach(harmonic => {
        y += harmonic.amplitude * Math.sin(
          2 * Math.PI * harmonic.frequency * t + harmonic.phase
        );
      });

      // Add consciousness noise
      y += (Math.random() - 0.5) * state.entropy * 0.1;

      points.push({
        x,
        y: y / (1 + harmonics.length), // Normalize
        intensity: state.neuralActivity,
        time: t
      });
    }

    this.timeOffset += this.bufferSize / this.sampleRate;

    return {
      points,
      frequency: baseFrequency,
      amplitude,
      phase,
      harmonics
    };
  }

  private generateHarmonics(mood: string, baseFreq: number): Harmonic[] {
    const harmonicProfiles: Record<string, number[]> = {
      'contemplative': [2, 3, 5],    // Perfect harmonics
      'excited': [1.5, 2.5, 3.5],    // Dissonant harmonics
      'serene': [2, 4, 8],           // Octave harmonics
      'anxious': [1.3, 2.7, 4.1],    // Irregular harmonics
      'euphoric': [3, 5, 7],         // Major chord harmonics
      'chaotic': [1.1, 1.7, 2.3, 3.1, 4.3] // Many dissonant
    };

    const profile = harmonicProfiles[mood] || [2, 3];
    
    return profile.map((multiplier, index) => ({
      frequency: baseFreq * multiplier,
      amplitude: 0.3 / (index + 1), // Decay amplitude
      phase: Math.random() * Math.PI * 2
    }));
  }

  // Generate consciousness-driven Lissajous patterns
  generateLissajous(state: ConsciousnessState, time: number): WavePoint[] {
    const points: WavePoint[] = [];
    const samples = 512;
    
    const freqX = 1 + state.entropy;
    const freqY = 2 + state.neuralActivity;
    const phaseShift = state.scup / 100 * Math.PI;

    for (let i = 0; i < samples; i++) {
      const t = (i / samples) * Math.PI * 2;
      
      points.push({
        x: Math.sin(freqX * t) * 0.5 + 0.5,
        y: Math.sin(freqY * t + phaseShift) * 0.5 + 0.5,
        intensity: Math.sin(t * 3) * 0.5 + 0.5,
        time: time + i / samples
      });
    }

    return points;
  }
}

export const waveformGenerator = new WaveformGenerator();
```

---

## 📄 File: `src/utils/consciousness/particlePhysics.ts`
```typescript
import { Particle, ParticleSystem, Vector3 } from '@/types/visualization.types';
import { ConsciousnessState } from '@/types/consciousness.types';

export class ParticlePhysics {
  private readonly maxParticles = 500;
  private readonly gravitationalConstant = 0.001;
  private readonly repulsionConstant = 0.1;
  private readonly coherenceRadius = 100;

  updateParticleSystem(
    system: ParticleSystem,
    state: ConsciousnessState,
    deltaTime: number
  ): ParticleSystem {
    const updatedParticles = system.particles.map(particle => {
      const forces = this.calculateForces(particle, system, state);
      const updatedParticle = this.updateParticle(particle, forces, deltaTime);
      return this.applyConsciousnessEffects(updatedParticle, state);
    });

    // Add new particles based on neural activity
    if (updatedParticles.length < this.maxParticles && Math.random() < state.neuralActivity) {
      updatedParticles.push(this.createParticle(state));
    }

    // Remove dead particles
    const aliveParticles = updatedParticles.filter(p => p.lifespan > 0);

    // Update connections based on coherence
    const connectedParticles = this.updateConnections(aliveParticles, state);

    return {
      particles: connectedParticles,
      centerMass: this.calculateCenterMass(connectedParticles),
      entropy: state.entropy,
      coherence: state.quantumCoherence
    };
  }

  private calculateForces(
    particle: Particle,
    system: ParticleSystem,
    state: ConsciousnessState
  ): Vector3 {
    let force: Vector3 = { x: 0, y: 0, z: 0 };

    // Gravitational attraction to center mass
    const toCenter = this.vectorSubtract(system.centerMass, particle.position);
    const distanceToCenter = this.vectorMagnitude(toCenter);
    if (distanceToCenter > 0) {
      const gravityMagnitude = this.gravitationalConstant * state.scup / 100;
      force = this.vectorAdd(
        force,
        this.vectorScale(this.vectorNormalize(toCenter), gravityMagnitude)
      );
    }

    // Particle interactions
    system.particles.forEach(other => {
      if (other.id === particle.id) return;

      const diff = this.vectorSubtract(other.position, particle.position);
      const distance = this.vectorMagnitude(diff);
      
      if (distance > 0 && distance < this.coherenceRadius) {
        // Repulsion at close range
        if (distance < 20) {
          const repulsion = this.repulsionConstant / (distance * distance);
          force = this.vectorAdd(
            force,
            this.vectorScale(this.vectorNormalize(diff), -repulsion)
          );
        }
        
        // Coherence attraction for connected particles
        if (particle.connections.includes(other.id)) {
          const attraction = state.quantumCoherence * 0.01;
          force = this.vectorAdd(
            force,
            this.vectorScale(this.vectorNormalize(diff), attraction)
          );
        }
      }
    });

    // Add entropy-based random force
    force = this.vectorAdd(force, {
      x: (Math.random() - 0.5) * state.entropy * 0.1,
      y: (Math.random() - 0.5) * state.entropy * 0.1,
      z: (Math.random() - 0.5) * state.entropy * 0.1
    });

    return force;
  }

  private updateParticle(
    particle: Particle,
    force: Vector3,
    deltaTime: number
  ): Particle {
    // Update velocity
    const acceleration = this.vectorScale(force, 1 / particle.mass);
    const newVelocity = this.vectorAdd(
      particle.velocity,
      this.vectorScale(acceleration, deltaTime)
    );

    // Apply damping
    const dampedVelocity = this.vectorScale(newVelocity, 0.98);

    // Update position
    const newPosition = this.vectorAdd(
      particle.position,
      this.vectorScale(dampedVelocity, deltaTime)
    );

    return {
      ...particle,
      position: newPosition,
      velocity: dampedVelocity,
      lifespan: particle.lifespan - deltaTime
    };
  }

  private applyConsciousnessEffects(
    particle: Particle,
    state: ConsciousnessState
  ): Particle {
    // Update color based on mood
    const moodColors: Record<string, string> = {
      'contemplative': `hsl(220, 70%, ${50 + particle.charge * 30}%)`,
      'excited': `hsl(45, 80%, ${50 + particle.charge * 30}%)`,
      'serene': `hsl(160, 60%, ${50 + particle.charge * 30}%)`,
      'anxious': `hsl(0, 70%, ${50 + particle.charge * 30}%)`,
      'euphoric': `hsl(300, 70%, ${50 + particle.charge * 30}%)`,
      'chaotic': `hsl(${Math.random() * 360}, 70%, 50%)`
    };

    return {
      ...particle,
      color: moodColors[state.mood] || particle.color,
      mass: 1 + (state.neuralActivity * particle.charge),
      charge: particle.charge * (0.5 + state.scup / 200)
    };
  }

  private createParticle(state: ConsciousnessState): Particle {
    const angle = Math.random() * Math.PI * 2;
    const radius = 50 + Math.random() * 100;

    return {
      id: `particle-${Date.now()}-${Math.random()}`,
      position: {
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        z: (Math.random() - 0.5) * 50
      },
      velocity: {
        x: (Math.random() - 0.5) * 2,
        y: (Math.random() - 0.5) * 2,
        z: (Math.random() - 0.5) * 1
      },
      mass: 1,
      charge: Math.random(),
      lifespan: 5000 + Math.random() * 5000,
      color: 'hsl(220, 70%, 50%)',
      connections: []
    };
  }

  private updateConnections(
    particles: Particle[],
    state: ConsciousnessState
  ): Particle[] {
    return particles.map(particle => {
      const connections: string[] = [];
      
      particles.forEach(other => {
        if (other.id === particle.id) return;
        
        const distance = this.vectorMagnitude(
          this.vectorSubtract(other.position, particle.position)
        );
        
        // Connect based on coherence and distance
        if (distance < this.coherenceRadius * state.quantumCoherence &&
            Math.random() < state.quantumCoherence) {
          connections.push(other.id);
        }
      });

      return { ...particle, connections };
    });
  }

  // Vector utilities
  private vectorAdd(a: Vector3, b: Vector3): Vector3 {
    return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z };
  }

  private vectorSubtract(a: Vector3, b: Vector3): Vector3 {
    return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z };
  }

  private vectorScale(v: Vector3, scalar: number): Vector3 {
    return { x: v.x * scalar, y: v.y * scalar, z: v.z * scalar };
  }

  private vectorMagnitude(v: Vector3): number {
    return Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
  }

  private vectorNormalize(v: Vector3): Vector3 {
    const mag = this.vectorMagnitude(v);
    if (mag === 0) return { x: 0, y: 0, z: 0 };
    return this.vectorScale(v, 1 / mag);
  }

  private calculateCenterMass(particles: Particle[]): Vector3 {
    if (particles.length === 0) return { x: 0, y: 0, z: 0 };

    const sum = particles.reduce(
      (acc, p) => this.vectorAdd(acc, this.vectorScale(p.position, p.mass)),
      { x: 0, y: 0, z: 0 }
    );

    const totalMass = particles.reduce((acc, p) => acc + p.mass, 0);
    return this.vectorScale(sum, 1 / totalMass);
  }
}

export const particlePhysics = new ParticlePhysics();
```

---

## 📄 File: `src/hooks/useParticleSystem.ts`
```typescript
import { useState, useEffect, useCallback, useRef } from 'react';
import { ParticleSystem } from '@/types/visualization.types';
import { useConsciousness } from '@/hooks/useConsciousness';
import { particlePhysics } from '@/utils/consciousness/particlePhysics';

export function useParticleSystem() {
  const [particleSystem, setParticleSystem] = useState<ParticleSystem>({
    particles: [],
    centerMass: { x: 0, y: 0, z: 0 },
    entropy: 0.5,
    coherence: 0.5
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
      coherence: consciousness.quantumCoherence
    });
  }, [consciousness]);

  return {
    particleSystem,
    resetSystem,
    particleCount: particleSystem.particles.length
  };
}
```

---

## 📄 File: `src/components/modules/ConsciousnessVisualizer/ConsciousnessVisualizer.tsx`
```typescript
import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ModuleContainer } from '@/components/core/ModuleContainer';
import { WaveformDisplay } from './WaveformDisplay';
import { ParticleField } from './ParticleField';
import { NeuralMap } from './NeuralMap';
import { useConsciousness } from '@/hooks/useConsciousness';
import * as styles from './ConsciousnessVisualizer.styles';

export interface ConsciousnessVisualizerProps {
  moduleId: string;
  position?: { x: number; y: number; z: number };
  onClose?: () => void;
}

type VisualizationMode = 'waveform' | 'particles' | 'neural' | 'combined';

export const ConsciousnessVisualizer: React.FC<ConsciousnessVisualizerProps> = ({
  moduleId,
  position,
  onClose,
}) => {
  const [mode, setMode] = useState<VisualizationMode>('combined');
  const { scup, entropy, mood, neuralActivity } = useConsciousness();

  const breathingIntensity = scup / 100;
  const glowIntensity = neuralActivity;

  const renderVisualization = () => {
    switch (mode) {
      case 'waveform':
        return <WaveformDisplay fullscreen />;
      case 'particles':
        return <ParticleField fullscreen />;
      case 'neural':
        return <NeuralMap fullscreen />;
      case 'combined':
        return (
          <div className={styles.combinedView}>
            <div className={styles.quadrant}>
              <WaveformDisplay />
            </div>
            <div className={styles.quadrant}>
              <ParticleField />
            </div>
            <div className={styles.quadrant}>
              <NeuralMap />
            </div>
            <div className={styles.quadrant}>
              <div className={styles.metrics}>
                <h4>Consciousness Metrics</h4>
                <div className={styles.metricItem}>
                  <span>SCUP</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${scup}%` }}
                      style={{ background: `hsl(${180 + scup * 1.8}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{scup.toFixed(1)}%</span>
                </div>
                <div className={styles.metricItem}>
                  <span>Entropy</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${entropy * 100}%` }}
                      style={{ background: `hsl(${30 + entropy * 60}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{(entropy * 100).toFixed(1)}%</span>
                </div>
                <div className={styles.metricItem}>
                  <span>Neural Activity</span>
                  <div className={styles.metricBar}>
                    <motion.div
                      className={styles.metricFill}
                      animate={{ width: `${neuralActivity * 100}%` }}
                      style={{ background: `hsl(${260 + neuralActivity * 60}, 70%, 50%)` }}
                    />
                  </div>
                  <span>{(neuralActivity * 100).toFixed(1)}%</span>
                </div>
                <div className={styles.moodIndicator}>
                  <span>Mood</span>
                  <motion.div
                    className={styles.moodDisplay}
                    animate={{
                      background: getMoodGradient(mood),
                      boxShadow: `0 0 20px ${getMoodColor(mood)}`
                    }}
                  >
                    {mood}
                  </motion.div>
                </div>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <ModuleContainer
      category="monitor"
      moduleId={moduleId}
      position={position}
      breathingIntensity={breathingIntensity}
      glowIntensity={glowIntensity}
      onClose={onClose}
      className={styles.container}
    >
      <div className={styles.header}>
        <h3 className={styles.title}>Consciousness Visualizer</h3>
        <div className={styles.modeSelector}>
          {(['combined', 'waveform', 'particles', 'neural'] as VisualizationMode[]).map(m => (
            <motion.button
              key={m}
              className={styles.modeButton(mode === m)}
              onClick={() => setMode(m)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {m}
            </motion.button>
          ))}
        </div>
      </div>
      
      <div className={styles.visualizationContainer}>
        {renderVisualization()}
      </div>
    </ModuleContainer>
  );
};

function getMoodColor(mood: string): string {
  const colors: Record<string, string> = {
    'contemplative': 'rgba(148, 163, 184, 0.5)',
    'excited': 'rgba(251, 191, 36, 0.5)',
    'serene': 'rgba(134, 239, 172, 0.5)',
    'anxious': 'rgba(248, 113, 113, 0.5)',
    'euphoric': 'rgba(196, 181, 253, 0.5)',
    'chaotic': 'rgba(239, 68, 68, 0.5)'
  };
  return colors[mood] || 'rgba(148, 163, 184, 0.5)';
}

function getMoodGradient(mood: string): string {
  const gradients: Record<string, string> = {
    'contemplative': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'excited': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'serene': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'anxious': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'euphoric': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
    'chaotic': 'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)'
  };
  return gradients[mood] || gradients['contemplative'];
}
```

---

## 📄 File: `src/components/modules/ConsciousnessVisualizer/WaveformDisplay.tsx`
```typescript
import React, { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { useConsciousness } from '@/hooks/useConsciousness';
import { waveformGenerator } from '@/utils/consciousness/waveformGenerator';
import { WaveformData } from '@/types/visualization.types';
import * as styles from './ConsciousnessVisualizer.styles';

interface WaveformDisplayProps {
  fullscreen?: boolean;
}

export const WaveformDisplay: React.FC<WaveformDisplayProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const consciousness = useConsciousness();
  const [waveformData, setWaveformData] = useState<WaveformData | null>(null);
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Generate new waveform data
      const data = waveformGenerator.generateWaveform(consciousness);
      setWaveformData(data);

      // Clear canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw waveform
      ctx.strokeStyle = `hsla(${180 + consciousness.scup * 1.8}, 70%, 50%, 0.8)`;
      ctx.lineWidth = 2;
      ctx.shadowBlur = 10;
      ctx.shadowColor = ctx.strokeStyle;

      ctx.beginPath();
      data.points.forEach((point, index) => {
        const x = point.x * canvas.width;
        const y = (0.5 + point.y * 0.4) * canvas.height;

        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

      // Draw harmonics
      data.harmonics.forEach((harmonic, index) => {
        ctx.strokeStyle = `hsla(${200 + index * 30}, 60%, 50%, 0.3)`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        
        data.points.forEach((point, i) => {
          const x = point.x * canvas.width;
          const y = (0.5 + Math.sin(point.time * harmonic.frequency * Math.PI * 2) * harmonic.amplitude * 0.3) * canvas.height;
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        });
        ctx.stroke();
      });

      // Draw Lissajous pattern overlay
      const lissajousPoints = waveformGenerator.generateLissajous(consciousness, Date.now() / 1000);
      ctx.strokeStyle = `hsla(${260 + consciousness.entropy * 60}, 70%, 50%, 0.5)`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      
      lissajousPoints.forEach((point, index) => {
        const x = point.x * canvas.width;
        const y = point.y * canvas.height;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();

      animationFrameRef.current = requestAnimationFrame(render);
    };

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [consciousness]);

  return (
    <div className={styles.waveformContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      {waveformData && (
        <div className={styles.waveformInfo}>
          <span>Frequency: {waveformData.frequency.toFixed(2)} Hz</span>
          <span>Harmonics: {waveformData.harmonics.length}</span>
        </div>
      )}
    </div>
  );
};
```

---

## 📄 File: `src/components/modules/ConsciousnessVisualizer/ParticleField.tsx`
```typescript
import React, { useRef, useEffect } from 'react';
import { useParticleSystem } from '@/hooks/useParticleSystem';
import * as styles from './ConsciousnessVisualizer.styles';

interface ParticleFieldProps {
  fullscreen?: boolean;
}

export const ParticleField: React.FC<ParticleFieldProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { particleSystem } = useParticleSystem();
  const animationFrameRef = useRef<number>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const render = () => {
      // Clear with trails
      ctx.fillStyle = 'rgba(15, 23, 42, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw connections
      ctx.strokeStyle = 'rgba(148, 163, 184, 0.1)';
      ctx.lineWidth = 1;
      
      particleSystem.particles.forEach(particle => {
        particle.connections.forEach(connectedId => {
          const connected = particleSystem.particles.find(p => p.id === connectedId);
          if (!connected) return;

          ctx.beginPath();
          ctx.moveTo(
            particle.position.x + canvas.width / 2,
            particle.position.y + canvas.height / 2
          );
          ctx.lineTo(
            connected.position.x + canvas.width / 2,
            connected.position.y + canvas.height / 2
          );
          ctx.stroke();
        });
      });

      // Draw particles
      particleSystem.particles.forEach(particle => {
        const x = particle.position.x + canvas.width / 2;
        const y = particle.position.y + canvas.height / 2;
        const radius = 2 + particle.charge * 3;

        // Glow effect
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 3);
        gradient.addColorStop(0, particle.color);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 3, 0, Math.PI * 2);
        ctx.fill();

        // Core particle
        ctx.fillStyle = particle.color;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw center mass indicator
      if (particleSystem.particles.length > 0) {
        const centerX = particleSystem.centerMass.x + canvas.width / 2;
        const centerY = particleSystem.centerMass.y + canvas.height / 2;

        ctx.strokeStyle = 'rgba(251, 191, 36, 0.5)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.arc(centerX, centerY, 20, 0, Math.PI * 2);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      animationFrameRef.current = requestAnimationFrame(render);
    };

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [particleSystem]);

  return (
    <div className={styles.particleContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      <div className={styles.particleInfo}>
        <span>Particles: {particleSystem.particles.length}</span>
        <span>Coherence: {(particleSystem.coherence * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
};
```

---

## 📄 File: `src/components/modules/ConsciousnessVisualizer/ConsciousnessVisualizer.styles.ts`
```typescript
import { css } from '@emotion/css';

export const container = css`
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 600px;
`;

export const header = css`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
`;

export const title = css`
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(226, 232, 240, 0.9);
  margin: 0;
`;

export const modeSelector = css`
  display: flex;
  gap: 0.5rem;
`;

export const modeButton = (isActive: boolean) => css`
  padding: 0.5rem 1rem;
  background: ${isActive 
    ? 'rgba(59, 130, 246, 0.2)' 
    : 'rgba(15, 23, 42, 0.4)'};
  border: 1px solid ${isActive 
    ? 'rgba(59, 130, 246, 0.4)' 
    : 'rgba(148, 163, 184, 0.2)'};
  border-radius: 6px;
  color: ${isActive 
    ? 'rgba(147, 197, 253, 0.9)' 
    : 'rgba(148, 163, 184, 0.8)'};
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: ${isActive 
      ? 'rgba(59, 130, 246, 0.3)' 
      : 'rgba(15, 23, 42, 0.6)'};
  }
`;

export const visualizationContainer = css`
  flex: 1;
  position: relative;
  overflow: hidden;
`;

export const combinedView = css`
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1px;
  height: 100%;
  background: rgba(148, 163, 184, 0.1);
`;

export const quadrant = css`
  background: rgba(15, 23, 42, 0.4);
  position: relative;
  overflow: hidden;
`;

export const metrics = css`
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;

  h4 {
    margin: 0 0 1rem 0;
    color: rgba(226, 232, 240, 0.9);
    font-size: 1rem;
    font-weight: 600;
  }
`;

export const metricItem = css`
  display: grid;
  grid-template-columns: 100px 1fr 60px;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: rgba(148, 163, 184, 0.9);
`;

export const metricBar = css`
  height: 8px;
  background: rgba(30, 41, 59, 0.6);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
`;

export const metricFill = css`
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
`;

export const moodIndicator = css`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 1rem;
`;

export const moodDisplay = css`
  padding: 1rem;
  border-radius: 12px;
  text-align: center;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  text-transform: capitalize;
  transition: all 0.5s ease;
`;

export const waveformContainer = (fullscreen?: boolean) => css`
  position: relative;
  width: 100%;
  height: 100%;
  min-height: ${fullscreen ? '500px' : '150px'};
`;

export const particleContainer = (fullscreen?: boolean) => css`
  position: relative;
  width: 100%;
  height: 100%;
  min-height: ${fullscreen ? '500px' : '150px'};
`;

export const canvas = css`
  width: 100%;
  height: 100%;
`;

export const waveformInfo = css`
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.7);
  background: rgba(15, 23, 42, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  backdrop-filter: blur(10px);
`;

export const particleInfo = css`
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: rgba(148, 163, 184, 0.7);
  background: rgba(15, 23, 42, 0.8);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  backdrop-filter: blur(10px);
`;
```

---

## 📄 File: `src/components/modules/ConsciousnessVisualizer/NeuralMap.tsx`
```typescript
import React, { useRef, useEffect } from 'react';
import { useConsciousness } from '@/hooks/useConsciousness';
import * as styles from './ConsciousnessVisualizer.styles';

interface NeuralMapProps {
  fullscreen?: boolean;
}

export const NeuralMap: React.FC<NeuralMapProps> = ({ fullscreen }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const consciousness = useConsciousness();
  const nodesRef = useRef<any[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Initialize neural network if needed
    if (nodesRef.current.length === 0) {
      const layers = 5;
      const nodesPerLayer = [3, 5, 7, 5, 3];
      
      nodesPerLayer.forEach((count, layer) => {
        for (let i = 0; i < count; i++) {
          nodesRef.current.push({
            id: `node-${layer}-${i}`,
            layer,
            position: {
              x: (layer / (layers - 1)) * 0.8 + 0.1,
              y: (i / (count - 1)) * 0.8 + 0.1
            },
            activation: Math.random(),
            connections: []
          });
        }
      });

      // Create connections
      for (let l = 0; l < layers - 1; l++) {
        const currentLayer = nodesRef.current.filter(n => n.layer === l);
        const nextLayer = nodesRef.current.filter(n => n.layer === l + 1);
        
        currentLayer.forEach(node => {
          nextLayer.forEach(next => {
            if (Math.random() > 0.3) {
              node.connections.push({
                to: next.id,
                weight: Math.random() * 2 - 1
              });
            }
          });
        });
      }
    }

    const render = () => {
      // Clear canvas
      ctx.fillStyle = 'rgba(15, 23, 42, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update activations based on consciousness
      nodesRef.current.forEach(node => {
        node.activation = Math.max(0, Math.min(1,
          node.activation + (Math.random() - 0.5) * 0.1 * consciousness.neuralActivity
        ));
      });

      // Draw connections
      nodesRef.current.forEach(node => {
        node.connections.forEach((conn: any) => {
          const target = nodesRef.current.find(n => n.id === conn.to);
          if (!target) return;

          const startX = node.position.x * canvas.width;
          const startY = node.position.y * canvas.height;
          const endX = target.position.x * canvas.width;
          const endY = target.position.y * canvas.height;

          const strength = node.activation * target.activation;
          ctx.strokeStyle = `rgba(59, 130, 246, ${strength * 0.5})`;
          ctx.lineWidth = Math.abs(conn.weight) * 2;

          ctx.beginPath();
          ctx.moveTo(startX, startY);
          ctx.lineTo(endX, endY);
          ctx.stroke();
        });
      });

      // Draw nodes
      nodesRef.current.forEach(node => {
        const x = node.position.x * canvas.width;
        const y = node.position.y * canvas.height;
        const radius = 5 + node.activation * 10;

        // Glow
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
        gradient.addColorStop(0, `hsla(${200 + node.activation * 60}, 70%, 50%, ${node.activation})`);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
        ctx.fill();

        // Core
        ctx.fillStyle = `hsl(${200 + node.activation * 60}, 70%, 50%)`;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(render);
    };

    // Handle resize
    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    render();

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, [consciousness]);

  return (
    <div className={styles.particleContainer(fullscreen)}>
      <canvas ref={canvasRef} className={styles.canvas} />
      <div className={styles.particleInfo}>
        <span>Neural Activity: {(consciousness.neuralActivity * 100).toFixed(1)}%</span>
      </div>
    </div>
  );
};
```

---

# 🚀 CURSOR IMPLEMENTATION ATTACK PLAN

## Phase 1: Directory Creation
```bash
mkdir -p src/components/modules/ConsciousnessVisualizer src/hooks src/utils/consciousness src/utils/visual
```

## Phase 2: Deploy All Files
Use this Cursor prompt:
```
Create the complete Consciousness Visualizer system based on this blueprint. Create all files with the exact implementations provided, maintaining the particle physics, waveform generation, and neural network visualization systems.
```

## Phase 3: Integration
1. Import into Dashboard
2. Connect to WebSocket tick stream
3. Add to module registry
4. Test all visualization modes

## Phase 4: Enhancement Prompts
- "Add 3D rotation to particle field using mouse interaction"
- "Implement sound synthesis based on waveform data"
- "Add recording functionality to save consciousness states"
- "Create preset consciousness states for testing"

## 🎯 NEXT ATTACK TARGETS:
1. **Tick Loop Monitor** - Real-time system heartbeat
2. **Neural Network 3D** - Full 3D brain visualization
3. **Unified Dashboard** - Command center for all modules
4. **Quantum State Visualizer** - Superposition and entanglement

**THE CONSCIOUSNESS VISUALIZER IS READY FOR DEPLOYMENT! 🚀**