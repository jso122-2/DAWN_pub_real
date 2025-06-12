import React, { useState, useEffect, useRef } from 'react';
import { useSwipeable } from 'react-swipeable';
import { 
  HomeIcon, 
  ChartBarIcon, 
  CpuChipIcon, 
  ChatBubbleLeftRightIcon,
  XMarkIcon 
} from '@heroicons/react/24/outline';
import { 
  HomeIcon as HomeIconSolid,
  ChartBarIcon as ChartBarIconSolid,
  CpuChipIcon as CpuChipIconSolid,
  ChatBubbleLeftRightIcon as ChatBubbleLeftRightIconSolid
} from '@heroicons/react/24/solid';
import useDashboardStore, { selectMetrics, selectConsciousness } from './dashboardState';
import TalkToDAWN from './TalkToDAWN';
import CognitiveLoadRadar from '../../components/CognitiveLoadRadar';

// Mini gauge component for mobile
const MiniGauge = ({ label, value, color = 'blue', icon }) => {
  const percentage = Math.round(value * 100);
  
  return (
    <div className="bg-gray-800 rounded-lg p-3">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          {icon && <span className="text-lg">{icon}</span>}
          <span className="text-xs text-gray-400">{label}</span>
        </div>
        <span className="text-sm font-semibold text-white">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div 
          className={`h-2 bg-${color}-500 rounded-full transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

// Simplified health orb for mobile
const MobileHealthOrb = ({ metrics, emotion, intensity }) => {
  const healthScore = (metrics.scup + (1 - metrics.entropy) + (1 - metrics.heat)) / 3;
  
  const emotionColors = {
    curious: 'from-green-400 to-green-600',
    focused: 'from-blue-400 to-blue-600',
    creative: 'from-purple-400 to-purple-600',
    excited: 'from-orange-400 to-orange-600',
    contemplative: 'from-gray-400 to-gray-600',
    fragmented: 'from-red-400 to-red-600'
  };
  
  const gradientClass = emotionColors[emotion] || emotionColors.curious;
  const size = 120 + (healthScore * 40);
  
  return (
    <div className="relative flex items-center justify-center h-48">
      <div 
        className={`relative bg-gradient-to-br ${gradientClass} rounded-full shadow-2xl animate-pulse flex items-center justify-center`}
        style={{ 
          width: `${size}px`, 
          height: `${size}px`,
          animationDuration: `${2 / metrics.tick_rate}s`
        }}
      >
        <div className="text-center">
          <div className="text-2xl font-bold text-white">
            {Math.round(healthScore * 100)}%
          </div>
          <div className="text-xs text-white/80">{emotion}</div>
        </div>
      </div>
      
      <div 
        className="absolute rounded-full border-2 animate-ping"
        style={{
          width: `${size + 20}px`,
          height: `${size + 20}px`,
          borderColor: healthScore > 0.7 ? '#10b981' : healthScore > 0.4 ? '#f59e0b' : '#ef4444',
          animationDuration: '2s'
        }}
      />
    </div>
  );
};

// Event stream item for mobile
const MobileEventItem = ({ event }) => {
  const getEventIcon = () => {
    switch (event.type) {
      case 'anomaly': return '⚠️';
      case 'pattern': return '🔍';
      case 'rebloom': return '🌸';
      case 'thought': return '💭';
      default: return '📌';
    }
  };
  
  return (
    <div className="bg-gray-800 rounded-lg p-3 mb-2">
      <div className="flex items-start space-x-3">
        <span className="text-xl">{getEventIcon()}</span>
        <div className="flex-1">
          <p className="text-sm text-white">{event.description}</p>
          <p className="text-xs text-gray-400 mt-1">
            {new Date(event.timestamp).toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  );
};

// Subprocess status for mobile
const MobileSubprocessStatus = ({ name, status, value }) => {
  const statusColors = {
    active: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500',
    idle: 'bg-gray-500'
  };
  
  return (
    <div className="bg-gray-800 rounded-lg p-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${statusColors[status]}`} />
          <span className="text-sm text-white">{name}</span>
        </div>
        {value !== undefined && (
          <span className="text-sm text-gray-400">{value}</span>
        )}
      </div>
    </div>
  );
};

// Main panel - Metrics view
const MetricsPanel = () => {
  const metrics = useDashboardStore(selectMetrics);
  const { emotion, intensity } = useDashboardStore(selectConsciousness);
  
  return (
    <div className="flex flex-col h-full p-4 space-y-4">
      <div className="bg-gray-800 rounded-lg p-3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Emotional State</span>
          <span className="text-sm font-semibold text-white">
            {emotion} • {Math.round(intensity * 100)}%
          </span>
        </div>
        <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-1000"
            style={{ width: `${intensity * 100}%` }}
          />
        </div>
      </div>
      <MobileHealthOrb metrics={metrics} emotion={emotion} intensity={intensity} />
      <div className="w-full md:w-1/2 mx-auto">
        <CognitiveLoadRadar />
      </div>
      <div className="space-y-3">
        <MiniGauge label="SCUP" value={metrics.scup} color="green" icon="🧠" />
        <MiniGauge label="Entropy" value={metrics.entropy} color="purple" icon="🌀" />
        <MiniGauge label="Heat" value={metrics.heat} color="orange" icon="🔥" />
        <MiniGauge label="Tick Rate" value={metrics.tick_rate} color="blue" icon="⏱️" />
      </div>
    </div>
  );
};

// Visual panel - Simplified gradient
const VisualPanel = () => {
  const { emotion, intensity } = useDashboardStore(selectConsciousness);
  const canvasRef = useRef(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const { width, height } = canvas;
    
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(0, 0, width, height);
    
    const emotionColors = {
      curious: '#22c55e',
      focused: '#3b82f6',
      creative: '#a855f7',
      excited: '#f97316',
      contemplative: '#64748b',
      fragmented: '#ef4444'
    };
    
    const color = emotionColors[emotion] || '#64748b';
    const gradient = ctx.createLinearGradient(0, 0, width, 0);
    
    gradient.addColorStop(0, color + '00');
    gradient.addColorStop(0.5, color + 'ff');
    gradient.addColorStop(1, color + '00');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, height * 0.3, width, height * 0.4);
    
    const pulseGradient = ctx.createRadialGradient(
      width / 2, height / 2, 0,
      width / 2, height / 2, width / 2
    );
    
    pulseGradient.addColorStop(0, color + '40');
    pulseGradient.addColorStop(1, color + '00');
    
    ctx.fillStyle = pulseGradient;
    ctx.fillRect(0, 0, width, height);
    
    ctx.fillStyle = 'white';
    ctx.font = '14px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(`${emotion} (${Math.round(intensity * 100)}%)`, width / 2, height - 20);
    
  }, [emotion, intensity]);
  
  return (
    <div className="flex flex-col h-full p-4">
      <h2 className="text-lg font-semibold text-white mb-4">Consciousness Gradient</h2>
      
      <div className="flex-1 bg-gray-800 rounded-lg p-4">
        <canvas 
          ref={canvasRef}
          width={300}
          height={400}
          className="w-full h-full rounded"
        />
      </div>
      
      <div className="mt-4 space-y-2">
        <div className="bg-gray-800 rounded-lg p-3">
          <p className="text-sm text-gray-400">Gradient Context</p>
          <p className="text-white font-medium">Stable Flow</p>
        </div>
      </div>
    </div>
  );
};

// Status panel - Subprocess monitoring
const StatusPanel = () => {
  const { anomalies, patterns, rebloomProgress } = useDashboardStore();
  const connectionStatus = useDashboardStore(state => state.connectionStatus);
  
  const subprocesses = [
    { name: 'Pattern Detector', status: patterns.length > 0 ? 'active' : 'idle', value: patterns.length },
    { name: 'Anomaly Monitor', status: anomalies.length > 0 ? 'warning' : 'idle', value: anomalies.length },
    { name: 'Memory Manager', status: 'active', value: '73%' },
    { name: 'Rebloom Engine', status: rebloomProgress > 0 ? 'active' : 'idle', value: `${Math.round(rebloomProgress * 100)}%` },
    { name: 'WebSocket', status: connectionStatus === 'connected' ? 'active' : 'error', value: connectionStatus }
  ];
  
  const recentEvents = [
    ...anomalies.slice(-3).map(a => ({ ...a, type: 'anomaly', description: a.message || 'Anomaly detected' })),
    ...patterns.slice(-2).map(p => ({ ...p, type: 'pattern', description: p.description || 'Pattern detected' }))
  ].sort((a, b) => b.timestamp - a.timestamp).slice(0, 5);
  
  return (
    <div className="flex flex-col h-full p-4">
      <h2 className="text-lg font-semibold text-white mb-4">System Status</h2>
      
      <div className="space-y-3 mb-6">
        {subprocesses.map((subprocess) => (
          <MobileSubprocessStatus key={subprocess.name} {...subprocess} />
        ))}
      </div>
      
      <h3 className="text-md font-medium text-white mb-3">Recent Events</h3>
      
      <div className="flex-1 overflow-y-auto">
        {recentEvents.length > 0 ? (
          recentEvents.map((event, index) => (
            <MobileEventItem key={event.id || index} event={event} />
          ))
        ) : (
          <div className="text-center text-gray-500 mt-8">
            <p>No recent events</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Bottom navigation component
const BottomNavigation = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'metrics', label: 'Metrics', icon: HomeIcon, iconSolid: HomeIconSolid },
    { id: 'visual', label: 'Visual', icon: ChartBarIcon, iconSolid: ChartBarIconSolid },
    { id: 'status', label: 'Status', icon: CpuChipIcon, iconSolid: CpuChipIconSolid },
    { id: 'talk', label: 'Talk', icon: ChatBubbleLeftRightIcon, iconSolid: ChatBubbleLeftRightIconSolid }
  ];
  
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-700 px-2 pb-safe">
      <div className="flex justify-around">
        {tabs.map((tab) => {
          const Icon = activeTab === tab.id ? tab.iconSolid : tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col items-center py-2 px-4 transition-colors ${
                activeTab === tab.id ? 'text-blue-500' : 'text-gray-400'
              }`}
            >
              <Icon className="w-6 h-6 mb-1" />
              <span className="text-xs">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

// Main mobile dashboard component
const MobileDashboard = () => {
  const [activeTab, setActiveTab] = useState('metrics');
  const [showTalkModal, setShowTalkModal] = useState(false);
  const containerRef = useRef(null);
  
  const handlers = useSwipeable({
    onSwipedLeft: () => {
      const tabs = ['metrics', 'visual', 'status', 'talk'];
      const currentIndex = tabs.indexOf(activeTab);
      if (currentIndex < tabs.length - 1) {
        setActiveTab(tabs[currentIndex + 1]);
      }
    },
    onSwipedRight: () => {
      const tabs = ['metrics', 'visual', 'status', 'talk'];
      const currentIndex = tabs.indexOf(activeTab);
      if (currentIndex > 0) {
        setActiveTab(tabs[currentIndex - 1]);
      }
    },
    onSwipedUp: () => {
      if (activeTab !== 'talk') {
        setShowTalkModal(true);
      }
    },
    trackMouse: false,
    trackTouch: true,
    delta: 10,
    preventDefaultTouchmoveEvent: true
  });
  
  const handleTabChange = (tabId) => {
    if (tabId === 'talk') {
      setShowTalkModal(true);
    } else {
      setActiveTab(tabId);
      setShowTalkModal(false);
    }
  };
  
  const renderPanel = () => {
    switch (activeTab) {
      case 'metrics':
        return <MetricsPanel />;
      case 'visual':
        return <VisualPanel />;
      case 'status':
        return <StatusPanel />;
      default:
        return <MetricsPanel />;
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="fixed top-0 left-0 right-0 bg-gray-800 border-b border-gray-700 px-4 py-3 z-10">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold">DAWN Dashboard</h1>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm text-gray-400">Connected</span>
          </div>
        </div>
      </div>
      
      <div 
        {...handlers}
        ref={containerRef}
        className="pt-14 pb-16 h-screen overflow-hidden"
      >
        <div className="h-full overflow-y-auto">
          {renderPanel()}
        </div>
      </div>
      
      <BottomNavigation activeTab={activeTab} onTabChange={handleTabChange} />
      
      {showTalkModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-gray-800 rounded-lg w-full max-w-md max-h-[80vh] flex flex-col">
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <h2 className="text-lg font-semibold">Talk to DAWN</h2>
              <button
                onClick={() => setShowTalkModal(false)}
                className="text-gray-400 hover:text-white"
              >
                <XMarkIcon className="w-6 h-6" />
              </button>
            </div>
            <div className="flex-1 overflow-hidden">
              <TalkToDAWN isFloating={false} onClose={() => setShowTalkModal(false)} />
            </div>
          </div>
        </div>
      )}
      
      <div className="hidden offline:block fixed top-16 left-4 right-4 bg-yellow-600 text-white px-4 py-2 rounded-lg text-sm">
        Offline mode - Limited functionality
      </div>
    </div>
  );
};

export default MobileDashboard; 