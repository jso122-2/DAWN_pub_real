import { config } from '../config';
import { EventEmitter } from 'events';

// Add Vite environment type definition
interface ImportMetaEnv {
  DEV: boolean;
  PROD: boolean;
}

declare global {
  interface ImportMeta {
    readonly env: ImportMetaEnv;
  }
}

// WebSocket configuration based on environment
const WS_CONFIG = {
  development: {
    url: 'ws://localhost:8000/ws',  // Direct backend connection
    reconnect: true,
    reconnectInterval: 1000,
    maxReconnectAttempts: 10,
    debug: true
  },
  production: {
    url: 'ws://localhost:8000/ws',  // Direct backend connection
    reconnect: true,
    reconnectInterval: 2000,
    maxReconnectAttempts: 20,
    debug: false
  }
};

// Get appropriate config based on environment
const wsConfig = import.meta.env.DEV ? WS_CONFIG.development : WS_CONFIG.production;

export interface WebSocketMessage {
  type: string;
  data?: any;
  timestamp?: number;
  content?: any;
}

export interface WebSocketConfig {
  url?: string;
  reconnect?: boolean;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
  debug?: boolean;
}

export interface WebSocketOptions {
  url: string;
  reconnectAttempts?: number;
  reconnectDelay?: number;
  debug?: boolean;
}

const defaultConfig: WebSocketConfig = {
  url: 'ws://localhost:8000/ws',
  reconnectInterval: 3000,
  maxReconnectAttempts: 5
};

export class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts: number;
  private reconnectInterval: number;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private eventEmitter: EventEmitter;
  private debug: boolean;
  private url: string;
  private reconnect: boolean;
  private config: Required<WebSocketConfig>;
  private messageHandlers: Array<(data: any) => void> = [];
  private _isConnected: boolean = false;

  constructor(config: WebSocketConfig = {}) {
    console.log('WebSocketManager config:', config);
    
    // Use environment-specific URL if not provided
    const baseUrl = config.url || wsConfig.url;
    // Ensure URL is clean without any parameters
    const cleanUrl = baseUrl.split('?')[0];

    this.config = {
      url: cleanUrl,
      reconnect: config.reconnect !== false,
      reconnectInterval: config.reconnectInterval || 1000,
      maxReconnectAttempts: config.maxReconnectAttempts || 10,
      heartbeatInterval: config.heartbeatInterval || 30000,
      debug: config.debug || false
    };
    
    this.url = this.config.url;
    this.reconnect = this.config.reconnect;
    this.maxReconnectAttempts = this.config.maxReconnectAttempts;
    this.reconnectInterval = this.config.reconnectInterval;
    this.debug = this.config.debug;
    
    this.eventEmitter = new EventEmitter();
    this.eventEmitter.setMaxListeners(20);
  }

  get isConnected(): boolean {
    return this._isConnected;
  }

  private set isConnected(value: boolean) {
    this._isConnected = value;
  }

  async connect() {
    // Skip health check for now - just try WebSocket directly
    console.log('[WebSocket] Attempting direct connection...');
    const wsUrl = 'ws://localhost:8000/ws';
    try {
      this.ws = new WebSocket(wsUrl);
      this.ws.onopen = () => {
        console.log('[WebSocket] Connected successfully!');
        this.isConnected = true;
        this.eventEmitter.emit('connected', { timestamp: Date.now() });
      };
      this.ws.onerror = (error) => {
        console.error('[WebSocket] Connection error:', error);
        // Try with IP address
        console.log('[WebSocket] Retrying with IP address...');
        this.ws = new WebSocket('ws://172.30.234.157:8000/ws');
      };
      this.ws.onclose = () => {
        console.log('[WebSocket] Connection closed');
        this.isConnected = false;
        this.eventEmitter.emit('disconnected', { timestamp: Date.now() });
        if (this.reconnect) {
          this.handleDisconnect();
        }
      };
      this.ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          this.eventEmitter.emit('message', message);
        } catch (error) {
          console.error('[WebSocket] Error parsing message:', error);
        }
      };
    } catch (error) {
      console.error('[WebSocket] Failed to connect:', error);
      if (this.reconnect) {
        this.handleDisconnect();
      }
    }
  }

  private handleDisconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`[WebSocket] Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      setTimeout(() => this.connect(), this.reconnectInterval);
    } else {
      console.error('[WebSocket] Max reconnection attempts reached');
      this.eventEmitter.emit('error', { message: 'Max reconnection attempts reached' });
    }
  }

  // Support both APIs
  on(eventOrHandler: string | ((data: any) => void), handler?: (data: any) => void) {
    if (typeof eventOrHandler === 'function') {
      // Called as: on(handler)
      this.on('message', eventOrHandler);
    } else if (typeof eventOrHandler === 'string' && typeof handler === 'function') {
      // Called as: on('eventName', handler)
      this.on(eventOrHandler, handler);
    } else {
      throw new Error('Invalid arguments to on');
    }
  }

  removeMessageHandler(eventOrHandler: string | ((data: any) => void), handler?: (data: any) => void) {
    if (typeof eventOrHandler === 'function') {
      this.off('message', eventOrHandler);
    } else if (typeof eventOrHandler === 'string' && typeof handler === 'function') {
      this.off(eventOrHandler, handler);
    }
  }

  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.stopHeartbeat();
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(message: any): boolean {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.error('WebSocket is not connected');
      return false;
    }

    try {
      const messageStr = typeof message === 'string' ? message : JSON.stringify(message);
      this.ws.send(messageStr);
      return true;
    } catch (error) {
      this.error('Error sending message:', error);
      this.eventEmitter.emit('error', error);
      return false;
    }
  }

  on(event: string, callback: (data: any) => void): void {
    this.eventEmitter.on(event, callback);
  }

  off(event: string, callback: (data: any) => void): void {
    this.eventEmitter.off(event, callback);
  }

  emit(event: string, data: any): void {
    this.eventEmitter.emit(event, data);
  }

  private log(...args: any[]): void {
    if (this.debug) {
      console.log('[WebSocket]', ...args);
    }
  }

  private error(...args: any[]): void {
    console.error('[WebSocket]', ...args);
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const message = JSON.parse(event.data);
      
      // Emit to event listeners
      this.eventEmitter.emit('message', message);
      
      // Call all registered message handlers
      this.messageHandlers.forEach(handler => {
        try {
          handler(message);
        } catch (error) {
          this.error('Error in message handler:', error);
        }
      });
      
      if (message.type) {
        this.eventEmitter.emit(message.type, message.data);
      }
    } catch (error) {
      this.error('Error parsing WebSocket message:', error);
      this.eventEmitter.emit('error', error);
    }
  }

  private startHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
    }
    this.heartbeatTimer = setInterval(() => {
      if (this.isConnected) {
        this.send({ type: 'ping', timestamp: Date.now() });
      }
    }, this.config.heartbeatInterval);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }
}

// Singleton instance
let instance: WebSocketManager | null = null;

export const getWebSocketManager = (): WebSocketManager => {
  if (!instance) {
    const config = {
      url: import.meta.env.DEV ? 'ws://localhost:3000/ws' : 'ws://localhost:8000/ws',
      reconnect: true,
      reconnectInterval: 1000,
      maxReconnectAttempts: 10,
      debug: true
    };
    
    console.log('Creating WebSocketManager singleton with config:', config);
    instance = new WebSocketManager(config);
  }
  return instance;
};

// Export the instance getter
export const wsManager = getWebSocketManager(); 