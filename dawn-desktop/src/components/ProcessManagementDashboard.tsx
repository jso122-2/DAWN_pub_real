import { motion } from 'framer-motion'
import { useState } from 'react'
import ProcessViewer from './processes/ProcessViewer'
import ProcessTimelineVisualizer from './timeline/ProcessTimelineVisualizer'
import PythonVisualIntegration from './processes/PythonVisualIntegration'
import VisualProcessManager from './VisualProcessManager'

export function ProcessManagementDashboard() {
  const [activeProcesses, setActiveProcesses] = useState<any[]>([])
  const [activeTab, setActiveTab] = useState<string>('processes')
  
  const handleToggleComponent = (componentName: string, enabled: boolean) => {
    console.log(`Toggling ${componentName}: ${enabled}`)
    // Add your component toggle logic here
  }

  const tabs = [
    { id: 'processes', label: 'Process Control', icon: '⚙️' },
    { id: 'visual', label: 'Visual Consciousness', icon: '🎬' },
    { id: 'timeline', label: 'Timeline', icon: '📊' },
    { id: 'integration', label: 'Python Integration', icon: '🐍' }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full h-full p-8 overflow-y-auto"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        <h2 className="text-3xl font-bold text-center text-purple-300 mb-8">Process Management</h2>
        
        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="flex bg-gray-800/50 p-1 rounded-lg border border-gray-700">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-6 py-3 rounded-md transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-purple-600 text-white shadow-lg'
                    : 'text-gray-300 hover:text-white hover:bg-gray-700'
                }`}
              >
                <span className="text-xl">{tab.icon}</span>
                <span className="font-medium">{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
        
        {/* Tab Content */}
        {activeTab === 'processes' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <ProcessViewer onToggleComponent={handleToggleComponent} />
          </motion.div>
        )}
        
        {activeTab === 'visual' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <VisualProcessManager />
          </motion.div>
        )}
        
        {activeTab === 'timeline' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <ProcessTimelineVisualizer />
          </motion.div>
        )}
        
        {activeTab === 'integration' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <PythonVisualIntegration activeProcesses={activeProcesses} />
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default ProcessManagementDashboard
