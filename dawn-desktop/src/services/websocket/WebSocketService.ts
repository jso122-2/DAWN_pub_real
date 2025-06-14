import { EventEmitter } from 'events';

export interface WebSocketConfig {
  url: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export class WebSocketService extends EventEmitter {
  private ws: WebSocket | null = null;
  private config: WebSocketConfig;
  private reconnectAttempts = 0;
  private reconnectTimeout: NodeJS.Timeout | null = null;
  private heartbeatInterval: NodeJS.Timeout | null = null;
  private connectionState: 'disconnected' | 'connecting' | 'connected' = 'disconnected';
  private messageQueue: any[] = [];

  constructor(config: WebSocketConfig) {
    super();
    this.config = {
      reconnectInterval: 1000,
      maxReconnectAttempts: 5,
      heartbeatInterval: 30000,
      ...config,
    };
  }

  connect(): void {
    if (this.connectionState !== 'disconnected') {
      console.warn('WebSocket already connecting or connected');
      return;
    }

    this.connectionState = 'connecting';
    this.ws = new WebSocket(this.config.url);
    
    this.ws.onopen = this.handleOpen.bind(this);
    this.ws.onmessage = this.handleMessage.bind(this);
    this.ws.onerror = this.handleError.bind(this);
    this.ws.onclose = this.handleClose.bind(this);
  }

  private handleOpen(): void {
    console.log('WebSocket connected');
    this.connectionState = 'connected';
    this.reconnectAttempts = 0;
    
    // Send queued messages
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
    
    // Start heartbeat
    this.startHeartbeat();
    
    this.emit('connected');
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const data = JSON.parse(event.data);
      this.emit('message', data);
      
      // Emit specific event types
      if (data.type) {
        this.emit(data.type, data.data);
      }
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
      this.emit('error', error);
    }
  }

  private handleError(event: Event): void {
    console.error('WebSocket error:', event);
    this.emit('error', event);
  }

  private handleClose(): void {
    console.log('WebSocket disconnected');
    this.connectionState = 'disconnected';
    this.stopHeartbeat();
    
    this.emit('disconnected');
    
    // Attempt reconnection
    if (this.reconnectAttempts < this.config.maxReconnectAttempts!) {
      this.scheduleReconnect();
    } else {
      this.emit('reconnect_failed');
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
    }

    const delay = Math.min(
      this.config.reconnectInterval! * Math.pow(2, this.reconnectAttempts),
      30000
    );

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts + 1})`);

    this.reconnectTimeout = setTimeout(() => {
      this.reconnectAttempts++;
      this.connect();
    }, delay);
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'heartbeat', timestamp: Date.now() });
      }
    }, this.config.heartbeatInterval!);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
  }

  send(data: any): void {
    if (!this.isConnected()) {
      // Queue message for later
      this.messageQueue.push(data);
      return;
    }

    try {
      this.ws!.send(JSON.stringify(data));
    } catch (error) {
      console.error('Failed to send WebSocket message:', error);
      this.emit('error', error);
    }
  }

  disconnect(): void {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }

    this.stopHeartbeat();
    
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    this.connectionState = 'disconnected';
    this.messageQueue = [];
  }

  isConnected(): boolean {
    return this.connectionState === 'connected' && 
           this.ws !== null && 
           this.ws.readyState === WebSocket.OPEN;
  }

  getState(): string {
    return this.connectionState;
  }
}

// Singleton instances
export const mainWebSocket = new WebSocketService({
  url: 'ws://localhost:8000/ws',
});

export const processWebSocket = new WebSocketService({
  url: 'ws://localhost:8000/process-stream',
}); 