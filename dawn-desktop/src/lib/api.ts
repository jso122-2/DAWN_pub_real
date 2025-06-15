// WebSocket connection manager
let ws: WebSocket | null = null;
const callbacks: { [key: string]: ((data: any) => void)[] } = {};

export const connectWebSocket = (url: string = 'ws://localhost:8001') => {
  if (ws && ws.readyState === WebSocket.OPEN) return;
  
  ws = new WebSocket(url);
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (callbacks[data.type]) {
        callbacks[data.type].forEach(cb => cb(data));
      }
    } catch (e) {
      console.error('WebSocket message parse error:', e);
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  ws.onclose = () => {
    setTimeout(() => connectWebSocket(url), 5000);
  };
};

export const onMetricsUpdate = (callback: (data: any) => void) => {
  if (!callbacks['metrics']) callbacks['metrics'] = [];
  callbacks['metrics'].push(callback);
  
  return () => {
    callbacks['metrics'] = callbacks['metrics'].filter(cb => cb !== callback);
  };
};
