export interface TickData {
  scup: number;
  entropy: number;
  heat: number;
  mood: 'analytical' | 'confident' | 'focused' | 'creative' | 'euphoric' | 'excited' | 'serene' | 'contemplative' | 'anxious' | 'active' | 'chaotic' | 'critical';
  timestamp: number;
  tick_count: number;
}

class WebSocketService {
  private ws: WebSocket | null = null;
  private baseUrl = 'ws://localhost:8000';
  private endpoints = {
    main: '/ws',
    talk: '/ws/talk',
    tick: '/ws/tick'
  };
  private currentEndpoint: keyof typeof this.endpoints = 'main';
  private callbacks: Set<(data: TickData) => void> = new Set();
  private reconnectTimeout: number | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private isConnecting = false;
  
  // Tick rate calculation
  private lastTickTime: number | null = null;
  private tickRate: number = 0;
  private tickCount: number = 0;
  
  constructor() {
    // Try to connect to all endpoints in sequence
    this.connectToEndpoint('main');
  }
  
  private connectToEndpoint(endpoint: keyof typeof this.endpoints) {
    if (this.isConnecting) return;
    
    this.isConnecting = true;
    this.currentEndpoint = endpoint;
    const url = `${this.baseUrl}${this.endpoints[endpoint]}`;
    
    console.log(`🔌 Connecting to DAWN WebSocket server on ${url}...`);
    try {
      this.ws = new WebSocket(url);
      
      this.ws.onopen = () => {
        console.log(`✅ Connected to DAWN consciousness engine on ${url}!`);
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        if (this.reconnectTimeout) {
          clearTimeout(this.reconnectTimeout);
          this.reconnectTimeout = null;
        }
      };
      
      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          
          // Handle different message formats from the server
          let tickData: TickData;
          
          if (message.type === 'tick' && message.data) {
            // Simple WebSocket server format with nested data
            const rawData = message.data;
            tickData = {
              scup: rawData.scup || 0.5,
              entropy: rawData.entropy || 0.5,
              heat: rawData.systemLoad || rawData.heat || rawData.neural_activity || 0.5,
              mood: this.mapMood(rawData.mood),
              timestamp: rawData.timestamp || Date.now(),
              tick_count: rawData.tick_number || rawData.tick_count || 0
            };
          } else if (message.type === 'tick_data' || message.type === 'consciousness_update') {
            // Server message format
            const rawData = message.data;
            tickData = {
              scup: rawData.scup ? rawData.scup / 100 : rawData.scup || 0.5,
              entropy: rawData.entropy || 0.5,
              heat: rawData.systemLoad || rawData.heat || 0.5,
              mood: this.mapMood(rawData.mood),
              timestamp: rawData.timestamp || Date.now(),
              tick_count: rawData.tick_count || 0
            };
          } else if (message.scup !== undefined) {
            // Direct tick data format
            tickData = {
              scup: message.scup,
              entropy: message.entropy || 0.5,
              heat: message.heat || 0.5,
              mood: this.mapMood(message.mood),
              timestamp: message.timestamp || Date.now(),
              tick_count: message.tick_count || 0
            };
          } else {
            // Fallback: use the whole message as tick data
            tickData = {
              scup: message.scup || 0.5,
              entropy: message.entropy || 0.5,
              heat: message.heat || 0.5,
              mood: this.mapMood(message.mood),
              timestamp: message.timestamp || Date.now(),
              tick_count: message.tick_count || 0
            };
          }
          
          // Calculate tick rate properly
          this.handleTickData(tickData);
          
          console.log('📡 Received tick data:', tickData);
          this.callbacks.forEach(callback => callback(tickData));
        } catch (error) {
          console.error('Failed to parse tick data:', error);
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
        this.scheduleReconnect();
      };
      
      this.ws.onclose = () => {
        console.log(`WebSocket disconnected from ${url}`);
        this.isConnecting = false;
        this.scheduleReconnect();
      };
    } catch (error) {
      console.error('Failed to connect:', error);
      this.isConnecting = false;
      this.scheduleReconnect();
    }
  }
  
  private mapMood(mood: string): TickData['mood'] {
    // Map server mood to our expected mood types
    const moodMap: Record<string, TickData['mood']> = {
      'euphoric': 'euphoric',
      'excited': 'excited', 
      'serene': 'serene',
      'contemplative': 'contemplative',
      'anxious': 'anxious',
      'active': 'active',
      'chaotic': 'chaotic',
      'critical': 'critical',
      'analytical': 'analytical',
      'confident': 'confident',
      'focused': 'focused',
      'creative': 'creative'
    };
    
    return moodMap[mood] || 'analytical';
  }
  
  private scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }
    
    if (!this.reconnectTimeout) {
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      this.reconnectTimeout = window.setTimeout(() => {
        console.log(`Attempting to reconnect... (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`);
        this.reconnectAttempts++;
        
        // Try next endpoint in sequence
        const endpoints = Object.keys(this.endpoints) as Array<keyof typeof this.endpoints>;
        const currentIndex = endpoints.indexOf(this.currentEndpoint);
        const nextEndpoint = endpoints[(currentIndex + 1) % endpoints.length];
        this.connectToEndpoint(nextEndpoint);
      }, delay);
    }
  }
  
  subscribe(callback: (data: TickData) => void) {
    this.callbacks.add(callback);
    return () => this.callbacks.delete(callback);
  }
  
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    this.reconnectAttempts = 0;
    this.isConnecting = false;
  }
  
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
  
  getConnectionState(): 'connecting' | 'connected' | 'disconnected' | 'error' {
    if (this.isConnecting) return 'connecting';
    if (!this.ws) return 'disconnected';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING: return 'connecting';
      case WebSocket.OPEN: return 'connected';
      case WebSocket.CLOSING:
      case WebSocket.CLOSED: return 'disconnected';
      default: return 'error';
    }
  }
  
  // Fix tick rate calculation 
  private handleTickData(tickData: TickData): void {
    // Update tick count
    this.tickCount++;
    
    // Calculate tick rate (ticks per second)
    const now = Date.now();
    if (this.lastTickTime) {
      const timeDiff = now - this.lastTickTime;
      this.tickRate = 1000 / timeDiff; // Hz
    }
    this.lastTickTime = now;
    
    // Update the tick data with our calculated values
    tickData.tick_count = this.tickCount;
  }
  
  getTickRate(): number {
    return this.tickRate;
  }
  
  getTickCount(): number {
    return this.tickCount;
  }
}

export const webSocketService = new WebSocketService(); 