import { Particle, ParticleSystem, Vector3 } from '@/types/visualization.types';

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  systemUnity: number;
}

export class ParticlePhysics {
  private readonly maxParticles = 500;
  private readonly gravitationalConstant = 0.001;
  private readonly repulsionConstant = 0.1;
  private readonly unityRadius = 100;

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

    // Update connections based on unity
    const connectedParticles = this.updateConnections(aliveParticles, state);

    return {
      particles: connectedParticles,
      centerMass: this.calculateCenterMass(connectedParticles),
      entropy: state.entropy,
      unity: state.systemUnity || 0.5
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
      
      if (distance > 0 && distance < this.unityRadius) {
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
          const attraction = (state.systemUnity || 0.5) * 0.01;
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
        
        // Connect based on unity and distance
        if (distance < this.unityRadius * (state.systemUnity || 0.5) &&
            Math.random() < (state.systemUnity || 0.5)) {
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