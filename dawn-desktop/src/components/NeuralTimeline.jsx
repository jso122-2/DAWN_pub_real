import React, { useState, useEffect, useRef } from 'react';
import eventBus, { EventTypes } from './eventBus';

const NeuralTimeline = ({ maxEvents = 50, timeWindow = 30000 }) => {
  const [events, setEvents] = useState([]);
  const [isAutoScroll, setIsAutoScroll] = useState(true);
  const scrollRef = useRef(null);

  // Event type configurations
  const eventConfig = {
    [EventTypes.TICK]: { color: '#10b981', icon: '⏱️', label: 'Tick' },
    [EventTypes.METRICS_UPDATE]: { color: '#3b82f6', icon: '📊', label: 'Metrics' },
    [EventTypes.ALERT]: { color: '#ef4444', icon: '🚨', label: 'Alert' },
    [EventTypes.PATTERN]: { color: '#f59e0b', icon: '🔍', label: 'Pattern' },
    [EventTypes.ANOMALY]: { color: '#dc2626', icon: '⚠️', label: 'Anomaly' },
    [EventTypes.PREDICTION]: { color: '#8b5cf6', icon: '🔮', label: 'Prediction' },
    [EventTypes.STATE_CHANGE]: { color: '#06b6d4', icon: '🔄', label: 'State' },
    [EventTypes.ERROR]: { color: '#f87171', icon: '❌', label: 'Error' },
    [EventTypes.CONNECTION_STATUS]: { color: '#6b7280', icon: '🔗', label: 'Connection' }
  };

  // Add event to timeline
  const addEvent = (type, data) => {
    const newEvent = {
      id: `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      timestamp: Date.now(),
      data,
      config: eventConfig[type] || { color: '#6b7280', icon: '📝', label: 'Unknown' }
    };

    setEvents(prevEvents => {
      const updated = [...prevEvents, newEvent];
      const cutoffTime = Date.now() - timeWindow;
      return updated
        .filter(event => event.timestamp > cutoffTime)
        .slice(-maxEvents)
        .sort((a, b) => b.timestamp - a.timestamp); // Most recent first
    });
  };

  // Format event data for display
  const formatEventData = (type, data) => {
    if (!data) return '';

    switch (type) {
      case EventTypes.TICK:
        return `Tick #${data.tick_count || 'unknown'}`;
      case EventTypes.METRICS_UPDATE:
        return `SCUP: ${data.scup?.toFixed(3) || 'N/A'}, Entropy: ${data.entropy?.toFixed(3) || 'N/A'}, Heat: ${data.heat?.toFixed(3) || 'N/A'}`;
      case EventTypes.ALERT:
        return data.message || data.description || 'Alert triggered';
      case EventTypes.PATTERN:
        return `Pattern detected: ${data.type || 'Unknown'} (${data.confidence || 0}% confidence)`;
      case EventTypes.ANOMALY:
        return `Anomaly: ${data.type || 'Unknown'} - Severity: ${data.severity || 'unknown'}`;
      case EventTypes.PREDICTION:
        return `Prediction: ${data.prediction || 'Unknown'} (${data.confidence || 0}% confidence)`;
      case EventTypes.STATE_CHANGE:
        return `State changed to: ${data.state || data.newState || 'unknown'}`;
      case EventTypes.ERROR:
        return data.message || data.error || 'Error occurred';
      case EventTypes.CONNECTION_STATUS:
        return `Connection ${data.connected ? 'established' : 'lost'} (${data.mode || 'unknown'})`;
      default:
        return typeof data === 'string' ? data : JSON.stringify(data);
    }
  };

  // Format timestamp
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Auto-scroll to latest events
  useEffect(() => {
    if (isAutoScroll && scrollRef.current) {
      scrollRef.current.scrollTop = 0; // Scroll to top since we show newest first
    }
  }, [events, isAutoScroll]);

  // Event bus listeners
  useEffect(() => {
    const handleEvent = (event) => {
      addEvent(event.type, event.detail);
    };

    // Listen to all event types
    Object.values(EventTypes).forEach(eventType => {
      eventBus.addEventListener(eventType, handleEvent);
    });

    // Add initial event
    addEvent(EventTypes.STATE_CHANGE, { state: 'Neural Timeline Initialized' });

    return () => {
      Object.values(EventTypes).forEach(eventType => {
        eventBus.removeEventListener(eventType, handleEvent);
      });
    };
  }, []);

  return (
    <div className="bg-gray-900 rounded-2xl border border-gray-700 p-6 shadow-lg">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="mr-2">🧠</span>
          Neural Timeline
        </h3>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsAutoScroll(!isAutoScroll)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              isAutoScroll 
                ? 'bg-green-600 hover:bg-green-700 text-white' 
                : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
            }`}
          >
            {isAutoScroll ? '📌 Auto-scroll ON' : '📌 Auto-scroll OFF'}
          </button>
          
          <span className="text-gray-400 text-sm">
            {events.length} events
          </span>
        </div>
      </div>

      {/* Timeline */}
      <div 
        ref={scrollRef}
        className="max-h-64 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800"
      >
        {events.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p>No events yet...</p>
            <p className="text-sm mt-2">Neural events will appear here in real-time</p>
          </div>
        ) : (
          events.map((event) => (
            <div
              key={event.id}
              className="flex items-start space-x-3 p-3 rounded-lg bg-gray-800 hover:bg-gray-750 transition-colors"
            >
              {/* Event icon */}
              <span className="text-lg flex-shrink-0" title={event.config.label}>
                {event.config.icon}
              </span>

              {/* Event content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  {/* Timestamp */}
                  <span className="text-xs text-gray-400 font-mono">
                    {formatTime(event.timestamp)}
                  </span>

                  {/* Event type badge */}
                  <span 
                    className="px-2 py-0.5 rounded text-xs font-medium"
                    style={{ 
                      backgroundColor: event.config.color + '20',
                      color: event.config.color,
                      border: `1px solid ${event.config.color}40`
                    }}
                  >
                    {event.config.label}
                  </span>
                </div>

                {/* Event data */}
                <p className="text-sm text-gray-300 break-words">
                  {formatEventData(event.type, event.data)}
                </p>
              </div>

              {/* Timeline indicator */}
              <div 
                className="w-1 h-full flex-shrink-0 rounded-full min-h-[40px]"
                style={{ backgroundColor: event.config.color + '60' }}
              />
            </div>
          ))
        )}
      </div>

      {/* Legend */}
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="grid grid-cols-3 md:grid-cols-5 gap-2 text-xs">
          {Object.entries(eventConfig).map(([type, config]) => (
            <div key={type} className="flex items-center space-x-1">
              <span>{config.icon}</span>
              <span style={{ color: config.color }}>{config.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NeuralTimeline; 