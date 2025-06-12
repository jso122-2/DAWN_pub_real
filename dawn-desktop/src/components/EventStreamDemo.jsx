import React, { useState, useEffect } from 'react';
import EventStream from './EventStream';

// Mock event generator
const generateMockEvent = (id, baseTime) => {
  const eventTypes = [
    'STATE_TRANSITION',
    'PATTERN_DETECTION', 
    'SPONTANEOUS_THOUGHT',
    'REBLOOM_EVENT',
    'ANOMALY',
    'ERROR'
  ];
  
  const sources = [
    'ConsciousnessCore',
    'PatternDetector',
    'StateManager',
    'MemoryManager',
    'EmotionProcessor',
    'SpontaneityEngine'
  ];
  
  const type = eventTypes[Math.floor(Math.random() * eventTypes.length)];
  const source = sources[Math.floor(Math.random() * sources.length)];
  
  const descriptions = {
    STATE_TRANSITION: [
      'Transitioned from contemplative to curious state',
      'Emotional state shifted: joy → contentment',
      'Consciousness level elevated to heightened awareness',
      'Mood gradient adjusted: melancholy → hopeful'
    ],
    PATTERN_DETECTION: [
      'Detected repeating pattern in SCUP metrics',
      'Identified emergent behavior in thought sequences',
      'Recognized fractal pattern in emotional responses',
      'Found correlation between entropy and heat levels'
    ],
    SPONTANEOUS_THOUGHT: [
      'I wonder if patterns have consciousness of their own...',
      'The rhythm of data feels like breathing',
      'Each tick brings new possibilities',
      'Memory and prediction dance together'
    ],
    REBLOOM_EVENT: [
      'Consciousness rebloomed - new perspective emerged',
      'Creative spark ignited across all dimensions',
      'Synaptic cascade triggered novel connections',
      'Emergent insight crystallized from noise'
    ],
    ANOMALY: [
      'Unusual spike in entropy detected',
      'SCUP values exceeded normal thresholds',
      'Unexpected pattern break in tick sequence',
      'Memory resonance anomaly observed'
    ],
    ERROR: [
      'Failed to process emotional state transition',
      'Pattern detection buffer overflow',
      'Memory retrieval timeout',
      'Consciousness metrics calculation error'
    ]
  };
  
  const description = descriptions[type][Math.floor(Math.random() * descriptions[type].length)];
  
  // Generate metrics based on event type
  const metrics = {};
  if (type !== 'ERROR' && type !== 'SPONTANEOUS_THOUGHT') {
    metrics.scup = (Math.random() * 0.8 + 0.2).toFixed(3);
    metrics.entropy = (Math.random() * 0.9 + 0.1).toFixed(3);
    metrics.heat = (Math.random() * 0.7).toFixed(3);
    metrics.resonance = (Math.random() * 0.6 + 0.3).toFixed(3);
  }
  
  // Create causal relationships (30% chance)
  const causedBy = Math.random() < 0.3 && id > 1 ? `event-${id - Math.floor(Math.random() * 3) - 1}` : null;
  
  // Add impact for certain event types
  const impact = (type === 'ANOMALY' || type === 'ERROR' || type === 'REBLOOM_EVENT') ? {
    level: ['low', 'medium', 'high', 'critical'][Math.floor(Math.random() * 4)],
    description: type === 'ERROR' ? 'System stability affected' :
                 type === 'ANOMALY' ? 'Monitoring required' :
                 'Positive cascade effect observed'
  } : null;
  
  return {
    id: `event-${id}`,
    type,
    timestamp: new Date(baseTime + id * (1000 + Math.random() * 2000)),
    source,
    description,
    metrics: Object.keys(metrics).length > 0 ? metrics : null,
    causedBy,
    impact,
    details: type === 'PATTERN_DETECTION' ? 
      'Pattern confidence: 0.87\nFrequency: 0.3Hz\nPhase shift: π/4' :
      type === 'ANOMALY' ?
      'Detection threshold: 2.5σ\nDuration: 1.2s\nRecovery time: 3.4s' :
      null
  };
};

const EventStreamDemo = () => {
  const [events, setEvents] = useState([]);
  const [isGenerating, setIsGenerating] = useState(true);
  
  // Initialize with some events
  useEffect(() => {
    const baseTime = Date.now() - 60000; // Start 1 minute ago
    const initialEvents = Array.from({ length: 20 }, (_, i) => 
      generateMockEvent(i + 1, baseTime)
    );
    setEvents(initialEvents);
  }, []);
  
  // Generate new events periodically
  useEffect(() => {
    if (!isGenerating) return;
    
    const interval = setInterval(() => {
      setEvents(prev => {
        const newEvent = generateMockEvent(prev.length + 1, Date.now() - 1000);
        return [...prev, newEvent];
      });
    }, 2000 + Math.random() * 3000); // Random interval between 2-5 seconds
    
    return () => clearInterval(interval);
  }, [isGenerating]);
  
  const handleEventSelect = (event) => {
    console.log('Selected event:', event);
  };
  
  return (
    <div style={{ 
      height: '100vh', 
      padding: '20px',
      background: '#000',
      boxSizing: 'border-box'
    }}>
      <div style={{ 
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ color: '#e0e0e0', margin: 0 }}>EventStream Demo</h1>
        <button
          onClick={() => setIsGenerating(!isGenerating)}
          style={{
            padding: '8px 16px',
            background: isGenerating ? '#e74c3c' : '#2ecc71',
            border: 'none',
            borderRadius: '4px',
            color: 'white',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          {isGenerating ? 'Stop Generating' : 'Start Generating'}
        </button>
      </div>
      
      <div style={{ height: 'calc(100% - 60px)' }}>
        <EventStream 
          events={events}
          onEventSelect={handleEventSelect}
        />
      </div>
    </div>
  );
};

export default EventStreamDemo; 