import { motion } from 'framer-motion'
import { useState } from 'react'
import ProcessViewer from './processes/ProcessViewer'
import ProcessTimelineVisualizer from './timeline/ProcessTimelineVisualizer'
import PythonVisualIntegration from './processes/PythonVisualIntegration'

export function ProcessManagementDashboard() {
  const [activeProcesses, setActiveProcesses] = useState<any[]>([])
  
  const handleToggleComponent = (componentName: string, enabled: boolean) => {
    console.log(`Toggling ${componentName}: ${enabled}`)
    // Add your component toggle logic here
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="w-full h-full p-8 overflow-y-auto"
    >
      <div className="max-w-7xl mx-auto space-y-6">
        <h2 className="text-3xl font-bold text-center text-purple-300 mb-8">Process Management</h2>
        
        {/* Process Viewer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <ProcessViewer onToggleComponent={handleToggleComponent} />
        </motion.div>
        
        {/* Process Timeline */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <ProcessTimelineVisualizer />
        </motion.div>
        
        {/* Python Visual Integration */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <PythonVisualIntegration activeProcesses={activeProcesses} />
        </motion.div>
      </div>
    </motion.div>
  )
}

export default ProcessManagementDashboard
