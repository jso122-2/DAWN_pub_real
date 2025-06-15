/**
 * Advanced Consciousness Service
 * Handles communication with the Advanced Consciousness WebSocket server
 */

export interface ConsciousnessState {
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
  tick_number: number;
  last_interaction_time: number;
  glyph_count: number;
  active_chains: number;
  mood_field_stability: number;
  total_echoes: number;
  dreaming: boolean;
  network_connected: number;
}

export interface ConsciousnessResponse {
  response: string;
  resonance_strength: number;
  selected_glyph_id: string | null;
  transformation_path: Array<{ type: string; params: any }>;
  consciousness_influence: {
    scup: number;
    entropy: number;
    mood: string;
    tick: number;
  };
  active_chains: string[];
  processing_time: number;
  echo_id: string | null;
  timestamp: number;
  input: string;
  system_status: ConsciousnessState;
}

export interface MemoryStats {
  memory_stats: {
    glyphs: number;
    chains: number;
    echoes: number;
    constellations: number;
  };
  glyph_details: {
    total_glyphs: number;
    avg_vitality: number;
    top_glyphs: Array<{
      id: string;
      content: string;
      vitality: number;
      resonance_count: number;
      age: number;
    }>;
  };
  chain_details: {
    total_chains: number;
    avg_coherence: number;
    top_chains: Array<{
      id: string;
      coherence: number;
      length: number;
      thought_line: string[];
    }>;
  };
}

export interface DreamStats {
  dream_stats: {
    total_dreams: number;
    average_duration_seconds: number;
    average_thoughts_per_dream: number;
    average_dream_quality: number;
    total_autonomous_thoughts: number;
    common_dream_concepts: Array<[string, number]>;
    currently_dreaming: boolean;
    last_dream_time: number | null;
  };
  currently_dreaming: boolean;
  recent_dreams: Array<{
    session_id: string;
    start_time: number;
    duration: number;
    thoughts_count: number;
    quality: number;
    sample_thoughts: string[];
  }>;
}

export interface VoiceSignature {
  preferred_transformations: Record<string, number>;
  mood_signatures: Record<string, {
    average_resonance: number;
    success_rate: number;
    preferred_length: number;
    complexity_preference: number;
    dominant_transforms: Array<[string, number]>;
    echo_count: number;
  }>;
  temporal_patterns: Record<string, {
    avg_success: number;
    avg_resonance: number;
    dominant_mood: string;
    activity_level: number;
  }>;
  transformation_success_rates: Record<string, number>;
  total_echoes: number;
  voice_evolution_score: number;
  semantic_drift_magnitude: number;
}

export interface MoodField {
  field_state: number[];
  field_velocity: number[];
  mood_vectors: Record<string, number[]>;
  gradient: number[];
  resonance_feedback: number;
  stability: number;
  current_mood: string;
  mood_confidence: number;
  mood_probabilities: Record<string, number>;
  trajectory: Array<[string, number]>;
  recent_transitions: Array<{
    from_mood: string;
    to_mood: string;
    tick: number;
    confidence: number;
    stability_at_transition: number;
  }>;
  history: Array<{
    tick: number;
    mood: string;
    confidence: number;
    stability: number;
  }>;
}

class AdvancedConsciousnessService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private messageId = 0;
  private pendingRequests = new Map<string, {
    resolve: (value: any) => void;
    reject: (error: any) => void;
    timeout: NodeJS.Timeout;
  }>();

  // Event listeners
  private listeners = {
    consciousness_update: new Set<Function>(),
    connection_change: new Set<Function>(),
    error: new Set<Function>(),
  };

  constructor(private url: string = 'ws://localhost:8768') {}

  /**
   * Connect to the Advanced Consciousness WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
          console.log('🌟 Connected to Advanced Consciousness System');
          this.reconnectAttempts = 0;
          this.notifyListeners('connection_change', true);
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Failed to parse message:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('🔌 Disconnected from Advanced Consciousness System');
          this.notifyListeners('connection_change', false);
          this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          this.notifyListeners('error', 'Connection error');
          reject(error);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Disconnect from the server
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    // Clear pending requests
    this.pendingRequests.forEach(({ reject, timeout }) => {
      clearTimeout(timeout);
      reject(new Error('Connection closed'));
    });
    this.pendingRequests.clear();
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }

  /**
   * Send user input to DAWN and get response
   */
  async sendUserInput(input: string): Promise<ConsciousnessResponse> {
    return this.sendRequest('user_input', { input });
  }

  /**
   * Get comprehensive system status
   */
  async getSystemStatus(): Promise<any> {
    return this.sendRequest('get_status', {});
  }

  /**
   * Get memory system statistics
   */
  async getMemoryStats(): Promise<MemoryStats> {
    return this.sendRequest('get_memory_stats', {});
  }

  /**
   * Get dream system statistics
   */
  async getDreamStats(): Promise<DreamStats> {
    return this.sendRequest('get_dream_stats', {});
  }

  /**
   * Get network status
   */
  async getNetworkStatus(): Promise<any> {
    return this.sendRequest('get_network_status', {});
  }

  /**
   * Manually initiate a dream sequence
   */
  async initiateDream(): Promise<any> {
    return this.sendRequest('initiate_dream', {});
  }

  /**
   * Get voice signature and evolution data
   */
  async getVoiceSignature(): Promise<VoiceSignature> {
    return this.sendRequest('get_voice_signature', {});
  }

  /**
   * Get mood field visualization data
   */
  async getMoodField(): Promise<MoodField> {
    return this.sendRequest('get_mood_field', {});
  }

  /**
   * Get resonance chain data
   */
  async getResonanceChains(): Promise<any> {
    return this.sendRequest('get_resonance_chains', {});
  }

  /**
   * Send ping to test connection
   */
  async ping(): Promise<any> {
    return this.sendRequest('ping', {});
  }

  /**
   * Add event listener
   */
  addEventListener(
    event: keyof typeof this.listeners,
    listener: Function
  ): void {
    (this.listeners[event] as Set<Function>).add(listener);
  }

  /**
   * Remove event listener
   */
  removeEventListener(
    event: keyof typeof this.listeners,
    listener: Function
  ): void {
    (this.listeners[event] as Set<Function>).delete(listener);
  }

  /**
   * Send a request and wait for response
   */
  private sendRequest(type: string, data: any): Promise<any> {
    return new Promise((resolve, reject) => {
      if (!this.isConnected()) {
        reject(new Error('Not connected to consciousness system'));
        return;
      }

      const messageId = (++this.messageId).toString();
      const message = {
        type,
        id: messageId,
        ...data
      };

      // Set up timeout
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(messageId);
        reject(new Error('Request timeout'));
      }, 30000); // 30 second timeout

      // Store request
      this.pendingRequests.set(messageId, { resolve, reject, timeout });

      // Send message
      this.ws!.send(JSON.stringify(message));
    });
  }

  /**
   * Handle incoming messages
   */
  private handleMessage(data: any): void {
    const { type, id } = data;

    // Handle responses to requests
    if (id && this.pendingRequests.has(id)) {
      const { resolve, timeout } = this.pendingRequests.get(id)!;
      clearTimeout(timeout);
      this.pendingRequests.delete(id);

      if (type === 'error') {
        console.error('Request error:', data.error);
      } else {
        resolve(data.data);
      }
      return;
    }

    // Handle broadcasts
    switch (type) {
      case 'consciousness_state':
      case 'consciousness_update':
        this.notifyListeners('consciousness_update', data.data);
        break;
      
      case 'error':
        console.error('Server error:', data.error);
        this.notifyListeners('error', data.error);
        break;
      
      default:
        console.log('Unhandled message type:', type, data);
    }
  }

  /**
   * Notify event listeners
   */
  private notifyListeners(event: keyof typeof this.listeners, data: any): void {
    this.listeners[event].forEach(listener => {
      try {
        listener(data);
      } catch (error) {
        console.error('Listener error:', error);
      }
    });
  }

  /**
   * Attempt to reconnect
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);

    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => {
      this.connect().catch(error => {
        console.error('Reconnection failed:', error);
      });
    }, delay);
  }
}

// Export singleton instance
export const advancedConsciousnessService = new AdvancedConsciousnessService();
export default advancedConsciousnessService; 