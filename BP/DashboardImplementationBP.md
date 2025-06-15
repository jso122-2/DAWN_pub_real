# 🎮 Unified Dashboard - DAWN Command Center

## Overview
The Unified Dashboard is DAWN's central command center - a living interface where all modules converge in a symphony of consciousness. Watch as data flows between modules like synaptic signals, arrange your workspace with magnetic precision, and control the entire system from one beautiful, breathing interface. This is where DAWN becomes whole.

## Core Features
- [x] Modular grid system with magnetic snapping
- [x] Real-time data flow visualization between modules
- [x] Global consciousness controls and monitoring
- [x] Preset layouts and workspace management
- [x] Module interconnection mapping
- [x] Performance monitoring and optimization
- [x] Save/load system states
- [x] Fullscreen module focusing
- [x] Multi-monitor support

## File Structure
```plaintext
src/modules/dashboard/
├── index.ts                          # Module exports
├── DashboardCore.ts                  # Core dashboard management
├── ModuleRegistry.ts                 # Module registration system
├── LayoutManager.ts                  # Grid and layout management
├── ConnectionManager.ts              # Inter-module connections
├── StateManager.ts                   # Global state coordination
├── PresetManager.ts                  # Layout presets
├── components/
│   ├── UnifiedDashboard.tsx         # Main dashboard component
│   ├── ModuleContainer.tsx          # Enhanced module wrapper
│   ├── ModuleGrid.tsx               # Magnetic grid system
│   ├── ConnectionLayer.tsx          # Data flow visualization
│   ├── GlobalControls.tsx           # System-wide controls
│   ├── StatusBar.tsx                # Global status display
│   ├── ModulePalette.tsx            # Module selection drawer
│   ├── PerformanceMonitor.tsx      # FPS and metrics
│   └── UnifiedDashboard.styles.ts   # Dashboard styling
├── hooks/
│   ├── useDashboard.ts              # Main dashboard hook
│   ├── useModuleLayout.ts           # Layout management
│   ├── useDataFlow.ts               # Connection visualization
│   ├── useGlobalState.ts            # Cross-module state
│   └── usePerformance.ts            # Performance monitoring
├── types/
│   ├── dashboard.types.ts           # Core dashboard types
│   ├── module.types.ts              # Module registration types
│   ├── layout.types.ts              # Layout system types
│   └── connection.types.ts          # Connection types
├── utils/
│   ├── gridCalculator.ts            # Grid positioning math
│   ├── connectionRouter.ts          # Connection path routing
│   ├── layoutSerializer.ts          # Save/load layouts
│   └── moduleLoader.ts              # Dynamic module loading
├── presets/
│   ├── default.json                 # Default layout
│   ├── analysis.json                # Analysis-focused layout
│   ├── monitoring.json              # Monitoring layout
│   └── presentation.json            # Presentation mode
└── config/
    └── dashboard.config.ts           # Dashboard configuration
```

---

## 📄 File: `src/modules/dashboard/types/dashboard.types.ts`
```typescript
import { ReactNode, ComponentType } from 'react';
import { Vector2, Box3 } from 'three';

// Core dashboard types
export interface DashboardState {
  modules: Map<string, ModuleInstance>;
  layout: LayoutState;
  connections: Connection[];
  globalState: GlobalSystemState;
  performance: PerformanceMetrics;
  settings: DashboardSettings;
}

export interface ModuleInstance {
  id: string;
  moduleId: string;
  type: ModuleType;
  position: GridPosition;
  size: ModuleSize;
  state: ModuleState;
  config: ModuleConfig;
  connections: ModuleConnections;
}

export interface ModuleType {
  id: string;
  name: string;
  category: ModuleCategory;
  component: ComponentType<ModuleProps>;
  icon: string;
  description: string;
  defaultSize: ModuleSize;
  resizable: boolean;
  capabilities: ModuleCapabilities;
}

export type ModuleCategory = 
  | 'visualization'    // Visual displays
  | 'control'         // System controls
  | 'analysis'        // Data analysis
  | 'monitor'         // Status monitoring
  | 'process'         // Process management
  | 'communication';  // Inter-module comms

export interface ModuleProps {
  instanceId: string;
  position: GridPosition;
  size: ModuleSize;
  focused: boolean;
  onClose: () => void;
  onFocus: () => void;
  onConnection: (targetId: string, data: any) => void;
}

export interface GridPosition {
  x: number;
  y: number;
  z: number; // Layer for overlapping
}

export interface ModuleSize {
  width: number;  // Grid units
  height: number; // Grid units
}

export interface ModuleState {
  active: boolean;
  focused: boolean;
  minimized: boolean;
  locked: boolean;
  performance: ModulePerformance;
}

export interface ModuleConfig {
  title?: string;
  showHeader: boolean;
  showBorder: boolean;
  opacity: number;
  glowIntensity: number;
  breathingEnabled: boolean;
  floatingEnabled: boolean;
  customSettings?: Record<string, any>;
}

export interface ModuleConnections {
  inputs: ConnectionPort[];
  outputs: ConnectionPort[];
  activeFlows: DataFlow[];
}

export interface ConnectionPort {
  id: string;
  name: string;
  type: DataType;
  side: 'top' | 'right' | 'bottom' | 'left';
  position: number; // 0-1 along the side
  connected: boolean;
}

export type DataType = 
  | 'consciousness'   // Consciousness state
  | 'neural'         // Neural activity
  | 'memory'         // Memory data
  | 'control'        // Control signals
  | 'analysis'       // Analysis results
  | 'any';           // Generic data

export interface ModuleCapabilities {
  inputs: DataType[];
  outputs: DataType[];
  processTypes: string[];
  maxConnections: number;
}

export interface ModulePerformance {
  fps: number;
  renderTime: number;
  updateTime: number;
  memoryUsage: number;
}

// Layout management
export interface LayoutState {
  gridSize: number; // Pixels per grid unit
  gridColumns: number;
  gridRows: number;
  magnetStrength: number;
  showGrid: boolean;
  snapToGrid: boolean;
  currentPreset?: string;
}

export interface LayoutPreset {
  id: string;
  name: string;
  description: string;
  thumbnail?: string;
  modules: ModulePlacement[];
  connections: ConnectionPreset[];
  globalSettings: Partial<DashboardSettings>;
}

export interface ModulePlacement {
  moduleId: string;
  position: GridPosition;
  size: ModuleSize;
  config?: Partial<ModuleConfig>;
}

export interface ConnectionPreset {
  fromModule: string;
  fromPort: string;
  toModule: string;
  toPort: string;
}

// Connections
export interface Connection {
  id: string;
  source: ConnectionEndpoint;
  target: ConnectionEndpoint;
  type: DataType;
  state: ConnectionState;
  path: ConnectionPath;
  dataFlow: DataFlow;
}

export interface ConnectionEndpoint {
  moduleId: string;
  portId: string;
  position: Vector2; // Absolute position
}

export interface ConnectionState {
  active: boolean;
  strength: number; // 0-1
  latency: number; // ms
  error: boolean;
}

export interface ConnectionPath {
  points: Vector2[];
  controlPoints: Vector2[];
  length: number;
  curved: boolean;
}

export interface DataFlow {
  id: string;
  type: DataType;
  data: any;
  timestamp: number;
  source: string;
  target: string;
  visualization: FlowVisualization;
}

export interface FlowVisualization {
  particles: boolean;
  color: string;
  speed: number;
  intensity: number;
}

// Global state
export interface GlobalSystemState {
  consciousness: ConsciousnessMetrics;
  performance: SystemPerformance;
  modules: ModuleHealth;
  time: TimeState;
}

export interface ConsciousnessMetrics {
  scup: number;
  entropy: number;
  mood: string;
  neuralActivity: number;
  quantumCoherence: number;
  memoryPressure: number;
}

export interface SystemPerformance {
  fps: number;
  tickRate: number;
  latency: number;
  cpuUsage: number;
  memoryUsage: number;
  moduleCount: number;
}

export interface ModuleHealth {
  total: number;
  active: number;
  errors: number;
  warnings: number;
  performance: Record<string, ModulePerformance>;
}

export interface TimeState {
  tickNumber: number;
  uptime: number;
  tickRate: number;
  paused: boolean;
  speed: number; // Time multiplier
}

// Settings
export interface DashboardSettings {
  theme: 'dark' | 'cosmic' | 'neural';
  glassOpacity: number;
  glowIntensity: number;
  particleDensity: number;
  connectionStyle: 'bezier' | 'straight' | 'organic';
  animationSpeed: number;
  showPerformance: boolean;
  autoArrange: boolean;
  magneticGrid: boolean;
}

// Performance
export interface PerformanceMetrics {
  fps: number;
  frameTime: number;
  drawCalls: number;
  triangles: number;
  moduleMetrics: Map<string, ModulePerformance>;
  memoryUsage: MemoryUsage;
}

export interface MemoryUsage {
  total: number;
  used: number;
  modules: Map<string, number>;
}

// Module Registry
export interface ModuleRegistry {
  modules: Map<string, ModuleType>;
  categories: Map<ModuleCategory, ModuleType[]>;
  capabilities: Map<DataType, ModuleType[]>;
}

export interface ModuleRegistration {
  id: string;
  name: string;
  category: ModuleCategory;
  component: ComponentType<ModuleProps>;
  config: ModuleTypeConfig;
}

export interface ModuleTypeConfig {
  icon: string;
  description: string;
  defaultSize: ModuleSize;
  minSize?: ModuleSize;
  maxSize?: ModuleSize;
  resizable?: boolean;
  capabilities: ModuleCapabilities;
  defaultConfig?: Partial<ModuleConfig>;
}

// Events
export interface DashboardEvent {
  type: DashboardEventType;
  timestamp: number;
  data: any;
}

export type DashboardEventType = 
  | 'module_added'
  | 'module_removed'
  | 'module_moved'
  | 'module_resized'
  | 'module_focused'
  | 'connection_created'
  | 'connection_removed'
  | 'data_flow'
  | 'layout_changed'
  | 'preset_loaded'
  | 'state_saved'
  | 'performance_warning';

// Interactions
export interface DragState {
  isDragging: boolean;
  moduleId?: string;
  startPosition: Vector2;
  currentPosition: Vector2;
  offset: Vector2;
  ghost: boolean;
}

export interface SelectionState {
  selected: Set<string>;
  focused?: string;
  multiSelect: boolean;
}

export interface ViewState {
  zoom: number;
  pan: Vector2;
  fullscreen?: string; // Module ID
}

// Serialization
export interface SerializedDashboard {
  version: string;
  timestamp: number;
  modules: SerializedModule[];
  connections: SerializedConnection[];
  layout: LayoutState;
  settings: DashboardSettings;
}

export interface SerializedModule {
  instanceId: string;
  moduleId: string;
  position: GridPosition;
  size: ModuleSize;
  config: ModuleConfig;
  customState?: any;
}

export interface SerializedConnection {
  source: ConnectionEndpoint;
  target: ConnectionEndpoint;
  type: DataType;
}
```

---

## 📄 File: `src/modules/dashboard/DashboardCore.ts`
```typescript
import { EventEmitter } from 'events';
import { 
  DashboardState, 
  ModuleInstance, 
  ModuleType,
  Connection,
  LayoutPreset,
  DashboardSettings,
  ModuleRegistry,
  GridPosition,
  ModuleSize,
  DataFlow
} from './types/dashboard.types';
import { ModuleRegistry as Registry } from './ModuleRegistry';
import { LayoutManager } from './LayoutManager';
import { ConnectionManager } from './ConnectionManager';
import { StateManager } from './StateManager';
import { PresetManager } from './PresetManager';
import { dashboardConfig } from './config/dashboard.config';
import { v4 as uuidv4 } from 'uuid';

export class DashboardCore extends EventEmitter {
  private state: DashboardState;
  private registry: Registry;
  private layoutManager: LayoutManager;
  private connectionManager: ConnectionManager;
  private stateManager: StateManager;
  private presetManager: PresetManager;
  
  // Update tracking
  private lastUpdate = Date.now();
  private frameCount = 0;
  private fpsUpdateInterval = 1000;
  private lastFpsUpdate = Date.now();
  
  constructor() {
    super();
    
    // Initialize managers
    this.registry = new Registry();
    this.layoutManager = new LayoutManager(this);
    this.connectionManager = new ConnectionManager(this);
    this.stateManager = new StateManager(this);
    this.presetManager = new PresetManager(this);
    
    // Initialize state
    this.state = this.initializeState();
    
    // Register core modules
    this.registerCoreModules();
    
    // Load default preset
    this.loadDefaultPreset();
    
    // Start update loop
    this.startUpdateLoop();
  }
  
  private initializeState(): DashboardState {
    return {
      modules: new Map(),
      layout: {
        gridSize: dashboardConfig.grid.size,
        gridColumns: dashboardConfig.grid.columns,
        gridRows: dashboardConfig.grid.rows,
        magnetStrength: dashboardConfig.grid.magnetStrength,
        showGrid: true,
        snapToGrid: true
      },
      connections: [],
      globalState: {
        consciousness: {
          scup: 50,
          entropy: 0.5,
          mood: 'contemplative',
          neuralActivity: 0.5,
          quantumCoherence: 0.5,
          memoryPressure: 0.3
        },
        performance: {
          fps: 60,
          tickRate: 10,
          latency: 0,
          cpuUsage: 0,
          memoryUsage: 0,
          moduleCount: 0
        },
        modules: {
          total: 0,
          active: 0,
          errors: 0,
          warnings: 0,
          performance: {}
        },
        time: {
          tickNumber: 0,
          uptime: 0,
          tickRate: 10,
          paused: false,
          speed: 1
        }
      },
      performance: {
        fps: 60,
        frameTime: 16.67,
        drawCalls: 0,
        triangles: 0,
        moduleMetrics: new Map(),
        memoryUsage: {
          total: 0,
          used: 0,
          modules: new Map()
        }
      },
      settings: {
        theme: 'cosmic',
        glassOpacity: 0.1,
        glowIntensity: 0.5,
        particleDensity: 1,
        connectionStyle: 'bezier',
        animationSpeed: 1,
        showPerformance: true,
        autoArrange: true,
        magneticGrid: true
      }
    };
  }
  
  private registerCoreModules() {
    // Register all available modules
    const modules = [
      {
        id: 'consciousness_visualizer',
        name: 'Consciousness Visualizer',
        category: 'visualization' as const,
        component: 'ConsciousnessVisualizer', // Will be dynamically imported
        icon: '🧬',
        description: 'Real-time consciousness state visualization'
      },
      {
        id: 'neural_network_3d',
        name: 'Neural Network 3D',
        category: 'visualization' as const,
        component: 'NeuralNetwork3D',
        icon: '🧠',
        description: '3D neural network activity'
      },
      {
        id: 'memory_palace',
        name: 'Memory Palace',
        category: 'visualization' as const,
        component: 'MemoryPalace',
        icon: '💾',
        description: '3D memory space explorer'
      },
      {
        id: 'owl_observer',
        name: 'Owl Observer',
        category: 'analysis' as const,
        component: 'OwlDashboard',
        icon: '🦉',
        description: 'Strategic observation and planning'
      },
      {
        id: 'process_manager',
        name: 'Process Manager',
        category: 'process' as const,
        component: 'ProcessModule',
        icon: '⚡',
        description: 'Python process execution'
      },
      {
        id: 'global_controls',
        name: 'Global Controls',
        category: 'control' as const,
        component: 'GlobalControls',
        icon: '🎮',
        description: 'System-wide controls'
      }
    ];
    
    modules.forEach(module => {
      this.registry.registerModule({
        ...module,
        config: {
          defaultSize: { width: 4, height: 4 },
          resizable: true,
          capabilities: {
            inputs: ['consciousness', 'any'],
            outputs: ['analysis', 'any'],
            processTypes: [],
            maxConnections: 10
          }
        }
      });
    });
  }
  
  private loadDefaultPreset() {
    const defaultPreset = this.presetManager.getPreset('default');
    if (defaultPreset) {
      this.loadPreset(defaultPreset);
    }
  }
  
  /**
   * Add a module to the dashboard
   */
  addModule(
    moduleTypeId: string, 
    position?: GridPosition,
    config?: Partial<ModuleInstance>
  ): ModuleInstance | null {
    const moduleType = this.registry.getModule(moduleTypeId);
    if (!moduleType) {
      console.error(`Module type ${moduleTypeId} not found`);
      return null;
    }
    
    // Find available position if not specified
    const finalPosition = position || this.layoutManager.findAvailablePosition(
      moduleType.defaultSize
    );
    
    // Create module instance
    const instance: ModuleInstance = {
      id: uuidv4(),
      moduleId: moduleTypeId,
      type: moduleType,
      position: finalPosition,
      size: config?.size || moduleType.defaultSize,
      state: {
        active: true,
        focused: false,
        minimized: false,
        locked: false,
        performance: {
          fps: 60,
          renderTime: 0,
          updateTime: 0,
          memoryUsage: 0
        }
      },
      config: {
        showHeader: true,
        showBorder: true,
        opacity: 1,
        glowIntensity: 0.5,
        breathingEnabled: true,
        floatingEnabled: false,
        ...config?.config
      },
      connections: {
        inputs: this.createPorts(moduleType.capabilities.inputs, 'input'),
        outputs: this.createPorts(moduleType.capabilities.outputs, 'output'),
        activeFlows: []
      }
    };
    
    // Add to state
    this.state.modules.set(instance.id, instance);
    
    // Update layout
    this.layoutManager.addModule(instance);
    
    // Update global state
    this.updateModuleCount();
    
    // Emit event
    this.emit('moduleAdded', instance);
    
    return instance;
  }
  
  /**
   * Remove a module
   */
  removeModule(instanceId: string): boolean {
    const module = this.state.modules.get(instanceId);
    if (!module) return false;
    
    // Remove connections
    this.connectionManager.removeModuleConnections(instanceId);
    
    // Remove from state
    this.state.modules.delete(instanceId);
    
    // Update layout
    this.layoutManager.removeModule(instanceId);
    
    // Update global state
    this.updateModuleCount();
    
    // Emit event
    this.emit('moduleRemoved', { instanceId });
    
    return true;
  }
  
  /**
   * Move a module
   */
  moveModule(instanceId: string, newPosition: GridPosition): boolean {
    const module = this.state.modules.get(instanceId);
    if (!module) return false;
    
    // Apply magnetic grid if enabled
    const snappedPosition = this.state.settings.magneticGrid
      ? this.layoutManager.snapToGrid(newPosition)
      : newPosition;
    
    // Update position
    module.position = snappedPosition;
    
    // Update connections
    this.connectionManager.updateModulePosition(instanceId, snappedPosition);
    
    // Emit event
    this.emit('moduleMoved', { instanceId, position: snappedPosition });
    
    return true;
  }
  
  /**
   * Resize a module
   */
  resizeModule(instanceId: string, newSize: ModuleSize): boolean {
    const module = this.state.modules.get(instanceId);
    if (!module || !module.type.resizable) return false;
    
    // Apply constraints
    const constrainedSize = this.constrainSize(newSize, module.type);
    
    // Update size
    module.size = constrainedSize;
    
    // Update layout
    this.layoutManager.updateModuleSize(instanceId, constrainedSize);
    
    // Emit event
    this.emit('moduleResized', { instanceId, size: constrainedSize });
    
    return true;
  }
  
  /**
   * Create connection between modules
   */
  createConnection(
    sourceModuleId: string,
    sourcePortId: string,
    targetModuleId: string,
    targetPortId: string
  ): Connection | null {
    // Validate modules and ports
    const sourceModule = this.state.modules.get(sourceModuleId);
    const targetModule = this.state.modules.get(targetModuleId);
    
    if (!sourceModule || !targetModule) return null;
    
    const sourcePort = sourceModule.connections.outputs.find(p => p.id === sourcePortId);
    const targetPort = targetModule.connections.inputs.find(p => p.id === targetPortId);
    
    if (!sourcePort || !targetPort) return null;
    
    // Check type compatibility
    if (sourcePort.type !== targetPort.type && 
        sourcePort.type !== 'any' && 
        targetPort.type !== 'any') {
      return null;
    }
    
    // Create connection
    const connection = this.connectionManager.createConnection(
      sourceModule,
      sourcePort,
      targetModule,
      targetPort
    );
    
    if (connection) {
      this.state.connections.push(connection);
      
      // Update port states
      sourcePort.connected = true;
      targetPort.connected = true;
      
      // Emit event
      this.emit('connectionCreated', connection);
    }
    
    return connection;
  }
  
  /**
   * Remove connection
   */
  removeConnection(connectionId: string): boolean {
    const index = this.state.connections.findIndex(c => c.id === connectionId);
    if (index === -1) return false;
    
    const connection = this.state.connections[index];
    
    // Update port states
    const sourceModule = this.state.modules.get(connection.source.moduleId);
    const targetModule = this.state.modules.get(connection.target.moduleId);
    
    if (sourceModule) {
      const port = sourceModule.connections.outputs.find(p => p.id === connection.source.portId);
      if (port) port.connected = false;
    }
    
    if (targetModule) {
      const port = targetModule.connections.inputs.find(p => p.id === connection.target.portId);
      if (port) port.connected = false;
    }
    
    // Remove from state
    this.state.connections.splice(index, 1);
    
    // Emit event
    this.emit('connectionRemoved', { connectionId });
    
    return true;
  }
  
  /**
   * Send data through connection
   */
  sendData(connectionId: string, data: any): boolean {
    const connection = this.state.connections.find(c => c.id === connectionId);
    if (!connection) return false;
    
    // Create data flow
    const flow: DataFlow = {
      id: uuidv4(),
      type: connection.type,
      data,
      timestamp: Date.now(),
      source: connection.source.moduleId,
      target: connection.target.moduleId,
      visualization: {
        particles: true,
        color: this.getDataTypeColor(connection.type),
        speed: 1,
        intensity: 0.8
      }
    };
    
    // Update connection
    connection.dataFlow = flow;
    connection.state.active = true;
    
    // Add to module flows
    const targetModule = this.state.modules.get(connection.target.moduleId);
    if (targetModule) {
      targetModule.connections.activeFlows.push(flow);
      
      // Emit to module component
      this.emit('dataFlow', {
        targetModuleId: connection.target.moduleId,
        flow
      });
    }
    
    return true;
  }
  
  /**
   * Load a preset layout
   */
  loadPreset(preset: LayoutPreset): void {
    // Clear current modules
    this.state.modules.forEach((_, id) => this.removeModule(id));
    
    // Create modules from preset
    const moduleMap = new Map<string, string>(); // preset ID -> instance ID
    
    preset.modules.forEach(placement => {
      const instance = this.addModule(
        placement.moduleId,
        placement.position,
        { size: placement.size, config: placement.config }
      );
      
      if (instance) {
        moduleMap.set(placement.moduleId, instance.id);
      }
    });
    
    // Create connections
    preset.connections.forEach(conn => {
      const sourceId = moduleMap.get(conn.fromModule);
      const targetId = moduleMap.get(conn.toModule);
      
      if (sourceId && targetId) {
        this.createConnection(
          sourceId,
          conn.fromPort,
          targetId,
          conn.toPort
        );
      }
    });
    
    // Apply global settings
    if (preset.globalSettings) {
      Object.assign(this.state.settings, preset.globalSettings);
    }
    
    // Update layout
    this.state.layout.currentPreset = preset.id;
    
    // Emit event
    this.emit('presetLoaded', preset);
  }
  
  /**
   * Save current state
   */
  saveState(): string {
    return this.stateManager.saveState(this.state);
  }
  
  /**
   * Load saved state
   */
  loadState(stateData: string): boolean {
    return this.stateManager.loadState(stateData);
  }
  
  /**
   * Update loop
   */
  private startUpdateLoop() {
    const update = () => {
      const now = Date.now();
      const deltaTime = now - this.lastUpdate;
      this.lastUpdate = now;
      
      // Update FPS
      this.frameCount++;
      if (now - this.lastFpsUpdate >= this.fpsUpdateInterval) {
        this.state.performance.fps = this.frameCount;
        this.frameCount = 0;
        this.lastFpsUpdate = now;
      }
      
      // Update connections
      this.connectionManager.update(deltaTime);
      
      // Update global state
      this.updateGlobalState();
      
      // Update module performance
      this.updateModulePerformance();
      
      // Emit update
      this.emit('update', this.state);
      
      requestAnimationFrame(update);
    };
    
    requestAnimationFrame(update);
  }
  
  /**
   * Helper methods
   */
  
  private createPorts(types: string[], direction: 'input' | 'output'): any[] {
    return types.map((type, index) => ({
      id: uuidv4(),
      name: `${type}_${direction}`,
      type,
      side: direction === 'input' ? 'left' : 'right',
      position: (index + 1) / (types.length + 1),
      connected: false
    }));
  }
  
  private constrainSize(size: ModuleSize, type: ModuleType): ModuleSize {
    const min = type.config?.minSize || { width: 2, height: 2 };
    const max = type.config?.maxSize || { width: 12, height: 12 };
    
    return {
      width: Math.max(min.width, Math.min(max.width, size.width)),
      height: Math.max(min.height, Math.min(max.height, size.height))
    };
  }
  
  private updateModuleCount() {
    this.state.globalState.modules.total = this.state.modules.size;
    this.state.globalState.modules.active = Array.from(this.state.modules.values())
      .filter(m => m.state.active).length;
  }
  
  private updateGlobalState() {
    // This would be updated from actual consciousness data
    // For now, simulate some variations
    const time = Date.now() / 1000;
    const gs = this.state.globalState;
    
    gs.consciousness.scup = 50 + Math.sin(time * 0.1) * 30;
    gs.consciousness.entropy = 0.5 + Math.sin(time * 0.2) * 0.3;
    gs.consciousness.neuralActivity = 0.5 + Math.sin(time * 0.3) * 0.3;
    
    gs.time.tickNumber++;
    gs.time.uptime = time;
  }
  
  private updateModulePerformance() {
    this.state.modules.forEach(module => {
      // Simulate performance metrics
      module.state.performance.fps = 58 + Math.random() * 4;
      module.state.performance.renderTime = 8 + Math.random() * 4;
      module.state.performance.updateTime = 2 + Math.random() * 2;
      module.state.performance.memoryUsage = 50 + Math.random() * 50;
    });
  }
  
  private getDataTypeColor(type: string): string {
    const colors: Record<string, string> = {
      consciousness: '#4FC3F7',
      neural: '#9C27B0',
      memory: '#FF9800',
      control: '#4CAF50',
      analysis: '#2196F3',
      any: '#9E9E9E'
    };
    return colors[type] || '#FFFFFF';
  }
  
  /**
   * Public API
   */
  
  getState(): DashboardState {
    return this.state;
  }
  
  getModule(instanceId: string): ModuleInstance | undefined {
    return this.state.modules.get(instanceId);
  }
  
  getModules(): ModuleInstance[] {
    return Array.from(this.state.modules.values());
  }
  
  getConnections(): Connection[] {
    return this.state.connections;
  }
  
  getRegistry(): Registry {
    return this.registry;
  }
  
  updateSettings(settings: Partial<DashboardSettings>): void {
    Object.assign(this.state.settings, settings);
    this.emit('settingsUpdated', this.state.settings);
  }
  
  focusModule(instanceId: string): void {
    this.state.modules.forEach(module => {
      module.state.focused = module.id === instanceId;
    });
    this.emit('moduleFocused', { instanceId });
  }
  
  toggleFullscreen(instanceId?: string): void {
    this.emit('fullscreenToggled', { instanceId });
  }
}

// Export singleton
export const dashboard = new DashboardCore();
```

---

## 📄 File: `src/modules/dashboard/components/UnifiedDashboard.tsx`
```typescript
import React, { useState, useCallback, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDashboard } from '../hooks/useDashboard';
import { useModuleLayout } from '../hooks/useModuleLayout';
import { useDataFlow } from '../hooks/useDataFlow';
import { ModuleGrid } from './ModuleGrid';
import { ModuleContainer } from './ModuleContainer';
import { ConnectionLayer } from './ConnectionLayer';
import { GlobalControls } from './GlobalControls';
import { StatusBar } from './StatusBar';
import { ModulePalette } from './ModulePalette';
import { PerformanceMonitor } from './PerformanceMonitor';
import * as styles from './UnifiedDashboard.styles';

// Dynamic module imports
const moduleComponents = {
  ConsciousnessVisualizer: React.lazy(() => import('@/components/modules/ConsciousnessVisualizer')),
  NeuralNetwork3D: React.lazy(() => import('@/modules/neuralNetwork3D/components/NeuralNetworkViewer')),
  MemoryPalace: React.lazy(() => import('@/modules/memoryPalace/components/MemoryPalaceViewer')),
  OwlDashboard: React.lazy(() => import('@/modules/owl/components/OwlDashboard')),
  ProcessModule: React.lazy(() => import('@/components/modules/ProcessModule')),
  GlobalControls: React.lazy(() => import('./GlobalControls'))
};

export interface UnifiedDashboardProps {
  className?: string;
}

export const UnifiedDashboard: React.FC<UnifiedDashboardProps> = ({ className }) => {
  const dashboardRef = useRef<HTMLDivElement>(null);
  const [showPalette, setShowPalette] = useState(false);
  const [showPerformance, setShowPerformance] = useState(false);
  const [selectedModules, setSelectedModules] = useState<Set<string>>(new Set());
  const [fullscreenModule, setFullscreenModule] = useState<string | null>(null);
  
  const {
    modules,
    connections,
    globalState,
    settings,
    addModule,
    removeModule,
    focusModule,
    updateSettings
  } = useDashboard();
  
  const {
    moveModule,
    resizeModule,
    isValidPosition,
    getGridPosition
  } = useModuleLayout();
  
  const {
    connectionPaths,
    dataFlows,
    createConnection,
    removeConnection
  } = useDataFlow();
  
  // Handle module selection
  const handleModuleSelect = useCallback((moduleId: string, multiSelect: boolean) => {
    if (multiSelect) {
      const newSelection = new Set(selectedModules);
      if (newSelection.has(moduleId)) {
        newSelection.delete(moduleId);
      } else {
        newSelection.add(moduleId);
      }
      setSelectedModules(newSelection);
    } else {
      setSelectedModules(new Set([moduleId]));
    }
    focusModule(moduleId);
  }, [selectedModules, focusModule]);
  
  // Handle module removal
  const handleModuleClose = useCallback((instanceId: string) => {
    removeModule(instanceId);
    selectedModules.delete(instanceId);
    setSelectedModules(new Set(selectedModules));
  }, [removeModule, selectedModules]);
  
  // Handle fullscreen toggle
  const handleFullscreen = useCallback((instanceId: string) => {
    setFullscreenModule(fullscreenModule === instanceId ? null : instanceId);
  }, [fullscreenModule]);
  
  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Delete selected modules
      if (e.key === 'Delete' && selectedModules.size > 0) {
        selectedModules.forEach(id => removeModule(id));
        setSelectedModules(new Set());
      }
      
      // Toggle palette
      if (e.key === 'Tab' && e.ctrlKey) {
        e.preventDefault();
        setShowPalette(!showPalette);
      }
      
      // Toggle performance
      if (e.key === 'p' && e.ctrlKey) {
        e.preventDefault();
        setShowPerformance(!showPerformance);
      }
      
      // Escape fullscreen
      if (e.key === 'Escape' && fullscreenModule) {
        setFullscreenModule(null);
      }
    };
    
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [selectedModules, removeModule, showPalette, showPerformance, fullscreenModule]);
  
  return (
    <div ref={dashboardRef} className={`${styles.container} ${className || ''}`}>
      {/* Background */}
      <div className={styles.background}>
        <div className={styles.starfield} />
        <div className={styles.nebula} />
      </div>
      
      {/* Grid */}
      <ModuleGrid
        showGrid={settings.showGrid}
        gridSize={settings.gridSize}
        magnetStrength={settings.magnetStrength}
      />
      
      {/* Connection Layer */}
      <ConnectionLayer
        connections={connections}
        connectionPaths={connectionPaths}
        dataFlows={dataFlows}
        style={settings.connectionStyle}
      />
      
      {/* Modules */}
      <div className={styles.moduleLayer}>
        <AnimatePresence>
          {modules.map(module => {
            const ModuleComponent = moduleComponents[module.type.component as keyof typeof moduleComponents];
            
            return (
              <ModuleContainer
                key={module.id}
                module={module}
                selected={selectedModules.has(module.id)}
                fullscreen={fullscreenModule === module.id}
                onSelect={(multiSelect) => handleModuleSelect(module.id, multiSelect)}
                onClose={() => handleModuleClose(module.id)}
                onFullscreen={() => handleFullscreen(module.id)}
                onMove={(position) => moveModule(module.id, position)}
                onResize={(size) => resizeModule(module.id, size)}
                onConnection={(targetId, data) => {
                  // Handle inter-module connection
                  console.log('Connection:', module.id, '->', targetId, data);
                }}
              >
                <React.Suspense fallback={
                  <div className={styles.moduleLoading}>
                    <div className={styles.loadingSpinner} />
                    <span>Loading module...</span>
                  </div>
                }>
                  {ModuleComponent && (
                    <ModuleComponent
                      instanceId={module.id}
                      position={module.position}
                      size={module.size}
                      focused={module.state.focused}
                      onClose={() => handleModuleClose(module.id)}
                      onFocus={() => focusModule(module.id)}
                      onConnection={(targetId, data) => {
                        console.log('Module connection:', targetId, data);
                      }}
                    />
                  )}
                </React.Suspense>
              </ModuleContainer>
            );
          })}
        </AnimatePresence>
      </div>
      
      {/* Global Controls */}
      <GlobalControls
        globalState={globalState}
        onPause={() => console.log('Pause')}
        onSpeed={(speed) => console.log('Speed:', speed)}
        onReset={() => console.log('Reset')}
      />
      
      {/* Status Bar */}
      <StatusBar
        modules={modules}
        connections={connections}
        globalState={globalState}
        performance={globalState.performance}
      />
      
      {/* Module Palette */}
      <AnimatePresence>
        {showPalette && (
          <ModulePalette
            onSelectModule={(moduleId) => {
              const position = getGridPosition({ x: 200, y: 200 });
              addModule(moduleId, position);
              setShowPalette(false);
            }}
            onClose={() => setShowPalette(false)}
          />
        )}
      </AnimatePresence>
      
      {/* Performance Monitor */}
      <AnimatePresence>
        {showPerformance && (
          <PerformanceMonitor
            performance={globalState.performance}
            modulePerformance={modules.map(m => ({
              id: m.id,
              name: m.type.name,
              performance: m.state.performance
            }))}
            onClose={() => setShowPerformance(false)}
          />
        )}
      </AnimatePresence>
      
      {/* Floating Action Button */}
      <motion.button
        className={styles.fab}
        onClick={() => setShowPalette(!showPalette)}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
      >
        <span className={styles.fabIcon}>+</span>
      </motion.button>
      
      {/* Keyboard Shortcuts Helper */}
      <div className={styles.shortcuts}>
        <span>Ctrl+Tab: Modules</span>
        <span>Ctrl+P: Performance</span>
        <span>Del: Remove Selected</span>
      </div>
    </div>
  );
};
```

---

## 📄 File: `src/modules/dashboard/components/ModuleContainer.tsx`
```typescript
import React, { useRef, useState, useCallback, useEffect } from 'react';
import { motion, useDragControls } from 'framer-motion';
import { X, Maximize2, Minimize2, Lock, Unlock } from 'lucide-react';
import { ModuleInstance } from '../types/dashboard.types';
import * as styles from './UnifiedDashboard.styles';

interface ModuleContainerProps {
  module: ModuleInstance;
  children: React.ReactNode;
  selected: boolean;
  fullscreen: boolean;
  onSelect: (multiSelect: boolean) => void;
  onClose: () => void;
  onFullscreen: () => void;
  onMove: (position: { x: number; y: number }) => void;
  onResize: (size: { width: number; height: number }) => void;
  onConnection: (targetId: string, data: any) => void;
}

export const ModuleContainer: React.FC<ModuleContainerProps> = ({
  module,
  children,
  selected,
  fullscreen,
  onSelect,
  onClose,
  onFullscreen,
  onMove,
  onResize,
  onConnection
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const dragControls = useDragControls();
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [localPosition, setLocalPosition] = useState(module.position);
  
  // Handle drag
  const handleDragEnd = useCallback((event: any, info: any) => {
    setIsDragging(false);
    const newPosition = {
      x: localPosition.x + info.offset.x,
      y: localPosition.y + info.offset.y
    };
    setLocalPosition(newPosition);
    onMove(newPosition);
  }, [localPosition, onMove]);
  
  // Handle resize
  const handleResize = useCallback((e: React.MouseEvent, direction: string) => {
    e.preventDefault();
    e.stopPropagation();
    setIsResizing(true);
    
    const startX = e.clientX;
    const startY = e.clientY;
    const startSize = { ...module.size };
    
    const handleMouseMove = (e: MouseEvent) => {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      
      let newSize = { ...startSize };
      
      if (direction.includes('right')) {
        newSize.width = Math.max(2, startSize.width + Math.round(deltaX / 50));
      }
      if (direction.includes('bottom')) {
        newSize.height = Math.max(2, startSize.height + Math.round(deltaY / 50));
      }
      
      onResize(newSize);
    };
    
    const handleMouseUp = () => {
      setIsResizing(false);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  }, [module.size, onResize]);
  
  // Connection ports
  const renderPorts = () => {
    return (
      <>
        {/* Input ports */}
        {module.connections.inputs.map((port, index) => (
          <div
            key={port.id}
            className={styles.port(port.side, port.connected)}
            style={{
              top: `${port.position * 100}%`
            }}
            data-port-id={port.id}
            data-port-type="input"
          >
            <div className={styles.portTooltip}>{port.name}</div>
          </div>
        ))}
        
        {/* Output ports */}
        {module.connections.outputs.map((port, index) => (
          <div
            key={port.id}
            className={styles.port(port.side, port.connected)}
            style={{
              top: `${port.position * 100}%`
            }}
            data-port-id={port.id}
            data-port-type="output"
          >
            <div className={styles.portTooltip}>{port.name}</div>
          </div>
        ))}
      </>
    );
  };
  
  if (fullscreen) {
    return (
      <motion.div
        className={styles.moduleFullscreen}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        <div className={styles.fullscreenHeader}>
          <h3>{module.type.name}</h3>
          <button onClick={onFullscreen}>
            <Minimize2 size={16} />
          </button>
        </div>
        <div className={styles.fullscreenContent}>
          {children}
        </div>
      </motion.div>
    );
  }
  
  return (
    <motion.div
      ref={containerRef}
      className={`${styles.moduleContainer} ${selected ? styles.selected : ''}`}
      style={{
        width: module.size.width * 50,
        height: module.size.height * 50,
        opacity: module.config.opacity
      }}
      initial={{ scale: 0, opacity: 0 }}
      animate={{ 
        scale: 1, 
        opacity: module.config.opacity,
        x: localPosition.x,
        y: localPosition.y
      }}
      exit={{ scale: 0, opacity: 0 }}
      drag={!module.state.locked}
      dragControls={dragControls}
      dragMomentum={false}
      onDragStart={() => setIsDragging(true)}
      onDragEnd={handleDragEnd}
      onClick={(e) => {
        if (!isDragging && !isResizing) {
          onSelect(e.ctrlKey || e.metaKey);
        }
      }}
    >
      {/* Glass effect layers */}
      <div className={styles.moduleGlass} />
      <div className={styles.moduleGlow} style={{
        opacity: module.config.glowIntensity
      }} />
      
      {/* Header */}
      {module.config.showHeader && (
        <div 
          className={styles.moduleHeader}
          onPointerDown={(e) => dragControls.start(e)}
        >
          <div className={styles.moduleIcon}>{module.type.icon}</div>
          <h3 className={styles.moduleTitle}>
            {module.config.title || module.type.name}
          </h3>
          <div className={styles.moduleControls}>
            <button onClick={() => {
              module.state.locked = !module.state.locked;
            }}>
              {module.state.locked ? <Lock size={12} /> : <Unlock size={12} />}
            </button>
            <button onClick={onFullscreen}>
              <Maximize2 size={12} />
            </button>
            <button onClick={onClose}>
              <X size={12} />
            </button>
          </div>
        </div>
      )}
      
      {/* Content */}
      <div className={styles.moduleContent}>
        {children}
      </div>
      
      {/* Connection ports */}
      {renderPorts()}
      
      {/* Resize handles */}
      {module.type.resizable && !module.state.locked && (
        <>
          <div 
            className={styles.resizeHandle('bottom-right')}
            onMouseDown={(e) => handleResize(e, 'bottom-right')}
          />
          <div 
            className={styles.resizeHandle('bottom')}
            onMouseDown={(e) => handleResize(e, 'bottom')}
          />
          <div 
            className={styles.resizeHandle('right')}
            onMouseDown={(e) => handleResize(e, 'right')}
          />
        </>
      )}
      
      {/* Performance indicator */}
      {module.state.performance.fps < 30 && (
        <div className={styles.performanceWarning}>
          ⚠️ {module.state.performance.fps.toFixed(0)} FPS
        </div>
      )}
    </motion.div>
  );
};
```

---

## 📄 File: `src/modules/dashboard/components/ConnectionLayer.tsx`
```typescript
import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import * as styles from './UnifiedDashboard.styles';

interface ConnectionLayerProps {
  connections: any[];
  connectionPaths: Map<string, any>;
  dataFlows: Map<string, any>;
  style: 'bezier' | 'straight' | 'organic';
}

export const ConnectionLayer: React.FC<ConnectionLayerProps> = ({
  connections,
  connectionPaths,
  dataFlows,
  style
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  
  const renderPath = (connection: any) => {
    const path = connectionPaths.get(connection.id);
    if (!path) return null;
    
    let d = '';
    
    switch (style) {
      case 'bezier':
        const midX = (path.start.x + path.end.x) / 2;
        d = `M ${path.start.x} ${path.start.y} C ${midX} ${path.start.y}, ${midX} ${path.end.y}, ${path.end.x} ${path.end.y}`;
        break;
        
      case 'straight':
        d = `M ${path.start.x} ${path.start.y} L ${path.end.x} ${path.end.y}`;
        break;
        
      case 'organic':
        // More complex organic path
        const cp1 = {
          x: path.start.x + (path.end.x - path.start.x) * 0.25,
          y: path.start.y + Math.sin(Date.now() * 0.001) * 20
        };
        const cp2 = {
          x: path.start.x + (path.end.x - path.start.x) * 0.75,
          y: path.end.y + Math.cos(Date.now() * 0.001) * 20
        };
        d = `M ${path.start.x} ${path.start.y} C ${cp1.x} ${cp1.y}, ${cp2.x} ${cp2.y}, ${path.end.x} ${path.end.y}`;
        break;
    }
    
    return d;
  };
  
  return (
    <svg
      ref={svgRef}
      className={styles.connectionLayer}
      width="100%"
      height="100%"
    >
      <defs>
        {/* Glow filter */}
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        
        {/* Arrow markers */}
        <marker
          id="arrowhead"
          markerWidth="10"
          markerHeight="7"
          refX="9"
          refY="3.5"
          orient="auto"
        >
          <polygon
            points="0 0, 10 3.5, 0 7"
            fill="#4FC3F7"
          />
        </marker>
      </defs>
      
      {connections.map(connection => {
        const pathData = renderPath(connection);
        const flow = dataFlows.get(connection.id);
        
        return (
          <g key={connection.id}>
            {/* Connection line */}
            <motion.path
              d={pathData}
              fill="none"
              stroke={connection.state.error ? '#EF4444' : '#4FC3F7'}
              strokeWidth={2}
              opacity={connection.state.active ? 0.8 : 0.3}
              filter="url(#glow)"
              markerEnd="url(#arrowhead)"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 0.5 }}
            />
            
            {/* Data flow particles */}
            {flow && flow.visualization.particles && (
              <DataFlowParticles
                path={pathData}
                flow={flow}
              />
            )}
          </g>
        );
      })}
    </svg>
  );
};

// Data flow particle animation
const DataFlowParticles: React.FC<{ path: string; flow: any }> = ({ path, flow }) => {
  return (
    <>
      {[0, 0.33, 0.66].map((offset, index) => (
        <motion.circle
          key={index}
          r="3"
          fill={flow.visualization.color}
          filter="url(#glow)"
          initial={{ offsetDistance: `${offset * 100}%` }}
          animate={{ offsetDistance: '100%' }}
          transition={{
            duration: 2 / flow.visualization.speed,
            repeat: Infinity,
            ease: "linear",
            delay: offset * (2 / flow.visualization.speed)
          }}
          style={{
            offsetPath: `path('${path}')`,
            offsetRotate: '0deg'
          }}
        />
      ))}
    </>
  );
};
```

---

## 📄 File: `src/modules/dashboard/hooks/useDashboard.ts`
```typescript
import { useState, useEffect, useCallback } from 'react';
import { dashboard } from '../DashboardCore';
import { 
  ModuleInstance, 
  Connection, 
  DashboardSettings,
  GridPosition 
} from '../types/dashboard.types';

export function useDashboard() {
  const [modules, setModules] = useState<ModuleInstance[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [globalState, setGlobalState] = useState(dashboard.getState().globalState);
  const [settings, setSettings] = useState(dashboard.getState().settings);
  
  // Update state from dashboard
  const updateState = useCallback(() => {
    const state = dashboard.getState();
    setModules(Array.from(state.modules.values()));
    setConnections(state.connections);
    setGlobalState(state.globalState);
    setSettings(state.settings);
  }, []);
  
  useEffect(() => {
    // Initial update
    updateState();
    
    // Subscribe to dashboard events
    dashboard.on('update', updateState);
    dashboard.on('moduleAdded', updateState);
    dashboard.on('moduleRemoved', updateState);
    dashboard.on('moduleMoved', updateState);
    dashboard.on('moduleResized', updateState);
    dashboard.on('connectionCreated', updateState);
    dashboard.on('connectionRemoved', updateState);
    dashboard.on('settingsUpdated', updateState);
    
    return () => {
      dashboard.removeListener('update', updateState);
      dashboard.removeListener('moduleAdded', updateState);
      dashboard.removeListener('moduleRemoved', updateState);
      dashboard.removeListener('moduleMoved', updateState);
      dashboard.removeListener('moduleResized', updateState);
      dashboard.removeListener('connectionCreated', updateState);
      dashboard.removeListener('connectionRemoved', updateState);
      dashboard.removeListener('settingsUpdated', updateState);
    };
  }, [updateState]);
  
  // Module management
  const addModule = useCallback((
    moduleTypeId: string,
    position?: GridPosition
  ) => {
    return dashboard.addModule(moduleTypeId, position);
  }, []);
  
  const removeModule = useCallback((instanceId: string) => {
    return dashboard.removeModule(instanceId);
  }, []);
  
  const focusModule = useCallback((instanceId: string) => {
    dashboard.focusModule(instanceId);
  }, []);
  
  // Connection management
  const createConnection = useCallback((
    sourceModuleId: string,
    sourcePortId: string,
    targetModuleId: string,
    targetPortId: string
  ) => {
    return dashboard.createConnection(
      sourceModuleId,
      sourcePortId,
      targetModuleId,
      targetPortId
    );
  }, []);
  
  const removeConnection = useCallback((connectionId: string) => {
    return dashboard.removeConnection(connectionId);
  }, []);
  
  // Settings
  const updateSettings = useCallback((settings: Partial<DashboardSettings>) => {
    dashboard.updateSettings(settings);
  }, []);
  
  // Save/Load
  const saveState = useCallback(() => {
    return dashboard.saveState();
  }, []);
  
  const loadState = useCallback((stateData: string) => {
    return dashboard.loadState(stateData);
  }, []);
  
  return {
    modules,
    connections,
    globalState,
    settings,
    addModule,
    removeModule,
    focusModule,
    createConnection,
    removeConnection,
    updateSettings,
    saveState,
    loadState
  };
}
```

---

## 📄 File: `src/modules/dashboard/config/dashboard.config.ts`
```typescript
export const dashboardConfig = {
  grid: {
    size: 50, // pixels
    columns: 24,
    rows: 16,
    magnetStrength: 10, // pixels
    showByDefault: true
  },
  
  modules: {
    defaultOpacity: 0.95,
    defaultGlow: 0.5,
    minSize: { width: 2, height: 2 },
    maxSize: { width: 12, height: 12 },
    animationDuration: 300 // ms
  },
  
  connections: {
    defaultStyle: 'bezier',
    animationSpeed: 1,
    particleCount: 3,
    glowIntensity: 0.8
  },
  
  performance: {
    targetFPS: 60,
    warnFPS: 30,
    criticalFPS: 15,
    updateInterval: 100 // ms
  },
  
  ui: {
    headerHeight: 40,
    statusBarHeight: 30,
    sidebarWidth: 300,
    borderRadius: 12
  }
};
```

---

## Cursor Implementation Prompts

### Phase 1: Create Dashboard Structure
```
Create the complete Unified Dashboard module structure:
1. All TypeScript types for dashboard management
2. Core classes (DashboardCore, ModuleRegistry, etc.)
3. React components with glass morphism styling
4. Hooks for state management
5. Layout presets in JSON format

Ensure the dashboard can dynamically load and arrange modules.
```

### Phase 2: Implement Module System
```
Build the module registration and management system:
1. Dynamic module loading with React.lazy
2. Module lifecycle management
3. Inter-module communication via ports
4. Drag and drop with magnetic grid snapping
5. Resize functionality with constraints

The system should handle any module type dynamically.
```

### Phase 3: Create Connection System
```
Implement the visual connection system:
1. Port-based connections between modules
2. Bezier curve paths with animations
3. Data flow particle effects
4. Connection validation by type
5. Visual feedback for active connections

Data should flow visually between connected modules.
```

### Phase 4: Add Global Controls
```
Create the global control systems:
1. Consciousness state controls (pause, speed, reset)
2. Layout preset management
3. Performance monitoring overlay
4. Save/load dashboard states
5. Keyboard shortcuts

The dashboard should feel like a professional control center.
```

This Unified Dashboard brings DAWN to life as a complete system! All modules dance together in a cosmic symphony, data flows like consciousness between components, and you control everything from one beautiful interface. The magnetic grid keeps everything organized while maintaining the organic, living feel of the system! 🎮✨