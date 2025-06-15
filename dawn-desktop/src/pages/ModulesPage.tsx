import React, { useState, useEffect } from 'react';
import { Brain, Archive, Search, Eye, Zap, TrendingUp, Database, Settings, Play, Pause, Download, BarChart3, Map, RotateCcw } from 'lucide-react';

// Inline VisualConsciousnessModule component to avoid import path issues
const VisualConsciousnessModule: React.FC<{ onProcessToggle?: (processId: string, enabled: boolean) => void }> = ({ onProcessToggle }) => {
  const [processes, setProcesses] = useState([
    { id: 'pulse_map_renderer', name: 'Pulse Map Renderer', enabled: true, priority: 'CRITICAL', mode: 'realtime', fps: 15.0 },
    { id: 'mood_heatmap', name: 'Mood Heatmap', enabled: false, priority: 'HIGH', mode: 'realtime', fps: 10.0 },
    { id: 'drift_vector_field', name: 'Drift Vector Field', enabled: true, priority: 'HIGH', mode: 'periodic', fps: 8.0 },
    { id: 'sigil_trace_visualizer', name: 'Sigil Trace Visualizer', enabled: false, priority: 'MEDIUM', mode: 'triggered', fps: 12.0 },
    { id: 'tracer_drift_vectors', name: 'Tracer Drift Vectors', enabled: true, priority: 'MEDIUM', mode: 'realtime', fps: 6.0 },
    { id: 'synthesis_entropy_chart', name: 'Synthesis Entropy Chart', enabled: false, priority: 'MEDIUM', mode: 'periodic', fps: 5.0 },
    { id: 'rebloom_trail_animation', name: 'Rebloom Trail Animation', enabled: true, priority: 'LOW', mode: 'triggered', fps: 10.0 },
    { id: 'recursive_bloom_tree', name: 'Recursive Bloom Tree', enabled: false, priority: 'LOW', mode: 'snapshot', fps: 10.0 },
    { id: 'hybrid_field_visualizer', name: 'Hybrid Field Visualizer', enabled: true, priority: 'LOW', mode: 'periodic', fps: 4.0 },
    { id: 'semantic_timeline_animator', name: 'Semantic Timeline Animator', enabled: false, priority: 'LOW', mode: 'periodic', fps: 3.0 },
    { id: 'stall_density_animator', name: 'Stall Density Animator', enabled: false, priority: 'POETIC', mode: 'triggered', fps: 2.0 },
    { id: 'scup_zone_animator', name: 'SCUP Zone Animator', enabled: true, priority: 'POETIC', mode: 'periodic', fps: 1.0 }
  ]);

  const [systemStats, setSystemStats] = useState({
    activeProcesses: 5,
    totalProcesses: 12,
    systemLoad: 34.7,
    averageFps: 28.4
  });

  const [visualOutputs, setVisualOutputs] = useState<{[key: string]: {image_data: string, timestamp: number}}>({});
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);

  // WebSocket connection for real-time visual updates
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/ws/visual');
    
    ws.onopen = () => {
      console.log('🔗 Connected to visual WebSocket');
      setWebsocket(ws);
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'visual_update' && data.processes) {
          setVisualOutputs(data.processes);
        }
      } catch (error) {
        console.error('Error parsing visual WebSocket message:', error);
      }
    };
    
    ws.onclose = () => {
      console.log('🔌 Visual WebSocket disconnected');
      setWebsocket(null);
    };
    
    ws.onerror = (error) => {
      console.error('Visual WebSocket error:', error);
    };
    
    return () => {
      ws.close();
    };
  }, []);

  const handleProcessToggle = async (processId: string) => {
    const process = processes.find(p => p.id === processId);
    if (!process) return;

    const newEnabled = !process.enabled;
    
    try {
      const API_BASE_URL = 'http://localhost:8001';
      
      if (newEnabled) {
        // Start the process
        const response = await fetch(`${API_BASE_URL}/api/visual/start`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            process_id: processId,
            script: `${processId}.py`,
            parameters: { fps: process.fps, duration: 300 }
          })
        });
        
        if (response.ok) {
          console.log(`✅ Started visual process: ${processId}`);
        } else {
          console.error(`❌ Failed to start visual process: ${processId}`);
        }
      } else {
        // Stop the process
        const response = await fetch(`${API_BASE_URL}/api/visual/stop`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ process_id: processId })
        });
        
        if (response.ok) {
          console.log(`🛑 Stopped visual process: ${processId}`);
        } else {
          console.error(`❌ Failed to stop visual process: ${processId}`);
        }
      }

      // Update local state
      setProcesses(prev => prev.map(p => 
        p.id === processId ? { ...p, enabled: newEnabled } : p
      ));

      // Update system stats
      setSystemStats(prev => ({
        ...prev,
        activeProcesses: prev.activeProcesses + (newEnabled ? 1 : -1)
      }));

      // Call parent callback if provided
      if (onProcessToggle) {
        onProcessToggle(processId, newEnabled);
      }
    } catch (error) {
      console.error(`Error toggling process ${processId}:`, error);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'CRITICAL': return 'text-red-400 bg-red-500/20';
      case 'HIGH': return 'text-orange-400 bg-orange-500/20';
      case 'MEDIUM': return 'text-yellow-400 bg-yellow-500/20';
      case 'LOW': return 'text-blue-400 bg-blue-500/20';
      case 'POETIC': return 'text-purple-400 bg-purple-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const activeCount = processes.filter(p => p.enabled).length;

  return (
    <div className="space-y-6">
      {/* System Status */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-emerald-400">{activeCount}/{processes.length}</div>
          <div className="text-sm text-gray-400">Active Processes</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-blue-400">{systemStats.systemLoad}%</div>
          <div className="text-sm text-gray-400">System Load</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-purple-400">{systemStats.averageFps}</div>
          <div className="text-sm text-gray-400">Avg FPS</div>
        </div>
        <div className="bg-white/5 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-green-400">●</div>
          <div className="text-sm text-gray-400">Status: Active</div>
        </div>
      </div>

      {/* Process Grid */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {processes.map((process) => (
          <div
            key={process.id}
            className={`bg-white/5 border rounded-lg p-4 transition-all duration-200 ${
              process.enabled 
                ? 'border-emerald-500/50 bg-emerald-500/10' 
                : 'border-white/10 hover:border-white/20'
            }`}
          >
            <div className="flex items-center justify-between mb-3">
              <h4 className="font-medium text-sm">{process.name}</h4>
              <button
                onClick={() => handleProcessToggle(process.id)}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
                  process.enabled 
                    ? 'bg-emerald-500 hover:bg-emerald-600' 
                    : 'bg-gray-600 hover:bg-gray-500'
                }`}
              >
                {process.enabled ? <Pause size={12} /> : <Play size={12} />}
              </button>
            </div>
            
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-gray-400">Priority:</span>
                <span className={`px-2 py-1 rounded text-xs ${getPriorityColor(process.priority)}`}>
                  {process.priority}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Mode:</span>
                <span className="text-white">{process.mode}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Target FPS:</span>
                <span className="text-white">{process.fps}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Visual Rendering Area */}
      <div className="mt-8">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-white">Visual Output</h3>
          <div className="flex gap-2">
            <button className="px-3 py-1 bg-blue-500/20 border border-blue-500/30 rounded text-blue-400 text-sm hover:bg-blue-500/30">
              Fullscreen
            </button>
            <button className="px-3 py-1 bg-purple-500/20 border border-purple-500/30 rounded text-purple-400 text-sm hover:bg-purple-500/30">
              Record
            </button>
          </div>
        </div>
        
        {/* Main Viewing Area */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          {/* Primary Display */}
          <div className="bg-black/40 border border-white/20 rounded-lg aspect-video relative overflow-hidden">
            {Object.keys(visualOutputs).length > 0 ? (
              <img 
                src={Object.values(visualOutputs)[0]?.image_data} 
                alt="Primary Visual Output"
                className="absolute inset-0 w-full h-full object-contain"
              />
            ) : activeCount > 0 ? (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 border-4 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin mb-4"></div>
                  <p className="text-emerald-400 text-sm">Visual processes rendering...</p>
                  <p className="text-gray-400 text-xs mt-1">{activeCount} active process{activeCount !== 1 ? 'es' : ''}</p>
                </div>
              </div>
            ) : (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <Eye size={48} className="mx-auto mb-3 opacity-30" />
                  <p className="text-sm">Start visual processes to see output</p>
                </div>
              </div>
            )}
            {/* Process name overlay */}
            {Object.keys(visualOutputs).length > 0 && (
              <div className="absolute top-2 left-2 bg-black/60 px-2 py-1 rounded text-xs text-white">
                {Object.keys(visualOutputs)[0]}
              </div>
            )}
          </div>

          {/* Secondary Display */}
          <div className="bg-black/40 border border-white/20 rounded-lg aspect-video relative overflow-hidden">
            {Object.keys(visualOutputs).length > 1 ? (
              <img 
                src={Object.values(visualOutputs)[1]?.image_data} 
                alt="Secondary Visual Output"
                className="absolute inset-0 w-full h-full object-contain"
              />
            ) : (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <BarChart3 size={32} className="mx-auto mb-2 opacity-30" />
                  <p className="text-xs">Secondary Display</p>
                </div>
              </div>
            )}
            {/* Process name overlay */}
            {Object.keys(visualOutputs).length > 1 && (
              <div className="absolute top-2 left-2 bg-black/60 px-2 py-1 rounded text-xs text-white">
                {Object.keys(visualOutputs)[1]}
              </div>
            )}
          </div>
        </div>

        {/* Mini Process Previews */}
        <div className="grid grid-cols-6 gap-2">
          {processes.filter(p => p.enabled).map((process) => (
            <div
              key={`preview-${process.id}`}
              className="bg-black/30 border border-emerald-500/30 rounded aspect-video relative overflow-hidden group cursor-pointer hover:border-emerald-400/50"
              title={process.name}
            >
              {visualOutputs[process.id] ? (
                <img 
                  src={visualOutputs[process.id].image_data} 
                  alt={process.name}
                  className="absolute inset-0 w-full h-full object-cover"
                />
              ) : (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
                </div>
              )}
              <div className="absolute bottom-0 left-0 right-0 bg-black/60 p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <p className="text-xs text-white truncate">{process.name}</p>
              </div>
            </div>
          ))}
          
          {/* Empty slots for inactive processes */}
          {Array.from({ length: Math.max(0, 6 - processes.filter(p => p.enabled).length) }).map((_, i) => (
            <div
              key={`empty-${i}`}
              className="bg-black/20 border border-white/10 rounded aspect-video relative overflow-hidden"
            >
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-2 h-2 bg-gray-600 rounded-full opacity-30"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Rendering Stats */}
        <div className="mt-4 grid grid-cols-4 gap-4 text-xs">
          <div className="bg-white/5 rounded p-3 text-center">
            <div className="text-emerald-400 font-mono">{systemStats.averageFps} FPS</div>
            <div className="text-gray-400">Render Rate</div>
          </div>
          <div className="bg-white/5 rounded p-3 text-center">
            <div className="text-blue-400 font-mono">{systemStats.systemLoad}%</div>
            <div className="text-gray-400">GPU Load</div>
          </div>
          <div className="bg-white/5 rounded p-3 text-center">
            <div className="text-purple-400 font-mono">2.3 GB</div>
            <div className="text-gray-400">VRAM Usage</div>
          </div>
          <div className="bg-white/5 rounded p-3 text-center">
            <div className="text-yellow-400 font-mono">4K</div>
            <div className="text-gray-400">Resolution</div>
          </div>
        </div>
      </div>
    </div>
  );
};

const ModulesPage: React.FC = () => {
  const [activeModule, setActiveModule] = useState<string | null>(null);

  // Module data with enhanced functionality
  const modules = [
    {
      id: 'memory_archive',
      title: 'Memory Archive',
      icon: Archive,
      description: 'Long-term memory storage and retrieval system',
      stats: {
        memories: 1247,
        active: 324,
        links: 2891,
        efficiency: 87.5
      },
      controls: ['Archive', 'Search', 'Optimize']
    },
    {
      id: 'pattern_engine',
      title: 'Pattern Engine',
      icon: TrendingUp,
      description: 'Real-time pattern recognition and analysis',
      stats: {
        patterns: 89,
        accuracy: 94.2,
        processing: 1250,
        rate: '1.25k ops/sec'
      },
      controls: ['Analyze', 'History', 'Train']
    },
    {
      id: 'visual_consciousness',
      title: 'Visual Consciousness',
      icon: Eye,
      description: 'Visual processing and consciousness rendering',
      stats: {
        processes: '5/12',
        load: 34.7,
        fps: 28.4,
        status: 'Active'
      },
      controls: ['Start Core', 'Dashboard', 'Export']
    },
    {
      id: 'reality_parser',
      title: 'Reality Parser',
      icon: Map,
      description: 'Multi-dimensional reality analysis and parsing',
      stats: {
        layers: 7,
        accuracy: 91.8,
        stability: 85.3,
        processing: 'Real-time'
      },
      controls: ['Parse', 'Map', 'Sync']
    }
  ];

  const handleModuleAction = async (moduleId: string, action: string) => {
    console.log(`🎯 Module Action: ${moduleId} - ${action}`);
    
    try {
      const API_BASE_URL = 'http://localhost:8001';
      
      // Handle different module actions
      switch (moduleId) {
        case 'memory_archive':
          if (action === 'Archive') {
            console.log('📁 Archiving current memories...');
          } else if (action === 'Search') {
            console.log('🔍 Opening memory search interface...');
          } else if (action === 'Optimize') {
            console.log('⚡ Optimizing memory storage...');
          }
          break;
          
        case 'pattern_engine':
          if (action === 'Analyze') {
            console.log('🔬 Starting pattern analysis...');
          } else if (action === 'History') {
            console.log('📊 Loading pattern history...');
          } else if (action === 'Train') {
            console.log('🎯 Training pattern recognition...');
          }
          break;
          
        case 'visual_consciousness':
          if (action === 'Start Core') {
            // Start core visual processes
            const response = await fetch(`${API_BASE_URL}/api/visual/start`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                process_id: 'pulse_map_renderer',
                script: 'pulse_map_renderer.py',
                parameters: { fps: 15, duration: 300 }
              })
            });
            if (response.ok) {
              console.log('🎬 Core visual processes started');
            }
          } else if (action === 'Dashboard') {
            setActiveModule(moduleId);
          } else if (action === 'Export') {
            console.log('💾 Exporting visual data...');
          }
          break;
          
        case 'reality_parser':
          if (action === 'Parse') {
            console.log('🌐 Parsing reality layers...');
          } else if (action === 'Map') {
            console.log('🗺️ Mapping dimensional structures...');
          } else if (action === 'Sync') {
            console.log('🔄 Synchronizing reality states...');
          }
          break;
      }
    } catch (error) {
      console.error(`Error executing ${action} on ${moduleId}:`, error);
    }
  };

  const getStatColor = (moduleId: string, statKey: string, value: any) => {
    if (typeof value === 'number') {
      if (value > 80) return 'text-green-400';
      if (value > 60) return 'text-yellow-400';
      return 'text-red-400';
    }
    return 'text-blue-400';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <Brain className="w-10 h-10 text-purple-400" />
            Module Laboratory
          </h1>
          <p className="text-gray-300 text-lg">
            Advanced cognitive module control and monitoring interface
          </p>
        </div>

        {activeModule === 'visual_consciousness' ? (
          <div className="space-y-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold flex items-center gap-2">
                <Eye className="w-6 h-6 text-purple-400" />
                Visual Consciousness Manager
              </h2>
              <button 
                onClick={() => setActiveModule(null)}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
              >
                ← Back to Modules
              </button>
            </div>
            <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
              <VisualConsciousnessModule />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {modules.map((module) => {
              const IconComponent = module.icon;
              return (
                <div
                  key={module.id}
                  className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10 hover:border-white/20 transition-all duration-300 group"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-purple-500/20 rounded-lg">
                      <IconComponent className="w-6 h-6 text-purple-400" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold">{module.title}</h3>
                      <p className="text-gray-400 text-sm">{module.description}</p>
                    </div>
                  </div>

                  {/* Statistics */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    {Object.entries(module.stats).map(([key, value]) => (
                      <div key={key} className="bg-white/5 rounded-lg p-3">
                        <div className={`text-lg font-bold ${getStatColor(module.id, key, value)}`}>
                          {typeof value === 'number' && value < 100 && key !== 'layers' ? `${value}%` : value}
                        </div>
                        <div className="text-xs text-gray-400 capitalize">
                          {key.replace('_', ' ')}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Controls */}
                  <div className="flex gap-2 flex-wrap">
                    {module.controls.map((action) => (
                      <button
                        key={action}
                        onClick={() => handleModuleAction(module.id, action)}
                        className="px-3 py-2 bg-purple-600/30 hover:bg-purple-600/50 rounded-lg text-sm transition-colors border border-purple-500/30 hover:border-purple-500/50"
                      >
                        {action}
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* System Status Dashboard */}
        <div className="mt-8 bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Settings className="w-5 h-5 text-purple-400" />
            System Status
          </h3>
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">4/4</div>
              <div className="text-sm text-gray-400">Modules Active</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">92.3%</div>
              <div className="text-sm text-gray-400">Overall Efficiency</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-400">847ms</div>
              <div className="text-sm text-gray-400">Avg Response</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-400">●</div>
              <div className="text-sm text-gray-400">System Health</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModulesPage; 