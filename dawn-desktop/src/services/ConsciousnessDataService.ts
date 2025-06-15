import { webSocketService } from './websocket/WebSocketService';
import WebSocketService from './websocket/WebSocketService';
import { useCosmicStore } from '../store/cosmicStore';

export interface TickData {
  timestamp: number;
  entropy: number;
  neuralActivity: number;
  systemUnity: number;
  systemLoad: number;
  mood?: string;
  scup?: number;
  performance?: {
    fps: number;
    latency: number;
    memoryUsage: number;
  };
}

export interface ConsciousnessMetrics {
  scup: number;
  entropy: number;
  neuralActivity: number;
  systemUnity: number;
  systemLoad: number;
  mood: string;
}

export class ConsciousnessDataService {
  private static instance: ConsciousnessDataService;
  private webSocket: WebSocketService;
  private isActive: boolean = false;
  private lastUpdate: number = 0;
  private buffer: TickData[] = [];
  private readonly bufferSize = 100;
  private updateCallbacks: ((metrics: ConsciousnessMetrics) => void)[] = [];

  constructor() {
    this.webSocket = webSocketService;
    this.setupEventListeners();
  }

  static getInstance(): ConsciousnessDataService {
    if (!ConsciousnessDataService.instance) {
      ConsciousnessDataService.instance = new ConsciousnessDataService();
    }
    return ConsciousnessDataService.instance;
  }

  private setupEventListeners(): void {
    // Listen for tick data
    this.webSocket.on('tick_data', (data: TickData) => {
      this.handleTickData(data);
    });

    // Listen for consciousness updates
    this.webSocket.on('consciousness_update', (data: ConsciousnessMetrics) => {
      this.handleConsciousnessUpdate(data);
    });

    // Connection status
    this.webSocket.on('connected', () => {
      console.log('🧠 Consciousness Data Service: Connected to WebSocket');
      this.requestInitialData();
    });

    this.webSocket.on('disconnected', () => {
      console.log('🧠 Consciousness Data Service: Disconnected from WebSocket');
    });
  }

  private handleTickData(data: TickData): void {
    if (!this.isActive) return;

    // Add to buffer
    this.buffer.push(data);
    if (this.buffer.length > this.bufferSize) {
      this.buffer.shift();
    }

    // Calculate consciousness metrics from tick data
    const metrics = this.calculateConsciousnessMetrics(data);
    
    // Notify callbacks
    this.notifyCallbacks(metrics);

    this.lastUpdate = Date.now();
  }

  private handleConsciousnessUpdate(data: ConsciousnessMetrics): void {
    if (!this.isActive) return;
    this.notifyCallbacks(data);
  }

  private calculateConsciousnessMetrics(tickData: TickData): ConsciousnessMetrics {
    // Base metrics from tick data
    let entropy = tickData.entropy || 0.5;
    let neuralActivity = tickData.neuralActivity || 0.5;
    let systemUnity = tickData.systemUnity || 0.5;
    let systemLoad = tickData.systemLoad || 0.3;

    // Calculate SCUP (System Consciousness Unified Percentage)
    let scup = tickData.scup;
    if (scup === undefined) {
      scup = (entropy + neuralActivity + systemUnity) / 3 * 100;
    }

    // Determine mood based on metrics
    let mood = tickData.mood || this.calculateMood(entropy, neuralActivity, systemUnity, systemLoad);

    return {
      scup: Math.max(0, Math.min(100, scup)),
      entropy: Math.max(0, Math.min(1, entropy)),
      neuralActivity: Math.max(0, Math.min(1, neuralActivity)),
      systemUnity: Math.max(0, Math.min(1, systemUnity)),
      systemLoad: Math.max(0, Math.min(1, systemLoad)),
      mood
    };
  }

  private calculateMood(entropy: number, neural: number, consciousness: number, load: number): string {
    const activity = (neural + consciousness) / 2;
    const stability = 1 - entropy;
    const stress = load;

    if (stress > 0.8) return 'critical';
    if (entropy > 0.7) return 'chaotic';
    if (activity > 0.8 && stability > 0.6) return 'euphoric';
    if (activity > 0.6 && stability > 0.7) return 'excited';
    if (stability > 0.8 && activity < 0.4) return 'serene';
    if (activity < 0.3) return 'contemplative';
    if (stress > 0.6 || entropy > 0.6) return 'anxious';
    
    return 'active';
  }

  private notifyCallbacks(metrics: ConsciousnessMetrics): void {
    this.updateCallbacks.forEach(callback => {
      try {
        callback(metrics);
      } catch (error) {
        console.error('Consciousness data callback error:', error);
      }
    });
  }

  private requestInitialData(): void {
    if (this.webSocket.isConnected) {
      this.webSocket.send('request_consciousness_data', {
        subscribe: true,
        timestamp: Date.now()
      });
    }
  }

  // Public API
  start(): void {
    if (this.isActive) return;
    
    this.isActive = true;
    console.log('🧠 Consciousness Data Service: Started');
    
    if (!this.webSocket.isConnected) {
      this.webSocket.connect();
    } else {
      this.requestInitialData();
    }
  }

  stop(): void {
    this.isActive = false;
    console.log('🧠 Consciousness Data Service: Stopped');
  }

  isRunning(): boolean {
    return this.isActive && this.webSocket.isConnected;
  }

  subscribeToUpdates(callback: (metrics: ConsciousnessMetrics) => void): () => void {
    this.updateCallbacks.push(callback);
    
    // Return unsubscribe function
    return () => {
      const index = this.updateCallbacks.indexOf(callback);
      if (index > -1) {
        this.updateCallbacks.splice(index, 1);
      }
    };
  }

  // Manual data injection for testing
  injectTestData(data: Partial<TickData>): void {
    if (!this.isActive) return;
    
    const testTick: TickData = {
      timestamp: Date.now(),
      entropy: 0.5,
      neuralActivity: 0.5,
      systemUnity: 0.5,
      systemLoad: 0.3,
      ...data
    };
    
    this.handleTickData(testTick);
  }
}

export const consciousnessDataService = ConsciousnessDataService.getInstance(); 