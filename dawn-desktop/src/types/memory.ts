export type EventType = 'mood' | 'system' | 'override' | 'error';
export type EventSeverity = 'info' | 'warning' | 'critical';

export interface MemoryEvent {
  id: string;
  timestamp: Date;
  source: string;
  type: EventType;
  severity: EventSeverity;
  message: string;
  emotionalWeight?: number; // 0-1
  metadata?: Record<string, any>;
} 