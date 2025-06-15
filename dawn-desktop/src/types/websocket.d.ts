declare module '@/services/websocket/WebSocketService' {
  export interface WebSocketMessage {
    type: string;
    data: any;
  }
  
  export interface WebSocketError {
    code: number;
    message: string;
  }
} 