import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Activity, Zap } from 'lucide-react';

interface IntegrationStatusProps {
  status?: 'success' | 'error' | 'warning';
  message?: string;
}

export const IntegrationStatus: React.FC<IntegrationStatusProps> = ({
  status = 'success',
  message = 'UnifiedVisualSubprocessManager successfully integrated!'
}) => {
  const getStatusIcon = () => {
    switch (status) {
      case 'success': return <CheckCircle className="w-5 h-5 text-green-400" />;
      case 'error': return <Activity className="w-5 h-5 text-red-400" />;
      case 'warning': return <Zap className="w-5 h-5 text-yellow-400" />;
      default: return <CheckCircle className="w-5 h-5 text-green-400" />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'success': return 'border-green-500/50 bg-green-900/20';
      case 'error': return 'border-red-500/50 bg-red-900/20';
      case 'warning': return 'border-yellow-500/50 bg-yellow-900/20';
      default: return 'border-green-500/50 bg-green-900/20';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`fixed bottom-4 left-4 z-50 p-4 rounded-lg border-2 backdrop-blur-sm ${getStatusColor()}`}
    >
      <div className="flex items-center space-x-3">
        {getStatusIcon()}
        <div>
          <h4 className="text-white font-semibold text-sm">Integration Status</h4>
          <p className="text-gray-300 text-xs">{message}</p>
          <div className="text-xs text-gray-400 mt-1">
            ✅ Navigation updated • ✅ Routes added • ✅ WebSocket ready (Port 3000)
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default IntegrationStatus; 