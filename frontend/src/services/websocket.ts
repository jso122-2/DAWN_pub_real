import { WebSocketMessage as WSMessage, TickData, ModuleStatus } from '../types';
import { config } from '../config';
import { useState, useEffect, useCallback } from 'react';
import { create } from 'zustand';
import { NeuralMetrics } from '../types/neural';
import { Subject } from 'rxjs';

type MessageHandler = (data: any) => void;

type ConnectionStatus = 'connected' | 'disconnected' | 'connecting';

interface WebSocketHook {
    lastMessage: string | null;
    connectionStatus: ConnectionStatus;
    sendMessage: (message: string) => void;
}

interface WebSocketState {
  connected: boolean;
  neuralMetrics: NeuralMetrics | null;
  error: string | null;
  connect: () => void;
  disconnect: () => void;
}

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  debug?: boolean;
}

export interface WebSocketMessage {
  type: string;
  content?: string;
  metadata?: any;
  default_viz?: string[];
}

export class WebSocketManager {
  private ws: WebSocket | null = null;
  private config: Required<WebSocketConfig>;
  private reconnectAttempts = 0;
  private messageHandlers: Map<string, ((data: any) => void)[]> = new Map();
  private isIntentionallyClosed = false;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private pingInterval: NodeJS.Timeout | null = null;
  private lastPingTime: number = 0;
  private connectionStatus = new Subject<boolean>();
  private connectPromise: Promise<void> | null = null;
  private currentResolve: ((value: void | PromiseLike<void>) => void) | null = null;
  private currentReject: ((reason?: any) => void) | null = null;
  private isConnecting = false;
  private isConnected = false;
  private cleanupInProgress = false;
  
  constructor(config: WebSocketConfig) {
    this.config = {
      reconnectInterval: 3000,
      maxReconnectAttempts: 10,
      debug: true,
      ...config
    };
  }

  private cleanup() {
    if (this.cleanupInProgress) return;
    this.cleanupInProgress = true;

    try {
      if (this.ws) {
        // Only close if we're actually connected
        if (this.ws.readyState === WebSocket.OPEN) {
          this.ws.close(1000, 'Client disconnect');
        }
        
        // Remove all event listeners
        this.ws.onopen = null;
        this.ws.onclose = null;
        this.ws.onerror = null;
        this.ws.onmessage = null;
        
        this.ws = null;
      }

      if (this.pingInterval) {
        clearInterval(this.pingInterval);
        this.pingInterval = null;
      }

      if (this.reconnectTimeout) {
        clearTimeout(this.reconnectTimeout);
        this.reconnectTimeout = null;
      }

      this.currentResolve = null;
      this.currentReject = null;
      this.connectPromise = null;
      this.isConnecting = false;
      this.isConnected = false;
      this.isIntentionallyClosed = false;
      this.reconnectAttempts = 0;
    } finally {
      this.cleanupInProgress = false;
    }
  }

  private setupWebSocketHandlers(resolve: (value: void | PromiseLike<void>) => void, reject: (reason?: any) => void) {
    if (!this.ws) return;

    this.currentResolve = resolve;
    this.currentReject = reject;

    this.ws.onopen = () => {
      if (this.config.debug) {
        console.log('[WebSocket] Connected successfully');
      }
      this.reconnectAttempts = 0;
      this.startPingInterval();
      this.connectionStatus.next(true);
      this.isConnecting = false;
      this.isConnected = true;
      resolve();
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        if (this.config.debug) {
          console.log('[WebSocket] Received:', message);
        }
        
        // Handle ping/pong
        if (message.type === 'ping') {
          this.send({ type: 'pong', content: 'pong' });
          return;
        }
        
        this.handleMessage(message);
      } catch (error) {
        console.error('[WebSocket] Failed to parse message:', error);
      }
    };

    this.ws.onerror = (error) => {
      console.error('[WebSocket] Error:', error);
      this.connectionStatus.next(false);
      this.isConnected = false;
      
      // Only reject if this is the initial connection attempt
      if (this.reconnectAttempts === 0 && this.currentReject) {
        this.currentReject(error);
      }
    };

    this.ws.onclose = (event) => {
      if (this.config.debug) {
        console.log(`[WebSocket] Closed. Code: ${event.code}, Reason: ${event.reason}`);
      }
      
      this.stopPingInterval();
      this.connectionStatus.next(false);
      this.isConnecting = false;
      this.isConnected = false;
      
      if (!this.isIntentionallyClosed && this.reconnectAttempts < this.config.maxReconnectAttempts) {
        this.handleReconnect();
      } else if (this.reconnectAttempts >= this.config.maxReconnectAttempts) {
        console.error('[WebSocket] Max reconnection attempts reached');
        this.cleanup();
      }
    };
  }

  private async connect(): Promise<void> {
    if (this.isConnected) {
      return Promise.resolve();
    }

    if (this.isConnecting) {
      return new Promise((resolve) => {
        const checkConnection = setInterval(() => {
          if (this.isConnected) {
            clearInterval(checkConnection);
            resolve();
          }
        }, 100);
      });
    }

    this.isConnecting = true;
    this.isConnected = false;
    this.cleanup();

    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.config.url);

        this.ws.onopen = () => {
          this.isConnected = true;
          this.isConnecting = false;
          this.connectionStatus.next(true);
          this.startPingInterval();
          resolve();
        };

        this.ws.onclose = () => {
          this.isConnected = false;
          this.isConnecting = false;
          this.connectionStatus.next(false);
          this.stopPingInterval();
          if (!this.isIntentionallyClosed) {
            this.handleReconnect();
          }
        };

        this.ws.onerror = (error) => {
          console.error('[WebSocket] Connection error:', error);
          this.isConnected = false;
          this.isConnecting = false;
          this.connectionStatus.next(false);
          this.stopPingInterval();
          if (!this.isIntentionallyClosed) {
            this.handleReconnect();
          }
          reject(error);
        };

        this.setupWebSocketHandlers(resolve, reject);
      } catch (error) {
        this.isConnecting = false;
        reject(error);
      }
    });
  }

  private handleReconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }
    
    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    
    if (this.config.debug) {
      console.log(`[WebSocket] Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts}/${this.config.maxReconnectAttempts})`);
    }
    
    this.reconnectTimeout = setTimeout(() => {
      this.connect().catch(error => {
        console.error('[WebSocket] Reconnection failed:', error);
      });
    }, delay);
  }

  private startPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
    }
    
    this.pingInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.send({ type: 'ping', content: 'ping' });
        this.lastPingTime = Date.now();
      }
    }, 30000); // Send ping every 30 seconds
  }

  private stopPingInterval() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  disconnect() {
    this.isIntentionallyClosed = true;
    this.cleanup();
  }

  send(message: WebSocketMessage): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.isConnected) {
        this.connect()
          .then(() => {
            this.sendMessage(message);
            resolve();
          })
          .catch(reject);
      } else {
        this.sendMessage(message);
        resolve();
      }
    });
  }

  private sendMessage(message: WebSocketMessage) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('[WebSocket] Cannot send message - connection not open');
      return;
    }

    const messageWithTimestamp = {
      ...message,
      timestamp: new Date().toISOString()
    };

    if (this.config.debug) {
      console.log('[WebSocket] Sending:', messageWithTimestamp);
    }

    try {
      this.ws.send(JSON.stringify(messageWithTimestamp));
    } catch (error) {
      console.error('[WebSocket] Error sending message:', error);
      this.handleReconnect();
    }
  }

  onMessage(type: string, handler: (data: any) => void) {
    if (!this.messageHandlers.has(type)) {
      this.messageHandlers.set(type, []);
    }
    this.messageHandlers.get(type)?.push(handler);
  }

  offMessage(type: string, handler: (data: any) => void) {
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index !== -1) {
        handlers.splice(index, 1);
      }
    }
  }

  private handleMessage(message: WebSocketMessage) {
    const handlers = this.messageHandlers.get(message.type);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message);
        } catch (error) {
          console.error(`[WebSocket] Error in message handler for ${message.type}:`, error);
        }
      });
    }
  }

  onConnectionChange(callback: (connected: boolean) => void) {
    return this.connectionStatus.subscribe(callback);
  }
}

// Create a default WebSocket manager instance
const defaultConfig: WebSocketConfig = {
  url: 'ws://localhost:8000/ws/visualization',
  debug: true
};

export const wsService = new WebSocketManager(defaultConfig);

export const useWebSocket = create<WebSocketState>((set) => {
  let ws: WebSocket | null = null;

  const connect = () => {
    if (ws) return;

    ws = new WebSocket(config.wsUrl);

    ws.onopen = () => {
      set({ connected: true, error: null });
    };

    ws.onclose = () => {
      set({ connected: false });
      ws = null;
    };

    ws.onerror = (error) => {
      set({ error: 'WebSocket connection error' });
      console.error('WebSocket error:', error);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'neural_metrics') {
          set({ neuralMetrics: data.metrics });
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  };

  const disconnect = () => {
    if (ws) {
      ws.close();
      ws = null;
    }
  };

  return {
    connected: false,
    neuralMetrics: null,
    error: null,
    connect,
    disconnect,
  };
}); 