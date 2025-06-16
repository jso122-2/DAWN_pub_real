import { wsManager } from './websocketManager';

type MessageHandler = (data: any) => void;

export const wsService = {
  on: (eventOrHandler: string | MessageHandler, handler?: MessageHandler) => {
    if (typeof eventOrHandler === 'function') {
      // Legacy support - if only function passed, assume 'message' event
      wsManager.on('message', eventOrHandler);
    } else if (typeof eventOrHandler === 'string' && typeof handler === 'function') {
      // New pattern - event name + handler
      wsManager.on(eventOrHandler, handler);
    } else {
      throw new Error('Invalid arguments to on');
    }
  },
  
  removeMessageHandler: (eventOrHandler: string | MessageHandler, handler?: MessageHandler) => {
    if (typeof eventOrHandler === 'function') {
      // Legacy support - if only function passed, assume 'message' event
      wsManager.off('message', eventOrHandler);
    } else if (typeof eventOrHandler === 'string' && typeof handler === 'function') {
      // New pattern - event name + handler
      wsManager.off(eventOrHandler, handler);
    }
  },
  
  // Add direct event emitter methods for flexibility
  on: (event: string, handler: MessageHandler) => {
    wsManager.on(event, handler);
  },
  
  off: (event: string, handler: MessageHandler) => {
    wsManager.off(event, handler);
  },
  
  send: (message: any) => {
    wsManager.send(message);
  },
  
  connect: async () => {
    return wsManager.connect();
  },
  
  disconnect: () => {
    wsManager.disconnect();
  },
  
  get isConnected() {
    return wsManager.isConnected;
  }
}; 