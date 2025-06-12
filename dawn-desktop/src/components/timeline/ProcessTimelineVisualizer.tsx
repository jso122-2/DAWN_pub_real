import React, { useState, useEffect, useRef } from 'react';
import eventBus from '../../lib/eventBus';
import { motion, AnimatePresence } from 'framer-motion';
import { useCosmicStore } from '../../store/cosmic.store';
import { FixedSizeList as List, ListChildComponentProps } from 'react-window';
import { Download, Filter as FilterIcon } from 'lucide-react';

const COSMIC_COLORS = {
  purple: '#a78bfa',
  cyan: '#22d3ee',
  pink: '#f472b6',
  yellow: '#f59e0b',
  green: '#10b981',
  red: '#ef4444',
  blue: '#3b82f6',
};

const glassButton =
  'glass px-4 py-2 rounded-lg text-sm font-semibold text-white backdrop-blur border border-purple-500/30 hover:bg-white/10 transition-all';

// Event type
interface TimelineEvent {
  id: string;
  type: keyof typeof eventTypes;
  timestamp: number;
  data: any;
  priority: number;
}

// Event types and configurations
const eventTypes = {
  tick: { color: COSMIC_COLORS.green, label: 'Tick', priority: 1 },
  'metrics-update': { color: COSMIC_COLORS.blue, label: 'Metrics', priority: 2 },
  'pattern-detected': { color: COSMIC_COLORS.yellow, label: 'Pattern', priority: 3 },
  'anomaly-detected': { color: COSMIC_COLORS.red, label: 'Anomaly', priority: 4 },
  'cognitive-load': { color: COSMIC_COLORS.purple, label: 'Load', priority: 2 },
  disturbance: { color: COSMIC_COLORS.pink, label: 'Disturbance', priority: 3 },
} as const;

type EventTypeKey = keyof typeof eventTypes;

const ProcessTimelineVisualizer = ({ timeWindow = 60000, maxEvents = 100 }) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number | null>(null);
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [currentTime, setCurrentTime] = useState(Date.now());
  const [selectedEvent, setSelectedEvent] = useState<TimelineEvent | null>(null);
  const {
    timelineZoom,
    setTimelineZoom,
    timelinePaused,
    setTimelinePaused,
    timelineEventTypeFilters,
    setTimelineEventTypeFilters,
  } = useCosmicStore();

  // Add new event
  const addEvent = (type: EventTypeKey, data = {}) => {
    const newEvent = {
      id: `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      type,
      timestamp: Date.now(),
      data,
      priority: eventTypes[type]?.priority || 1,
    };
    setEvents((prevEvents) => {
      const updated = [...prevEvents, newEvent];
      const cutoffTime = Date.now() - timeWindow;
      return updated
        .filter((event) => event.timestamp > cutoffTime)
        .slice(-maxEvents)
        .sort((a, b) => a.timestamp - b.timestamp);
    });
  };

  // Draw timeline
  const drawTimeline = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const width = canvas.width;
    const height = canvas.height;
    const now = timelinePaused ? currentTime : Date.now();

    // Clear canvas (transparent)
    ctx.clearRect(0, 0, width, height);

    // Glass effect background (optional, subtle)
    ctx.save();
    ctx.globalAlpha = 0.7;
    ctx.fillStyle = '#18181b';
    ctx.fillRect(0, 0, width, height);
    ctx.restore();

    // Timeline parameters
    const timelineHeight = height - 100;
    const timelineTop = 50;
    const timelineBottom = timelineTop + timelineHeight;
    const leftMargin = 80;
    const rightMargin = 50;
    const timelineWidth = width - leftMargin - rightMargin;

    // Time range
    const timeRange = timeWindow / timelineZoom;
    const startTime = now - timeRange;
    const endTime = now;

    // Draw time grid (cosmic cyan)
    ctx.strokeStyle = COSMIC_COLORS.cyan + '66';
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
      ctx.fillStyle = COSMIC_COLORS.cyan;
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(timeLabel, x, timelineBottom + 20);
    }
    ctx.setLineDash([]);

    // Draw event lanes (cosmic glass)
    const eventTypesArray: EventTypeKey[] = Object.keys(eventTypes) as EventTypeKey[];
    const laneHeight = timelineHeight / eventTypesArray.length;
    eventTypesArray.forEach((type: EventTypeKey, index: number) => {
      const laneTop = timelineTop + index * laneHeight;
      const laneBottom = laneTop + laneHeight;
      // Lane background (glass effect)
      ctx.save();
      ctx.globalAlpha = 0.18;
      ctx.fillStyle = index % 2 === 0 ? COSMIC_COLORS.purple : COSMIC_COLORS.cyan;
      ctx.fillRect(leftMargin, laneTop, timelineWidth, laneHeight);
      ctx.restore();
      // Lane label
      ctx.fillStyle = eventTypes[type].color;
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.fillText(eventTypes[type].label, leftMargin - 10, laneTop + laneHeight / 2);
      // Lane border
      ctx.strokeStyle = COSMIC_COLORS.pink + '66';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(leftMargin, laneBottom);
      ctx.lineTo(leftMargin + timelineWidth, laneBottom);
      ctx.stroke();
    });

    // Draw events (neon shapes with glow)
    events.forEach((event: TimelineEvent) => {
      if (event.timestamp < startTime || event.timestamp > endTime) return;
      const eventTypeIndex = eventTypesArray.indexOf(event.type);
      if (eventTypeIndex === -1) return;
      const x = leftMargin + ((event.timestamp - startTime) / timeRange) * timelineWidth;
      const laneTop = timelineTop + eventTypeIndex * laneHeight;
      const laneCenter = laneTop + laneHeight / 2;
      const config = eventTypes[event.type];
      const isSelected = selectedEvent?.id === event.id;
      const size = 6 + event.priority * 2;
      // Neon glow
      ctx.save();
      ctx.shadowBlur = isSelected ? 24 : 12;
      ctx.shadowColor = config.color;
      ctx.strokeStyle = config.color;
      ctx.lineWidth = isSelected ? 4 : 2;
      ctx.globalAlpha = isSelected ? 1 : 0.85;
      // Neon shapes
      if (event.priority >= 4) {
        // Diamond
        ctx.beginPath();
        ctx.moveTo(x, laneCenter - size);
        ctx.lineTo(x + size, laneCenter);
        ctx.lineTo(x, laneCenter + size);
        ctx.lineTo(x - size, laneCenter);
        ctx.closePath();
        ctx.stroke();
        ctx.fillStyle = config.color + '33';
        ctx.fill();
      } else if (event.priority >= 3) {
        // Triangle
        ctx.beginPath();
        ctx.moveTo(x, laneCenter - size);
        ctx.lineTo(x + size, laneCenter + size);
        ctx.lineTo(x - size, laneCenter + size);
        ctx.closePath();
        ctx.stroke();
        ctx.fillStyle = config.color + '33';
        ctx.fill();
      } else {
        // Circle
        ctx.beginPath();
        ctx.arc(x, laneCenter, size, 0, Math.PI * 2);
        ctx.stroke();
        ctx.fillStyle = config.color + '33';
        ctx.fill();
      }
      ctx.restore();
      // Glow effect for selected event
      if (isSelected) {
        ctx.save();
        ctx.shadowBlur = 32;
        ctx.shadowColor = config.color;
        ctx.globalAlpha = 0.7;
        ctx.beginPath();
        ctx.arc(x, laneCenter, size + 4, 0, Math.PI * 2);
        ctx.fillStyle = config.color + '44';
        ctx.fill();
        ctx.restore();
      }
    });

    // Current time indicator (neon pink)
    if (!timelinePaused) {
      const currentX = leftMargin + timelineWidth;
      ctx.save();
      ctx.strokeStyle = COSMIC_COLORS.pink;
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 5]);
      ctx.beginPath();
      ctx.moveTo(currentX, timelineTop);
      ctx.lineTo(currentX, timelineBottom);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = COSMIC_COLORS.pink;
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('NOW', currentX, timelineTop - 10);
      ctx.restore();
    }

    // Title
    ctx.fillStyle = COSMIC_COLORS.purple;
    ctx.font = 'bold 16px monospace';
    ctx.textAlign = 'left';
    ctx.fillText('Process Timeline', 20, 25);
    ctx.fillStyle = COSMIC_COLORS.cyan;
    ctx.font = '12px monospace';
    ctx.fillText(`Events: ${events.length} | Zoom: ${timelineZoom.toFixed(1)}x`, width - 200, 25);
  };

  // Mouse interaction
  const handleCanvasClick = (event: React.MouseEvent<HTMLCanvasElement>) => {
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
    const now = timelinePaused ? currentTime : Date.now();
    const timeRange = timeWindow / timelineZoom;
    const startTime = now - timeRange;
    let clickedEvent = null;
    events.forEach((event) => {
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
      if (!timelinePaused) {
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
  }, [events, selectedEvent, timelineZoom, timelinePaused, currentTime]);

  // Event bus integration
  useEffect(() => {
    const eventHandlers = {
      tick: (event) => addEvent('tick', event.detail),
      'metrics-update': (event) => addEvent('metrics-update', event.detail),
      'pattern-detected': (event) => addEvent('pattern-detected', event.detail),
      'anomaly-detected': (event) => addEvent('anomaly-detected', event.detail),
      'cognitive-load': (event) => addEvent('cognitive-load', event.detail),
      disturbance: (event) => addEvent('disturbance', event.detail),
    };
    Object.entries(eventHandlers).forEach(([eventType, handler]) => {
      eventBus.addEventListener(eventType, handler);
    });
    return () => {
      Object.entries(eventHandlers).forEach(([eventType, handler]) => {
        eventBus.removeEventListener(eventType, handler);
      });
    };
  }, []);

  // Simulate events
  useEffect(() => {
    const interval = setInterval(() => {
      if (!timelinePaused) {
        const eventType = Object.keys(eventTypes)[Math.floor(Math.random() * Object.keys(eventTypes).length)];
        addEvent(eventType, { value: Math.random(), source: 'simulation' });
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [timelinePaused]);

  // Filtering logic
  const eventTypesArray: EventTypeKey[] = Object.keys(eventTypes) as EventTypeKey[];
  const [showFilters, setShowFilters] = useState(false);
  const filteredEvents: TimelineEvent[] = events.filter(e => timelineEventTypeFilters.includes(e.type));

  // Export events
  const exportEvents = () => {
    const dataStr = JSON.stringify(filteredEvents, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `timeline_events_${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Infinite scroll: load more events (simulate for now)
  const [eventLimit, setEventLimit] = useState(100);
  const handleLoadMore = () => {
    setEventLimit(lim => lim + 100);
  };
  const visibleEvents: TimelineEvent[] = filteredEvents.slice(-eventLimit);

  // List item renderer
  const renderEventRow = ({ index, style }: ListChildComponentProps) => {
    const event = visibleEvents[visibleEvents.length - 1 - index]; // newest at bottom
    if (!event) return null;
    const config = eventTypes[event.type] || { color: '#fff', label: event.type };
    return (
      <motion.div
        key={event.id}
        style={style}
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -40 }}
        transition={{ duration: 0.2 }}
        className={`flex items-center gap-4 px-4 py-2 border-b border-cyan-400/10 cursor-pointer hover:bg-cyan-400/10 ${selectedEvent?.id === event.id ? 'bg-cyan-500/10 border-cyan-400' : ''}`}
        onClick={() => setSelectedEvent(event)}
      >
        <span className="inline-block w-3 h-3 rounded-full" style={{ background: config.color }} />
        <span className="font-mono text-xs text-gray-400 w-28">{new Date(event.timestamp).toLocaleTimeString()}</span>
        <span className="font-mono text-xs" style={{ color: config.color }}>{config.label}</span>
        <span className="flex-1 truncate text-xs text-gray-300 ml-2">{event.data?.message || event.data?.description || JSON.stringify(event.data)}</span>
      </motion.div>
    );
  };

  return (
    <div className="glass rounded-2xl border border-purple-500/30 p-6 shadow-glow-md backdrop-blur-xl">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold text-purple-300 flex items-center">
          <span className="mr-2">⏱️</span>
          Process Timeline
        </h3>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setTimelinePaused(!timelinePaused)}
            className={glassButton + ' ' + (timelinePaused ? 'ring-2 ring-green-400' : 'ring-2 ring-yellow-400')}
          >
            {timelinePaused ? '▶️ Resume' : '⏸️ Pause'}
          </button>
          <button
            onClick={() => setShowFilters(f => !f)}
            className={glassButton + (showFilters ? ' ring-2 ring-cyan-400' : '')}
            title="Filter Events"
          >
            <FilterIcon className="inline w-4 h-4 mr-1" /> Filter
          </button>
          <button
            onClick={exportEvents}
            className={glassButton}
            title="Export Events"
          >
            <Download className="inline w-4 h-4 mr-1" /> Export
          </button>
          <div className="flex items-center space-x-2 ml-4">
            <button
              onClick={() => setTimelineZoom(Math.max(0.1, timelineZoom - 0.5))}
              className={glassButton}
            >
              ➖
            </button>
            <span className="text-cyan-300 text-sm min-w-[60px] text-center">
              {timelineZoom.toFixed(1)}x
            </span>
            <button
              onClick={() => setTimelineZoom(Math.min(10, timelineZoom + 0.5))}
              className={glassButton}
            >
              ➕
            </button>
          </div>
        </div>
      </div>
      {/* Filter UI */}
      <AnimatePresence>
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25 }}
            className="mb-4 p-4 glass rounded-lg border border-cyan-400/20 flex flex-wrap gap-2"
          >
            {eventTypesArray.map((type: EventTypeKey) => (
              <button
                key={type}
                className={`px-3 py-1 rounded-full font-mono text-xs transition-all border ${timelineEventTypeFilters.includes(type) ? 'bg-cyan-500/20 text-cyan-300 border-cyan-400' : 'bg-black/30 text-gray-400 border-gray-700 hover:bg-cyan-500/10'}`}
                onClick={() => {
                  if (timelineEventTypeFilters.includes(type)) {
                    setTimelineEventTypeFilters(timelineEventTypeFilters.filter(t => t !== type as EventTypeKey));
                  } else {
                    setTimelineEventTypeFilters([...timelineEventTypeFilters, type as EventTypeKey]);
                  }
                }}
              >
                <span className="inline-block w-2 h-2 rounded-full mr-2" style={{ background: eventTypes[type].color }} />
                {eventTypes[type].label}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
      {/* Canvas with framer-motion zoom */}
      <motion.div
        animate={{ scale: timelineZoom }}
        transition={{ type: 'spring', stiffness: 120, damping: 18 }}
        className="w-full h-auto"
        style={{ overflow: 'visible' }}
      >
        <canvas
          ref={canvasRef}
          width={1000}
          height={400}
          className="w-full h-auto bg-transparent rounded-lg border border-purple-500/20 cursor-pointer"
          onClick={handleCanvasClick}
        />
      </motion.div>
      {/* Virtualized Event List Panel */}
      <div className="mt-6">
        <h4 className="text-lg font-bold text-cyan-300 mb-2">Event List</h4>
        <div className="glass rounded-lg border border-cyan-400/20 max-h-72 overflow-auto">
          <List
            height={288}
            itemCount={visibleEvents.length}
            itemSize={56}
            width={"100%"}
            onItemsRendered={({ visibleStartIndex }: { visibleStartIndex: number }) => {
              if (visibleStartIndex === 0 && visibleEvents.length < filteredEvents.length) {
                handleLoadMore();
              }
            }}
          >
            {renderEventRow}
          </List>
        </div>
      </div>
      {/* Selected Event Details */}
      <AnimatePresence>
        {selectedEvent && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="mt-4 p-4 glass rounded-lg border border-cyan-400/40"
          >
            <h4 className="text-lg font-bold text-cyan-300 mb-2">Event Details</h4>
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
                <pre className="mt-1 text-xs text-gray-300 font-mono bg-black/60 p-2 rounded overflow-auto">
                  {JSON.stringify(selectedEvent.data, null, 2)}
                </pre>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2 text-xs">
        {Object.entries(eventTypes).map(([type, config]) => (
          <div key={type} className="flex items-center space-x-2 p-2 glass rounded border border-purple-500/20">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: config.color, boxShadow: `0 0 8px 2px ${config.color}` }}
            />
            <span className="text-gray-300">{config.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProcessTimelineVisualizer; 