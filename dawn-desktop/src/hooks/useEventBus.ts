import { useEffect, useRef } from 'react';
import { eventBus, EventType, EventPayloads, Priority } from '../utils/eventBus';

export function useEventBus<T extends EventType>(
  type: T,
  handler: (event: { type: T; payload: EventPayloads[T]; priority: Priority; timestamp: number; id: string }) => void | Promise<void>,
  options?: { componentId?: string; rateLimit?: number }
) {
  const handlerRef = useRef(handler);
  handlerRef.current = handler;

  useEffect(() => {
    const wrappedHandler = (event: any) => handlerRef.current(event);
    eventBus.on(type, wrappedHandler, options?.componentId, options?.rateLimit);
    return () => {
      eventBus.off(type, wrappedHandler);
    };
  }, [type, options?.componentId, options?.rateLimit]);
} 