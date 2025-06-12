import React, { useState, useEffect } from 'react';
// import { invoke } from '@tauri-apps/api/tauri';

// Types for process objects
interface PythonProcess {
  id: string;
  name: string;
  script: string;
  category: string;
  status: string;
  enabled: boolean;
  cpu: number;
  memory: number;
  fps: number;
  description: string;
  modules?: { name: string; enabled: boolean }[];
  parameters?: Record<string, any>;
}

interface ReactComponentProcess {
  id: string;
  name: string;
  component: string;
  category: string;
  status: string;
  enabled: boolean;
  cpu: number;
  memory: number;
  fps: number;
  description: string;
}

type Process = PythonProcess | ReactComponentProcess;

type ProcessesViewerTabProps = {
  onToggleComponent?: (component: string, enabled: boolean) => void;
};

const ProcessesViewerTab: React.FC<ProcessesViewerTabProps> = ({ onToggleComponent }) => {
  const [pythonProcesses, setPythonProcesses] = useState<PythonProcess[]>([
    {
      id: 'main-pipeline',
      name: 'Main Processing Pipeline',
      script: 'main_pipeline.py',
      category: 'core',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Central CV pipeline with all modules',
      modules: [
        { name: 'Camera Capture', enabled: true },
        { name: 'Object Detection', enabled: true },
        { name: 'Object Tracking', enabled: true },
        { name: 'Depth Estimation', enabled: false },
        { name: '3D Reconstruction', enabled: false },
        { name: 'Point Cloud Gen', enabled: false },
        { name: 'Visualization', enabled: true }
      ]
    },
    {
      id: 'calibration',
      name: 'Camera Calibration',
      script: 'calibration.py',
      category: 'setup',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Camera intrinsic/extrinsic calibration',
      parameters: {
        checkerboardSize: [9, 6],
        squareSize: 25,
        stereoMode: false
      }
    },
    {
      id: 'detection',
      name: 'Object Detection',
      script: 'detection.py',
      category: 'processing',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'YOLO-based object detection',
      parameters: {
        model: 'yolov8n',
        confidence: 0.5,
        nmsThreshold: 0.4,
        classes: ['person', 'car', 'bicycle']
      }
    },
    {
      id: 'tracking',
      name: 'Object Tracking',
      script: 'tracking.py',
      category: 'processing',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Multi-object tracking with ID assignment',
      parameters: {
        algorithm: 'DeepSORT',
        maxAge: 30,
        minHits: 3,
        iouThreshold: 0.3
      }
    },
    {
      id: 'depth',
      name: 'Depth Estimation',
      script: 'depth_estimation.py',
      category: 'processing',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Stereo matching and depth computation',
      parameters: {
        method: 'SGBM',
        numDisparities: 96,
        blockSize: 11,
        preFilterCap: 63
      }
    },
    {
      id: 'reconstruction',
      name: '3D Reconstruction',
      script: 'reconstruction.py',
      category: 'processing',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Surface reconstruction and mesh generation',
      parameters: {
        algorithm: 'Poisson',
        depth: 9,
        scale: 1.1,
        pointWeight: 4.0
      }
    },
    {
      id: 'visualization',
      name: 'Visualization Engine',
      script: 'visualization.py',
      category: 'display',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: '2D/3D visualization and overlays',
      parameters: {
        mode: '2D',
        showTrajectories: true,
        showDepth: false,
        showPointCloud: false
      }
    },
    {
      id: 'preprocessing',
      name: 'Image Preprocessing',
      script: 'preprocessing.py',
      category: 'processing',
      status: 'stopped',
      enabled: false,
      cpu: 0,
      memory: 0,
      fps: 0,
      description: 'Image enhancement and correction',
      parameters: {
        denoising: true,
        colorCorrection: true,
        histogram: false,
        sharpening: false
      }
    }
  ]);

  const [reactComponents, setReactComponents] = useState<ReactComponentProcess[]>([
    {
      id: 'neural-activity',
      name: 'Neural Activity Visualizer',
      component: 'NeuralActivityVisualizer',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 12.3,
      memory: 45.2,
      fps: 60,
      description: 'Real-time EEG brainwave visualization'
    },
    {
      id: 'network-flow',
      name: 'Network Flow Diagram',
      component: 'NetworkFlowDiagram',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 8.7,
      memory: 32.1,
      fps: 30,
      description: 'SCUP → ENTROPY → HEAT → MOOD data flow'
    },
    {
      id: 'cognitive-radar',
      name: 'Cognitive Load Radar',
      component: 'CognitiveLoadRadar',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 5.2,
      memory: 28.4,
      fps: 15,
      description: '6-metric cognitive load analysis'
    },
    {
      id: 'diagnostic',
      name: 'Enhanced Live Diagnostic',
      component: 'EnhancedLiveDiagnostic',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 15.8,
      memory: 52.3,
      fps: 24,
      description: 'Spectrogram, waterfall, and correlation views'
    },
    {
      id: 'performance',
      name: 'Cognitive Performance Matrix',
      component: 'CognitivePerformanceMatrix',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 6.4,
      memory: 24.7,
      fps: 10,
      description: 'System performance metrics dashboard'
    },
    {
      id: 'alerts',
      name: 'Alert & Anomaly Panel',
      component: 'AlertAnomalyPanel',
      category: 'neural',
      status: 'running',
      enabled: true,
      cpu: 3.2,
      memory: 19.8,
      fps: 5,
      description: 'Real-time alerts and pattern detection'
    }
  ]);

  const [activeView, setActiveView] = useState<string>('all');
  const [selectedProcess, setSelectedProcess] = useState<string | null>(null);

  // Toggle Python process
  const togglePythonProcess = async (processId: string) => {
    const process = pythonProcesses.find(p => p.id === processId);
    if (!process) return;

    try {
      if (process.enabled) {
        // Stop the process
        console.log('Mock: stopping process', process.script);
      } else {
        // Start the process with parameters
        console.log('Mock: starting process', process.script, process.parameters || {}, process.modules || []);
      }

      setPythonProcesses(prev => prev.map(proc => {
        if (proc.id === processId) {
          const newEnabled = !proc.enabled;
          return {
            ...proc,
            enabled: newEnabled,
            status: newEnabled ? 'running' : 'stopped',
            cpu: newEnabled ? 15 + Math.random() * 20 : 0,
            memory: newEnabled ? 100 + Math.random() * 200 : 0,
            fps: newEnabled ? Math.floor(15 + Math.random() * 30) : 0
          };
        }
        return proc;
      }));
    } catch (error) {
      console.error('Failed to toggle Python process:', error);
    }
  };

  // Toggle React component
  const toggleReactComponent = (componentId: string) => {
    setReactComponents(prev => prev.map(comp => {
      if (comp.id === componentId) {
        const newEnabled = !comp.enabled;
        if (onToggleComponent) {
          onToggleComponent(comp.component, newEnabled);
        }
        return {
          ...comp,
          enabled: newEnabled,
          status: newEnabled ? 'running' : 'stopped',
          cpu: newEnabled ? comp.cpu : 0,
          fps: newEnabled ? comp.fps : 0
        };
      }
      return comp;
    }));
  };

  // Update module toggle for main pipeline
  const togglePipelineModule = (moduleIndex: number) => {
    setPythonProcesses(prev => prev.map(proc => {
      if (proc.id === 'main-pipeline' && proc.modules) {
        const newModules = [...proc.modules];
        newModules[moduleIndex].enabled = !newModules[moduleIndex].enabled;
        return { ...proc, modules: newModules };
      }
      return proc;
    }));
  };

  // Calculate totals
  const allProcesses: Process[] = [...pythonProcesses, ...reactComponents];
  const totalCPU = allProcesses.reduce((sum, proc) => sum + proc.cpu, 0);
  const totalMemory = allProcesses.reduce((sum, proc) => sum + proc.memory, 0);
  const activeProcesses = allProcesses.filter(proc => proc.enabled).length;

  // Filter processes by view
  const getFilteredProcesses = (): Process[] => {
    switch (activeView) {
      case 'python':
        return pythonProcesses;
      case 'react':
        return reactComponents;
      case 'active':
        return allProcesses.filter(p => p.enabled);
      default:
        return allProcesses;
    }
  };

  // Type guard for PythonProcess
  function isPythonProcess(proc: Process): proc is PythonProcess {
    return (proc as PythonProcess).script !== undefined;
  }

  return (
    <div className="bg-gray-900 rounded-lg p-6 border border-gray-700 backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center">
          <span className="text-3xl mr-3">⚙️</span>
          DAWN Process Manager
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
            <span className="text-green-400 font-bold ml-2">{activeProcesses}/{allProcesses.length}</span>
          </div>
        </div>
      </div>

      {/* View Filters */}
      <div className="mb-4 flex justify-between items-center">
        <div className="flex space-x-2">
          {['all', 'python', 'react', 'active'].map(view => (
            <button
              key={view}
              onClick={() => setActiveView(view)}
              className={`px-4 py-2 rounded text-sm capitalize ${
                activeView === view
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {view === 'python' ? 'Python CV' : view}
            </button>
          ))}
        </div>
        
        <div className="flex space-x-2">
          <button 
            onClick={() => {
              allProcesses.forEach(proc => {
                if (!proc.enabled) {
                  if (isPythonProcess(proc)) togglePythonProcess(proc.id);
                  else toggleReactComponent(proc.id);
                }
              });
            }}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
          >
            Enable All
          </button>
          <button 
            onClick={() => {
              allProcesses.forEach(proc => {
                if (proc.enabled) {
                  if (isPythonProcess(proc)) togglePythonProcess(proc.id);
                  else toggleReactComponent(proc.id);
                }
              });
            }}
            className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
          >
            Stop All
          </button>
        </div>
      </div>

      {/* Process List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        {getFilteredProcesses().map(process => (
          <div 
            key={process.id}
            className={`bg-gray-800 rounded-lg p-4 border ${
              process.enabled ? 'border-gray-600' : 'border-gray-700'
            } transition-all duration-300`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 flex-1">
                <button
                  onClick={() => isPythonProcess(process) ? togglePythonProcess(process.id) : toggleReactComponent(process.id)}
                  className={`w-12 h-6 rounded-full transition-colors duration-300 ${
                    process.enabled ? 'bg-green-600' : 'bg-gray-600'
                  } relative mt-1`}
                >
                  <div className={`absolute w-5 h-5 bg-white rounded-full top-0.5 transition-transform duration-300 ${
                    process.enabled ? 'translate-x-6' : 'translate-x-0.5'
                  }`}></div>
                </button>
                
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <h3 className="text-white font-semibold">{process.name}</h3>
                    {isPythonProcess(process) && (
                      <span className="px-2 py-0.5 bg-purple-900 text-purple-300 text-xs rounded">
                        Python
                      </span>
                    )}
                  </div>
                  <p className="text-gray-400 text-sm mt-1">{process.description}</p>
                  {isPythonProcess(process) && (
                    <p className="text-gray-500 text-xs mt-1 font-mono">{process.script}</p>
                  )}
                </div>
              </div>
              
              <button
                onClick={() => setSelectedProcess(selectedProcess === process.id ? null : process.id)}
                className="text-gray-400 hover:text-white ml-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                </svg>
              </button>
            </div>

            {/* Process Metrics */}
            {process.enabled && (
              <div className="mt-3 pt-3 border-t border-gray-700">
                <div className="grid grid-cols-3 gap-4 text-xs">
                  <div>
                    <span className="text-gray-400">CPU:</span>
                    <span className={`ml-1 font-bold ${
                      process.cpu > 20 ? 'text-yellow-400' : 'text-green-400'
                    }`}>{process.cpu.toFixed(1)}%</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Memory:</span>
                    <span className="ml-1 font-bold text-blue-400">{process.memory.toFixed(0)} MB</span>
                  </div>
                  <div>
                    <span className="text-gray-400">FPS:</span>
                    <span className="ml-1 font-bold text-purple-400">{process.fps}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Expanded Details */}
            {selectedProcess === process.id && (
              <div className="mt-3 pt-3 border-t border-gray-700 space-y-3">
                {/* Pipeline Modules */}
                {isPythonProcess(process) && process.modules && (
                  <div>
                    <h4 className="text-sm font-semibold text-white mb-2">Pipeline Modules</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {process.modules.map((module, idx) => (
                        <label key={idx} className="flex items-center space-x-2 text-xs">
                          <input
                            type="checkbox"
                            checked={module.enabled}
                            onChange={() => togglePipelineModule(idx)}
                            className="rounded"
                          />
                          <span className="text-gray-300">{module.name}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                )}

                {/* Process Parameters */}
                {isPythonProcess(process) && process.parameters && (
                  <div>
                    <h4 className="text-sm font-semibold text-white mb-2">Parameters</h4>
                    <div className="space-y-1">
                      {Object.entries(process.parameters).map(([key, value]) => (
                        <div key={key} className="flex justify-between text-xs">
                          <span className="text-gray-400">{key}:</span>
                          <span className="text-gray-300 font-mono">
                            {typeof value === 'object' ? JSON.stringify(value) : value.toString()}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex space-x-2 text-xs">
                  {isPythonProcess(process) && (
                    <>
                      <button className="text-blue-400 hover:text-blue-300">Configure</button>
                      <button className="text-yellow-400 hover:text-yellow-300">Restart</button>
                    </>
                  )}
                  <button className="text-gray-400 hover:text-gray-300">View Logs</button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* System Performance */}
      <div className="mt-6 bg-gray-800 rounded-lg p-4">
        <h3 className="text-sm font-bold text-white mb-3">System Performance Impact</h3>
        <div className="grid grid-cols-4 gap-4 text-sm">
          <div>
            <div className="text-gray-400 mb-1">CPU Load</div>
            <div className="bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-green-500 to-yellow-500 h-full transition-all duration-500"
                style={{ width: `${Math.min(totalCPU, 100)}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">{totalCPU.toFixed(1)}% of capacity</p>
          </div>
          <div>
            <div className="text-gray-400 mb-1">Memory Usage</div>
            <div className="bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-full transition-all duration-500"
                style={{ width: `${Math.min(totalMemory / 10, 100)}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">{totalMemory.toFixed(0)} MB used</p>
          </div>
          <div>
            <div className="text-gray-400 mb-1">Python Processes</div>
            <div className="bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-purple-500 to-pink-500 h-full transition-all duration-500"
                style={{ width: `${(pythonProcesses.filter(p => p.enabled).length / pythonProcesses.length) * 100}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {pythonProcesses.filter(p => p.enabled).length}/{pythonProcesses.length} active
            </p>
          </div>
          <div>
            <div className="text-gray-400 mb-1">React Components</div>
            <div className="bg-gray-700 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-cyan-500 to-teal-500 h-full transition-all duration-500"
                style={{ width: `${(reactComponents.filter(p => p.enabled).length / reactComponents.length) * 100}%` }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              {reactComponents.filter(p => p.enabled).length}/{reactComponents.length} active
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProcessesViewerTab;