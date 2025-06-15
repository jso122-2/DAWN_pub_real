import React, { useEffect, useRef, useState, useCallback } from 'react';
import { EventEmitter } from '@/lib/EventEmitter';

/**
 * Python Executor Service - Backend Communication Interface
 * 
 * Handles real-time communication with Python execution backends via WebSocket.
 * Manages process lifecycle, streams output, and provides resource monitoring.
 * 
 * @example
 * ```tsx
 * const executor = new PythonExecutorService({
 *   wsUrl: 'ws://localhost:8001/python-executor',
 *   emitter: eventEmitter
 * });
 * 
 * // Execute a script
 * executor.executeScript({
 *   script: 'sequence_analyzer.py',
 *   params: { sequence: 'ATCG', method: 'kmp' },
 *   category: 'Genomic Processing'
 * });
 * ```
 */

// Process execution types
export type ProcessStatus = 'idle' | 'running' | 'completed' | 'error' | 'queued' | 'terminated';
export type ProcessPriority = 'low' | 'normal' | 'high' | 'critical';

// Process execution request
export interface ExecutionRequest {
  script: string;
  params: Record<string, any>;
  category: string;
  priority?: ProcessPriority;
  timeout?: number; // milliseconds
  workingDir?: string;
  environment?: Record<string, string>;
}

// Process execution response
export interface ExecutionResponse {
  processId: string;
  status: ProcessStatus;
  output?: string;
  error?: string;
  progress?: number;
  resourceUsage?: {
    cpu: number;
    memory: number;
    duration: number;
  };
  exitCode?: number;
  metadata?: Record<string, any>;
}

// WebSocket message types
interface WSMessage {
  type: 'execute' | 'kill' | 'status' | 'output' | 'error' | 'complete' | 'heartbeat' | 'resource_update';
  processId?: string;
  data?: any;
  timestamp: number;
}

// Service configuration
interface PythonExecutorConfig {
  wsUrl: string;
  reconnectAttempts?: number;
  reconnectDelay?: number;
  heartbeatInterval?: number;
  defaultTimeout?: number;
  maxConcurrentProcesses?: number;
}

// Service events
interface ExecutorEvents {
  'connection-status': { connected: boolean; error?: string };
  'process-start': { processId: string; request: ExecutionRequest };
  'process-output': { processId: string; output: string; type: 'stdout' | 'stderr' };
  'process-progress': { processId: string; progress: number; stage?: string };
  'process-complete': { processId: string; exitCode: number; duration: number };
  'process-error': { processId: string; error: string; details?: any };
  'resource-update': { processId: string; cpu: number; memory: number };
  'service-error': { error: string; code?: string };
}

export class PythonExecutorService {
  private ws: WebSocket | null = null;
  private emitter: EventEmitter;
  private config: Required<PythonExecutorConfig>;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private reconnectCount = 0;
  private isConnected = false;
  private activeProcesses = new Map<string, ExecutionRequest>();
  private messageQueue: WSMessage[] = [];

  constructor(config: PythonExecutorConfig, emitter?: EventEmitter) {
    this.emitter = emitter || new EventEmitter();
    this.config = {
      wsUrl: config.wsUrl,
      reconnectAttempts: config.reconnectAttempts ?? 5,
      reconnectDelay: config.reconnectDelay ?? 3000,
      heartbeatInterval: config.heartbeatInterval ?? 30000,
      defaultTimeout: config.defaultTimeout ?? 300000, // 5 minutes
      maxConcurrentProcesses: config.maxConcurrentProcesses ?? 10
    };
  }

  // Initialize WebSocket connection
  async connect(): Promise<boolean> {
    try {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        return true;
      }

      this.ws = new WebSocket(this.config.wsUrl);
      
      this.ws.onopen = this.handleOpen.bind(this);
      this.ws.onmessage = this.handleMessage.bind(this);
      this.ws.onerror = this.handleError.bind(this);
      this.ws.onclose = this.handleClose.bind(this);

      return new Promise((resolve) => {
        const timeout = setTimeout(() => resolve(false), 5000);
        
        this.ws!.onopen = () => {
          clearTimeout(timeout);
          this.handleOpen();
          resolve(true);
        };
      });
    } catch (error) {
      this.emitError('Failed to create WebSocket connection', error);
      return false;
    }
  }

  // Handle WebSocket open
  private handleOpen(): void {
    this.isConnected = true;
    this.reconnectCount = 0;
    
    // Clear reconnect timer
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    // Start heartbeat
    this.startHeartbeat();

    // Process queued messages
    this.processMessageQueue();

    this.emitter.emit('connection-status', { connected: true });
    console.log('🐍 Python Executor Service: Connected');
  }

  // Handle WebSocket message
  private handleMessage(event: MessageEvent): void {
    try {
      const message: WSMessage = JSON.parse(event.data);
      
      switch (message.type) {
        case 'output':
          this.handleProcessOutput(message);
          break;
        case 'error':
          this.handleProcessError(message);
          break;
        case 'complete':
          this.handleProcessComplete(message);
          break;
        case 'status':
          this.handleStatusUpdate(message);
          break;
        case 'resource_update':
          this.handleResourceUpdate(message);
          break;
        case 'heartbeat':
          // Heartbeat acknowledged
          break;
        default:
          console.warn('Unknown message type:', message.type);
      }
    } catch (error) {
      this.emitError('Failed to parse WebSocket message', error);
    }
  }

  // Handle WebSocket error
  private handleError(event: Event): void {
    this.emitError('WebSocket error occurred', event);
  }

  // Handle WebSocket close
  private handleClose(event: CloseEvent): void {
    this.isConnected = false;
    this.stopHeartbeat();

    this.emitter.emit('connection-status', { 
      connected: false, 
      error: `Connection closed: ${event.reason}` 
    });

    // Attempt reconnection if not intentional
    if (event.code !== 1000 && this.reconnectCount < this.config.reconnectAttempts) {
      this.scheduleReconnect();
    }

    console.log('🐍 Python Executor Service: Disconnected');
  }

  // Schedule reconnection attempt
  private scheduleReconnect(): void {
    this.reconnectCount++;
    const delay = this.config.reconnectDelay * Math.pow(2, this.reconnectCount - 1); // Exponential backoff
    
    this.reconnectTimer = setTimeout(() => {
      console.log(`🐍 Reconnection attempt ${this.reconnectCount}/${this.config.reconnectAttempts}`);
      this.connect();
    }, delay);
  }

  // Start heartbeat mechanism
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.isConnected) {
        this.sendMessage({
          type: 'heartbeat',
          timestamp: Date.now()
        });
      }
    }, this.config.heartbeatInterval);
  }

  // Stop heartbeat mechanism
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  // Send WebSocket message
  private sendMessage(message: WSMessage): void {
    if (this.isConnected && this.ws) {
      try {
        this.ws.send(JSON.stringify(message));
      } catch (error) {
        this.emitError('Failed to send WebSocket message', error);
      }
    } else {
      // Queue message for later
      this.messageQueue.push(message);
    }
  }

  // Process queued messages
  private processMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      if (message) {
        this.sendMessage(message);
      }
    }
  }

  // Execute Python script
  async executeScript(request: ExecutionRequest): Promise<string> {
    // Check concurrent process limit
    if (this.activeProcesses.size >= this.config.maxConcurrentProcesses) {
      throw new Error(`Maximum concurrent processes (${this.config.maxConcurrentProcesses}) exceeded`);
    }

    const processId = `${request.script}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    // Store process info
    this.activeProcesses.set(processId, request);

    // Send execution request
    this.sendMessage({
      type: 'execute',
      processId,
      data: {
        script: request.script,
        params: request.params,
        category: request.category,
        priority: request.priority || 'normal',
        timeout: request.timeout || this.config.defaultTimeout,
        workingDir: request.workingDir,
        environment: request.environment
      },
      timestamp: Date.now()
    });

    // Emit process start event
    this.emitter.emit('process-start', { processId, request });

    return processId;
  }

  // Kill running process
  killProcess(processId: string): void {
    if (this.activeProcesses.has(processId)) {
      this.sendMessage({
        type: 'kill',
        processId,
        timestamp: Date.now()
      });
    }
  }

  // Get process status
  getProcessStatus(processId: string): void {
    this.sendMessage({
      type: 'status',
      processId,
      timestamp: Date.now()
    });
  }

  // Handle process output
  private handleProcessOutput(message: WSMessage): void {
    if (message.processId && message.data) {
      this.emitter.emit('process-output', {
        processId: message.processId,
        output: message.data.output,
        type: message.data.type || 'stdout'
      });

      // Update progress if provided
      if (message.data.progress !== undefined) {
        this.emitter.emit('process-progress', {
          processId: message.processId,
          progress: message.data.progress,
          stage: message.data.stage
        });
      }
    }
  }

  // Handle process error
  private handleProcessError(message: WSMessage): void {
    if (message.processId) {
      this.activeProcesses.delete(message.processId);
      
      this.emitter.emit('process-error', {
        processId: message.processId,
        error: message.data?.error || 'Unknown error',
        details: message.data?.details
      });
    }
  }

  // Handle process completion
  private handleProcessComplete(message: WSMessage): void {
    if (message.processId) {
      this.activeProcesses.delete(message.processId);
      
      this.emitter.emit('process-complete', {
        processId: message.processId,
        exitCode: message.data?.exitCode || 0,
        duration: message.data?.duration || 0
      });
    }
  }

  // Handle status update
  private handleStatusUpdate(message: WSMessage): void {
    if (message.processId && message.data) {
      // Emit status-specific events based on data
      if (message.data.progress !== undefined) {
        this.emitter.emit('process-progress', {
          processId: message.processId,
          progress: message.data.progress,
          stage: message.data.stage
        });
      }
    }
  }

  // Handle resource update
  private handleResourceUpdate(message: WSMessage): void {
    if (message.processId && message.data) {
      this.emitter.emit('resource-update', {
        processId: message.processId,
        cpu: message.data.cpu || 0,
        memory: message.data.memory || 0
      });
    }
  }

  // Emit error event
  private emitError(message: string, error?: any): void {
    console.error(`🐍 Python Executor Service Error: ${message}`, error);
    this.emitter.emit('service-error', { 
      error: message, 
      code: error?.code 
    });
  }

  // Get active processes
  getActiveProcesses(): string[] {
    return Array.from(this.activeProcesses.keys());
  }

  // Get connection status
  isServiceConnected(): boolean {
    return this.isConnected;
  }

  // Cleanup and disconnect
  disconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    this.stopHeartbeat();

    if (this.ws) {
      this.ws.close(1000, 'Service shutdown');
      this.ws = null;
    }

    this.isConnected = false;
    this.activeProcesses.clear();
    this.messageQueue = [];
  }
}

// React hook for using the Python Executor Service
export function usePythonExecutor(config: PythonExecutorConfig) {
  const [service, setService] = useState<PythonExecutorService | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [activeProcesses, setActiveProcesses] = useState<string[]>([]);
  const emitterRef = useRef<EventEmitter>(new EventEmitter());

  // Initialize service
  useEffect(() => {
    const executor = new PythonExecutorService(config, emitterRef.current);
    setService(executor);

    // Setup event listeners
    const handleConnectionStatus = (data: { connected: boolean; error?: string }) => {
      setIsConnected(data.connected);
      if (data.error) {
        console.error('Connection error:', data.error);
      }
    };

    const handleProcessStart = (data: { processId: string; request: ExecutionRequest }) => {
      setActiveProcesses(prev => [...prev, data.processId]);
    };

    const handleProcessComplete = (data: { processId: string; exitCode: number; duration: number }) => {
      setActiveProcesses(prev => prev.filter(id => id !== data.processId));
    };

    const handleProcessError = (data: { processId: string; error: string; details?: any }) => {
      setActiveProcesses(prev => prev.filter(id => id !== data.processId));
    };

    emitterRef.current.on('connection-status', handleConnectionStatus);
    emitterRef.current.on('process-start', handleProcessStart);
    emitterRef.current.on('process-complete', handleProcessComplete);
    emitterRef.current.on('process-error', handleProcessError);

    // Auto-connect
    executor.connect();

    // Cleanup
    return () => {
      emitterRef.current.off('connection-status', handleConnectionStatus);
      emitterRef.current.off('process-start', handleProcessStart);
      emitterRef.current.off('process-complete', handleProcessComplete);
      emitterRef.current.off('process-error', handleProcessError);
      executor.disconnect();
    };
  }, [config.wsUrl]);

  // Execute script wrapper
  const executeScript = useCallback(async (request: ExecutionRequest): Promise<string> => {
    if (!service) {
      throw new Error('Python Executor Service not initialized');
    }
    return service.executeScript(request);
  }, [service]);

  // Kill process wrapper
  const killProcess = useCallback((processId: string): void => {
    if (service) {
      service.killProcess(processId);
    }
  }, [service]);

  return {
    service,
    isConnected,
    activeProcesses,
    executeScript,
    killProcess,
    emitter: emitterRef.current
  };
}

// Export default instance
export default getPythonExecutor();