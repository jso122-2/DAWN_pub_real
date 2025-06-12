// src/components/eventBus.js
// Merged EventBus: supports both class-based and EventTarget-based usage

class EventBus {
  constructor() {
    this.events = {};
    this.eventTarget = new EventTarget();
  }
  
  on(event, callback) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(callback);
    // Also add as EventTarget listener for compatibility
    this.eventTarget.addEventListener(event, (e) => callback(e.detail));
  }
  
  emit(event, data) {
    // Class-based callbacks
    if (this.events[event]) {
      this.events[event].forEach(callback => callback(data));
    }
    // EventTarget-based
    this.eventTarget.dispatchEvent(new CustomEvent(event, { detail: data }));
  }
  
  // For compatibility with addEventListener
  addEventListener(event, callback) {
    this.eventTarget.addEventListener(event, callback);
  }
  
  // For compatibility with removeEventListener
  removeEventListener(event, callback) {
    this.eventTarget.removeEventListener(event, callback);
  }
}

const eventBus = new EventBus();

export const emitPrediction = (data) => {
  eventBus.emit('prediction', data);
};

export default eventBus; 