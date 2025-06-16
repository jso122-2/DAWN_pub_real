export const config = {
  wsUrl: 'ws://localhost:8000/ws',
  apiUrl: 'http://localhost:8000',
  reconnectAttempts: 5,
  reconnectTimeout: 1000,
  debug: true
} as const; 