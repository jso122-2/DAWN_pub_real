// EventStream Component Type Definitions

export type EventType = 
  | 'STATE_TRANSITION'
  | 'PATTERN_DETECTION'
  | 'SPONTANEOUS_THOUGHT'
  | 'REBLOOM_EVENT'
  | 'ANOMALY'
  | 'ERROR';

export type ImpactLevel = 'low' | 'medium' | 'high' | 'critical';

export interface EventMetrics {
  scup?: number;
  entropy?: number;
  heat?: number;
  resonance?: number;
  tick_rate?: number;
  tick_count?: number;
  [key: string]: number | undefined;
}

export interface EventImpact {
  level: ImpactLevel;
  description: string;
}

export interface SystemEvent {
  // Unique identifier for the event
  id: string;
  
  // Type of event - determines color coding and icon
  type: EventType;
  
  // When the event occurred
  timestamp: Date | string | number;
  
  // Source system/component that generated the event
  source: string;
  
  // Human-readable description of what happened
  description: string;
  
  // Optional detailed information about the event
  details?: string;
  
  // System metrics at the time of the event
  metrics?: EventMetrics;
  
  // ID of the event that caused this one (for causal chains)
  causedBy?: string;
  
  // Impact assessment for significant events
  impact?: EventImpact;
}

export interface TimeRange {
  start: Date | null;
  end: Date | null;
}

export interface EventStreamProps {
  // Array of events to display
  events: SystemEvent[];
  
  // Callback when an event is selected for detailed view
  onEventSelect?: (event: SystemEvent) => void;
  
  // Optional: Control auto-scroll externally
  autoScroll?: boolean;
  
  // Optional: Initial filter state
  initialFilters?: {
    eventTypes?: EventType[];
    searchTerm?: string;
    timeRange?: TimeRange;
  };
}

export interface EventTypeConfig {
  name: string;
  color: string;
  bgColor: string;
  icon: React.ComponentType;
  isGradient?: boolean;
}

export interface CausalChainNode {
  event: SystemEvent;
  children: string[];
  parent?: string;
  depth: number;
} 