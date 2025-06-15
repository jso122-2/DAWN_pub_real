import { EventEmitter } from '@/lib/EventEmitter';

export interface ProcessHandle {
  id: string;
  script: string;
  args: Record<string, any>;
  pid?: number;
  startTime: number;
  exitCode?: number;
  error?: string;
  status: 'running' | 'completed' | 'error';
}

export interface OutputChunk {
  processId: string;
  data: string;
  timestamp: number;
  stream: 'stdout' | 'stderr';
}

export interface ResourceMetrics {
  processId: string;
  cpu: number; // CPU usage percentage (0-100)
  memory: number; // Memory usage in MB
  timestamp: number;
}

export class PythonExecutor extends EventEmitter {
  private processes: Map<string, ProcessHandle> = new Map();
  private baseUrl: string;

  constructor(baseUrl = 'http://localhost:8001') {
    super();
    this.baseUrl = baseUrl;
  }

  async execute(script: string, args: Record<string, any> = {}): Promise<ProcessHandle> {
    const handle: ProcessHandle = {
      id: `proc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      script,
      args,
      startTime: Date.now(),
      status: 'running'
    };

    try {
      const response = await fetch(`${this.baseUrl}/api/python/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script,
          args,
          processId: handle.id
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      handle.pid = result.pid;

      this.processes.set(handle.id, handle);
      this.emit('process-started', handle);

      return handle;
    } catch (error) {
      handle.status = 'error';
      handle.error = error instanceof Error ? error.message : 'Unknown error';
      this.emit('process-error', handle);
      throw error;
    }
  }

  async kill(processId: string): Promise<void> {
    try {
      await fetch(`${this.baseUrl}/api/python/kill/${processId}`, {
        method: 'DELETE',
      });

      const handle = this.processes.get(processId);
      if (handle) {
        handle.status = 'completed';
        handle.exitCode = -1; // Terminated
        this.processes.delete(processId);
        this.emit('process-completed', handle);
      }
    } catch (error) {
      console.error(`Failed to kill process ${processId}:`, error);
    }
  }

  async getStatus(processId: string): Promise<ProcessHandle | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/python/status/${processId}`);
      if (!response.ok) return null;

      const data = await response.json();
      return data.handle || null;
    } catch {
      return null;
    }
  }

  getActiveProcesses(): ProcessHandle[] {
    return Array.from(this.processes.values()).filter(p => p.status === 'running');
  }

  // Simulate resource metrics (in a real implementation, this would come from the API)
  private startResourceMonitoring() {
    setInterval(() => {
      this.processes.forEach(handle => {
        if (handle.status === 'running') {
          const metrics: ResourceMetrics = {
            processId: handle.id,
            cpu: Math.random() * 100,
            memory: Math.random() * 512,
            timestamp: Date.now()
          };
          this.emit('metrics', metrics);
        }
      });
    }, 1000);
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      // Simulate connection
      setTimeout(() => {
        this.emit('connected');
        this.startResourceMonitoring();
        resolve();
      }, 100);
    });
  }

  disconnect(): void {
    this.processes.clear();
    this.emit('disconnected');
  }
}

// Singleton instance
let executorInstance: PythonExecutor | null = null;

export function getPythonExecutor(): PythonExecutor {
  if (!executorInstance) {
    executorInstance = new PythonExecutor();
    executorInstance.connect().catch(console.error);
  }
  return executorInstance;
} 