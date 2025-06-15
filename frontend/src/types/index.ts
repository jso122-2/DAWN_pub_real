export interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
}

export interface PythonProcess {
  script: string;
  status: 'running' | 'completed' | 'error';
  output: any;
}

export interface ModuleStatus {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'error';
  lastTick: number;
  metrics: {
    scup: number;
    entropy: number;
  };
}

export interface WebSocketMessage {
  type: 'tick' | 'module_status' | 'error' | 'visualization' | 'request_visualization' | 'connection_status';
  data: TickData | ModuleStatus | string | any;
  timestamp?: string;
} 