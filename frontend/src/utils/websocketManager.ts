import { config } from '../config';

type WebSocketMessage = {
  type: string;
  payload: any;
};

class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000; // Start with 1 second
  private messageHandlers: Map<string, ((payload: any) => void)[]> = new Map();
  private onConnectionChange: ((connected: boolean) => void) | null = null;

  constructor(private url: string = config.wsUrl) {}

  connect() {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.reconnectTimeout = 1000;
        if (this.onConnectionChange) {
          this.onConnectionChange(true);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        if (this.onConnectionChange) {
          this.onConnectionChange(false);
        }
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Error creating WebSocket connection:', error);
      this.handleReconnect();
    }
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      this.reconnectTimeout *= 2; // Exponential backoff
      console.log(`Attempting to reconnect in ${this.reconnectTimeout}ms...`);
      setTimeout(() => this.connect(), this.reconnectTimeout);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }

  private handleMessage(message: WebSocketMessage) {
    const handlers = this.messageHandlers.get(message.type);
    if (handlers) {
      handlers.forEach(handler => handler(message.payload));
    }
  }

  send(type: string, payload: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      const message: WebSocketMessage = { type, payload };
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  on(type: string, handler: (payload: any) => void) {
    const handlers = this.messageHandlers.get(type) || [];
    handlers.push(handler);
    this.messageHandlers.set(type, handlers);
  }

  off(type: string, handler: (payload: any) => void) {
    const handlers = this.messageHandlers.get(type);
    if (handlers) {
      const index = handlers.indexOf(handler);
      if (index !== -1) {
        handlers.splice(index, 1);
      }
    }
  }

  setConnectionChangeHandler(handler: (connected: boolean) => void) {
    this.onConnectionChange = handler;
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export default WebSocketManager; 