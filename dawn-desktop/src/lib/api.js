// DAWN Neural System API Integration
const API_BASE_URL = 'http://localhost:8000'
const WS_URL = 'ws://localhost:8000/ws'

import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';

class DAWNApi {
  constructor() {
    this.isConnected = false
    this.websocket = null
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 10
    this.reconnectDelay = 1000 // Start with 1 second
    this.maxReconnectDelay = 30000 // Max 30 seconds
    this.listeners = new Map()
    this.statusCheckInterval = null
  }

  // HTTP API Functions
  async fetchMetrics() {
    try {
      console.log('🔄 Fetching metrics from backend...')
      const response = await fetch(`${API_BASE_URL}/metrics`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000) // 5 second timeout
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('✅ Metrics fetched successfully:', data)
      return data
    } catch (error) {
      console.error('❌ Failed to fetch metrics:', error)
      throw new Error(`Failed to fetch metrics: ${error.message}`)
    }
  }

  async fetchSubsystems() {
    try {
      console.log('🔄 Fetching subsystems from backend...')
      const response = await fetch(`${API_BASE_URL}/subsystems`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000)
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('✅ Subsystems fetched successfully:', data.length, 'subsystems')
      return data
    } catch (error) {
      console.error('❌ Failed to fetch subsystems:', error)
      throw new Error(`Failed to fetch subsystems: ${error.message}`)
    }
  }

  async checkHealth() {
    try {
      console.log('🏥 Checking backend health...')
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(3000) // Quick health check
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('✅ Backend health check passed:', data)
      return data
    } catch (error) {
      console.error('❌ Backend health check failed:', error)
      throw new Error(`Backend health check failed: ${error.message}`)
    }
  }

  async setAlertThreshold(metric, threshold, direction = 'above') {
    try {
      console.log(`🚨 Setting alert threshold: ${metric} ${direction} ${threshold}`)
      const response = await fetch(`${API_BASE_URL}/alerts/threshold`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          metric,
          threshold,
          direction
        }),
        signal: AbortSignal.timeout(5000)
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log('✅ Alert threshold set successfully:', data)
      return data
    } catch (error) {
      console.error('❌ Failed to set alert threshold:', error)
      throw new Error(`Failed to set alert threshold: ${error.message}`)
    }
  }

  // WebSocket Functions
  connectWebSocket() {
    if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
      console.log('🔗 WebSocket already connected')
      return Promise.resolve()
    }

    return new Promise((resolve, reject) => {
      try {
        console.log('🔌 Connecting to WebSocket...', WS_URL)
        this.websocket = new WebSocket(WS_URL)

        this.websocket.onopen = () => {
          console.log('✅ WebSocket connected successfully')
          this.isConnected = true
          this.reconnectAttempts = 0
          this.reconnectDelay = 1000 // Reset delay
          this.emit('connected')
          resolve()
        }

        this.websocket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            console.log('📨 WebSocket message received:', { 
              scup: data.scup?.toFixed(3), 
              mood: data.mood,
              tick: data.tick_count 
            })
            this.emit('metrics', data)
          } catch (error) {
            console.error('❌ Failed to parse WebSocket message:', error)
            this.emit('error', `Failed to parse message: ${error.message}`)
          }
        }

        this.websocket.onclose = (event) => {
          console.log('🔌 WebSocket connection closed:', event.code, event.reason)
          this.isConnected = false
          this.emit('disconnected')
          
          // Auto-reconnect if not a clean close
          if (event.code !== 1000) {
            this.scheduleReconnect()
          }
        }

        this.websocket.onerror = (error) => {
          console.error('❌ WebSocket error:', error)
          this.isConnected = false
          this.emit('error', 'WebSocket connection error')
          reject(error)
        }

        // Timeout for connection
        setTimeout(() => {
          if (this.websocket.readyState !== WebSocket.OPEN) {
            this.websocket.close()
            reject(new Error('WebSocket connection timeout'))
          }
        }, 10000) // 10 second timeout

      } catch (error) {
        console.error('❌ Failed to create WebSocket:', error)
        reject(error)
      }
    })
  }

  scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('❌ Max WebSocket reconnection attempts reached')
      this.emit('error', 'Max reconnection attempts reached')
      return
    }

    this.reconnectAttempts++
    console.log(`🔄 Scheduling WebSocket reconnection attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${this.reconnectDelay}ms`)

    setTimeout(() => {
      console.log(`🔄 WebSocket reconnection attempt ${this.reconnectAttempts}`)
      this.connectWebSocket().catch(error => {
        console.error('❌ WebSocket reconnection failed:', error)
        // Exponential backoff
        this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay)
        this.scheduleReconnect()
      })
    }, this.reconnectDelay)
  }

  disconnectWebSocket() {
    if (this.websocket) {
      console.log('🔌 Disconnecting WebSocket...')
      this.websocket.close(1000, 'User requested disconnect')
      this.websocket = null
      this.isConnected = false
    }
  }

  // Event System
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event).push(callback)
    
    return () => {
      const callbacks = this.listeners.get(event)
      if (callbacks) {
        const index = callbacks.indexOf(callback)
        if (index > -1) {
          callbacks.splice(index, 1)
        }
      }
    }
  }

  emit(event, data) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      callbacks.forEach(callback => {
        try {
          callback(data)
        } catch (error) {
          console.error(`❌ Error in event callback for ${event}:`, error)
        }
      })
    }
  }

  // Connection Status
  getConnectionStatus() {
    return {
      connected: this.isConnected,
      websocket: this.websocket?.readyState === WebSocket.OPEN,
      reconnectAttempts: this.reconnectAttempts
    }
  }

  // Control methods
  async start() {
    try {
      const result = await invoke('start_tick_engine');
      console.log('Tick engine started:', result);
      return result;
    } catch (error) {
      console.error('Failed to start tick engine:', error);
      throw error;
    }
  }
  
  async stop() {
    try {
      const result = await invoke('stop_tick_engine');
      console.log('Tick engine stopped:', result);
      return result;
    } catch (error) {
      console.error('Failed to stop tick engine:', error);
      throw error;
    }
  }
  
  async pause() {
    try {
      const result = await invoke('pause_tick_engine');
      console.log('Tick engine paused:', result);
      return result;
    } catch (error) {
      console.error('Failed to pause tick engine:', error);
      throw error;
    }
  }
  
  async resume() {
    try {
      const result = await invoke('resume_tick_engine');
      console.log('Tick engine resumed:', result);
      return result;
    } catch (error) {
      console.error('Failed to resume tick engine:', error);
      throw error;
    }
  }
  
  async step() {
    try {
      // Using execute_single_tick as the step method
      const result = await invoke('execute_single_tick');
      console.log('Tick engine step executed:', result);
      return result;
    } catch (error) {
      console.error('Failed to execute tick step:', error);
      throw error;
    }
  }
  
  async setTiming(intervalMs) {
    try {
      const result = await invoke('set_tick_timing', { intervalMs });
      console.log('Tick timing updated:', result);
      return result;
    } catch (error) {
      console.error('Failed to set tick timing:', error);
      throw error;
    }
  }
  
  async getStatus() {
    try {
      const result = await invoke('get_tick_status');
      this.isConnected = true;
      return result;
    } catch (error) {
      console.error('Failed to get tick status:', error);
      this.isConnected = false;
      throw error;
    }
  }
  
  // Configuration methods
  async getConfig() {
    try {
      const result = await invoke('get_tick_config');
      console.log('Tick config retrieved:', result);
      return result;
    } catch (error) {
      console.error('Failed to get tick config:', error);
      throw error;
    }
  }
  
  async updateConfig(config) {
    try {
      const result = await invoke('update_tick_config', { config });
      console.log('Tick config updated:', result);
      return result;
    } catch (error) {
      console.error('Failed to update tick config:', error);
      throw error;
    }
  }
  
  // Subsystem management (These would need corresponding Rust commands)
  async addSubsystem(name, config) {
    try {
      // Note: This command would need to be implemented in the Rust backend
      const result = await invoke('add_subsystem', { name, config });
      console.log('Subsystem added:', result);
      return result;
    } catch (error) {
      console.error('Failed to add subsystem:', error);
      // Fallback: return a mock response for now
      return { success: false, error: 'Subsystem management not yet implemented in backend' };
    }
  }
  
  async removeSubsystem(id) {
    try {
      // Note: This command would need to be implemented in the Rust backend
      const result = await invoke('remove_subsystem', { id });
      console.log('Subsystem removed:', result);
      return result;
    } catch (error) {
      console.error('Failed to remove subsystem:', error);
      // Fallback: return a mock response for now
      return { success: false, error: 'Subsystem management not yet implemented in backend' };
    }
  }
  
  async updateSubsystem(id, config) {
    try {
      // Note: This command would need to be implemented in the Rust backend
      const result = await invoke('update_subsystem', { id, config });
      console.log('Subsystem updated:', result);
      return result;
    } catch (error) {
      console.error('Failed to update subsystem:', error);
      // Fallback: return a mock response for now
      return { success: false, error: 'Subsystem management not yet implemented in backend' };
    }
  }
  
  // Event subscriptions
  onTickUpdate(callback) {
    const unlisten = listen('tick-update', (event) => {
      try {
        // Handle both TickUpdate and legacy Metrics formats
        const payload = event.payload;
        if (payload) {
          callback(payload);
        }
      } catch (error) {
        console.error('Error in tick update callback:', error);
      }
    });
    
    this.listeners.set(callback, unlisten);
    
    // Return unsubscribe function
    return () => this.removeListener(callback);
  }
  
  onMetricsUpdate(callback) {
    const unlisten = listen('metrics-update', (event) => {
      try {
        const payload = event.payload;
        if (payload) {
          callback(payload);
        }
      } catch (error) {
        console.error('Error in metrics update callback:', error);
      }
    });
    
    this.listeners.set(callback, unlisten);
    
    // Return unsubscribe function
    return () => this.removeListener(callback);
  }
  
  onStatusChange(callback) {
    const unlisten = listen('status-change', (event) => {
      try {
        const payload = event.payload;
        if (payload) {
          callback(payload);
        }
      } catch (error) {
        console.error('Error in status change callback:', error);
      }
    });
    
    this.listeners.set(callback, unlisten);
    
    // Return unsubscribe function
    return () => this.removeListener(callback);
  }
  
  removeListener(callback) {
    const unlisten = this.listeners.get(callback);
    if (unlisten) {
      unlisten.then(fn => fn()).catch(err => console.error('Error removing listener:', err));
      this.listeners.delete(callback);
    }
  }
  
  // Utility methods
  async healthCheck() {
    try {
      const status = await this.getStatus();
      return { 
        healthy: true, 
        connected: this.isConnected,
        status 
      };
    } catch (error) {
      return { 
        healthy: false, 
        connected: false,
        error: error.message 
      };
    }
  }
  
  startStatusMonitoring(intervalMs = 5000) {
    if (this.statusCheckInterval) {
      clearInterval(this.statusCheckInterval);
    }
    
    this.statusCheckInterval = setInterval(async () => {
      try {
        await this.getStatus();
      } catch (error) {
        console.warn('Status check failed:', error);
      }
    }, intervalMs);
  }
  
  stopStatusMonitoring() {
    if (this.statusCheckInterval) {
      clearInterval(this.statusCheckInterval);
      this.statusCheckInterval = null;
    }
  }
  
  // Cleanup method
  cleanup() {
    // Remove all listeners
    for (const [callback, unlisten] of this.listeners) {
      unlisten.then(fn => fn()).catch(err => console.error('Error during cleanup:', err));
    }
    this.listeners.clear();
    
    // Stop status monitoring
    this.stopStatusMonitoring();
  }
  
  // Batch operations
  async batchControl(operations) {
    const results = [];
    for (const operation of operations) {
      try {
        let result;
        switch (operation.type) {
          case 'start':
            result = await this.start();
            break;
          case 'stop':
            result = await this.stop();
            break;
          case 'pause':
            result = await this.pause();
            break;
          case 'resume':
            result = await this.resume();
            break;
          case 'step':
            result = await this.step();
            break;
          case 'setTiming':
            result = await this.setTiming(operation.params.intervalMs);
            break;
          default:
            throw new Error(`Unknown operation type: ${operation.type}`);
        }
        results.push({ operation, result, success: true });
      } catch (error) {
        results.push({ operation, error: error.message, success: false });
      }
    }
    return results;
  }
  
  // Convenience methods
  async toggle() {
    try {
      const status = await this.getStatus();
      if (status.is_running) {
        return await this.stop();
      } else {
        return await this.start();
      }
    } catch (error) {
      console.error('Failed to toggle tick engine:', error);
      throw error;
    }
  }
  
  async restart() {
    try {
      await this.stop();
      // Small delay to ensure clean stop
      await new Promise(resolve => setTimeout(resolve, 100));
      return await this.start();
    } catch (error) {
      console.error('Failed to restart tick engine:', error);
      throw error;
    }
  }
}

// Singleton instance
const dawnApi = new DAWNApi()

// Convenience functions
export const fetchMetrics = () => dawnApi.fetchMetrics()
export const fetchSubsystems = () => dawnApi.fetchSubsystems()
export const checkBackendHealth = () => dawnApi.checkHealth()
export const setAlertThreshold = (metric, threshold, direction) => 
  dawnApi.setAlertThreshold(metric, threshold, direction)

export const connectWebSocket = () => dawnApi.connectWebSocket()
export const disconnectWebSocket = () => dawnApi.disconnectWebSocket()
export const onMetricsUpdate = (callback) => dawnApi.on('metrics', callback)
export const onConnectionChange = (callback) => {
  const unsubscribeConnected = dawnApi.on('connected', () => callback(true))
  const unsubscribeDisconnected = dawnApi.on('disconnected', () => callback(false))
  
  return () => {
    unsubscribeConnected()
    unsubscribeDisconnected()
  }
}
export const onError = (callback) => dawnApi.on('error', callback)
export const getConnectionStatus = () => dawnApi.getConnectionStatus()

export default dawnApi 