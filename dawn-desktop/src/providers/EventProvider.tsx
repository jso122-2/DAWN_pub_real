import React, { createContext, useContext } from 'react';
import { EventEmitter } from '../lib/EventEmitter';

const EventContext = createContext<EventEmitter | null>(null);

export const EventProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const emitter = new EventEmitter();
  
  return (
    <EventContext.Provider value={emitter}>
      {children}
    </EventContext.Provider>
  );
};

export const useEventEmitter = () => {
  const emitter = useContext(EventContext);
  if (!emitter) {
    throw new Error('useEventEmitter must be used within EventProvider');
  }
  return emitter;
}; 