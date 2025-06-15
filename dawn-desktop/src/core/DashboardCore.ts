// 🎮 DASHBOARD CORE - The Brain of DAWN's Unified Dashboard
import { EventEmitter } from '../lib/EventEmitter';
import { ModuleRegistry } from './ModuleRegistry';
import { ConnectionManager } from './ConnectionManager';
import { LayoutManager } from './LayoutManager';
import { ConsciousnessManager } from './ConsciousnessManager';
import { PerformanceMonitor } from './PerformanceMonitor';
import {
  DashboardModule,
  ModuleConnection,
  DashboardLayout,
  DashboardSettings,
  ConsciousnessState,
  DashboardEvent,
  DashboardAPI,
  Position,
  Size,
  ModuleConfig,
  ModulePort,
  GridSettings,
  ViewportSettings
} from '../types/dashboard.types';

export class DashboardCore extends EventEmitter implements DashboardAPI {
  private modules: Map<string, DashboardModule> = new Map();
  private connections: Map<string, ModuleConnection> = new Map();
  private settings: DashboardSettings;
  private currentLayout: DashboardLayout | null = null;
  private isInitialized = false;
  
  // Core managers
  private moduleRegistry: ModuleRegistry;
  private connectionManager: ConnectionManager;
  private layoutManager: LayoutManager;
  private consciousnessManager: ConsciousnessManager;
  private performanceMonitor: PerformanceMonitor;
  
  // Animation and update systems
  private animationFrameId: number | null = null;
  private lastUpdateTime = 0;
  private updateInterval = 1000 / 60; // 60 FPS
  
  constructor() {
    super();
    
    // Initialize default settings
    this.settings = this.getDefaultSettings();
    
    // Initialize core managers
    this.moduleRegistry = new ModuleRegistry();
    this.connectionManager = new ConnectionManager(this);
    this.layoutManager = new LayoutManager(this);
    this.consciousnessManager = new ConsciousnessManager(this);
    this.performanceMonitor = new PerformanceMonitor(this);
    
    // Bind methods to preserve context
    this.update = this.update.bind(this);
    this.handleModuleStateChange = this.handleModuleStateChange.bind(this);
    this.handleConnectionStateChange = this.handleConnectionStateChange.bind(this);
  }

  // ========================================
  // INITIALIZATION & LIFECYCLE
  // ========================================
  
  async initialize(): Promise<void> {
    if (this.isInitialized) return;
    
    try {
      // Initialize all managers
      await this.moduleRegistry.initialize();
      await this.connectionManager.initialize();
      await this.layoutManager.initialize();
      await this.consciousnessManager.initialize();
      await this.performanceMonitor.initialize();
      
      // Start update loop
      this.startUpdateLoop();
      
      // Load default layout if available
      const defaultLayout = await this.layoutManager.getDefaultLayout();
      if (defaultLayout) {
        await this.loadLayout(defaultLayout.id);
      }
      
      this.isInitialized = true;
      this.emit({ type: 'DASHBOARD_INITIALIZED', payload: {} });
      
    } catch (error) {
      this.emit({ type: 'ERROR', payload: { error: error as Error } });
      throw error;
    }
  }
  
  async destroy(): Promise<void> {
    // Stop update loop
    this.stopUpdateLoop();
    
    // Destroy all modules
    for (const moduleId of this.modules.keys()) {
      await this.removeModule(moduleId);
    }
    
    // Cleanup managers
    await this.performanceMonitor.destroy();
    await this.consciousnessManager.destroy();
    await this.layoutManager.destroy();
    await this.connectionManager.destroy();
    await this.moduleRegistry.destroy();
    
    this.isInitialized = false;
    this.emit({ type: 'DASHBOARD_DESTROYED', payload: {} });
  }

  // ========================================
  // MODULE MANAGEMENT
  // ========================================
  
  async addModule(
    type: string, 
    position?: Position, 
    config?: ModuleConfig
  ): Promise<DashboardModule> {
    const moduleDefinition = this.moduleRegistry.getModuleDefinition(type);
    if (!moduleDefinition) {
      throw new Error(`Module type '${type}' not found in registry`);
    }
    
    // Generate unique ID
    const id = `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    // Calculate position (snap to grid if enabled)
    const finalPosition = position ? 
      this.snapToGrid(position) : 
      this.findOptimalPosition(moduleDefinition.defaultSize);
    
    // Create module instance
    const module: DashboardModule = {
      id,
      type,
      title: moduleDefinition.title,
      category: moduleDefinition.category,
      component: moduleDefinition.component,
      position: finalPosition,
      size: { ...moduleDefinition.defaultSize },
      zIndex: this.getNextZIndex(),
      isActive: true,
      isMinimized: false,
      isMaximized: false,
      isLocked: false,
      isDragging: false,
      isResizing: false,
      
      // Visual states
      glowIntensity: 0.5,
      breathingIntensity: 0.5,
      particleDensity: 0.5,
      
      // Configuration
      config: { ...moduleDefinition.defaultConfig, ...config },
      state: {
        status: 'loading',
        lastUpdate: Date.now(),
        consciousness: this.consciousnessManager.getCurrentState()
      },
      
      // Ports
      inputPorts: this.createModulePorts(moduleDefinition.ports?.filter(p => p.type === 'input' || p.type === 'bidirectional') || [], id),
      outputPorts: this.createModulePorts(moduleDefinition.ports?.filter(p => p.type === 'output' || p.type === 'bidirectional') || [], id),
      
      // Lifecycle
      lifecycle: {
        created: Date.now(),
        errorCount: 0,
        restartCount: 0
      },
      
      // Metrics
      metrics: {
        cpuUsage: 0,
        memoryUsage: 0,
        renderTime: 0,
        updateFrequency: 0,
        dataProcessed: 0,
        connectionCount: 0
      }
    };
    
    // Add to modules map
    this.modules.set(id, module);
    
    // Initialize module
    await this.initializeModule(module);
    
    // Emit event
    this.emit({ type: 'MODULE_ADDED', payload: { module } });
    
    return module;
  }
  
  async removeModule(moduleId: string): Promise<void> {
    const module = this.modules.get(moduleId);
    if (!module) {
      throw new Error(`Module '${moduleId}' not found`);
    }
    
    // Remove all connections
    const moduleConnections = this.getConnections(moduleId);
    for (const connection of moduleConnections) {
      await this.removeConnection(connection.id);
    }
    
    // Cleanup module
    await this.cleanupModule(module);
    
    // Remove from map
    this.modules.delete(moduleId);
    
    // Emit event
    this.emit({ type: 'MODULE_REMOVED', payload: { moduleId } });
  }
  
  async updateModule(moduleId: string, updates: Partial<DashboardModule>): Promise<void> {
    const module = this.modules.get(moduleId);
    if (!module) {
      throw new Error(`Module '${moduleId}' not found`);
    }
    
    // Apply updates
    Object.assign(module, {
      ...updates,
      state: {
        ...module.state,
        ...(updates.state || {}),
        lastUpdate: Date.now()
      }
    });
    
    // Handle position updates
    if (updates.position) {
      module.position = this.snapToGrid(updates.position);
    }
    
    // Update connections if ports changed
    if (updates.inputPorts || updates.outputPorts) {
      await this.updateModuleConnections(moduleId);
    }
    
    // Emit event
    this.emit({ type: 'MODULE_UPDATED', payload: { moduleId, updates } });
  }
  
  getModule(moduleId: string): DashboardModule | null {
    return this.modules.get(moduleId) || null;
  }
  
  getAllModules(): DashboardModule[] {
    return Array.from(this.modules.values());
  }

  // ========================================
  // CONNECTION MANAGEMENT
  // ========================================
  
  async createConnection(
    sourceModuleId: string,
    sourcePortId: string,
    targetModuleId: string,
    targetPortId: string
  ): Promise<ModuleConnection> {
    return this.connectionManager.createConnection(
      sourceModuleId,
      sourcePortId,
      targetModuleId,
      targetPortId
    );
  }
  
  async removeConnection(connectionId: string): Promise<void> {
    return this.connectionManager.removeConnection(connectionId);
  }
  
  getConnections(moduleId?: string): ModuleConnection[] {
    return this.connectionManager.getConnections(moduleId);
  }

  // ========================================
  // LAYOUT MANAGEMENT
  // ========================================
  
  async saveLayout(name: string, description?: string): Promise<DashboardLayout> {
    return this.layoutManager.saveLayout(name, description);
  }
  
  async loadLayout(layoutId: string): Promise<void> {
    return this.layoutManager.loadLayout(layoutId);
  }
  
  getLayouts(): DashboardLayout[] {
    return this.layoutManager.getLayouts();
  }
  
  async deleteLayout(layoutId: string): Promise<void> {
    return this.layoutManager.deleteLayout(layoutId);
  }

  // ========================================
  // SETTINGS MANAGEMENT
  // ========================================
  
  async updateSettings(settings: Partial<DashboardSettings>): Promise<void> {
    this.settings = {
      ...this.settings,
      ...settings,
      consciousness: {
        ...this.settings.consciousness,
        ...(settings.consciousness || {})
      },
      performance: {
        ...this.settings.performance,
        ...(settings.performance || {})
      },
      visual: {
        ...this.settings.visual,
        ...(settings.visual || {})
      },
      audio: {
        ...this.settings.audio,
        ...(settings.audio || {})
      },
      interaction: {
        ...this.settings.interaction,
        ...(settings.interaction || {})
      }
    };
    
    // Apply settings changes
    await this.applySettings();
    
    this.emit({ type: 'SETTINGS_UPDATED', payload: { settings: this.settings } });
  }
  
  getSettings(): DashboardSettings {
    return { ...this.settings };
  }

  // ========================================
  // CONSCIOUSNESS CONTROL
  // ========================================
  
  async updateConsciousness(updates: Partial<ConsciousnessState>): Promise<void> {
    return this.consciousnessManager.updateConsciousness(updates);
  }
  
  async pauseConsciousness(): Promise<void> {
    return this.consciousnessManager.pause();
  }
  
  async resumeConsciousness(): Promise<void> {
    return this.consciousnessManager.resume();
  }
  
  async resetConsciousness(): Promise<void> {
    return this.consciousnessManager.reset();
  }

  // ========================================
  // PERFORMANCE MONITORING
  // ========================================
  
  async getMetrics(): Promise<{ dashboard: any; modules: Record<string, any> }> {
    return this.performanceMonitor.getMetrics();
  }

  // ========================================
  // INTERNAL METHODS
  // ========================================
  
  private startUpdateLoop(): void {
    const update = (currentTime: number) => {
      if (currentTime - this.lastUpdateTime >= this.updateInterval) {
        this.update(currentTime);
        this.lastUpdateTime = currentTime;
      }
      this.animationFrameId = requestAnimationFrame(update);
    };
    
    this.animationFrameId = requestAnimationFrame(update);
  }
  
  private stopUpdateLoop(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }
  
  private update(currentTime: number): void {
    // Update consciousness state
    this.consciousnessManager.update(currentTime);
    
    // Update connections (data flow animation)
    this.connectionManager.update(currentTime);
    
    // Update performance metrics
    this.performanceMonitor.update(currentTime);
    
    // Update module states
    this.updateModuleStates(currentTime);
  }
  
  private updateModuleStates(currentTime: number): void {
    for (const module of this.modules.values()) {
      // Update consciousness awareness for each module
      module.state.consciousness = this.consciousnessManager.getCurrentState();
      
      // Update visual states based on consciousness
      this.updateModuleVisualStates(module);
      
      // Update metrics
      this.performanceMonitor.updateModuleMetrics(module);
    }
  }
  
  private updateModuleVisualStates(module: DashboardModule): void {
    const consciousness = module.state.consciousness;
    if (!consciousness) return;
    
    // Update breathing intensity based on neural activity
    module.breathingIntensity = 0.3 + (consciousness.neuralActivity * 0.7);
    
    // Update glow intensity based on SCUP
    module.glowIntensity = 0.2 + (consciousness.scup / 100 * 0.8);
    
    // Update particle density based on entropy
    module.particleDensity = 0.1 + (consciousness.entropy * 0.9);
  }
  
  private async initializeModule(module: DashboardModule): Promise<void> {
    try {
      // Set status to active
      module.state.status = 'active';
      module.lifecycle.activated = Date.now();
      
      // Register event handlers
      this.setupModuleEventHandlers(module);
      
    } catch (error) {
      module.state.status = 'error';
      module.state.error = (error as Error).message;
      module.lifecycle.errorCount++;
      throw error;
    }
  }
  
  private async cleanupModule(module: DashboardModule): Promise<void> {
    // Set status to idle
    module.state.status = 'idle';
    module.lifecycle.deactivated = Date.now();
    
    // Remove event handlers
    this.removeModuleEventHandlers(module);
  }
  
  private setupModuleEventHandlers(module: DashboardModule): void {
    // Add module-specific event handling logic here
  }
  
  private removeModuleEventHandlers(module: DashboardModule): void {
    // Remove module-specific event handling logic here
  }
  
  private createModulePorts(portDefinitions: any[], moduleId: string): ModulePort[] {
    return portDefinitions.map((def, index) => ({
      id: `${moduleId}-port-${index}`,
      type: def.type,
      dataType: def.dataType,
      position: def.position || { x: 0, y: 0 },
      isActive: true,
      isConnected: false,
      maxConnections: def.maxConnections || (def.type === 'input' ? 1 : Infinity),
      currentConnections: [],
      signalStrength: 0,
      description: def.description
    }));
  }
  
  private snapToGrid(position: Position): Position {
    if (!this.settings.interaction.snapToGrid) {
      return position;
    }
    
    const gridSize = 20; // Could be configurable
    return {
      x: Math.round(position.x / gridSize) * gridSize,
      y: Math.round(position.y / gridSize) * gridSize,
      z: position.z
    };
  }
  
  private findOptimalPosition(size: Size): Position {
    // Simple algorithm to find non-overlapping position
    const padding = 20;
    let x = padding;
    let y = padding;
    
    // Check for overlaps and adjust position
    while (this.hasOverlap({ x, y }, size)) {
      x += size.width + padding;
      if (x > 1200) { // Assume max width
        x = padding;
        y += size.height + padding;
      }
    }
    
    return { x, y };
  }
  
  private hasOverlap(position: Position, size: Size): boolean {
    for (const module of this.modules.values()) {
      if (this.rectsOverlap(
        position.x, position.y, size.width, size.height,
        module.position.x, module.position.y, module.size.width, module.size.height
      )) {
        return true;
      }
    }
    return false;
  }
  
  private rectsOverlap(
    x1: number, y1: number, w1: number, h1: number,
    x2: number, y2: number, w2: number, h2: number
  ): boolean {
    return !(x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
  }
  
  private getNextZIndex(): number {
    let maxZ = 0;
    for (const module of this.modules.values()) {
      maxZ = Math.max(maxZ, module.zIndex);
    }
    return maxZ + 1;
  }
  
  private async updateModuleConnections(moduleId: string): Promise<void> {
    // Update connection positions and validity
    const connections = this.getConnections(moduleId);
    for (const connection of connections) {
      await this.connectionManager.updateConnection(connection.id);
    }
  }
  
  private async applySettings(): Promise<void> {
    // Apply consciousness settings
    if (this.settings.consciousness) {
      await this.consciousnessManager.applySettings(this.settings.consciousness);
    }
    
    // Apply performance settings
    if (this.settings.performance) {
      this.updateInterval = 1000 / this.settings.performance.maxFPS;
      await this.performanceMonitor.applySettings(this.settings.performance);
    }
    
    // Update all modules with new settings
    for (const module of this.modules.values()) {
      this.updateModuleVisualStates(module);
    }
  }
  
  private handleModuleStateChange(moduleId: string, state: any): void {
    // Handle module state changes
    this.emit({ type: 'MODULE_STATE_CHANGED', payload: { moduleId, state } });
  }
  
  private handleConnectionStateChange(connectionId: string, state: any): void {
    // Handle connection state changes
    this.emit({ type: 'CONNECTION_STATE_CHANGED', payload: { connectionId, state } });
  }
  
  private getDefaultSettings(): DashboardSettings {
    return {
      consciousness: {
        globalSCUP: 50,
        globalEntropy: 0.5,
        globalMood: 'calm',
        tickRate: 60,
        isPaused: false,
        systemUnity: 0.5,
        neuralActivity: 0.5,
        dreamMode: false
      },
      performance: {
        maxFPS: 60,
        lowPowerMode: false,
        particleQuality: 'high',
        animationQuality: 'high',
        enableProfiling: false,
        memoryLimit: 512
      },
      visual: {
        theme: 'cosmic',
        glowEnabled: true,
        particlesEnabled: true,
        connectionsVisible: true,
        gridVisible: true,
        backgroundIntensity: 0.8,
        uiOpacity: 0.9
      },
      audio: {
        enabled: true,
        volume: 0.5,
        spatialAudio: true,
        consciousnessAudio: true,
        dataFlowSounds: true
      },
      interaction: {
        dragSensitivity: 1.0,
        snapToGrid: true,
        magneticSnap: true,
        keyboardShortcuts: true,
        gestureControls: false,
        voiceCommands: false
      }
    };
  }
}

// Export singleton instance
export const dashboardCore = new DashboardCore(); 