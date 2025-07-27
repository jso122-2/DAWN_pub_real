// Visual Service for managing DAWN visual processes
export interface VisualProcess {
  id: string;
  name: string;
  script: string;
  running: boolean;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'POETIC';
  mode: 'realtime' | 'periodic' | 'triggered' | 'snapshot';
  target_fps: number;
  enabled: boolean;
  cpu_usage?: number;
  memory_usage?: number;
  error_count: number;
  last_update: string | null;
}

export interface VisualSystemStatus {
  is_running: boolean;
  active_processes: number;
  max_processes: number;
  system_load: number;
  processes: Record<string, VisualProcess>;
}

export interface VisualOutput {
  process_id: string;
  filename: string;
  timestamp: number;
  image_data: string;
  file_size?: number;
  status: string;
}

export interface ProcessStartRequest {
  process_id: string;
  script: string;
  parameters?: Record<string, any>;
  modules?: Array<Record<string, any>>;
}

export interface ProcessStopRequest {
  process_id: string;
}

export interface ProcessResponse {
  success: boolean;
  message: string;
  process_status?: VisualProcess;
}

class VisualService {
  private baseUrl = 'http://localhost:8001';
  private wsUrl = 'ws://localhost:8001/ws/visual';
  private ws: WebSocket | null = null;
  private outputCallbacks: Set<(outputs: Record<string, VisualOutput>) => void> = new Set();
  private statusCallbacks: Set<(status: VisualSystemStatus) => void> = new Set();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 3; // Limit reconnection attempts
  private wsEnabled = false; // Disable WebSocket by default for now

  // Get overall visual system status
  async getVisualStatus(): Promise<VisualSystemStatus> {
    try {
      const response = await fetch(`${this.baseUrl}/api/visual/status`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to get visual status:', error);
      // Return default status if API fails
      return {
        is_running: false,
        active_processes: 0,
        max_processes: 0,
        system_load: 0,
        processes: {}
      };
    }
  }

  // Start a visual process
  async startVisualProcess(processId: string, script: string, parameters: Record<string, any> = {}): Promise<ProcessResponse> {
    try {
      console.log(`🎬 Starting visual process: ${processId} with script: ${script}`);
      
      const request: ProcessStartRequest = {
        process_id: processId,
        script: script,
        parameters: parameters
      };

      console.log('🔄 Sending start request:', request);

      const response = await fetch(`${this.baseUrl}/api/visual/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
      });

      console.log(`📡 Start API Response - Status: ${response.status}, OK: ${response.ok}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Start API Error: ${response.status} - ${errorText}`);
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('✅ Start API Success:', result);
      return result;
    } catch (error) {
      console.error(`💥 Failed to start visual process ${processId}:`, error);
      return {
        success: false,
        message: `Failed to start process: ${error}`
      };
    }
  }

  // Stop a visual process
  async stopVisualProcess(processId: string): Promise<ProcessResponse> {
    try {
      console.log(`🛑 Stopping visual process: ${processId}`);
      
      const request: ProcessStopRequest = {
        process_id: processId
      };

      console.log('🔄 Sending stop request:', request);

      const response = await fetch(`${this.baseUrl}/api/visual/stop`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
      });

      console.log(`📡 Stop API Response - Status: ${response.status}, OK: ${response.ok}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Stop API Error: ${response.status} - ${errorText}`);
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('✅ Stop API Success:', result);
      return result;
    } catch (error) {
      console.error(`💥 Failed to stop visual process ${processId}:`, error);
      return {
        success: false,
        message: `Failed to stop process: ${error}`
      };
    }
  }

  // Get latest visual output for a process
  async getLatestVisualOutput(processId: string): Promise<VisualOutput | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/visual/output/${processId}/latest`);
      if (!response.ok) {
        return null;
      }
      const data = await response.json();
      if (data.error) {
        return null;
      }
      return data;
    } catch (error) {
      console.error(`Failed to get visual output for ${processId}:`, error);
      return null;
    }
  }

  // List all available visual outputs
  async listVisualOutputs(): Promise<Record<string, VisualOutput>> {
    try {
      const response = await fetch(`${this.baseUrl}/api/visual/outputs/list`);
      if (!response.ok) {
        return {};
      }
      const data = await response.json();
      return data.outputs || {};
    } catch (error) {
      console.error('Failed to list visual outputs:', error);
      return {};
    }
  }

  // Connect to real-time visual WebSocket (optional, disabled for now)
  connectToVisualUpdates(): void {
    if (!this.wsEnabled) {
      console.log('🎬 Visual WebSocket disabled - using HTTP polling only');
      return;
    }

    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.warn('🎬 Max WebSocket reconnection attempts reached, disabling WebSocket');
      this.wsEnabled = false;
      return;
    }

    if (this.ws) {
      this.ws.close();
    }

    try {
      this.ws = new WebSocket(this.wsUrl);

      this.ws.onopen = () => {
        console.log('🎬 Connected to Visual WebSocket');
        this.reconnectAttempts = 0; // Reset on successful connection
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'visual_update' && data.processes) {
            // Broadcast visual output updates
            this.outputCallbacks.forEach(callback => callback(data.processes));
          }
        } catch (error) {
          console.error('Failed to parse visual WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('🎬 Visual WebSocket disconnected');
        this.reconnectAttempts++;
        
        // Only attempt to reconnect if enabled and under max attempts
        if (this.wsEnabled && this.reconnectAttempts < this.maxReconnectAttempts) {
          setTimeout(() => this.connectToVisualUpdates(), 5000);
        }
      };

      this.ws.onerror = (error) => {
        console.warn('🎬 Visual WebSocket error (falling back to HTTP polling):', error);
        this.reconnectAttempts++;
        
        // Disable WebSocket after too many errors
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
          this.wsEnabled = false;
          console.log('🎬 WebSocket disabled due to repeated errors - HTTP polling active');
        }
      };
    } catch (error) {
      console.error('Failed to create visual WebSocket:', error);
      this.wsEnabled = false;
    }
  }

  // Subscribe to visual output updates
  subscribeToVisualOutputs(callback: (outputs: Record<string, VisualOutput>) => void): () => void {
    this.outputCallbacks.add(callback);
    return () => this.outputCallbacks.delete(callback);
  }

  // Subscribe to status updates
  subscribeToStatusUpdates(callback: (status: VisualSystemStatus) => void): () => void {
    this.statusCallbacks.add(callback);
    return () => this.statusCallbacks.delete(callback);
  }

  // Poll for status updates and visual outputs
  startStatusPolling(intervalMs: number = 2000): () => void {
    const interval = setInterval(async () => {
      try {
        // Poll status
        const status = await this.getVisualStatus();
        this.statusCallbacks.forEach(callback => callback(status));

        // Poll visual outputs (if no WebSocket)
        if (!this.wsEnabled) {
          const outputs = await this.listVisualOutputs();
          this.outputCallbacks.forEach(callback => callback(outputs));
        }
      } catch (error) {
        console.error('Status polling error:', error);
      }
    }, intervalMs);

    return () => clearInterval(interval);
  }

  // Disconnect from all services
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.outputCallbacks.clear();
    this.statusCallbacks.clear();
    this.wsEnabled = false;
    this.reconnectAttempts = 0;
  }

  // Toggle process (start if stopped, stop if running)
  async toggleProcess(processId: string, currentStatus: boolean, script: string): Promise<ProcessResponse> {
    if (currentStatus) {
      return await this.stopVisualProcess(processId);
    } else {
      return await this.startVisualProcess(processId, script);
    }
  }

  // Enable WebSocket (for future use when backend is fixed)
  enableWebSocket(): void {
    this.wsEnabled = true;
    this.reconnectAttempts = 0;
    this.connectToVisualUpdates();
  }

  // Get connection info
  getConnectionInfo(): { wsEnabled: boolean; reconnectAttempts: number } {
    return {
      wsEnabled: this.wsEnabled,
      reconnectAttempts: this.reconnectAttempts
    };
  }
}

export const visualService = new VisualService(); 