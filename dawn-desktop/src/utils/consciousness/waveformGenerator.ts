import { WaveformData, WavePoint, Harmonic } from '@/types/visualization.types';

interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
}

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