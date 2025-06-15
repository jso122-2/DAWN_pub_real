export const WS_CONFIG = {
  development: {
    url: 'ws://localhost:8000/ws/tick-stream',
    reconnect: true,
    reconnectInterval: 1000,
    maxReconnectAttempts: 10,
    heartbeatInterval: 30000
  },
  production: {
    url: 'wss://your-production-server.com/ws/tick-stream',
    reconnect: true,
    reconnectInterval: 2000,
    maxReconnectAttempts: 20,
    heartbeatInterval: 60000
  }
};

export const getWebSocketUrl = (): string => {
  const env = process.env.NODE_ENV || 'development';
  return WS_CONFIG[env as keyof typeof WS_CONFIG].url;
}; 