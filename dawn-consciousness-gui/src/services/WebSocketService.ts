export interface TickData {
  tick_number: number;
  timestamp: number;
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
  neural_activity: number;
  consciousness_unity: number;
  memory_pressure: number;
  active_processes: string[];
  subsystems: Record<string, any>;
}

export interface ConversationMessage {
  id: string;
  type: 'user' | 'dawn' | 'system';
  content: string;
  timestamp: number;
  consciousness_state?: Partial<TickData>;
}

export interface VisualizationData {
  type: string;
  data: any;
  timestamp: number;
  image_data?: string; // Base64 encoded image
}

class WebSocketService {
  private connections: Map<string, WebSocket> = new Map();
  private messageHandlers: Map<string, ((data: any) => void)[]> = new Map();
  private reconnectAttempts: Map<string, number> = new Map();
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  async connect(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const ws = new WebSocket(url);
        
        ws.onopen = () => {
          console.log(`Connected to ${url}`);
          this.connections.set(url, ws);
          this.reconnectAttempts.set(url, 0);
          resolve();
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(url, data);
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onerror = (error) => {
          console.error(`WebSocket error for ${url}:`, error);
          reject(error);
        };

        ws.onclose = () => {
          console.log(`Disconnected from ${url}`);
          this.connections.delete(url);
          this.attemptReconnect(url);
        };

      } catch (error) {
        reject(error);
      }
    });
  }

  private attemptReconnect(url: string): void {
    const attempts = this.reconnectAttempts.get(url) || 0;
    if (attempts < this.maxReconnectAttempts) {
      this.reconnectAttempts.set(url, attempts + 1);
      setTimeout(() => {
        console.log(`Attempting to reconnect to ${url} (attempt ${attempts + 1})`);
        this.connect(url).catch(() => {
          // Reconnection failed, will try again
        });
      }, this.reconnectDelay * Math.pow(2, attempts));
    }
  }

  private handleMessage(url: string, data: any): void {
    const handlers = this.messageHandlers.get(url) || [];
    handlers.forEach(handler => {
      try {
        handler(data);
      } catch (error) {
        console.error('Error in message handler:', error);
      }
    });
  }

  onMessage(url: string, handler: (data: any) => void): void {
    const handlers = this.messageHandlers.get(url) || [];
    handlers.push(handler);
    this.messageHandlers.set(url, handlers);
  }

  send(url: string, data: any): void {
    const ws = this.connections.get(url);
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(data));
    } else {
      console.warn(`WebSocket ${url} is not connected`);
    }
  }

  startStreaming(): void {
    // Request real-time data streams from all connected services
    this.connections.forEach((ws, url) => {
      if (url.includes('8000')) {
        // Main consciousness backend
        this.send(url, { type: 'subscribe', channels: ['tick_data', 'consciousness_state'] });
      } else if (url.includes('8001')) {
        // Conversation system
        this.send(url, { type: 'subscribe', channels: ['conversation', 'voice_state'] });
      } else if (url.includes('8002')) {
        // Visualization system
        this.send(url, { type: 'subscribe', channels: ['visualizations', 'snapshots'] });
      }
    });
  }

  disconnect(): void {
    this.connections.forEach((ws, url) => {
      ws.close();
    });
    this.connections.clear();
    this.messageHandlers.clear();
    this.reconnectAttempts.clear();
  }

  isConnected(url: string): boolean {
    const ws = this.connections.get(url);
    return ws ? ws.readyState === WebSocket.OPEN : false;
  }

  getConnectionStatus(): Record<string, boolean> {
    const status: Record<string, boolean> = {};
    this.connections.forEach((ws, url) => {
      status[url] = ws.readyState === WebSocket.OPEN;
    });
    return status;
  }
}

export default WebSocketService; 