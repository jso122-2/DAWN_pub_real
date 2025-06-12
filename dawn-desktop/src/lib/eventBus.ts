// Enhanced event bus for React components

export enum EventTypes {
  TICK = 'tick',
  METRICS_UPDATE = 'metrics-update',
  ALERT = 'alert',
  PATTERN = 'pattern',
  ANOMALY = 'anomaly',
  PREDICTION = 'prediction',
  STATE_CHANGE = 'state-change',
  ERROR = 'error',
  THRESHOLD_EXCEEDED = 'threshold-exceeded',
  CONNECTION_STATUS = 'connection-status',
}

// Payload interfaces
export interface TickEvent {
  tick: number;
  timestamp: number;
}

export interface MetricsUpdateEvent {
  metrics: Record<string, number>;
  timestamp: number;
}

export interface AlertEvent {
  message: string;
  severity: 'info' | 'warning' | 'error';
  timestamp: number;
}

export interface PatternEvent {
  pattern: string;
  confidence: number;
  timestamp: number;
}

export interface AnomalyEvent {
  description: string;
  value: number;
  timestamp: number;
}

export interface PredictionEvent {
  message: string;
  probability: number;
  severity: 'low' | 'medium' | 'high';
  type: string;
}

export interface StateChangeEvent {
  from: string;
  to: string;
  timestamp: number;
}

export interface ErrorEvent {
  error: string;
  code?: number;
  timestamp: number;
}

export interface ThresholdExceededEvent {
  metric: string;
  value: number;
  threshold: number;
  timestamp: number;
}

export interface ConnectionStatusEvent {
  status: 'connected' | 'disconnected';
  timestamp: number;
}

// Event payload type map
export type EventPayloadMap = {
  [EventTypes.TICK]: TickEvent;
  [EventTypes.METRICS_UPDATE]: MetricsUpdateEvent;
  [EventTypes.ALERT]: AlertEvent;
  [EventTypes.PATTERN]: PatternEvent;
  [EventTypes.ANOMALY]: AnomalyEvent;
  [EventTypes.PREDICTION]: PredictionEvent;
  [EventTypes.STATE_CHANGE]: StateChangeEvent;
  [EventTypes.ERROR]: ErrorEvent;
  [EventTypes.THRESHOLD_EXCEEDED]: ThresholdExceededEvent;
  [EventTypes.CONNECTION_STATUS]: ConnectionStatusEvent;
};

const eventBus = new EventTarget();

// Typed emit function
export function emitEvent<T extends EventTypes>(type: T, payload: EventPayloadMap[T]) {
  eventBus.dispatchEvent(new CustomEvent(type, { detail: payload }));
}

// Individual emitters for convenience
export const emitTick = (payload: TickEvent) => emitEvent(EventTypes.TICK, payload);
export const emitMetricsUpdate = (payload: MetricsUpdateEvent) => emitEvent(EventTypes.METRICS_UPDATE, payload);
export const emitAlert = (payload: AlertEvent) => emitEvent(EventTypes.ALERT, payload);
export const emitPattern = (payload: PatternEvent) => emitEvent(EventTypes.PATTERN, payload);
export const emitAnomaly = (payload: AnomalyEvent) => emitEvent(EventTypes.ANOMALY, payload);
export const emitPrediction = (payload: PredictionEvent) => emitEvent(EventTypes.PREDICTION, payload);
export const emitStateChange = (payload: StateChangeEvent) => emitEvent(EventTypes.STATE_CHANGE, payload);
export const emitError = (payload: ErrorEvent) => emitEvent(EventTypes.ERROR, payload);
export const emitThresholdExceeded = (payload: ThresholdExceededEvent) => emitEvent(EventTypes.THRESHOLD_EXCEEDED, payload);
export const emitConnectionStatus = (payload: ConnectionStatusEvent) => emitEvent(EventTypes.CONNECTION_STATUS, payload);

export default eventBus; 