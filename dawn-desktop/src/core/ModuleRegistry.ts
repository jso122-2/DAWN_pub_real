// 🧠 MODULE REGISTRY - Dynamic Module System for DAWN Dashboard
import React from 'react';
import { ModuleDefinition, Size, ModuleConfig } from '../types/dashboard.types';

// Dynamic imports for existing modules
const ConsciousnessVisualizer = React.lazy(() => 
  import('../components/modules/ConsciousnessVisualizer/ConsciousnessVisualizer').then(m => ({ default: m.ConsciousnessVisualizer }))
);

const DAWNDashboard = React.lazy(() => 
  import('../components/modules/DAWNDashboard').then(m => ({ default: m.default }))
);

const TickLoopMonitor = React.lazy(() => 
  import('../components/modules/TickLoopMonitor').then(m => ({ default: m.default }))
);

const PythonProcessManager = React.lazy(() => 
  import('../components/modules/PythonProcessManager').then(m => ({ default: m.default }))
);

const ProcessControlPanel = React.lazy(() => 
  import('../components/modules/ProcessControlPanel').then(m => ({ default: m.default }))
);

const NeuralNetworkModule = React.lazy(() => 
  import('../components/modules/NeuralNetworkModule').then(m => ({ default: m.default }))
);

const ConsciousnessCore = React.lazy(() => 
  import('../components/modules/ConsciousnessCore').then(m => ({ default: m.default }))
);

const MetricsPanel = React.lazy(() => 
  import('../components/MetricsPanel').then(m => ({ default: m.default }))
);

const EventStream = React.lazy(() => 
  import('../components/EventStream').then(m => ({ default: m.default }))
);

export class ModuleRegistry {
  private moduleDefinitions: Map<string, ModuleDefinition> = new Map();
  private loadedModules: Map<string, React.ComponentType<any>> = new Map();
  private isInitialized = false;

  constructor() {
    this.registerBuiltInModules();
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) return;
    await this.preloadCriticalModules();
    this.isInitialized = true;
  }

  async destroy(): Promise<void> {
    this.moduleDefinitions.clear();
    this.loadedModules.clear();
    this.isInitialized = false;
  }

  registerModule(definition: ModuleDefinition): void {
    this.moduleDefinitions.set(definition.type, definition);
  }

  unregisterModule(type: string): void {
    this.moduleDefinitions.delete(type);
    this.loadedModules.delete(type);
  }

  getModuleDefinition(type: string): ModuleDefinition | null {
    return this.moduleDefinitions.get(type) || null;
  }

  getAllModuleDefinitions(): ModuleDefinition[] {
    return Array.from(this.moduleDefinitions.values());
  }

  getModulesByCategory(category: string): ModuleDefinition[] {
    return Array.from(this.moduleDefinitions.values())
      .filter(def => def.category === category);
  }

  async loadModule(type: string): Promise<React.ComponentType<any>> {
    const loadedModule = this.loadedModules.get(type);
    if (loadedModule) return loadedModule;

    const definition = this.getModuleDefinition(type);
    if (!definition) {
      throw new Error(`Module type '${type}' not found in registry`);
    }

    try {
      if (definition.component) {
        this.loadedModules.set(type, definition.component);
        return definition.component;
      }

      const moduleComponent = await this.dynamicImport(type);
      this.loadedModules.set(type, moduleComponent);
      return moduleComponent;

    } catch (error) {
      throw new Error(`Failed to load module '${type}': ${(error as Error).message}`);
    }
  }

  validateModule(definition: ModuleDefinition): string[] {
    const errors: string[] = [];

    if (!definition.type || definition.type.trim() === '') {
      errors.push('Module type is required');
    }

    if (!definition.title || definition.title.trim() === '') {
      errors.push('Module title is required');
    }

    if (!definition.category) {
      errors.push('Module category is required');
    }

    if (!definition.component && !definition.type.startsWith('external:')) {
      errors.push('Module component is required for built-in modules');
    }

    return errors;
  }

  searchModules(query: string): ModuleDefinition[] {
    const lowerQuery = query.toLowerCase();
    
    return Array.from(this.moduleDefinitions.values())
      .filter(def => 
        def.title.toLowerCase().includes(lowerQuery) ||
        def.description.toLowerCase().includes(lowerQuery) ||
        def.type.toLowerCase().includes(lowerQuery) ||
        (def.tags && def.tags.some(tag => tag.toLowerCase().includes(lowerQuery)))
      );
  }

  private registerBuiltInModules(): void {
    // Consciousness and Monitoring Modules
    this.registerModule({
      type: 'consciousness-visualizer',
      title: 'Consciousness Visualizer',
      category: 'monitor',
      description: 'Real-time visualization of consciousness states with waveforms, particles, and neural maps',
      component: ConsciousnessVisualizer,
      defaultConfig: { fullscreen: false },
      defaultSize: { width: 600, height: 400, minWidth: 400, minHeight: 300 },
      icon: '🧠',
      color: '#667eea',
             ports: [
         { type: 'input', dataType: 'consciousness', position: { x: 0, y: 50 }, maxConnections: 1, description: 'Consciousness data input' },
         { type: 'output', dataType: 'neural', position: { x: 100, y: 25 }, maxConnections: -1, description: 'Neural activity output' }
       ],
      tags: ['consciousness', 'visualization', 'neural'],
      version: '2.0.0'
    });

    this.registerModule({
      type: 'dawn-dashboard',
      title: 'DAWN System Dashboard',
      category: 'monitor',
      description: 'Main system dashboard with real-time metrics and controls',
      component: DAWNDashboard,
      defaultConfig: {},
      defaultSize: { width: 800, height: 600, minWidth: 600, minHeight: 400 },
      icon: '🎛️',
      color: '#3b82f6',
      tags: ['dashboard', 'system', 'metrics'],
      version: '1.5.0'
    });

    this.registerModule({
      type: 'tick-loop-monitor',
      title: 'Tick Loop Monitor',
      category: 'timeline',
      description: 'Monitor and visualize the system tick loop with real-time performance metrics',
      component: TickLoopMonitor,
      defaultConfig: { showParticles: true },
      defaultSize: { width: 500, height: 350, minWidth: 400, minHeight: 250 },
      icon: '⏱️',
      color: '#10b981',
      tags: ['timing', 'performance', 'monitor'],
      version: '1.2.0'
    });

    this.registerModule({
      type: 'python-process-manager',
      title: 'Python Process Manager',
      category: 'process',
      description: 'Manage and monitor Python processes with tick-aware execution',
      component: PythonProcessManager,
      defaultConfig: { autoStart: false },
      defaultSize: { width: 700, height: 500, minWidth: 500, minHeight: 350 },
      icon: '🐍',
      color: '#f59e0b',
      tags: ['python', 'process', 'execution'],
      version: '2.1.0'
    });

    this.registerModule({
      type: 'process-control-panel',
      title: 'Process Control Panel',
      category: 'process',
      description: 'Visual process pipeline control with dependency management',
      component: ProcessControlPanel,
      defaultConfig: { showDependencies: true },
      defaultSize: { width: 800, height: 600, minWidth: 600, minHeight: 400 },
      icon: '⚙️',
      color: '#8b5cf6',
      tags: ['process', 'control', 'pipeline'],
      version: '1.8.0'
    });

    this.registerModule({
      type: 'neural-network-module',
      title: 'Neural Network',
      category: 'neural',
      description: 'Interactive neural network visualization with real-time processing',
      component: NeuralNetworkModule,
      defaultConfig: { layers: 3, animated: true },
      defaultSize: { width: 600, height: 400, minWidth: 400, minHeight: 300 },
      icon: '🧬',
      color: '#ec4899',
      tags: ['neural', 'network', 'ai'],
      version: '1.4.0'
    });

    this.registerModule({
      type: 'consciousness-core',
      title: 'Consciousness Core',
      category: 'consciousness',
      description: 'Consciousness state management and unity visualization',
      component: ConsciousnessCore,
      defaultConfig: { unityThreshold: 0.7 },
      defaultSize: { width: 400, height: 300, minWidth: 300, minHeight: 250 },
      icon: '⚛️',
      color: '#06b6d4',
      tags: ['consciousness', 'unity', 'state'],
      version: '1.1.0'
    });

    this.registerModule({
      type: 'metrics-panel',
      title: 'Metrics Panel',
      category: 'monitor',
      description: 'Advanced metrics visualization with gauges and charts',
      component: MetricsPanel,
      defaultConfig: { showHistory: true },
      defaultSize: { width: 600, height: 500, minWidth: 400, minHeight: 350 },
      icon: '📊',
      color: '#84cc16',
      tags: ['metrics', 'charts', 'visualization'],
      version: '2.0.0'
    });

    this.registerModule({
      type: 'event-stream',
      title: 'Event Stream',
      category: 'timeline',
      description: 'Real-time event monitoring and timeline visualization',
      component: EventStream,
      defaultConfig: { maxEvents: 100 },
      defaultSize: { width: 500, height: 600, minWidth: 400, minHeight: 400 },
      icon: '📺',
      color: '#6366f1',
      tags: ['events', 'timeline', 'monitoring'],
      version: '1.6.0'
    });
  }

  private async preloadCriticalModules(): Promise<void> {
    const criticalModules = [
      'consciousness-visualizer',
      'dawn-dashboard',
      'tick-loop-monitor'
    ];

    for (const type of criticalModules) {
      try {
        await this.loadModule(type);
      } catch (error) {
        console.warn(`Failed to preload critical module '${type}':`, error);
      }
    }
  }

  private async dynamicImport(type: string): Promise<React.ComponentType<any>> {
    throw new Error(`Dynamic import not implemented for external module: ${type}`);
  }
}

export const moduleRegistry = new ModuleRegistry();
