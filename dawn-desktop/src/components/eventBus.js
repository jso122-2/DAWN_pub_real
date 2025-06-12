// Enhanced event bus for React components
const eventBus = new EventTarget();

// Event types
export const EventTypes = {
  TICK: 'tick',
  METRICS_UPDATE: 'metrics-update',
  ALERT: 'alert',
  PATTERN: 'pattern',
  ANOMALY: 'anomaly',
  PREDICTION: 'prediction',
  STATE_CHANGE: 'state-change',
  ERROR: 'error',
  THRESHOLD_EXCEEDED: 'threshold-exceeded',
  CONNECTION_STATUS: 'connection-status'
};

// Utility functions for emitting events
export function emitTick(tickData) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.TICK, { detail: tickData }));
}

export function emitMetricsUpdate(metrics) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.METRICS_UPDATE, { detail: metrics }));
}

export function emitAlert(alert) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.ALERT, { detail: alert }));
}

export function emitPattern(pattern) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.PATTERN, { detail: pattern }));
}

export function emitAnomaly(anomaly) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.ANOMALY, { detail: anomaly }));
}

export function emitPrediction(prediction) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.PREDICTION, { detail: prediction }));
}

export function emitStateChange(state) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.STATE_CHANGE, { detail: state }));
}

export function emitError(error) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.ERROR, { detail: error }));
}

export function emitThresholdExceeded(data) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.THRESHOLD_EXCEEDED, { detail: data }));
}

export function emitConnectionStatus(status) {
  eventBus.dispatchEvent(new CustomEvent(EventTypes.CONNECTION_STATUS, { detail: status }));
}

export default eventBus; 