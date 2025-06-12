// Event types
export type EventType =
  | 'entropy:spike'
  | 'memory:overflow'
  | 'neural:pulse';

export interface EventPayloads {
  'entropy:spike': { value: number; timestamp: number };
  'memory:overflow': { used: number; total: number; timestamp: number };
  'neural:pulse': { intensity: number; region: string; timestamp: number };
}

export type Priority = 'critical' | 'normal' | 'low';

interface EventEnvelope<T extends EventType> {
  type: T;
  payload: EventPayloads[T];
  priority: Priority;
  timestamp: number;
  id: string;
}

interface Listener<T extends EventType = EventType> {
  (event: EventEnvelope<T>): void | Promise<void>;
  componentId?: string;
  rateLimit?: number; // ms
  lastCalled?: number;
}

class EventBus {
  private listeners: Map<EventType, Listener<EventType>[]> = new Map();
  private componentRegistry: Set<string> = new Set();
  private queues: Record<Priority, EventEnvelope<any>[]> = {
    critical: [],
    normal: [],
    low: [],
  };
  private deadLetterQueue: EventEnvelope<any>[] = [];
  private replayLog: EventEnvelope<any>[] = [];
  private processing = false;

  registerComponent(componentId: string) {
    this.componentRegistry.add(componentId);
  }

  unregisterComponent(componentId: string) {
    this.componentRegistry.delete(componentId);
  }

  on<T extends EventType>(type: T, listener: Listener<T>, componentId?: string, rateLimit?: number) {
    if (!this.listeners.has(type)) this.listeners.set(type, [] as Listener<EventType>[]);
    listener.componentId = componentId;
    listener.rateLimit = rateLimit;
    (this.listeners.get(type) as Listener<EventType>[]).push(listener as Listener<EventType>);
    if (componentId) this.registerComponent(componentId);
  }

  off<T extends EventType>(type: T, listener: Listener<T>) {
    if (!this.listeners.has(type)) return;
    this.listeners.set(
      type,
      this.listeners.get(type)!.filter(l => l !== listener)
    );
  }

  emit<T extends EventType>(type: T, payload: EventPayloads[T], priority: Priority = 'normal') {
    const envelope: EventEnvelope<T> = {
      type,
      payload,
      priority,
      timestamp: Date.now(),
      id: `${type}:${Date.now()}:${Math.random().toString(36).slice(2, 8)}`,
    };
    this.queues[priority].push(envelope);
    this.replayLog.push(envelope);
    this.process();
  }

  private async process() {
    if (this.processing) return;
    this.processing = true;
    try {
      for (const priority of ['critical', 'normal', 'low'] as Priority[]) {
        while (this.queues[priority].length > 0) {
          const event = this.queues[priority].shift()!;
          const listeners = this.listeners.get(event.type) || [];
          let delivered = false;
          for (const listener of listeners) {
            // Rate limiting
            const now = Date.now();
            if (listener.rateLimit && listener.lastCalled && now - listener.lastCalled < listener.rateLimit) {
              continue;
            }
            try {
              await listener(event);
              listener.lastCalled = now;
              delivered = true;
            } catch (err) {
              // Delivery failed
              this.deadLetterQueue.push(event);
            }
          }
          if (!delivered) {
            this.deadLetterQueue.push(event);
          }
        }
      }
    } finally {
      this.processing = false;
    }
  }

  getDeadLetters() {
    return this.deadLetterQueue;
  }

  getReplayLog() {
    return this.replayLog;
  }

  replayEvents(count: number = 10) {
    const toReplay = this.replayLog.slice(-count);
    for (const event of toReplay) {
      this.emit(event.type, event.payload, event.priority);
    }
  }
}

export const eventBus = new EventBus(); 