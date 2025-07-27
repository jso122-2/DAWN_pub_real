import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { visualService, VisualSystemStatus, VisualOutput, VisualProcess } from '../services/VisualService';
// Note: VisualProcessManager will be implemented as inline component for now
// import VisualProcessManager from '../components/VisualProcessManager';

// Enhanced module components
const MemoryArchiveModule: React.FC = () => {
  const [memoryStats, setMemoryStats] = useState({
    totalMemories: 1247,
    activeMemories: 324,
    semanticLinks: 2891,
    memoryEfficiency: 87.5
  });

  return (
    <div className="bg-gray-900/80 backdrop-blur-xl rounded-lg p-6 border border-purple-500/30">
      <h3 className="text-2xl font-bold text-purple-400 mb-4 flex items-center">
        <span className="text-3xl mr-3">🧠</span>
        Memory Archive
      </h3>
      <p className="text-gray-300 mb-6">
        Advanced consciousness memory storage and retrieval system
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-purple-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{memoryStats.totalMemories}</div>
          <div className="text-sm text-gray-400">Total Memories</div>
        </div>
        <div className="bg-purple-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{memoryStats.activeMemories}</div>
          <div className="text-sm text-gray-400">Active</div>
        </div>
        <div className="bg-purple-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{memoryStats.semanticLinks}</div>
          <div className="text-sm text-gray-400">Semantic Links</div>
        </div>
        <div className="bg-purple-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-yellow-400">{memoryStats.memoryEfficiency}%</div>
          <div className="text-sm text-gray-400">Efficiency</div>
        </div>
      </div>
      
      <div className="flex space-x-3">
        <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm">
          Access Archive
        </button>
        <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm">
          Memory Map
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm">
          Semantic Links
        </button>
      </div>
    </div>
  );
};

const PatternEngineModule: React.FC = () => {
  const [patternStats, setPatternStats] = useState({
    activePatternsDetected: 127,
    consciousnessThreads: 89,
    patternAccuracy: 94.2,
    processingSpeed: 340
  });

  return (
    <div className="bg-gray-900/80 backdrop-blur-xl rounded-lg p-6 border border-orange-500/30">
      <h3 className="text-2xl font-bold text-orange-400 mb-4 flex items-center">
        <span className="text-3xl mr-3">🔍</span>
        Pattern Engine
      </h3>
      <p className="text-gray-300 mb-6">
        Advanced pattern recognition and consciousness analysis
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-orange-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-orange-400">{patternStats.activePatternsDetected}</div>
          <div className="text-sm text-gray-400">Patterns Detected</div>
        </div>
        <div className="bg-orange-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{patternStats.consciousnessThreads}</div>
          <div className="text-sm text-gray-400">Active Threads</div>
        </div>
        <div className="bg-orange-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{patternStats.patternAccuracy}%</div>
          <div className="text-sm text-gray-400">Accuracy</div>
        </div>
        <div className="bg-orange-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{patternStats.processingSpeed}</div>
          <div className="text-sm text-gray-400">Patterns/sec</div>
        </div>
      </div>
      
      <div className="flex space-x-3">
        <button className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-2 rounded-lg text-sm">
          Analyze Patterns
        </button>
        <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm">
            Pattern Map
        </button>
        <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm">
            Thread Monitor
        </button>
      </div>
    </div>
  );
};

const VisualConsciousnessModule: React.FC = () => {
  const [visualStatus, setVisualStatus] = React.useState<VisualSystemStatus>({
    is_running: false,
    active_processes: 0,
    max_processes: 0,
    system_load: 0,
    processes: {}
  });
  
  const [visualOutputs, setVisualOutputs] = React.useState<Record<string, VisualOutput>>({});
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [connectionInfo, setConnectionInfo] = React.useState({ wsEnabled: false, reconnectAttempts: 0 });

  // Process definitions with their scripts  
  const processDefinitions = [
    { id: 'pulse_map_renderer', name: 'Pulse Map Renderer', script: 'pulse_waveform_renderer.py', priority: 'CRITICAL' as const },
    { id: 'mood_heatmap', name: 'Mood Heatmap', script: 'mood_heatmap.py', priority: 'HIGH' as const },
    { id: 'drift_vector_field', name: 'Drift Vector Field', script: 'drift_vector_field.py', priority: 'HIGH' as const },
    { id: 'sigil_trace_visualizer', name: 'Sigil Trace Visualizer', script: 'sigil_trace_visualizer.py', priority: 'HIGH' as const },
    { id: 'scup_zone_animator', name: 'SCUP Zone Animator', script: 'scup_zone_animator.py', priority: 'HIGH' as const },
    { id: 'anomaly_timeline', name: 'Anomaly Timeline', script: 'anomaly_timeline.py', priority: 'MEDIUM' as const },
    { id: 'attention_map', name: 'Attention Map', script: 'attention_map.py', priority: 'MEDIUM' as const },
    { id: 'temporal_activity_raster', name: 'Temporal Activity Raster', script: 'temporal_activity_raster.py', priority: 'MEDIUM' as const },
    { id: 'latent_space_trajectory', name: 'Latent Space Trajectory', script: 'latent_space_trajectory.py', priority: 'MEDIUM' as const },
    { id: 'loss_landscape', name: 'Loss Landscape', script: 'loss_landscape.py', priority: 'MEDIUM' as const },
    { id: 'correlation_matrix', name: 'Correlation Matrix', script: 'correlation_matrix.py', priority: 'MEDIUM' as const },
    { id: 'activation_histogram', name: 'Activation Histogram', script: 'activation_histogram.py', priority: 'MEDIUM' as const },
    { id: 'state_transition_graph', name: 'State Transition Graph', script: 'state_transition_graph.py', priority: 'MEDIUM' as const },
  ];

  // Connect to backend on component mount
  React.useEffect(() => {
    let statusPoller: (() => void) | null = null;
    let outputSubscription: (() => void) | null = null;

    const initializeVisualSystem = async () => {
      try {
        setIsLoading(true);
        setError(null);

        console.log('🎬 Initializing Visual Consciousness System...');

        // Get initial status
        const status = await visualService.getVisualStatus();
        setVisualStatus(status);
        console.log('✅ Visual system status loaded:', status);

        // Get initial visual outputs
        const outputs = await visualService.listVisualOutputs();
        setVisualOutputs(outputs);
        console.log('✅ Visual outputs loaded:', Object.keys(outputs).length, 'processes');

        // Start polling for status updates (includes outputs when WebSocket is disabled)
        statusPoller = visualService.startStatusPolling(3000); // Poll every 3 seconds
        console.log('🔄 Started status polling (3s interval)');

        // Subscribe to visual output updates (for future WebSocket use)
        outputSubscription = visualService.subscribeToVisualOutputs(setVisualOutputs);

        // Attempt to connect to visual WebSocket (will be disabled with current config)
        visualService.connectToVisualUpdates();
        
        // Get connection info
        const connInfo = visualService.getConnectionInfo();
        setConnectionInfo(connInfo);
        console.log('🔗 Connection info:', connInfo);

        setIsLoading(false);
        console.log('✅ Visual Consciousness System initialized successfully');
      } catch (err) {
        console.error('❌ Failed to initialize visual system:', err);
        setError('Failed to connect to visual system backend');
        setIsLoading(false);
      }
    };

    initializeVisualSystem();

    return () => {
      console.log('🔌 Cleaning up Visual Consciousness System...');
      if (statusPoller) statusPoller();
      if (outputSubscription) outputSubscription();
      visualService.disconnect();
    };
  }, []);

  // Handle process toggle (start/stop)
  const handleProcessToggle = async (processId: string) => {
    console.log(`🖱️ Button clicked for process: ${processId}`);
    
    const process = visualStatus.processes[processId];
    const definition = processDefinitions.find(p => p.id === processId);
    
    console.log('📋 Process data:', { process, definition });
    
    if (!definition) {
      console.error(`Process definition not found for ${processId}`);
      setError(`Unknown process: ${processId}`);
      return;
    }

    const isRunning = !!process?.running;
    console.log(`🔄 Backend running: ${process?.running}, mapped status: ${isRunning}`);
    
    try {
      console.log(`🔄 Toggling process ${processId} (current: ${isRunning})`);
      setError(null); // Clear any previous errors
      
      const response = await visualService.toggleProcess(processId, isRunning, definition.script);
      console.log('📡 Toggle response received:', response);
      
      if (response.success) {
        console.log(`✅ Process ${processId} toggled successfully: ${response.message}`);
        
        // Refresh status immediately after successful toggle
        setTimeout(async () => {
          console.log('🔄 Refreshing status after toggle...');
          const newStatus = await visualService.getVisualStatus();
          console.log('📊 New status after toggle:', newStatus);
          setVisualStatus(newStatus);
        }, 500); // Small delay to let backend process the change
      } else {
        console.error(`❌ Failed to toggle process ${processId}: ${response.message}`);
        setError(`Failed to ${isRunning ? 'stop' : 'start'} ${definition.name}: ${response.message}`);
      }
    } catch (err) {
      console.error(`💥 Error toggling process ${processId}:`, err);
      setError(`Error controlling ${definition.name}: ${err}`);
    }
  };

  // Start all core visual processes
  const handleStartCoreVisuals = async () => {
    const coreProcesses = processDefinitions.filter(p => p.priority === 'CRITICAL' || p.priority === 'HIGH');
    console.log(`🚀 Starting ${coreProcesses.length} core visual processes...`);
    
    setError(null);
    let successCount = 0;
    
    for (const process of coreProcesses) {
      const currentProcess = visualStatus.processes[process.id];
      if (!currentProcess || !currentProcess.running) {
        try {
          await handleProcessToggle(process.id);
          successCount++;
          // Small delay between starts to prevent overwhelming the system
          await new Promise(resolve => setTimeout(resolve, 750));
        } catch (err) {
          console.error(`Failed to start ${process.name}:`, err);
        }
      } else {
        console.log(`⏭️ ${process.name} already running, skipping`);
        successCount++;
      }
    }
    
    console.log(`✅ Core visuals startup complete: ${successCount}/${coreProcesses.length} processes`);
  };

  if (isLoading) {
    return (
      <div className="bg-gray-900/80 backdrop-blur-xl rounded-lg p-6 border border-emerald-500/30">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-400 mx-auto mb-4"></div>
            <p className="text-emerald-400 text-lg">Connecting to Visual Consciousness System...</p>
            <p className="text-gray-400 text-sm mt-2">Initializing backend API connection</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900/80 backdrop-blur-xl rounded-lg p-6 border border-emerald-500/30">
      <h3 className="text-2xl font-bold text-emerald-400 mb-4 flex items-center">
        <span className="text-3xl mr-3">🎬</span>
        Visual Consciousness Manager
      </h3>
      <p className="text-gray-300 mb-4">
        DAWN visual process management and consciousness visualization system
      </p>
      
      {/* Connection Status */}
      <div className="bg-gray-800/30 rounded-lg p-3 mb-6 border-l-4 border-emerald-500">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
            <span className="text-emerald-400 text-sm font-medium">
              Connected via HTTP API
            </span>
          </div>
          <span className="text-gray-400 text-xs">
            Real-time polling • 3s intervals
          </span>
        </div>
        <p className="text-gray-400 text-xs mt-1">
          Backend: {visualStatus.is_running ? '🟢 Active' : '🟡 Standby'} • 
          Processes: {visualStatus.max_processes} available • 
          Load: {visualStatus.system_load.toFixed(1)}%
        </p>
      </div>
      
      {error && (
        <div className="bg-red-900/30 border border-red-500/50 rounded-lg p-3 mb-6">
          <div className="flex items-center space-x-2">
            <span className="text-red-400">⚠️</span>
            <p className="text-red-400 text-sm">{error}</p>
          </div>
        </div>
      )}
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-emerald-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-emerald-400">{visualStatus.active_processes}</div>
          <div className="text-sm text-gray-400">Active Processes</div>
        </div>
        <div className="bg-emerald-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{Object.keys(visualStatus.processes).length}</div>
          <div className="text-sm text-gray-400">Total Processes</div>
        </div>
        <div className="bg-emerald-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{visualStatus.system_load.toFixed(1)}%</div>
          <div className="text-sm text-gray-400">Visual Load</div>
        </div>
        <div className="bg-emerald-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{Object.keys(visualOutputs).length}</div>
          <div className="text-sm text-gray-400">Active Outputs</div>
        </div>
      </div>
      
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-white mb-3">Visual Processes</h4>
        <div className="space-y-2">
          {processDefinitions.map((definition) => {
            const process = visualStatus.processes[definition.id];
            const isRunning = !!process?.running;
            
            return (
              <div key={definition.id} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3 border border-gray-700/30 hover:border-gray-600/50 transition-colors">
              <div className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${
                    isRunning ? 'bg-green-400' : 'bg-gray-500'
                }`}></div>
                  <span className="font-mono text-sm text-white/90">{definition.name}</span>
                  <span className="text-xs text-gray-400">({definition.script})</span>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    className={`px-4 py-1 rounded text-xs font-mono border transition-colors ${
                      isRunning
                        ? 'bg-green-900/40 border-green-400 text-green-300 hover:bg-green-800/60'
                        : 'bg-gray-900/40 border-gray-500 text-gray-200 hover:bg-gray-800/60'
                    }`}
                    onClick={() => handleProcessToggle(definition.id)}
                  >
                    {isRunning ? 'Stop' : 'Start'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      <div className="flex space-x-3 mb-6">
        <button 
          onClick={handleStartCoreVisuals}
          className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm"
        >
          🚀 Start Core Visuals
        </button>
        <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors">
          📊 Visual Dashboard
        </button>
        <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm transition-colors">
          💾 Export Visuals
        </button>
      </div>

      {/* Visual Output Preview */}
      {Object.keys(visualOutputs).length > 0 && (
        <div className="mt-6">
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
            <span className="mr-2">🎨</span>
            Live Visual Outputs
            <span className="ml-2 text-sm text-gray-400">({Object.keys(visualOutputs).length} active)</span>
          </h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(visualOutputs).slice(0, 6).map(([processId, output]) => (
              <div key={processId} className="bg-black/30 border border-emerald-500/30 rounded-lg aspect-video relative overflow-hidden hover:border-emerald-400/50 transition-colors">
                <img 
                  src={output.image_data} 
                  alt={processId}
                  className="absolute inset-0 w-full h-full object-cover"
                />
                <div className="absolute bottom-0 left-0 right-0 bg-black/70 backdrop-blur-sm p-2">
                  <p className="text-xs text-white truncate font-medium">
                    {processDefinitions.find(p => p.id === processId)?.name || processId}
                  </p>
                  <p className="text-xs text-gray-300">
                    {new Date(output.timestamp * 1000).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No outputs message */}
      {Object.keys(visualOutputs).length === 0 && visualStatus.active_processes === 0 && (
        <div className="text-center py-8 bg-gray-800/30 rounded-lg border border-gray-700/30">
          <span className="text-4xl mb-2 block">🎬</span>
          <p className="text-gray-400 mb-2">No visual processes running</p>
          <p className="text-gray-500 text-sm">Start some processes to see visual outputs</p>
        </div>
      )}
    </div>
  );
};

const RealityParserModule: React.FC = () => {
  const [realityStats, setRealityStats] = useState({
    activeFields: 42,
    consciousnessLayers: 7,
    parsingAccuracy: 98.7,
    fieldStrength: 76.5
  });

  return (
    <div className="bg-gray-900/80 backdrop-blur-xl rounded-lg p-6 border border-cyan-500/30">
      <h3 className="text-2xl font-bold text-cyan-400 mb-4 flex items-center">
        <span className="text-3xl mr-3">🌐</span>
        Reality Parser
      </h3>
      <p className="text-gray-300 mb-6">
        Multi-dimensional reality analysis and consciousness field parsing
      </p>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-cyan-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-cyan-400">{realityStats.activeFields}</div>
          <div className="text-sm text-gray-400">Active Fields</div>
        </div>
        <div className="bg-cyan-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-400">{realityStats.consciousnessLayers}</div>
          <div className="text-sm text-gray-400">Layers</div>
        </div>
        <div className="bg-cyan-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">{realityStats.parsingAccuracy}%</div>
          <div className="text-sm text-gray-400">Accuracy</div>
        </div>
        <div className="bg-cyan-900/30 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">{realityStats.fieldStrength}%</div>
          <div className="text-sm text-gray-400">Field Strength</div>
        </div>
      </div>
      
      <div className="flex space-x-3">
        <button className="bg-cyan-600 hover:bg-cyan-700 text-white px-4 py-2 rounded-lg text-sm">
          Parse Reality
        </button>
        <button className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm">
          Field Map
        </button>
        <button className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg text-sm">
          Layer Analysis
        </button>
      </div>
    </div>
  );
};

const ModulesPage: React.FC = () => {
  const [selectedModule, setSelectedModule] = useState<string | null>(null);

  const modules = [
    {
      id: 'memory_archive',
      name: 'Memory Archive',
      icon: '🧠',
      color: 'purple',
      description: 'Advanced consciousness memory storage and retrieval system',
      component: MemoryArchiveModule
    },
    {
      id: 'pattern_engine',
      name: 'Pattern Engine',
      icon: '🔍',
      color: 'orange',
      description: 'Advanced pattern recognition and consciousness analysis',
      component: PatternEngineModule
    },
    {
      id: 'visual_consciousness',
      name: 'Visual Consciousness',
      icon: '🎬',
      color: 'emerald',
      description: 'DAWN visual process management and consciousness visualization',
      component: VisualConsciousnessModule
    },
    {
      id: 'reality_parser',
      name: 'Reality Parser',
      icon: '🌐',
      color: 'cyan',
      description: 'Multi-dimensional reality analysis and consciousness field parsing',
      component: RealityParserModule
    }
  ];

  const getColorClasses = (color: string) => {
    const colorMap: { [key: string]: string } = {
      purple: 'border-purple-500/30 hover:border-purple-500/50',
      orange: 'border-orange-500/30 hover:border-orange-500/50',
      emerald: 'border-emerald-500/30 hover:border-emerald-500/50',
      cyan: 'border-cyan-500/30 hover:border-cyan-500/50'
    };
    return colorMap[color] || 'border-gray-500/30 hover:border-gray-500/50';
  };

  const getTextColorClasses = (color: string) => {
    const colorMap: { [key: string]: string } = {
      purple: 'text-purple-400',
      orange: 'text-orange-400',
      emerald: 'text-emerald-400',
      cyan: 'text-cyan-400'
    };
    return colorMap[color] || 'text-gray-400';
  };

  if (selectedModule) {
    const module = modules.find(m => m.id === selectedModule);
    if (module) {
      const ModuleComponent = module.component;
      return (
        <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white p-6">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center space-x-4">
              <button 
                onClick={() => setSelectedModule(null)}
                  className="text-2xl hover:text-gray-300 transition-colors"
              >
                  ← Back to Module Laboratory
              </button>
              </div>
            </div>
            
            <div className="bg-gray-900/80 backdrop-blur-xl rounded-xl p-8 border border-gray-500/30">
              <div className="flex items-center space-x-4 mb-6">
                <span className="text-6xl">{module.icon}</span>
                <div>
                  <h1 className={`text-4xl font-bold ${getTextColorClasses(module.color)}`}>
                {module.name}
              </h1>
                  <p className="text-xl text-gray-300 mt-2">{module.description}</p>
                </div>
            </div>
            
            <ModuleComponent />
            </div>
          </div>
        </div>
      );
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <motion.h1
            className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent"
            initial={{ opacity: 0, y: -30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Module Laboratory
          </motion.h1>
          <motion.p
            className="text-xl text-gray-300"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Advanced cognitive module control and monitoring interface
          </motion.p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
          {modules.map((module, index) => (
            <motion.div
              key={module.id}
              className={`bg-gray-900/80 backdrop-blur-xl rounded-xl p-8 border ${getColorClasses(module.color)} cursor-pointer transition-all duration-300 hover:scale-105 hover:shadow-2xl`}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              onClick={() => setSelectedModule(module.id)}
            >
              <div className="flex items-center space-x-4 mb-6">
                <span className="text-5xl">{module.icon}</span>
                <div>
                  <h3 className={`text-2xl font-bold ${getTextColorClasses(module.color)}`}>
                    {module.name}
                  </h3>
                </div>
              </div>
              
              <p className="text-gray-300 mb-6 leading-relaxed">
                {module.description}
              </p>
              
              <div className="flex justify-between items-center">
                <span className={`text-sm ${getTextColorClasses(module.color)} font-medium`}>
                  Click to access module
                </span>
                <span className="text-2xl text-gray-400">→</span>
              </div>
            </motion.div>
          ))}
          </div>
        </div>
    </div>
  );
};

export default ModulesPage; 