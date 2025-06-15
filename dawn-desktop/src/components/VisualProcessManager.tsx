import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

// Types for visual processes
interface VisualProcess {
  id: string;
  name: string;
  script: string;
  category: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'POETIC';
  mode: 'realtime' | 'periodic' | 'triggered' | 'snapshot';
  target_fps: number;
  status: string;
  enabled: boolean;
  cpu: number;
  memory: number;
  description: string;
  data_requirements: string[];
  memory_limit_mb: number;
}

// API helper for visual process communication
const API_BASE_URL = process.env.NODE_ENV === 'development' ? 'http://localhost:8001' : '';

const visualProcessAPI = {
  async startVisualProcess(processId: string, script: string, parameters?: any) {
    const response = await fetch(`${API_BASE_URL}/api/visual/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        process_id: processId,
        script: script,
        parameters: parameters || {}
      })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to start visual process: ${response.statusText}`);
    }
    
    return await response.json();
  },

  async stopVisualProcess(processId: string) {
    const response = await fetch(`${API_BASE_URL}/api/visual/stop`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        process_id: processId
      })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to stop visual process: ${response.statusText}`);
    }
    
    return await response.json();
  },

  async getVisualStatus() {
    const response = await fetch(`${API_BASE_URL}/api/visual/status`);
    
    if (!response.ok) {
      throw new Error(`Failed to get visual status: ${response.statusText}`);
    }
    
    return await response.json();
  }
};

const VisualProcessManager: React.FC = () => {
  // State for the 12 best visual processes
  const [visualProcesses, setVisualProcesses] = useState<VisualProcess[]>([
    {
      id: 'pulse_map_renderer',
      name: 'Pulse Map Renderer',
      script: 'pulse_waveform_renderer.py',
      category: 'consciousness',
      priority: 'CRITICAL',
      mode: 'realtime',
      target_fps: 15,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 150,
      description: 'Core consciousness pulse visualization - thermal state mapping',
      data_requirements: ['thermal_stats', 'tick_stats', 'consciousness_state']
    },
    {
      id: 'mood_heatmap',
      name: 'Mood Heatmap',
      script: 'mood_heatmap.py',
      category: 'consciousness',
      priority: 'HIGH',
      mode: 'realtime',
      target_fps: 10,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 100,
      description: 'Real-time emotional state heatmap visualization',
      data_requirements: ['mood_state', 'entropy_snapshot']
    },
    {
      id: 'drift_vector_field',
      name: 'Drift Vector Field',
      script: 'drift_vector_field.py',
      category: 'analysis',
      priority: 'HIGH',
      mode: 'realtime',
      target_fps: 12,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 200,
      description: 'Semantic drift and vector field analysis visualization',
      data_requirements: ['semantic_field', 'alignment_snapshot']
    },
    {
      id: 'sigil_trace_visualizer',
      name: 'Sigil Trace Visualizer',
      script: 'sigil_trace_visualizer.py',
      category: 'consciousness',
      priority: 'HIGH',
      mode: 'triggered',
      target_fps: 8,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 120,
      description: 'Emotional sigil patterns and trace visualization',
      data_requirements: ['sigil_states', 'emotional_context']
    },
    {
      id: 'tracer_drift_vectors',
      name: 'Tracer Drift Vectors',
      script: 'tracer_drift_vectors.py',
      category: 'analysis',
      priority: 'MEDIUM',
      mode: 'periodic',
      target_fps: 6,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 180,
      description: 'Semantic tracer movement and drift analysis',
      data_requirements: ['semantic_field', 'tracer_data']
    },
    {
      id: 'synthesis_entropy_chart',
      name: 'Synthesis Entropy Chart',
      script: 'synthesis_entropy_chart.py',
      category: 'analysis',
      priority: 'MEDIUM',
      mode: 'periodic',
      target_fps: 5,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 90,
      description: 'Entropy synthesis and distribution analysis',
      data_requirements: ['entropy_snapshot', 'synthesis_data']
    },
    {
      id: 'rebloom_trail_animation',
      name: 'Rebloom Trail Animation',
      script: 'rebloom_trail_animation.py',
      category: 'dynamics',
      priority: 'MEDIUM',
      mode: 'triggered',
      target_fps: 8,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 130,
      description: 'Rebloom event trails and cascading effects',
      data_requirements: ['rebloom_events', 'bloom_state']
    },
    {
      id: 'recursive_bloom_tree',
      name: 'Recursive Bloom Tree',
      script: 'recursive_bloom_tree.py',
      category: 'structure',
      priority: 'LOW',
      mode: 'snapshot',
      target_fps: 2,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 110,
      description: 'Hierarchical bloom structure visualization',
      data_requirements: ['semantic_field', 'bloom_hierarchy']
    },
    {
      id: 'hybrid_field_visualizer',
      name: 'Hybrid Field Visualizer',
      script: 'hybrid_field_visualizer.py',
      category: 'structure',
      priority: 'LOW',
      mode: 'periodic',
      target_fps: 4,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 160,
      description: 'Multi-dimensional consciousness field visualization',
      data_requirements: ['consciousness_field', 'dimensional_data']
    },
    {
      id: 'semantic_timeline_animator',
      name: 'Semantic Timeline Animator',
      script: 'semantic_timeline_animator.py',
      category: 'timeline',
      priority: 'LOW',
      mode: 'periodic',
      target_fps: 4,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 100,
      description: 'Semantic evolution timeline and progression',
      data_requirements: ['semantic_field', 'tick_count', 'historical_data']
    },
    {
      id: 'stall_density_animator',
      name: 'Stall Density Animator',
      script: 'stall_density_animator.py',
      category: 'analysis',
      priority: 'MEDIUM',
      mode: 'periodic',
      target_fps: 6,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 95,
      description: 'Cognitive stall pattern and density visualization',
      data_requirements: ['stall_data', 'density_metrics']
    },
    {
      id: 'scup_zone_animator',
      name: 'SCUP Zone Animator',
      script: 'scup_zone_animator.py',
      category: 'consciousness',
      priority: 'HIGH',
      mode: 'realtime',
      target_fps: 10,
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      memory_limit_mb: 120,
      description: 'SCUP (Subsystem Cognitive Unity Potential) zone visualization',
      data_requirements: ['scup_data', 'unity_metrics', 'subsystem_states']
    }
  ]);

  const [activeView, setActiveView] = useState<string>('all');
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);
  const [systemStatus, setSystemStatus] = useState({
    running: false,
    total_cpu: 0,
    total_memory: 0,
    active_processes: 0
  });

  // Toggle visual process
  const toggleVisualProcess = async (processId: string) => {
    const process = visualProcesses.find(p => p.id === processId);
    if (!process) return;

    try {
      setVisualProcesses(prev => prev.map(proc => {
        if (proc.id === processId) {
          return { ...proc, status: process.enabled ? 'stopping' : 'starting' };
        }
        return proc;
      }));

      if (process.enabled) {
        // Stop the process
        console.log('🛑 Stopping visual process:', process.script);
        await visualProcessAPI.stopVisualProcess(processId);
        
        setVisualProcesses(prev => prev.map(proc => {
          if (proc.id === processId) {
            return {
              ...proc,
              enabled: false,
              status: 'stopped',
              cpu: 0,
              memory: 0
            };
          }
          return proc;
        }));
        
        console.log('✅ Successfully stopped:', process.script);
      } else {
        // Start the process
        console.log('🚀 Starting visual process:', process.script);
        await visualProcessAPI.startVisualProcess(processId, process.script);
        
        setVisualProcesses(prev => prev.map(proc => {
          if (proc.id === processId) {
            return {
              ...proc,
              enabled: true,
              status: 'running',
              cpu: Math.random() * 30 + 10,
              memory: Math.random() * (process.memory_limit_mb - 20) + 20
            };
          }
          return proc;
        }));
        
        console.log('✅ Successfully started:', process.script);
      }
    } catch (error) {
      console.error('❌ Failed to toggle visual process:', error);
      
      // Revert the status on error
      setVisualProcesses(prev => prev.map(proc => {
        if (proc.id === processId) {
          return {
            ...proc,
            status: process.enabled ? 'running' : 'stopped'
          };
        }
        return proc;
      }));
      
      // Show user-friendly error message
      alert(`Failed to ${process.enabled ? 'stop' : 'start'} ${process.name}: ${error instanceof Error ? error.message : String(error)}`);
    }
  };

  // Calculate totals
  const totalCPU = visualProcesses.reduce((sum, proc) => sum + proc.cpu, 0);
  const totalMemory = visualProcesses.reduce((sum, proc) => sum + proc.memory, 0);
  const activeProcesses = visualProcesses.filter(proc => proc.enabled).length;

  // Filter processes by view
  const getFilteredProcesses = (): VisualProcess[] => {
    switch (activeView) {
      case 'critical':
        return visualProcesses.filter(p => p.priority === 'CRITICAL');
      case 'high':
        return visualProcesses.filter(p => p.priority === 'HIGH');
      case 'medium':
        return visualProcesses.filter(p => p.priority === 'MEDIUM');
      case 'low':
        return visualProcesses.filter(p => p.priority === 'LOW');
      case 'active':
        return visualProcesses.filter(p => p.enabled);
      default:
        return visualProcesses;
    }
  };

  // Priority color mapping
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'CRITICAL': return 'text-red-400 bg-red-900/20';
      case 'HIGH': return 'text-orange-400 bg-orange-900/20';
      case 'MEDIUM': return 'text-yellow-400 bg-yellow-900/20';
      case 'LOW': return 'text-blue-400 bg-blue-900/20';
      case 'POETIC': return 'text-purple-400 bg-purple-900/20';
      default: return 'text-gray-400 bg-gray-900/20';
    }
  };

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700 backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <span className="text-3xl mr-3">🎬</span>
          DAWN Visual Consciousness Manager
        </h2>
        <div className="flex items-center space-x-6">
          <div className="text-sm">
            <span className="text-gray-400">Total CPU:</span>
            <span className="text-white font-bold ml-2">{totalCPU.toFixed(1)}%</span>
          </div>
          <div className="text-sm">
            <span className="text-gray-400">Total Memory:</span>
            <span className="text-white font-bold ml-2">{totalMemory.toFixed(1)} MB</span>
          </div>
          <div className="text-sm">
            <span className="text-gray-400">Active:</span>
            <span className="text-green-400 font-bold ml-2">{activeProcesses}/12</span>
          </div>
        </div>
      </div>

      {/* View Filters */}
      <div className="mb-4 flex justify-between items-center">
        <div className="flex space-x-2">
          {['all', 'critical', 'high', 'medium', 'low', 'active'].map(view => (
            <button
              key={view}
              onClick={() => setActiveView(view)}
              className={`px-4 py-2 rounded text-sm capitalize ${
                activeView === view
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {view}
            </button>
          ))}
        </div>
        
        <div className="flex space-x-2">
          <button 
            onClick={() => {
              // Enable all critical and high priority processes
              visualProcesses.forEach(proc => {
                if (!proc.enabled && (proc.priority === 'CRITICAL' || proc.priority === 'HIGH')) {
                  toggleVisualProcess(proc.id);
                }
              });
            }}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
          >
            Start Core
          </button>
          <button 
            onClick={() => {
              visualProcesses.forEach(proc => {
                if (proc.enabled) {
                  toggleVisualProcess(proc.id);
                }
              });
            }}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
          >
            Stop All
          </button>
        </div>
      </div>

      {/* Process Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
        {getFilteredProcesses().map(process => (
          <motion.div 
            key={process.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`bg-gray-800 rounded-lg p-4 border ${
              process.enabled ? 'border-purple-500/50 bg-purple-900/10' : 'border-gray-700'
            } transition-all duration-300`}
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <h3 className="text-white font-semibold text-sm">{process.name}</h3>
                  <span className={`px-2 py-0.5 text-xs rounded ${getPriorityColor(process.priority)}`}>
                    {process.priority}
                  </span>
                </div>
                <p className="text-gray-400 text-xs mb-2">{process.description}</p>
                <div className="text-xs text-gray-500 space-y-1">
                  <div>Mode: {process.mode} | FPS: {process.target_fps}</div>
                  <div>Script: {process.script}</div>
                </div>
              </div>
              
              <button
                onClick={() => toggleVisualProcess(process.id)}
                className={`w-10 h-5 rounded-full transition-colors duration-300 ${
                  process.enabled ? 'bg-purple-600' : 'bg-gray-600'
                } relative ml-3 flex-shrink-0`}
              >
                <div className={`absolute w-4 h-4 bg-white rounded-full top-0.5 transition-transform duration-300 ${
                  process.enabled ? 'translate-x-5' : 'translate-x-0.5'
                }`}></div>
              </button>
            </div>
            
            {/* Status and Metrics */}
            <div className="flex items-center justify-between text-xs">
              <div className={`px-2 py-1 rounded text-xs font-medium ${
                process.status === 'running' ? 'bg-green-900/30 text-green-400' :
                process.status === 'starting' ? 'bg-yellow-900/30 text-yellow-400' :
                process.status === 'stopping' ? 'bg-orange-900/30 text-orange-400' :
                'bg-gray-900/30 text-gray-400'
              }`}>
                {process.status}
              </div>
              
              {process.enabled && (
                <div className="flex space-x-3 text-gray-400">
                  <span>CPU: {process.cpu.toFixed(1)}%</span>
                  <span>MEM: {process.memory.toFixed(0)}MB</span>
                </div>
              )}
            </div>
            
            {/* Data Requirements */}
            {selectedProcess === process.id && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="mt-3 pt-3 border-t border-gray-700"
              >
                <h4 className="text-xs font-semibold text-white mb-2">Data Requirements:</h4>
                <div className="flex flex-wrap gap-1">
                  {process.data_requirements.map((req, idx) => (
                    <span key={idx} className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded">
                      {req}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
            
            <button
              onClick={() => setSelectedProcess(selectedProcess === process.id ? null : process.id)}
              className="text-xs text-purple-400 hover:text-purple-300 mt-2"
            >
              {selectedProcess === process.id ? 'Hide details' : 'Show details'}
            </button>
          </motion.div>
        ))}
      </div>
      
      {/* System Status Footer */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="flex items-center justify-between text-sm text-gray-400">
          <div>
            Visual Consciousness System: {activeProcesses > 0 ? '🟢 Active' : '🔴 Idle'}
          </div>
          <div>
            Resource Usage: {((totalCPU / (activeProcesses || 1)) || 0).toFixed(1)}% avg CPU, 
            {(totalMemory / 1024).toFixed(2)} GB total
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualProcessManager; 