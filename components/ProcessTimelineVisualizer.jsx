import React, { useState, useEffect, useRef } from 'react';
import eventBus from './eventBus';

const ProcessTimelineVisualizer = ({ 
  timeWindow = 60000, // 60 seconds
  maxEvents = 100 
}) => {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);
  const [events, setEvents] = useState([]);
  const [currentTime, setCurrentTime] = useState(Date.now());
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isPaused, setIsPaused] = useState(false);

  // Event types and configurations
  const eventTypes = {
    'tick': { color: '#10b981', label: 'Tick', priority: 1 },
    'metrics-update': { color: '#3b82f6', label: 'Metrics', priority: 2 },
    'pattern-detected': { color: '#f59e0b', label: 'Pattern', priority: 3 },
    'anomaly-detected': { color: '#ef4444', label: 'Anomaly', priority: 4 },
    'cognitive-load': { color: '#8b5cf6', label: 'Load', priority: 2 },
    'disturbance': { color: '#ec4899', label: 'Disturbance', priority: 3 }
  };

  // Add new event
  const addEvent = (type, data = {}) => {
    const newEvent = {
      id: `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      timestamp: Date.now(),
      data,
      priority: eventTypes[type]?.priority || 1
    };

    setEvents(prevEvents => {
      const updated = [...prevEvents, newEvent];
      const cutoffTime = Date.now() - timeWindow;
      return updated
        .filter(event => event.timestamp > cutoffTime)
        .slice(-maxEvents)
        .sort((a, b) => a.timestamp - b.timestamp);
    });
  };

  // Draw timeline
  const drawTimeline = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    const now = isPaused ? currentTime : Date.now();

    // Clear canvas
    ctx.fillStyle = '#0a0f1b';
    ctx.fillRect(0, 0, width, height);

    // Timeline parameters
    const timelineHeight = height - 100;
    const timelineTop = 50;
    const timelineBottom = timelineTop + timelineHeight;
    const leftMargin = 80;
    const rightMargin = 50;
    const timelineWidth = width - leftMargin - rightMargin;

    // Time range
    const timeRange = timeWindow / zoomLevel;
    const startTime = now - timeRange;
    const endTime = now;

    // Draw background
    ctx.fillStyle = '#1f2937';
    ctx.fillRect(leftMargin, timelineTop, timelineWidth, timelineHeight);

    // Draw time grid
    ctx.strokeStyle = '#374151';
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 2]);

    const timeSteps = 10;
    for (let i = 0; i <= timeSteps; i++) {
      const x = leftMargin + (i / timeSteps) * timelineWidth;
      ctx.beginPath();
      ctx.moveTo(x, timelineTop);
      ctx.lineTo(x, timelineBottom);
      ctx.stroke();

      // Time labels
      const time = startTime + (i / timeSteps) * timeRange;
      const timeLabel = new Date(time).toLocaleTimeString();
      ctx.fillStyle = '#9ca3af';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(timeLabel, x, timelineBottom + 20);
    }
    ctx.setLineDash([]);

    // Draw event lanes
    const eventTypesArray = Object.keys(eventTypes);
    const laneHeight = timelineHeight / eventTypesArray.length;

    eventTypesArray.forEach((type, index) => {
      const laneTop = timelineTop + index * laneHeight;
      const laneBottom = laneTop + laneHeight;

      // Lane background
      ctx.fillStyle = index % 2 === 0 ? '#111827' : '#1f2937';
      ctx.fillRect(leftMargin, laneTop, timelineWidth, laneHeight);

      // Lane label
      ctx.fillStyle = eventTypes[type].color;
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.fillText(eventTypes[type].label, leftMargin - 10, laneTop + laneHeight / 2);

      // Lane border
      ctx.strokeStyle = '#374151';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(leftMargin, laneBottom);
      ctx.lineTo(leftMargin + timelineWidth, laneBottom);
      ctx.stroke();
    });

    // Draw events
    events.forEach(event => {
      if (event.timestamp < startTime || event.timestamp > endTime) return;

      const eventTypeIndex = eventTypesArray.indexOf(event.type);
      if (eventTypeIndex === -1) return;

      const x = leftMargin + ((event.timestamp - startTime) / timeRange) * timelineWidth;
      const laneTop = timelineTop + eventTypeIndex * laneHeight;
      const laneCenter = laneTop + laneHeight / 2;

      const config = eventTypes[event.type];
      const isSelected = selectedEvent?.id === event.id;
      const size = 6 + event.priority * 2;

      // Event marker
      ctx.fillStyle = config.color;
      ctx.strokeStyle = isSelected ? '#ffffff' : config.color;
      ctx.lineWidth = isSelected ? 3 : 1;

      // Different shapes for different priorities
      if (event.priority >= 4) {
        // Diamond for high priority
        ctx.beginPath();
        ctx.moveTo(x, laneCenter - size);
        ctx.lineTo(x + size, laneCenter);
        ctx.lineTo(x, laneCenter + size);
        ctx.lineTo(x - size, laneCenter);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      } else if (event.priority >= 3) {
        // Triangle for medium-high priority
        ctx.beginPath();
        ctx.moveTo(x, laneCenter - size);
        ctx.lineTo(x + size, laneCenter + size);
        ctx.lineTo(x - size, laneCenter + size);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      } else {
        // Circle for normal priority
        ctx.beginPath();
        ctx.arc(x, laneCenter, size, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();
      }

      // Glow effect for selected event
      if (isSelected) {
        ctx.shadowBlur = 20;
        ctx.shadowColor = config.color;
        ctx.beginPath();
        ctx.arc(x, laneCenter, size + 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    });

    // Current time indicator
    if (!isPaused) {
      const currentX = leftMargin + timelineWidth;
      ctx.strokeStyle = '#ef4444';
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(currentX, timelineTop);
      ctx.lineTo(currentX, timelineBottom);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#ef4444';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('NOW', currentX, timelineTop - 10);
    }

    // Title
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 16px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('Process Timeline', 20, 25);

    ctx.fillStyle = '#9ca3af';
    ctx.font = '12px monospace';
    ctx.fillText(`Events: ${events.length} | Zoom: ${zoomLevel.toFixed(1)}x`, width - 200, 25);
  };

  // Mouse interaction
  const handleCanvasClick = (event) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const canvasX = (x / rect.width) * canvas.width;
    const canvasY = (y / rect.height) * canvas.height;

    const leftMargin = 80;
    const timelineTop = 50;
    const timelineHeight = canvas.height - 100;
    const timelineWidth = canvas.width - leftMargin - 50;
    const laneHeight = timelineHeight / Object.keys(eventTypes).length;

    const now = isPaused ? currentTime : Date.now();
    const timeRange = timeWindow / zoomLevel;
    const startTime = now - timeRange;

    let clickedEvent = null;
    events.forEach(event => {
      if (event.timestamp < startTime || event.timestamp > now) return;

      const eventX = leftMargin + ((event.timestamp - startTime) / timeRange) * timelineWidth;
      const eventTypeIndex = Object.keys(eventTypes).indexOf(event.type);
      const eventY = timelineTop + eventTypeIndex * laneHeight + laneHeight / 2;

      const distance = Math.sqrt(Math.pow(canvasX - eventX, 2) + Math.pow(canvasY - eventY, 2));
      if (distance < 15) {
        clickedEvent = event;
      }
    });

    setSelectedEvent(clickedEvent);
  };

  // Animation loop
  useEffect(() => {
    const animate = () => {
      if (!isPaused) {
        setCurrentTime(Date.now());
      }
      drawTimeline();
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [events, selectedEvent, zoomLevel, isPaused, currentTime]);

  // Event bus integration
  useEffect(() => {
    const eventHandlers = {
      'tick': (data) => addEvent('tick', data),
      'metrics-update': (data) => addEvent('metrics-update', data),
      'pattern-detected': (data) => addEvent('pattern-detected', data),
      'anomaly-detected': (data) => addEvent('anomaly-detected', data),
      'cognitive-load': (data) => addEvent('cognitive-load', data),
      'disturbance': (data) => addEvent('disturbance', data)
    };

    Object.entries(eventHandlers).forEach(([eventType, handler]) => {
      eventBus.on(eventType, handler);
    });

    return () => {
      Object.entries(eventHandlers).forEach(([eventType, handler]) => {
        eventBus.off(eventType, handler);
      });
    };
  }, []);

  // Simulate events
  useEffect(() => {
    const interval = setInterval(() => {
      if (!isPaused) {
        const eventType = Object.keys(eventTypes)[Math.floor(Math.random() * Object.keys(eventTypes).length)];
        addEvent(eventType, { value: Math.random(), source: 'simulation' });
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [isPaused]);

  return (
    <div className="bg-gray-900 rounded-2xl border border-gray-700 p-6 shadow-lg">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-white flex items-center">
          <span className="mr-2">⏱️</span>
          Process Timeline
        </h3>
        
        {/* Controls */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsPaused(!isPaused)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
              isPaused 
                ? 'bg-green-600 hover:bg-green-700 text-white' 
                : 'bg-yellow-600 hover:bg-yellow-700 text-white'
            }`}
          >
            {isPaused ? '▶️ Resume' : '⏸️ Pause'}
          </button>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setZoomLevel(Math.max(0.1, zoomLevel - 0.5))}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm"
            >
              ➖
            </button>
            <span className="text-gray-300 text-sm min-w-[60px] text-center">
              {zoomLevel.toFixed(1)}x
            </span>
            <button
              onClick={() => setZoomLevel(Math.min(10, zoomLevel + 0.5))}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm"
            >
              ➕
            </button>
          </div>
        </div>
      </div>

      {/* Canvas */}
      <canvas
        ref={canvasRef}
        width={1000}
        height={400}
        className="w-full h-auto bg-gray-800 rounded-lg border border-gray-600 cursor-pointer"
        onClick={handleCanvasClick}
      />

      {/* Selected Event Details */}
      {selectedEvent && (
        <div className="mt-4 p-4 bg-gray-800 rounded-lg border border-gray-600">
          <h4 className="text-lg font-bold text-white mb-2">Event Details</h4>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-400">Type:</span>
              <span className="ml-2 font-mono" style={{ color: eventTypes[selectedEvent.type]?.color }}>
                {selectedEvent.type}
              </span>
            </div>
            <div>
              <span className="text-gray-400">Time:</span>
              <span className="ml-2 font-mono text-white">
                {new Date(selectedEvent.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div>
              <span className="text-gray-400">Priority:</span>
              <span className="ml-2 font-mono text-white">
                {selectedEvent.priority}
              </span>
            </div>
          </div>
          {selectedEvent.data && Object.keys(selectedEvent.data).length > 0 && (
            <div className="mt-2">
              <span className="text-gray-400">Data:</span>
              <pre className="mt-1 text-xs text-gray-300 font-mono bg-gray-900 p-2 rounded overflow-auto">
                {JSON.stringify(selectedEvent.data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
        {Object.entries(eventTypes).map(([type, config]) => (
          <div key={type} className="flex items-center space-x-2 p-2 bg-gray-800 rounded border border-gray-600">
            <div 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: config.color }}
            />
            <span className="text-gray-300">{config.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// PropTypes removed for simpler integration

export default ProcessTimelineVisualizer; 