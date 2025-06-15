import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { format } from 'date-fns';
import {
  Filter,
  Search,
  Download,
  X,
  Play,
  Pause,
  AlertTriangle,
  Brain,
  Sparkles,
  RefreshCw,
  LineChart,
  Link as LinkIcon,
  Clock,
  ChevronRight
} from 'lucide-react';
import '../styles/EventStream.css';
import { FixedSizeList as List, ListChildComponentProps } from 'react-window';
import debounce from 'lodash.debounce';

// Event interface
type Event = {
  id: string;
  type: string;
  timestamp: Date;
  description: string;
  source: string;
  details?: string;
  causedBy?: string;
  metrics?: Record<string, number>;
  impact?: { level: string; description?: string };
};

// Event type configurations
const EVENT_TYPES = {
  STATE_TRANSITION: {
    name: 'State Transition',
    color: '#3498db',
    bgColor: 'rgba(52, 152, 219, 0.1)',
    icon: RefreshCw
  },
  PATTERN_DETECTION: {
    name: 'Pattern Detection',
    color: '#9b59b6',
    bgColor: 'rgba(155, 89, 182, 0.1)',
    icon: LineChart
  },
  SPONTANEOUS_THOUGHT: {
    name: 'Spontaneous Thought',
    color: '#2ecc71',
    bgColor: 'rgba(46, 204, 113, 0.1)',
    icon: Brain
  },
  REBLOOM_EVENT: {
    name: 'Rebloom Event',
    color: 'linear-gradient(45deg, #ff6b6b, #ffd93d, #6bcf7f, #4ecdc4, #9b59b6)',
    bgColor: 'rgba(255, 107, 107, 0.1)',
    icon: Sparkles,
    isGradient: true
  },
  ANOMALY: {
    name: 'Anomaly',
    color: '#e67e22',
    bgColor: 'rgba(230, 126, 34, 0.1)',
    icon: AlertTriangle
  },
  ERROR: {
    name: 'Error',
    color: '#e74c3c',
    bgColor: 'rgba(231, 76, 60, 0.1)',
    icon: X
  }
};

interface EventStreamProps {
  events?: Event[];
  onEventSelect?: (event: Event) => void;
}

const EventStream: React.FC<EventStreamProps> = ({ events = [], onEventSelect }) => {
  const [selectedTypes, setSelectedTypes] = useState<Set<string>>(new Set(Object.keys(EVENT_TYPES)));
  const [searchTerm, setSearchTerm] = useState('');
  const [timeRange, setTimeRange] = useState<{ start: Date | null; end: Date | null }>({ start: null, end: null });
  const [isPaused, setIsPaused] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [showFilters, setShowFilters] = useState(false);
  const [causalLinks, setCausalLinks] = useState<Map<string, string[]>>(new Map());
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('');
  
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const eventRefs = useRef<Map<string, HTMLDivElement | null>>(new Map());
  const shouldAutoScroll = useRef(true);

  // Event handlers defined early to avoid hoisting issues
  const handleEventSelect = useCallback((event: Event) => {
    setSelectedEvent(event);
    if (onEventSelect) {
      onEventSelect(event);
    }
  }, [onEventSelect]);

  // Debounce search term
  const debouncedSetSearchTerm = useMemo(() => debounce(setDebouncedSearchTerm, 200), []);
  useEffect(() => {
    debouncedSetSearchTerm(searchTerm);
    return () => debouncedSetSearchTerm.cancel();
  }, [searchTerm, debouncedSetSearchTerm]);

  // Memoize filtered events
  const filteredEvents = useMemo(() => {
    let filtered = events;
    filtered = filtered.filter(event => selectedTypes.has(event.type));
    if (debouncedSearchTerm) {
      const term = debouncedSearchTerm.toLowerCase();
      filtered = filtered.filter(event => 
        event.description.toLowerCase().includes(term) ||
        event.source.toLowerCase().includes(term) ||
        event.details?.toLowerCase().includes(term)
      );
    }
    if (timeRange.start || timeRange.end) {
      filtered = filtered.filter(event => {
        const eventTime = new Date(event.timestamp);
        return (!timeRange.start || eventTime >= timeRange.start) &&
               (!timeRange.end || eventTime <= timeRange.end);
      });
    }
    return filtered;
  }, [events, selectedTypes, debouncedSearchTerm, timeRange]);

  // Render event item
  const renderEvent = useCallback((event: Event, index: number) => {
    const typeConfig = EVENT_TYPES[event.type as keyof typeof EVENT_TYPES];
    if (!typeConfig) return null;
    
    const Icon = typeConfig.icon;
    const hasChildren = causalLinks.has(event.id);
    const isGradient = 'isGradient' in typeConfig ? typeConfig.isGradient : false;
    
    return (
      <div
        key={event.id}
        ref={el => eventRefs.current.set(event.id, el)}
        className={`event-item ${selectedEvent?.id === event.id ? 'selected' : ''}`}
        style={{ 
          borderLeftColor: isGradient ? 'transparent' : typeConfig.color,
          borderImage: isGradient ? typeConfig.color : 'none',
          borderImageSlice: isGradient ? 1 : 'initial'
        }}
        onClick={() => handleEventSelect(event)}
      >
        <div className="event-header">
          <div className="event-time">
            <Clock className="time-icon" />
            {format(new Date(event.timestamp), 'HH:mm:ss.SSS')}
          </div>
          <div 
            className="event-type" 
            style={{ 
              color: isGradient ? 'transparent' : typeConfig.color,
              background: isGradient ? typeConfig.color : 'none',
              backgroundClip: isGradient ? 'text' : 'initial',
              WebkitBackgroundClip: isGradient ? 'text' : 'initial'
            }}
          >
            <Icon className="type-icon" />
            {typeConfig.name}
          </div>
        </div>
        
        <div className="event-body">
          <div className="event-source">{event.source}</div>
          <div className="event-description">{event.description}</div>
          
          {event.metrics && (
            <div className="event-metrics">
              {Object.entries(event.metrics).map(([key, value]) => (
                <span key={key} className="metric">
                  {key}: {typeof value === 'number' ? value.toFixed(3) : value}
                </span>
              ))}
            </div>
          )}
        </div>
        
        {event.causedBy && (
          <div className="event-causal-link">
            <LinkIcon className="link-icon" />
            Caused by: {event.causedBy}
          </div>
        )}
        
        {hasChildren && causalLinks.get(event.id) && (
          <div className="event-has-effects">
            <ChevronRight className="effects-icon" />
            Triggers {causalLinks.get(event.id)!.length} event(s)
          </div>
        )}
      </div>
    );
  }, [selectedEvent, causalLinks, handleEventSelect]);

  // Memoize event item renderer
  const MemoEventItem = useMemo(() => React.memo(renderEvent), [renderEvent]);

  // Virtualized list row renderer
  const Row = useCallback(({ index, style }: ListChildComponentProps) => {
    const event = filteredEvents[index];
    return (
      <div style={style}>
        {MemoEventItem(event, index)}
      </div>
    );
  }, [filteredEvents, MemoEventItem]);

  // Process events and build causal links
  useEffect(() => {
    const links = new Map();
    const eventMap = new Map();
    
    events.forEach(event => {
      eventMap.set(event.id, event);
      if (event.causedBy) {
        if (!links.has(event.causedBy)) {
          links.set(event.causedBy, []);
        }
        links.get(event.causedBy).push(event.id);
      }
    });
    
    setCausalLinks(links);
  }, [events]);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    if (!isPaused && shouldAutoScroll.current && scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [filteredEvents, isPaused]);

  // Handle mouse enter/leave for auto-scroll
  const handleMouseEnter = () => {
    shouldAutoScroll.current = false;
  };

  const handleMouseLeave = () => {
    if (!isPaused) {
      shouldAutoScroll.current = true;
    }
  };

  // Toggle event type filter
  const toggleEventType = (type) => {
    const newTypes = new Set(selectedTypes);
    if (newTypes.has(type)) {
      newTypes.delete(type);
    } else {
      newTypes.add(type);
    }
    setSelectedTypes(newTypes);
  };

  // Export events to file
  const exportEvents = () => {
    const dataStr = JSON.stringify(filteredEvents, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `events_${format(new Date(), 'yyyyMMdd_HHmmss')}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  // Get causal chain for an event
  const getCausalChain = (event) => {
    const chain = [];
    let current = event;
    
    // Trace back to root cause
    while (current && current.causedBy) {
      const parent = events.find(e => e.id === current.causedBy);
      if (parent) {
        chain.unshift(parent);
        current = parent;
      } else {
        break;
      }
    }
    
    // Add the selected event
    chain.push(event);
    
    // Trace forward to effects
    const addEffects = (eventId) => {
      const effects = causalLinks.get(eventId) || [];
      effects.forEach(effectId => {
        const effectEvent = events.find(e => e.id === effectId);
        if (effectEvent && !chain.includes(effectEvent)) {
          chain.push(effectEvent);
          addEffects(effectId);
        }
      });
    };
    
    addEffects(event.id);
    
    return chain;
  };

  // Render event details panel
  const renderEventDetails = () => {
    if (!selectedEvent) return null;
    
    const chain = getCausalChain(selectedEvent);
    const typeConfig = EVENT_TYPES[selectedEvent.type];
    
    return (
      <div className="event-details-panel">
        <div className="details-header">
          <h3>Event Details</h3>
          <button 
            className="close-button"
            onClick={() => setSelectedEvent(null)}
          >
            <X />
          </button>
        </div>
        
        <div className="details-content">
          <div className="detail-section">
            <h4>Basic Information</h4>
            <div className="detail-row">
              <span className="detail-label">ID:</span>
              <span className="detail-value">{selectedEvent.id}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Type:</span>
              <span 
                className="detail-value"
                style={{ color: typeConfig.isGradient ? 'inherit' : typeConfig.color }}
              >
                {typeConfig.name}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Time:</span>
              <span className="detail-value">
                {format(new Date(selectedEvent.timestamp), 'yyyy-MM-dd HH:mm:ss.SSS')}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Source:</span>
              <span className="detail-value">{selectedEvent.source}</span>
            </div>
          </div>
          
          {selectedEvent.details && (
            <div className="detail-section">
              <h4>Additional Details</h4>
              <div className="detail-text">{selectedEvent.details}</div>
            </div>
          )}
          
          {selectedEvent.metrics && (
            <div className="detail-section">
              <h4>Metrics at Time</h4>
              <div className="metrics-grid">
                {Object.entries(selectedEvent.metrics).map(([key, value]) => (
                  <div key={key} className="metric-item">
                    <span className="metric-label">{key}:</span>
                    <span className="metric-value">
                      {typeof value === 'number' ? value.toFixed(3) : value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {selectedEvent.impact && (
            <div className="detail-section">
              <h4>Impact Assessment</h4>
              <div className="impact-level" data-level={selectedEvent.impact.level}>
                Level: {selectedEvent.impact.level}
              </div>
              {selectedEvent.impact.description && (
                <div className="impact-description">
                  {selectedEvent.impact.description}
                </div>
              )}
            </div>
          )}
          
          <div className="detail-section">
            <h4>Causal Chain ({chain.length} events)</h4>
            <div className="causal-chain">
              {chain.map((event, index) => {
                const eventType = EVENT_TYPES[event.type];
                const isSelected = event.id === selectedEvent.id;
                
                return (
                  <div 
                    key={event.id}
                    className={`chain-event ${isSelected ? 'selected' : ''}`}
                    onClick={() => selectEvent(event)}
                  >
                    {index > 0 && <div className="chain-connector" />}
                    <div className="chain-event-content">
                      <div 
                        className="chain-event-type"
                        style={{ color: eventType.isGradient ? 'inherit' : eventType.color }}
                      >
                        {eventType.name}
                      </div>
                      <div className="chain-event-desc">{event.description}</div>
                      <div className="chain-event-time">
                        {format(new Date(event.timestamp), 'HH:mm:ss.SSS')}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="event-stream-container">
      <div className="event-stream-header">
        <h2>Event Stream</h2>
        <div className="header-controls">
          <button 
            className={`control-button ${showFilters ? 'active' : ''}`}
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter />
          </button>
          <button 
            className={`control-button ${isPaused ? 'active' : ''}`}
            onClick={() => setIsPaused(!isPaused)}
          >
            {isPaused ? <Play /> : <Pause />}
          </button>
          <button className="control-button" onClick={exportEvents}>
            <Download />
          </button>
        </div>
      </div>
      
      {showFilters && (
        <div className="filters-panel">
          <div className="filter-section">
            <h4>Event Types</h4>
            <div className="event-type-filters">
              {Object.entries(EVENT_TYPES).map(([key, config]) => (
                <label key={key} className="type-filter">
                  <input
                    type="checkbox"
                    checked={selectedTypes.has(key)}
                    onChange={() => toggleEventType(key)}
                  />
                  <span 
                    className="type-label"
                    style={{ 
                      color: config.isGradient ? 'inherit' : config.color,
                      background: config.isGradient ? config.color : 'none',
                      backgroundClip: config.isGradient ? 'text' : 'initial',
                      WebkitBackgroundClip: config.isGradient ? 'text' : 'initial'
                    }}
                  >
                    {config.name}
                  </span>
                </label>
              ))}
            </div>
          </div>
          
          <div className="filter-section">
            <h4>Search</h4>
            <div className="search-input">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Search events..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          <div className="filter-section">
            <h4>Time Range</h4>
            <div className="time-range-inputs">
              <input
                type="datetime-local"
                value={timeRange.start ? format(timeRange.start, "yyyy-MM-dd'T'HH:mm") : ''}
                onChange={(e) => setTimeRange({
                  ...timeRange,
                  start: e.target.value ? new Date(e.target.value) : null
                })}
              />
              <span>to</span>
              <input
                type="datetime-local"
                value={timeRange.end ? format(timeRange.end, "yyyy-MM-dd'T'HH:mm") : ''}
                onChange={(e) => setTimeRange({
                  ...timeRange,
                  end: e.target.value ? new Date(e.target.value) : null
                })}
              />
            </div>
          </div>
        </div>
      )}
      
      <div className="event-stream-body">
        <div 
          className="events-container"
          ref={scrollContainerRef}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >
          {filteredEvents.length === 0 ? (
            <div className="no-events">
              No events match the current filters
            </div>
          ) : (
            <List
              height={400}
              itemCount={filteredEvents.length}
              itemSize={80}
              width={"100%"}
            >
              {Row}
            </List>
          )}
        </div>
        
        {selectedEvent && renderEventDetails()}
      </div>
      
      <div className="event-stream-footer">
        <div className="event-count">
          {filteredEvents.length} of {events.length} events
        </div>
        <div className="stream-status">
          {isPaused ? 'Paused' : 'Live'}
        </div>
      </div>
    </div>
  );
};

export default EventStream; 