import { EventEmitter } from 'events';
import { config } from '../config';

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

export class WebSocketManager extends EventEmitter {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectAttempts = 0;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private isConnecting = false;
  private isConnected = false;
  private messageHandlers: Map<string, ((payload: any) => void)[]> = new Map();
  private onConnectionChange: ((connected: boolean) => void) | null = null;

  constructor(wsConfig?: Partial<WebSocketConfig>) {
    super();
    this.config = {
      url: config.wsUrl,
      reconnectInterval: config.reconnectTimeout,
      maxReconnectAttempts: config.reconnectAttempts,
      heartbeatInterval: 30000,
      ...wsConfig
    };

    // Set up error handler
    this.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  connect(): Promise<void> {
    if (this.isConnecting || this.isConnected) {
      return Promise.resolve();
    }

    this.isConnecting = true;
    
    return new Promise((resolve, reject) => {
      try {
        console.log('Connecting to WebSocket:', this.config.url);
        this.ws = new WebSocket(this.config.url);
        
        this.ws.onopen = () => {
          console.log('WebSocket connected successfully');
          this.isConnecting = false;
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.startHeartbeat();
          this.emit('connected');
          if (this.onConnectionChange) {
            this.onConnectionChange(true);
          }
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data);
            this.emit('message', message);
            this.handleMessage(message);
          } catch (error) {
            console.warn('Failed to parse WebSocket message:', error);
            this.emit('error', new Error('Failed to parse WebSocket message'));
          }
        };

        this.ws.onclose = (event) => {
          console.log('WebSocket closed:', event.code, event.reason);
          this.isConnecting = false;
          this.isConnected = false;
          this.stopHeartbeat();
          this.emit('disconnected', event);
          if (this.onConnectionChange) {
            this.onConnectionChange(false);
          }
          
          if (!event.wasClean && this.shouldReconnect()) {
            this.scheduleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          console.error('WebSocket error occurred:', error);
          this.isConnecting = false;
          // Don't reject here, let the onclose handler handle reconnection
          this.emit('error', new Error('WebSocket connection error'));
        };

      } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
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
      console.warn('Cannot send message: WebSocket is not connected');
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
      this.emit('error', new Error('Failed to send WebSocket message'));
      return false;
    }
  }

  private handleMessage(message: WebSocketMessage) {
    try {
      const handlers = this.messageHandlers.get(message.type);
      if (handlers) {
        handlers.forEach(handler => handler(message.data));
      }
    } catch (error) {
      console.error('Error handling WebSocket message:', error);
      this.emit('error', new Error('Error handling WebSocket message'));
    }
  }

  addMessageHandler(type: string, handler: (payload: any) => void): void {
    const handlers = this.messageHandlers.get(type) || [];
    handlers.push(handler);
    this.messageHandlers.set(type, handlers);
  }

  setConnectionChangeHandler(handler: (connected: boolean) => void): void {
    this.onConnectionChange = handler;
  }

  private shouldReconnect(): boolean {
    return this.reconnectAttempts < (this.config.maxReconnectAttempts || 10);
  }

  private scheduleReconnect(): void {
    if (!this.shouldReconnect()) {
      console.log('Max reconnection attempts reached');
      this.emit('maxReconnectAttemptsReached');
      return;
    }

    this.reconnectAttempts++;
    const delay = this.config.reconnectInterval || 5000;
    console.log(`Scheduling reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);
    
    setTimeout(() => {
      if (!this.isConnected) {
        this.connect().catch(error => {
          console.error('Reconnection failed:', error);
          this.emit('error', new Error('Reconnection failed'));
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

// Create a singleton instance
export const wsManager = new WebSocketManager();
export default WebSocketManager; 