// WebSocket Service for DAWN
// Handles all WebSocket connections to the Python backend
import React from 'react';

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export interface TickData {
  scup: number;
  entropy: number;
  heat: number;
  mood: string;
  timestamp: number;
  tick_count: number;
  signals?: Record<string, any>;
  duration?: number;
  lag?: number;
}

export interface ConsciousnessData {
  memory_usage: number;
  neural_activity: number;
  consciousness_unity: number;
  timestamp: number;
}

export interface ProcessData {
  process_id: string;
  output: string;
  level: 'info' | 'warning' | 'error' | 'success';
  timestamp: number;
}

type MessageHandler = (data: any) => void;
type ConnectionHandler = (connected: boolean) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private messageHandlers: Map<string, Set<MessageHandler>> = new Map();
  private connectionHandlers: Set<ConnectionHandler> = new Set();
  private reconnectAttempts = 0;
  private reconnectTimeout?: NodeJS.Timeout;
  private heartbeatInterval?: NodeJS.Timeout;
  private isConnecting = false;
  
  constructor(config: WebSocketConfig) {
    this.config = {
      reconnectInterval: 3000,
      maxReconnectAttempts: 10,
      heartbeatInterval: 30000,
      ...config
    };
  }
  
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN || this.isConnecting) {
      return;
    }
    
    this.isConnecting = true;
    
    try {
      this.ws = new WebSocket(this.config.url);
      
      this.ws.onopen = () => {
        console.log('[WebSocket] Connected to', this.config.url);
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.notifyConnectionHandlers(true);
        this.startHeartbeat();
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          // Handle different message types based on data structure
          if (data.scup !== undefined && data.mood !== undefined) {
            // This is tick data
            this.handleMessage({ type: 'tick', data });
          } else if (data.process_id !== undefined) {
            // This is process data
            this.handleMessage({ type: 'process', data });
          } else if (data.memory_usage !== undefined) {
            // This is consciousness data
            this.handleMessage({ type: 'consciousness', data });
          } else {
            // Generic message handling
            this.handleMessage({ type: 'message', data });
          }
        } catch (error) {
          console.error('[WebSocket] Failed to parse message:', error);
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('[WebSocket] Error:', error);
        this.isConnecting = false;
      };
      
      this.ws.onclose = () => {
        console.log('[WebSocket] Disconnected');
        this.isConnecting = false;
        this.notifyConnectionHandlers(false);
        this.stopHeartbeat();
        this.scheduleReconnect();
      };
    } catch (error) {
      console.error('[WebSocket] Failed to connect:', error);
      this.isConnecting = false;
      this.scheduleReconnect();
    }
  }
  
  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = undefined;
    }
    
    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
  
  send(type: string, data: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, data }));
    } else {
      console.warn('[WebSocket] Cannot send message, not connected');
    }
  }
  
  on(event: string, handler: MessageHandler): () => void {
    if (!this.messageHandlers.has(event)) {
      this.messageHandlers.set(event, new Set());
    }
    
    this.messageHandlers.get(event)!.add(handler);
    
    // Return unsubscribe function
    return () => {
      this.messageHandlers.get(event)?.delete(handler);
    };
  }
  
  onConnectionChange(handler: ConnectionHandler): () => void {
    this.connectionHandlers.add(handler);
    
    // Return unsubscribe function
    return () => {
      this.connectionHandlers.delete(handler);
    };
  }
  
  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
  
  private handleMessage(message: any): void {
    const { type, data } = message;
    
    // Notify specific event handlers
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(data);
        } catch (error) {
          console.error(`[WebSocket] Error in ${type} handler:`, error);
        }
      });
    }
    
    // Notify wildcard handlers
    const wildcardHandlers = this.messageHandlers.get('*');
    if (wildcardHandlers) {
      wildcardHandlers.forEach(handler => {
        try {
          handler(message);
        } catch (error) {
          console.error('[WebSocket] Error in wildcard handler:', error);
        }
      });
    }
  }
  
  private notifyConnectionHandlers(connected: boolean): void {
    this.connectionHandlers.forEach(handler => {
      try {
        handler(connected);
      } catch (error) {
        console.error('[WebSocket] Error in connection handler:', error);
      }
    });
  }
  
  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.config.maxReconnectAttempts!) {
      console.error('[WebSocket] Max reconnection attempts reached');
      return;
    }
    
    this.reconnectAttempts++;
    const delay = this.config.reconnectInterval! * Math.min(this.reconnectAttempts, 5);
    
    console.log(`[WebSocket] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    this.reconnectTimeout = setTimeout(() => {
      this.connect();
    }, delay);
  }
  
  private startHeartbeat(): void {
    if (this.config.heartbeatInterval) {
      this.heartbeatInterval = setInterval(() => {
        if (this.isConnected) {
          this.send('ping', { timestamp: Date.now() });
        }
      }, this.config.heartbeatInterval);
    }
  }
  
  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = undefined;
    }
  }
}

// Create a single WebSocket instance for the main connection
export const webSocketService = new WebSocketService({
      url: (import.meta as any).env?.VITE_WS_URL || 'ws://localhost:8001'
});

// React hook for easy component integration
export const useWebSocket = (eventType: string) => {
  const [data, setData] = React.useState<any>(null);
  const [connected, setConnected] = React.useState(false);
  
  React.useEffect(() => {
    // Subscribe to connection changes
    const unsubscribeConnection = webSocketService.onConnectionChange(setConnected);
    
    // Subscribe to specific event type
    const unsubscribeEvent = webSocketService.on(eventType, (eventData) => {
      setData(eventData);
    });
    
    // Connect if not already connected
    if (!webSocketService.isConnected) {
      webSocketService.connect();
    }
    
    return () => {
      unsubscribeConnection();
      unsubscribeEvent();
    };
  }, [eventType]);
  
  return { data, connected };
};

// Auto-connect on module load (optional)
if ((import.meta as any).env?.MODE !== 'test') {
  webSocketService.connect();
}

// Export the service class for custom instances
export default WebSocketService; 