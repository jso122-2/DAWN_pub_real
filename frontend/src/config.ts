export const config = {
  wsUrl: 'ws://localhost:8001/ws',
  apiUrl: 'http://localhost:8001',
  reconnectAttempts: 5,
  reconnectTimeout: 1000,
} as const; 