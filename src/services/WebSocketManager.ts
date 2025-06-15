import { EventEmitter } from 'events';

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: number;
}

export class WebSocketManager extends EventEmitter {
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

  get connected(): boolean {
    return this.isConnected;
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

  send(message: WebSocketMessage): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected');
    }
    this.ws.send(JSON.stringify(message));
  }

  private startHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
    }
    this.heartbeatTimer = setInterval(() => {
      this.send({
        type: 'heartbeat',
        data: { timestamp: Date.now() },
        timestamp: Date.now()
      });
    }, this.config.heartbeatInterval);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  private shouldReconnect(): boolean {
    return this.reconnectAttempts < (this.config.maxReconnectAttempts || 10);
  }

  private scheduleReconnect(): void {
    if (this.shouldReconnect()) {
      this.reconnectAttempts++;
      setTimeout(() => {
        this.connect().catch(error => {
          console.error('Failed to reconnect:', error);
        });
      }, this.config.reconnectInterval);
    }
  }
}

// Create a singleton instance
export const webSocketManager = new WebSocketManager({
  url: (import.meta as any).env?.VITE_WS_URL || 'ws://localhost:8001'
}); 