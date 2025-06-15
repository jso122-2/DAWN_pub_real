import { EventEmitter } from 'events';

export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: number;
}

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export class WebSocketIntegration extends EventEmitter {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectAttempts = 0;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private isConnecting = false;
  private isConnected = false;

  constructor(config: WebSocketConfig) {
    super();
    this.config = {
      reconnectInterval: 5000,
      maxReconnectAttempts: 10,
      heartbeatInterval: 30000,
      ...config
    };
  }

  connect(): Promise<void> {
    if (this.isConnecting || this.isConnected) {
      return Promise.resolve();
    }

    this.isConnecting = true;
    
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.config.url);
        
        this.ws.onopen = () => {
          this.isConnecting = false;
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.startHeartbeat();
          this.emit('connected');
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.emit('message', message);
          } catch (error) {
            console.warn('Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onclose = (event) => {
          this.isConnecting = false;
          this.isConnected = false;
          this.stopHeartbeat();
          this.emit('disconnected', event);
          
          if (!event.wasClean && this.shouldReconnect()) {
            this.scheduleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          this.isConnecting = false;
          this.emit('error', error);
          reject(error);
        };

      } catch (error) {
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    this.stopHeartbeat();
    this.isConnected = false;
    this.isConnecting = false;
  }

  send(message: Omit<WebSocketMessage, 'timestamp'>): boolean {
    if (!this.isConnected || !this.ws) {
      return false;
    }

    try {
      const fullMessage: WebSocketMessage = {
        ...message,
        timestamp: Date.now()
      };
      
      this.ws.send(JSON.stringify(fullMessage));
      return true;
    } catch (error) {
      console.error('Failed to send WebSocket message:', error);
      return false;
    }
  }

  private shouldReconnect(): boolean {
    return this.reconnectAttempts < (this.config.maxReconnectAttempts || 10);
  }

  private scheduleReconnect(): void {
    if (!this.shouldReconnect()) {
      this.emit('maxReconnectAttemptsReached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.config.reconnectInterval || 5000;
    
    setTimeout(() => {
      if (!this.isConnected) {
        this.connect().catch(error => {
          console.error('Reconnection failed:', error);
        });
      }
    }, delay);
  }

  private startHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
    }

    this.heartbeatTimer = setInterval(() => {
      if (this.isConnected) {
        this.send({
          type: 'heartbeat',
          data: { timestamp: Date.now() }
        });
      }
    }, this.config.heartbeatInterval || 30000);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  get connectionState(): 'connecting' | 'connected' | 'disconnected' {
    if (this.isConnecting) return 'connecting';
    if (this.isConnected) return 'connected';
    return 'disconnected';
  }
}

// Export a default instance
export const defaultWebSocketIntegration = new WebSocketIntegration({
  url: process.env.REACT_APP_WEBSOCKET_URL || 'ws://localhost:8001'
}); 