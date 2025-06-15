import React, { useEffect, useState } from 'react';
import eventBus from '../../lib/eventBus';

interface DiagnosticEvent {
  type: string;
  source: string;
  time: number;
  data?: any;
}

interface SystemDiagnosticsProps {
  onEvent?: (event: DiagnosticEvent) => void;
}

const SystemDiagnostics: React.FC<SystemDiagnosticsProps> = ({ onEvent }) => {
  const [events, setEvents] = useState<DiagnosticEvent[]>([]);

  useEffect(() => {
    const handleEvent = (e: CustomEvent) => {
      const event = e.detail;
      setEvents(prev => [event, ...prev].slice(0, 10));
      if (onEvent) onEvent(event);
    };

    // Listen for all module events
    eventBus.addEventListener('neural:spike', handleEvent as EventListener);
    eventBus.addEventListener('neural:pattern', handleEvent as EventListener);
    eventBus.addEventListener('consciousness:fluctuation', handleEvent as EventListener);
    eventBus.addEventListener('consciousness:collapse', handleEvent as EventListener);

    return () => {
      eventBus.removeEventListener('neural:spike', handleEvent as EventListener);
      eventBus.removeEventListener('neural:pattern', handleEvent as EventListener);
      eventBus.removeEventListener('consciousness:fluctuation', handleEvent as EventListener);
      eventBus.removeEventListener('consciousness:collapse', handleEvent as EventListener);
    };
  }, [onEvent]);

  const emitDiagnostic = () => {
    const event = {
      type: 'system:diagnostic',
      source: 'SystemDiagnostics',
      time: Date.now(),
      data: {
        status: 'operational',
        modules: ['NeuralProcessor', 'ConsciousnessCore'],
        uptime: Date.now()
      }
    };
    eventBus.dispatchEvent(new CustomEvent('system:diagnostic', { detail: event }));
    if (onEvent) onEvent(event);
  };

  return (
    <div className="glass-diagnostic rounded-lg p-4">
      <h3 className="text-lg font-semibold text-white mb-2">System Diagnostics</h3>
      <div className="space-y-2">
        {events.map((event, index) => (
          <div key={index} className="text-sm text-white/80 bg-black/20 p-2 rounded">
            <div className="font-mono">{event.type}</div>
            <div className="text-xs text-white/60">
              {new Date(event.time).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>
      <button 
        onClick={emitDiagnostic}
        className="mt-4 px-3 py-1 bg-blue-500/20 hover:bg-blue-500/30 rounded text-white text-sm"
      >
        Run Diagnostic
      </button>
    </div>
  );
};

export default SystemDiagnostics; 