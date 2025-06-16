import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';
const MAX_RECONNECT_ATTEMPTS = 5;
const RECONNECT_DELAY = 2000; // 2 seconds

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const healthCheck = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/health', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      credentials: 'include'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Health check failed:', error);
    // Return a default response instead of throwing
    return {
      status: 'unhealthy',
      message: 'Unable to connect to DAWN system',
      timestamp: new Date().toISOString()
    };
  }
};

export const getTickSnapshot = async (processId: string) => {
  try {
    const response = await apiClient.get(`/api/tick-snapshot/${processId}`);
    return response.data;
  } catch (error) {
    console.error('Failed to get tick snapshot:', error);
    throw error;
  }
};

// WebSocket connection helper
export const createWebSocket = (path: string) => {
  const ws = new WebSocket(`ws://localhost:8000${path}`);
  
  ws.onopen = () => {
    console.log(`WebSocket connected to ${path}`);
    // Subscribe to tick updates
    ws.send(JSON.stringify({ type: 'subscribe' }));
  };
  
  ws.onclose = (event) => {
    console.log(`WebSocket disconnected from ${path}`, event.code, event.reason);
  };
  
  ws.onerror = (error) => {
    console.error(`WebSocket error on ${path}:`, error);
  };
  
  return ws;
};

export default apiClient; 