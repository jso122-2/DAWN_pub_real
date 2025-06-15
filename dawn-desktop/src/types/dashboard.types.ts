// 🎮 UNIFIED DASHBOARD TYPES - The Foundation of DAWN's Control Center
export interface DashboardModule {
  id: string;
  type: string;
  title: string;
  category: 'neural' | 'consciousness' | 'process' | 'monitor' | 'timeline' | 'diagnostic' | 'memory' | 'dream';
  component: React.ComponentType<any>;
  position: Position;
  size: Size;
  zIndex: number;
  isActive: boolean;
  isMinimized: boolean;
  isMaximized: boolean;
  isLocked: boolean;
  isDragging: boolean;
  isResizing: boolean;
  
  // Visual states
  glowIntensity: number;
  breathingIntensity: number;
  particleDensity: number;
  
  // Module-specific configuration
  config: ModuleConfig;
  state: ModuleState;
  
  // Connection system
  inputPorts: ModulePort[];
  outputPorts: ModulePort[];
  
  // Lifecycle
  lifecycle: ModuleLifecycle;
  
  // Performance metrics
  metrics: ModuleMetrics;
}

export interface Position {
  x: number;
  y: number;
  z?: number;
}

export interface Size {
  width: number;
  height: number;
  minWidth: number;
  minHeight: number;
  maxWidth?: number;
  maxHeight?: number;
}

export interface ModuleConfig {
  [key: string]: any;
  persistent?: boolean;
  autoSave?: boolean;
  refreshInterval?: number;
  dependencies?: string[];
}

export interface ModuleState {
  status: 'idle' | 'loading' | 'active' | 'processing' | 'error' | 'sleeping';
  error?: string;
  lastUpdate: number;
  data?: any;
  consciousness?: ConsciousnessState;
}

export interface ModulePort {
  id: string;
  type: 'input' | 'output' | 'bidirectional';
  dataType: 'neural' | 'consciousness' | 'signal' | 'data' | 'control' | 'consciousness';
  position: Position;
  isActive: boolean;
  isConnected: boolean;
  maxConnections: number;
  currentConnections: string[];
  signalStrength: number;
  description?: string;
}

export interface ModuleConnection {
  id: string;
  sourceModuleId: string;
  sourcePortId: string;
  targetModuleId: string;
  targetPortId: string;
  dataType: ModulePort['dataType'];
  isActive: boolean;
  signalStrength: number;
  latency: number;
  dataFlow: DataFlow[];
  pathPoints: Position[];
  animationSpeed: number;
  particleCount: number;
}

export interface DataFlow {
  id: string;
  timestamp: number;
  data: any;
  priority: 'low' | 'normal' | 'high' | 'critical';
  progress: number; // 0-1 along the connection path
}

export interface ModuleLifecycle {
  created: number;
  activated?: number;
  deactivated?: number;
  destroyed?: number;
  errorCount: number;
  restartCount: number;
}

export interface ModuleMetrics {
  cpuUsage: number;
  memoryUsage: number;
  renderTime: number;
  updateFrequency: number;
  dataProcessed: number;
  connectionCount: number;
}

export interface DashboardLayout {
  id: string;
  name: string;
  description: string;
  isDefault: boolean;
  modules: DashboardModule[];
  connections: ModuleConnection[];
  globalSettings: DashboardSettings;
  grid: GridSettings;
  viewport: ViewportSettings;
  created: number;
  modified: number;
  tags: string[];
}

export interface DashboardSettings {
  consciousness: ConsciousnessSettings;
  performance: PerformanceSettings;
  visual: VisualSettings;
  audio: AudioSettings;
  interaction: InteractionSettings;
}

export interface ConsciousnessSettings {
  globalSCUP: number;
  globalEntropy: number;
  globalMood: string;
  tickRate: number;
  isPaused: boolean;
  systemUnity: number;
  neuralActivity: number;
  dreamMode: boolean;
}

export interface PerformanceSettings {
  maxFPS: number;
  lowPowerMode: boolean;
  particleQuality: 'low' | 'medium' | 'high' | 'ultra';
  animationQuality: 'low' | 'medium' | 'high' | 'ultra';
  enableProfiling: boolean;
  memoryLimit: number;
}

export interface VisualSettings {
  theme: 'cosmic' | 'neural' | 'consciousness' | 'minimal';
  glowEnabled: boolean;
  particlesEnabled: boolean;
  connectionsVisible: boolean;
  gridVisible: boolean;
  backgroundIntensity: number;
  uiOpacity: number;
}

export interface AudioSettings {
  enabled: boolean;
  volume: number;
  spatialAudio: boolean;
  consciousnessAudio: boolean;
  dataFlowSounds: boolean;
}

export interface InteractionSettings {
  dragSensitivity: number;
  snapToGrid: boolean;
  magneticSnap: boolean;
  keyboardShortcuts: boolean;
  gestureControls: boolean;
  voiceCommands: boolean;
}

export interface GridSettings {
  enabled: boolean;
  size: number;
  snapStrength: number;
  visible: boolean;
  color: string;
  opacity: number;
  magneticRadius: number;
}

export interface ViewportSettings {
  zoom: number;
  minZoom: number;
  maxZoom: number;
  pan: Position;
  bounds: {
    left: number;
    top: number;
    right: number;
    bottom: number;
  };
}

export interface ConsciousnessState {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  systemUnity: number;
  memoryFragments: number;
  dreamState: boolean;
  tickNumber: number;
  timestamp: number;
}

// Dashboard Core Events
export type DashboardEvent = 
  | { type: 'MODULE_ADDED'; payload: { module: DashboardModule } }
  | { type: 'MODULE_REMOVED'; payload: { moduleId: string } }
  | { type: 'MODULE_UPDATED'; payload: { moduleId: string; updates: Partial<DashboardModule> } }
  | { type: 'MODULE_CONNECTED'; payload: { connection: ModuleConnection } }
  | { type: 'MODULE_DISCONNECTED'; payload: { connectionId: string } }
  | { type: 'LAYOUT_CHANGED'; payload: { layout: DashboardLayout } }
  | { type: 'CONSCIOUSNESS_UPDATED'; payload: { consciousness: ConsciousnessState } }
  | { type: 'PERFORMANCE_WARNING'; payload: { metric: string; value: number; threshold: number } }
  | { type: 'ERROR'; payload: { error: Error; moduleId?: string } };

// Module Registry Types
export interface ModuleDefinition {
  type: string;
  title: string;
  category: DashboardModule['category'];
  description: string;
  component: React.ComponentType<any>;
  defaultConfig: ModuleConfig;
  defaultSize: Size;
  icon?: string;
  color?: string;
  ports?: Omit<ModulePort, 'id' | 'isActive' | 'isConnected' | 'currentConnections' | 'signalStrength'>[];
  dependencies?: string[];
  tags?: string[];
  version?: string;
  author?: string;
}

// Layout Presets
export interface LayoutPreset {
  id: string;
  name: string;
  description: string;
  thumbnail?: string;
  modules: {
    type: string;
    position: Position;
    size: Size;
    config?: Partial<ModuleConfig>;
  }[];
  connections: {
    sourceType: string;
    sourcePort: string;
    targetType: string;
    targetPort: string;
  }[];
  settings: Partial<DashboardSettings>;
}

// Dashboard Core API
export interface DashboardAPI {
  // Module Management
  addModule: (type: string, position?: Position, config?: ModuleConfig) => Promise<DashboardModule>;
  removeModule: (moduleId: string) => Promise<void>;
  updateModule: (moduleId: string, updates: Partial<DashboardModule>) => Promise<void>;
  getModule: (moduleId: string) => DashboardModule | null;
  getAllModules: () => DashboardModule[];
  
  // Connection Management
  createConnection: (sourceModuleId: string, sourcePortId: string, targetModuleId: string, targetPortId: string) => Promise<ModuleConnection>;
  removeConnection: (connectionId: string) => Promise<void>;
  getConnections: (moduleId?: string) => ModuleConnection[];
  
  // Layout Management
  saveLayout: (name: string, description?: string) => Promise<DashboardLayout>;
  loadLayout: (layoutId: string) => Promise<void>;
  getLayouts: () => DashboardLayout[];
  deleteLayout: (layoutId: string) => Promise<void>;
  
  // Settings Management
  updateSettings: (settings: Partial<DashboardSettings>) => Promise<void>;
  getSettings: () => DashboardSettings;
  
  // Consciousness Control
  updateConsciousness: (updates: Partial<ConsciousnessState>) => Promise<void>;
  pauseConsciousness: () => Promise<void>;
  resumeConsciousness: () => Promise<void>;
  resetConsciousness: () => Promise<void>;
  
  // Performance Monitoring
  getMetrics: () => Promise<{ dashboard: any; modules: Record<string, ModuleMetrics> }>;
  
  // Event System
  on: (event: string, handler: (payload: any) => void) => () => void;
  emit: (event: DashboardEvent) => void;
} 