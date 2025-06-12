import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Howl } from 'howler';
import { useModulationStore } from '../../state/modulation';

interface SliderProps {
  label: string;
  value: number;
  onChange: (value: number) => void;
  color: string;
  id: string;
}

// Initialize sound effects
const sounds = {
  hover: new Howl({
    src: ['/sounds/hover.mp3', '/sounds/hover.ogg'],
    volume: 0.2,
    sprite: {
      hover: [0, 100]
    }
  }),
  change: new Howl({
    src: ['/sounds/slide.mp3', '/sounds/slide.ogg'],
    volume: 0.15,
    sprite: {
      slide: [0, 50]
    }
  })
};

const ModulationSlider: React.FC<SliderProps> = ({ label, value, onChange, color, id }) => {
  const [isPulsing, setIsPulsing] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const sliderRef = useRef<HTMLInputElement>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = parseInt(e.target.value);
    onChange(newValue);
    
    // Trigger haptic pulse effect
    setIsPulsing(true);
    setTimeout(() => setIsPulsing(false), 200);
    
    // Play sound
    if (sounds.change.state() === 'loaded') {
      sounds.change.play('slide');
    }
  };

  const handleHover = () => {
    if (sounds.hover.state() === 'loaded') {
      sounds.hover.play('hover');
    }
  };

  return (
    <div className="relative group">
      <label 
        htmlFor={id}
        className="block text-sm font-medium text-gray-300 mb-2"
      >
        {label}
        <span className="ml-2 text-xs text-gray-500">{value}%</span>
      </label>
      
      <div className="relative">
        <input
          ref={sliderRef}
          id={id}
          type="range"
          min="0"
          max="100"
          value={value}
          onChange={handleChange}
          onMouseEnter={handleHover}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          className={`
            w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer
            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900
            ${isFocused ? 'ring-2' : ''}
            slider-thumb
          `}
          style={{
            background: `linear-gradient(to right, ${color} 0%, ${color} ${value}%, #374151 ${value}%, #374151 100%)`,
            boxShadow: isPulsing ? `0 0 20px ${color}` : 'none',
            transition: 'box-shadow 0.2s ease-out',
          }}
          aria-label={`${label} slider`}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={value}
        />
        
        {/* Glow effect on track */}
        <div
          className={`absolute inset-0 rounded-lg pointer-events-none transition-opacity duration-200 ${
            isPulsing ? 'opacity-100' : 'opacity-0'
          }`}
          style={{
            background: `radial-gradient(circle at ${value}% 50%, ${color}40 0%, transparent 70%)`,
            filter: 'blur(8px)',
          }}
        />
      </div>
    </div>
  );
};

const ModulationConsole: React.FC = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [isDragging, setIsDragging] = useState(false);
  const [position, setPosition] = useState({ x: 100, y: 100 });
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const consoleRef = useRef<HTMLDivElement>(null);
  const inactivityTimerRef = useRef<ReturnType<typeof setTimeout>>();
  
  const { mood, pulse, noiseInjection, setMood, setPulse, setNoiseInjection, resetToDefaults } = useModulationStore();

  // Auto-hide functionality
  const resetInactivityTimer = useCallback(() => {
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
    }
    setIsVisible(true);
    inactivityTimerRef.current = setTimeout(() => {
      setIsVisible(false);
    }, 15000);
  }, []);

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'M') {
        setIsVisible(prev => !prev);
        resetInactivityTimer();
      }
      
      // Reset with Ctrl+R when console is focused
      if (e.ctrlKey && e.key === 'r' && consoleRef.current?.contains(document.activeElement)) {
        e.preventDefault();
        resetToDefaults();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [resetInactivityTimer, resetToDefaults]);

  // Mouse activity detection
  useEffect(() => {
    const handleActivity = () => resetInactivityTimer();
    
    if (consoleRef.current) {
      consoleRef.current.addEventListener('mouseenter', handleActivity);
      consoleRef.current.addEventListener('mousemove', handleActivity);
      consoleRef.current.addEventListener('focus', handleActivity, true);
    }

    return () => {
      if (consoleRef.current) {
        consoleRef.current.removeEventListener('mouseenter', handleActivity);
        consoleRef.current.removeEventListener('mousemove', handleActivity);
        consoleRef.current.removeEventListener('focus', handleActivity, true);
      }
    };
  }, [resetInactivityTimer]);

  // Initialize timer
  useEffect(() => {
    resetInactivityTimer();
    return () => {
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
    };
  }, [resetInactivityTimer]);

  // Dragging functionality
  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('input')) return;
    
    setIsDragging(true);
    const rect = consoleRef.current?.getBoundingClientRect();
    if (rect) {
      setDragOffset({
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
      });
    }
  };

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      setPosition({
        x: e.clientX - dragOffset.x,
        y: e.clientY - dragOffset.y
      });
    };

    const handleMouseUp = () => setIsDragging(false);

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  return (
    <>
      <style>{`
        .slider-thumb::-webkit-slider-thumb {
          appearance: none;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
          transition: all 0.2s ease;
        }
        
        .slider-thumb::-webkit-slider-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
        }
        
        .slider-thumb::-moz-range-thumb {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: white;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
          transition: all 0.2s ease;
        }
        
        .slider-thumb::-moz-range-thumb:hover {
          transform: scale(1.2);
          box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
        }
      `}</style>
      
      <div
        ref={consoleRef}
        className={`fixed z-50 transition-all duration-300 ${
          isVisible ? 'opacity-100 scale-100' : 'opacity-0 scale-95 pointer-events-none'
        }`}
        style={{
          left: `${position.x}px`,
          top: `${position.y}px`,
          cursor: isDragging ? 'grabbing' : 'grab',
        }}
        onMouseDown={handleMouseDown}
        role="dialog"
        aria-label="Modulation Console"
      >
        <div className="relative bg-gray-900/60 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-700/50 p-6 min-w-[320px]">
          {/* Glassmorphic effect layers */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-2xl" />
          <div className="absolute inset-0 backdrop-blur-3xl rounded-2xl" />
          
          {/* Content */}
          <div className="relative">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-100">Modulation Console</h3>
              <button
                onClick={() => setIsVisible(false)}
                className="text-gray-400 hover:text-gray-200 transition-colors p-1 rounded-lg hover:bg-gray-800/50"
                aria-label="Close console"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="space-y-6">
              <ModulationSlider
                id="mood-slider"
                label="Mood"
                value={mood}
                onChange={setMood}
                color="#10b981"
              />
              
              <ModulationSlider
                id="pulse-slider"
                label="Pulse"
                value={pulse}
                onChange={setPulse}
                color="#3b82f6"
              />
              
              <ModulationSlider
                id="noise-slider"
                label="Noise Injection"
                value={noiseInjection}
                onChange={setNoiseInjection}
                color="#f59e0b"
              />
            </div>
            
            <div className="mt-6 flex items-center justify-between">
              <button
                onClick={resetToDefaults}
                className="text-sm text-gray-400 hover:text-gray-200 transition-colors"
                aria-label="Reset to defaults"
              >
                Reset (Ctrl+R)
              </button>
              
              <div className="text-xs text-gray-500">
                Auto-hide in 15s • Ctrl+Shift+M to toggle
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ModulationConsole; 