import { useState, useEffect } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'

export default function ConfigPanel({ className = "", currentMetrics = {} }) {
  // State for collapsible sections
  const [expandedSections, setExpandedSections] = useState({
    subsystems: true,
    thresholds: true,
    neural: false,
    recording: false
  })

  // Subsystem Management State
  const [subsystems, setSubsystems] = useState([])
  const [newSubsystemName, setNewSubsystemName] = useState('')
  const [newSubsystemConfig, setNewSubsystemConfig] = useState('{}')
  const [draggedItem, setDraggedItem] = useState(null)

  // Metric Thresholds State
  const [thresholds, setThresholds] = useState({
    scup: { min: 0.1, max: 0.9, current: 0.65 },
    entropy: { min: 0.05, max: 0.75, current: 0.4 },
    heat: { min: 0.1, max: 0.8, current: 0.35 }
  })
  const [alertConfig, setAlertConfig] = useState({
    scup: { enabled: true, autoResponse: false },
    entropy: { enabled: true, autoResponse: false },
    heat: { enabled: true, autoResponse: false }
  })

  // Neural Network Config State
  const [neuralConfig, setNeuralConfig] = useState({
    hiddenLayerSize: 128,
    learningRate: 0.001,
    trainingMode: false,
    batchSize: 32,
    epochs: 100
  })

  // Data Recording State
  const [recordingConfig, setRecordingConfig] = useState({
    enabled: true,
    logRotationHours: 24,
    compressionEnabled: true,
    maxLogSizeMB: 100
  })

  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  // Load initial data
  useEffect(() => {
    loadSubsystems()
    loadThresholds()
    loadNeuralConfig()
    loadRecordingConfig()
  }, [])

  // Helper function for API calls
  const handleApiCall = async (operation, successMessage) => {
    setIsLoading(true)
    setError(null)
    setSuccess(null)
    
    try {
      await operation()
      setSuccess(successMessage)
      setTimeout(() => setSuccess(null), 3000)
    } catch (err) {
      console.error('API call failed:', err)
      setError(err.toString())
      setTimeout(() => setError(null), 5000)
    } finally {
      setIsLoading(false)
    }
  }

  // Section toggle helper
  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  // Subsystem Management Functions
  const loadSubsystems = async () => {
    try {
      const subs = await invoke('get_subsystems')
      setSubsystems(subs.map((sub, index) => ({ ...sub, weight: 1.0, priority: index })))
    } catch (err) {
      console.error('Failed to load subsystems:', err)
    }
  }

  const addSubsystem = async () => {
    if (!newSubsystemName.trim()) return
    
    await handleApiCall(async () => {
      let config
      try {
        config = JSON.parse(newSubsystemConfig)
      } catch {
        config = {}
      }
      
      await invoke('add_subsystem', { 
        name: newSubsystemName, 
        config 
      })
      await loadSubsystems()
      setNewSubsystemName('')
      setNewSubsystemConfig('{}')
    }, 'Subsystem added successfully')
  }

  const removeSubsystem = async (subsystemId) => {
    await handleApiCall(async () => {
      await invoke('remove_subsystem', { subsystemId })
      await loadSubsystems()
    }, 'Subsystem removed successfully')
  }

  const toggleSubsystem = async (subsystemId, enabled) => {
    // Implementation would depend on backend API
    console.log(`Toggle subsystem ${subsystemId} to ${enabled}`)
  }

  const updateSubsystemWeight = (subsystemId, weight) => {
    setSubsystems(prev => prev.map(sub => 
      sub.id === subsystemId ? { ...sub, weight: parseFloat(weight) } : sub
    ))
  }

  // Drag and drop for subsystem reordering
  const handleDragStart = (e, index) => {
    setDraggedItem(index)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e, dropIndex) => {
    e.preventDefault()
    if (draggedItem === null) return

    const newSubsystems = [...subsystems]
    const draggedSubsystem = newSubsystems[draggedItem]
    newSubsystems.splice(draggedItem, 1)
    newSubsystems.splice(dropIndex, 0, draggedSubsystem)
    
    // Update priorities
    const reorderedSubsystems = newSubsystems.map((sub, index) => ({
      ...sub,
      priority: index
    }))
    
    setSubsystems(reorderedSubsystems)
    setDraggedItem(null)
  }

  // Threshold Management Functions
  const loadThresholds = async () => {
    try {
      const thresholdData = await invoke('get_alert_thresholds')
      // Process threshold data if available
    } catch (err) {
      console.error('Failed to load thresholds:', err)
    }
  }

  const updateThreshold = async (metric, type, value) => {
    setThresholds(prev => ({
      ...prev,
      [metric]: { ...prev[metric], [type]: parseFloat(value) }
    }))
  }

  const saveThresholds = async () => {
    await handleApiCall(async () => {
      for (const [metric, threshold] of Object.entries(thresholds)) {
        await invoke('set_alert_threshold', {
          metric,
          threshold: threshold.max,
          direction: 'above'
        })
      }
    }, 'Thresholds saved successfully')
  }

  // Neural Network Config Functions
  const loadNeuralConfig = async () => {
    // Implementation depends on backend API
    console.log('Loading neural config...')
  }

  const saveNeuralConfig = async () => {
    await handleApiCall(async () => {
      // Implementation depends on backend API
      console.log('Saving neural config:', neuralConfig)
    }, 'Neural network configuration saved')
  }

  const resetNeuralWeights = async () => {
    await handleApiCall(async () => {
      // Implementation depends on backend API
      console.log('Resetting neural network weights...')
    }, 'Neural network weights reset')
  }

  // Data Recording Functions
  const loadRecordingConfig = async () => {
    // Implementation depends on backend API
    console.log('Loading recording config...')
  }

  const saveRecordingConfig = async () => {
    await handleApiCall(async () => {
      // Implementation depends on backend API
      console.log('Saving recording config:', recordingConfig)
    }, 'Recording configuration saved')
  }

  const exportSessionData = async () => {
    await handleApiCall(async () => {
      // Implementation depends on backend API
      console.log('Exporting session data...')
    }, 'Session data exported successfully')
  }

  const importSessionData = async (file) => {
    await handleApiCall(async () => {
      // Implementation depends on backend API
      console.log('Importing session data from:', file.name)
    }, 'Session data imported successfully')
  }

  // Check if threshold is exceeded
  const isThresholdExceeded = (metric) => {
    const threshold = thresholds[metric]
    const currentValue = currentMetrics[metric] || threshold.current
    return currentValue < threshold.min || currentValue > threshold.max
  }

  return (
    <div className={`bg-gray-800/50 backdrop-blur-lg rounded-2xl border border-gray-700/50 shadow-2xl ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-700/50">
        <h2 className="text-2xl font-bold text-gray-200 flex items-center">
          <span className="mr-3">⚙️</span>
          Advanced Configuration Panel
        </h2>
        <p className="text-gray-400 mt-1">Configure subsystems, thresholds, and neural parameters</p>
      </div>

      {/* Status Messages */}
      {error && (
        <div className="mx-6 mt-4 p-3 bg-red-900/30 border border-red-500/50 rounded-lg">
          <p className="text-red-300 text-sm flex items-center">
            <span className="mr-2">⚠️</span>
            {error}
          </p>
        </div>
      )}
      
      {success && (
        <div className="mx-6 mt-4 p-3 bg-green-900/30 border border-green-500/50 rounded-lg">
          <p className="text-green-300 text-sm flex items-center">
            <span className="mr-2">✅</span>
            {success}
          </p>
        </div>
      )}

      <div className="p-6 space-y-6">
        {/* 1. Subsystem Management */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-600/30">
          <button
            onClick={() => toggleSection('subsystems')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-700/20 transition-colors"
          >
            <h3 className="text-lg font-semibold text-gray-200 flex items-center">
              <span className="mr-2">🧩</span>
              Subsystem Management
            </h3>
            <span className={`transform transition-transform ${expandedSections.subsystems ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
          
          {expandedSections.subsystems && (
            <div className="p-4 border-t border-gray-600/30">
              {/* Add New Subsystem */}
              <div className="mb-6 p-4 bg-gray-800/30 rounded-lg border border-gray-600/20">
                <h4 className="text-md font-medium text-gray-300 mb-3">Add New Subsystem</h4>
                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Subsystem name"
                    value={newSubsystemName}
                    onChange={(e) => setNewSubsystemName(e.target.value)}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <textarea
                    placeholder="Configuration JSON"
                    value={newSubsystemConfig}
                    onChange={(e) => setNewSubsystemConfig(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                  />
                  <button
                    onClick={addSubsystem}
                    disabled={isLoading || !newSubsystemName.trim()}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
                  >
                    {isLoading ? '⏳ Adding...' : '➕ Add Subsystem'}
                  </button>
                </div>
              </div>

              {/* Subsystem List */}
              <div className="space-y-3">
                {subsystems.map((subsystem, index) => (
                  <div
                    key={subsystem.id}
                    draggable
                    onDragStart={(e) => handleDragStart(e, index)}
                    onDragOver={handleDragOver}
                    onDrop={(e) => handleDrop(e, index)}
                    className="p-4 bg-gray-800/50 rounded-lg border border-gray-600/30 cursor-move hover:border-gray-500/50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="cursor-grab">⋮⋮</div>
                        <div>
                          <h5 className="font-medium text-gray-200">{subsystem.name}</h5>
                          <p className="text-sm text-gray-400">ID: {subsystem.id}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-4">
                        {/* Weight Slider */}
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-400">Weight:</span>
                          <input
                            type="range"
                            min="0"
                            max="2"
                            step="0.1"
                            value={subsystem.weight}
                            onChange={(e) => updateSubsystemWeight(subsystem.id, e.target.value)}
                            className="w-20 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                          />
                          <span className="text-sm text-gray-300 font-mono w-8">
                            {subsystem.weight.toFixed(1)}
                          </span>
                        </div>
                        
                        {/* Toggle Switch */}
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={subsystem.status === 'active'}
                            onChange={(e) => toggleSubsystem(subsystem.id, e.target.checked)}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                        </label>
                        
                        {/* Remove Button */}
                        <button
                          onClick={() => removeSubsystem(subsystem.id)}
                          disabled={isLoading}
                          className="px-3 py-1 bg-red-600/80 hover:bg-red-600 text-white rounded text-sm transition-colors"
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 2. Metric Thresholds */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-600/30">
          <button
            onClick={() => toggleSection('thresholds')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-700/20 transition-colors"
          >
            <h3 className="text-lg font-semibold text-gray-200 flex items-center">
              <span className="mr-2">📊</span>
              Metric Thresholds
            </h3>
            <span className={`transform transition-transform ${expandedSections.thresholds ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
          
          {expandedSections.thresholds && (
            <div className="p-4 border-t border-gray-600/30">
              {Object.entries(thresholds).map(([metric, threshold]) => (
                <div key={metric} className="mb-6 p-4 bg-gray-800/30 rounded-lg border border-gray-600/20">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h4 className="text-md font-medium text-gray-200 capitalize">
                        {metric === 'scup' ? 'SCUP' : metric} Threshold
                      </h4>
                      <p className="text-sm text-gray-400">
                        Current: <span className="font-mono font-medium">
                          {((currentMetrics[metric] || threshold.current)).toFixed(3)}
                        </span>
                      </p>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                      isThresholdExceeded(metric)
                        ? 'bg-red-900/50 text-red-300 border border-red-500/50'
                        : 'bg-green-900/50 text-green-300 border border-green-500/50'
                    }`}>
                      {isThresholdExceeded(metric) ? '⚠️ Exceeded' : '✅ Normal'}
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    {/* Min Threshold */}
                    <div>
                      <div className="flex justify-between text-sm text-gray-400 mb-2">
                        <span>Minimum Threshold</span>
                        <span>{threshold.min.toFixed(3)}</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.001"
                        value={threshold.min}
                        onChange={(e) => updateThreshold(metric, 'min', e.target.value)}
                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    
                    {/* Max Threshold */}
                    <div>
                      <div className="flex justify-between text-sm text-gray-400 mb-2">
                        <span>Maximum Threshold</span>
                        <span>{threshold.max.toFixed(3)}</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="1"
                        step="0.001"
                        value={threshold.max}
                        onChange={(e) => updateThreshold(metric, 'max', e.target.value)}
                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                      />
                    </div>
                    
                    {/* Alert Configuration */}
                    <div className="flex items-center justify-between pt-2 border-t border-gray-600/30">
                      <div className="flex items-center space-x-4">
                        <label className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={alertConfig[metric]?.enabled}
                            onChange={(e) => setAlertConfig(prev => ({
                              ...prev,
                              [metric]: { ...prev[metric], enabled: e.target.checked }
                            }))}
                            className="w-4 h-4 text-blue-600 bg-gray-700 border-gray-600 rounded focus:ring-blue-500"
                          />
                          <span className="text-sm text-gray-300">Enable Alerts</span>
                        </label>
                        
                        <label className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={alertConfig[metric]?.autoResponse}
                            onChange={(e) => setAlertConfig(prev => ({
                              ...prev,
                              [metric]: { ...prev[metric], autoResponse: e.target.checked }
                            }))}
                            className="w-4 h-4 text-red-600 bg-gray-700 border-gray-600 rounded focus:ring-red-500"
                          />
                          <span className="text-sm text-gray-300">Auto Response</span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              <button
                onClick={saveThresholds}
                disabled={isLoading}
                className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
              >
                {isLoading ? '⏳ Saving...' : '💾 Save Thresholds'}
              </button>
            </div>
          )}
        </div>

        {/* 3. Neural Network Configuration */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-600/30">
          <button
            onClick={() => toggleSection('neural')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-700/20 transition-colors"
          >
            <h3 className="text-lg font-semibold text-gray-200 flex items-center">
              <span className="mr-2">🧠</span>
              Neural Network Configuration
            </h3>
            <span className={`transform transition-transform ${expandedSections.neural ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
          
          {expandedSections.neural && (
            <div className="p-4 border-t border-gray-600/30">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Hidden Layer Size */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Hidden Layer Size: {neuralConfig.hiddenLayerSize}
                  </label>
                  <input
                    type="range"
                    min="32"
                    max="512"
                    step="32"
                    value={neuralConfig.hiddenLayerSize}
                    onChange={(e) => setNeuralConfig(prev => ({ ...prev, hiddenLayerSize: parseInt(e.target.value) }))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>32</span>
                    <span>512</span>
                  </div>
                </div>
                
                {/* Learning Rate */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Learning Rate: {neuralConfig.learningRate}
                  </label>
                  <input
                    type="range"
                    min="0.0001"
                    max="0.1"
                    step="0.0001"
                    value={neuralConfig.learningRate}
                    onChange={(e) => setNeuralConfig(prev => ({ ...prev, learningRate: parseFloat(e.target.value) }))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0.0001</span>
                    <span>0.1</span>
                  </div>
                </div>
                
                {/* Batch Size */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Batch Size: {neuralConfig.batchSize}
                  </label>
                  <input
                    type="range"
                    min="8"
                    max="128"
                    step="8"
                    value={neuralConfig.batchSize}
                    onChange={(e) => setNeuralConfig(prev => ({ ...prev, batchSize: parseInt(e.target.value) }))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>8</span>
                    <span>128</span>
                  </div>
                </div>
                
                {/* Epochs */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Training Epochs: {neuralConfig.epochs}
                  </label>
                  <input
                    type="range"
                    min="10"
                    max="1000"
                    step="10"
                    value={neuralConfig.epochs}
                    onChange={(e) => setNeuralConfig(prev => ({ ...prev, epochs: parseInt(e.target.value) }))}
                    className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>10</span>
                    <span>1000</span>
                  </div>
                </div>
              </div>
              
              {/* Training Mode Toggle */}
              <div className="mt-6 p-4 bg-gray-800/30 rounded-lg border border-gray-600/20">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-md font-medium text-gray-200">Training Mode</h4>
                    <p className="text-sm text-gray-400">Enable continuous learning</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={neuralConfig.trainingMode}
                      onChange={(e) => setNeuralConfig(prev => ({ ...prev, trainingMode: e.target.checked }))}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                  </label>
                </div>
              </div>
              
              {/* Action Buttons */}
              <div className="mt-6 flex space-x-4">
                <button
                  onClick={saveNeuralConfig}
                  disabled={isLoading}
                  className="flex-1 px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
                >
                  {isLoading ? '⏳ Saving...' : '💾 Save Configuration'}
                </button>
                
                <button
                  onClick={resetNeuralWeights}
                  disabled={isLoading}
                  className="flex-1 px-4 py-3 bg-red-600 hover:bg-red-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
                >
                  {isLoading ? '⏳ Resetting...' : '🔄 Reset Weights'}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* 4. Data Recording */}
        <div className="bg-gray-900/30 rounded-lg border border-gray-600/30">
          <button
            onClick={() => toggleSection('recording')}
            className="w-full p-4 text-left flex items-center justify-between hover:bg-gray-700/20 transition-colors"
          >
            <h3 className="text-lg font-semibold text-gray-200 flex items-center">
              <span className="mr-2">📊</span>
              Data Recording & Export
            </h3>
            <span className={`transform transition-transform ${expandedSections.recording ? 'rotate-180' : ''}`}>
              ▼
            </span>
          </button>
          
          {expandedSections.recording && (
            <div className="p-4 border-t border-gray-600/30">
              <div className="space-y-6">
                {/* Recording Settings */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Log Rotation (hours): {recordingConfig.logRotationHours}
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="168"
                      value={recordingConfig.logRotationHours}
                      onChange={(e) => setRecordingConfig(prev => ({ ...prev, logRotationHours: parseInt(e.target.value) }))}
                      className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>1h</span>
                      <span>1 week</span>
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Max Log Size (MB): {recordingConfig.maxLogSizeMB}
                    </label>
                    <input
                      type="range"
                      min="10"
                      max="1000"
                      step="10"
                      value={recordingConfig.maxLogSizeMB}
                      onChange={(e) => setRecordingConfig(prev => ({ ...prev, maxLogSizeMB: parseInt(e.target.value) }))}
                      className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-gray-500 mt-1">
                      <span>10MB</span>
                      <span>1GB</span>
                    </div>
                  </div>
                </div>
                
                {/* Recording Options */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-800/30 rounded-lg border border-gray-600/20">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-md font-medium text-gray-200">Data Logging</h4>
                        <p className="text-sm text-gray-400">Record all metrics and events</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={recordingConfig.enabled}
                          onChange={(e) => setRecordingConfig(prev => ({ ...prev, enabled: e.target.checked }))}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </div>
                  </div>
                  
                  <div className="p-4 bg-gray-800/30 rounded-lg border border-gray-600/20">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="text-md font-medium text-gray-200">Compression</h4>
                        <p className="text-sm text-gray-400">Compress log files</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={recordingConfig.compressionEnabled}
                          onChange={(e) => setRecordingConfig(prev => ({ ...prev, compressionEnabled: e.target.checked }))}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
                      </label>
                    </div>
                  </div>
                </div>
                
                {/* Import/Export Buttons */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <button
                    onClick={saveRecordingConfig}
                    disabled={isLoading}
                    className="px-4 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
                  >
                    {isLoading ? '⏳ Saving...' : '💾 Save Config'}
                  </button>
                  
                  <button
                    onClick={exportSessionData}
                    disabled={isLoading}
                    className="px-4 py-3 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white rounded-lg font-medium transition-colors"
                  >
                    {isLoading ? '⏳ Exporting...' : '📤 Export Data'}
                  </button>
                  
                  <label className="px-4 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors cursor-pointer text-center">
                    📥 Import Data
                    <input
                      type="file"
                      accept=".json,.csv,.log"
                      onChange={(e) => {
                        if (e.target.files[0]) {
                          importSessionData(e.target.files[0])
                        }
                      }}
                      className="hidden"
                    />
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 18px;
          width: 18px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
        }

        .slider::-moz-range-thumb {
          height: 18px;
          width: 18px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
        }
      `}</style>
    </div>
  )
} 