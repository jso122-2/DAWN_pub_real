import { useState, useEffect, useCallback } from 'react';
import { EventEmitter } from '@/lib/EventEmitter';

// Types for tick-aware processing
export interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: 'calm' | 'active' | 'excited' | 'critical' | 'chaotic' | 'unstable';
  timestamp: number;
  neural_activity: number;
  unity_level: number;
  memory_fragments: number;
}

export interface PythonProcess {
  process_id: string;
  script: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'queued';
  output: string[];
  exit_code?: number;
  started_at?: number;
  completed_at?: number;
  tick_started?: number;
  tick_completed?: number;
}

export interface ExecuteProcessRequest {
  script: string;
  params?: Record<string, any>;
  working_dir?: string;
  timeout?: number;
}

export interface ExecuteProcessResponse {
  process_id: string;
  status: string;
  message?: string;
}

class DAWNApiClient extends EventEmitter {
  private wsUrl: string;
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private isConnected = false;

  constructor(wsUrl: string = 'ws://localhost:8001') {
    super();
    this.wsUrl = wsUrl;
  }

  connect(): Promise<boolean> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.wsUrl);

        this.ws.onopen = () => {
          console.log('🌅 Connected to DAWN API');
          this.isConnected = true;
          this.reconnectAttempts = 0;
          this.emit('connected');
          resolve(true);
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
          }
        };

        this.ws.onclose = () => {
          console.log('🌅 Disconnected from DAWN API');
          this.isConnected = false;
          this.emit('disconnected');
          this.attemptReconnect();
        };

        this.ws.onerror = (error) => {
          console.error('🌅 DAWN API connection error:', error);
          this.emit('error', error);
          reject(error);
        };

        // Timeout for connection
        setTimeout(() => {
          if (!this.isConnected) {
            reject(new Error('Connection timeout'));
          }
        }, 5000);

      } catch (error) {
        reject(error);
      }
    });
  }

  private handleMessage(data: any) {
    const { type, ...payload } = data;

    switch (type) {
      case 'tick_update':
        this.emit('tick_update', payload);
        break;
      case 'python_output':
        this.emit('python_output', payload);
        break;
      case 'python_status':
        this.emit('python_status', payload);
        break;
      case 'system_metrics':
        this.emit('system_metrics', payload);
        break;
      default:
        console.log('🌅 Unknown message type:', type, payload);
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`🌅 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect().catch(() => {
          // Will retry again if connection fails
        });
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  async executeProcess(request: ExecuteProcessRequest): Promise<ExecuteProcessResponse> {
    return new Promise((resolve, reject) => {
      if (!this.isConnected || !this.ws) {
        reject(new Error('Not connected to DAWN API'));
        return;
      }

      const message = {
        type: 'execute_process',
        ...request
      };

      // Send request
      this.ws.send(JSON.stringify(message));

      // Wait for response
      const timeout = setTimeout(() => {
        reject(new Error('Process execution timeout'));
      }, request.timeout || 30000);

      const handleResponse = (data: any) => {
        if (data.type === 'process_started' && data.script === request.script) {
          clearTimeout(timeout);
          this.off('message', handleResponse);
          resolve({
            process_id: data.process_id,
            status: data.status,
            message: data.message
          });
        }
      };

      this.on('python_status', handleResponse);
    });
  }

  async killProcess(processId: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      if (!this.isConnected || !this.ws) {
        reject(new Error('Not connected to DAWN API'));
        return;
      }

      const message = {
        type: 'kill_process',
        process_id: processId
      };

      this.ws.send(JSON.stringify(message));

      // Wait for confirmation
      const timeout = setTimeout(() => {
        reject(new Error('Kill process timeout'));
      }, 5000);

      const handleResponse = (data: any) => {
        if (data.type === 'process_killed' && data.process_id === processId) {
          clearTimeout(timeout);
          this.off('message', handleResponse);
          resolve(true);
        }
      };

      this.on('python_status', handleResponse);
    });
  }

  getConnectionStatus(): boolean {
    return this.isConnected;
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }
}

// Global API client instance
const apiClient = new DAWNApiClient();

// Custom hook for using DAWN API
export function useDAWNApi() {
  const [isConnected, setIsConnected] = useState(false);
  const [currentTick, setCurrentTick] = useState<TickData | null>(null);
  const [systemMetrics, setSystemMetrics] = useState<any>(null);

  useEffect(() => {
    // Connect to API
    apiClient.connect().catch(console.error);

    // Set up event listeners
    const handleConnected = () => setIsConnected(true);
    const handleDisconnected = () => setIsConnected(false);
    const handleTickUpdate = (tick: TickData) => setCurrentTick(tick);
    const handleSystemMetrics = (metrics: any) => setSystemMetrics(metrics);

    apiClient.on('connected', handleConnected);
    apiClient.on('disconnected', handleDisconnected);
    apiClient.on('tick_update', handleTickUpdate);
    apiClient.on('system_metrics', handleSystemMetrics);

    // Cleanup
    return () => {
      apiClient.off('connected', handleConnected);
      apiClient.off('disconnected', handleDisconnected);
      apiClient.off('tick_update', handleTickUpdate);
      apiClient.off('system_metrics', handleSystemMetrics);
    };
  }, []);

  const executeProcess = useCallback(async (request: ExecuteProcessRequest) => {
    return apiClient.executeProcess(request);
  }, []);

  const killProcess = useCallback(async (processId: string) => {
    return apiClient.killProcess(processId);
  }, []);

  return {
    isConnected,
    currentTick,
    systemMetrics,
    executeProcess,
    killProcess,
    apiClient // Expose for event handling
  };
}

export default apiClient; 