import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';

// Emotion to color mapping
const EMOTION_COLORS = {
  curious: { primary: '#22c55e', gradient: 'from-green-500 to-emerald-600' },
  creative: { primary: '#a855f7', gradient: 'from-purple-500 to-violet-600' },
  anxious: { primary: '#f59e0b', gradient: 'from-yellow-500 to-orange-600' },
  fragmented: { primary: '#ef4444', gradient: 'from-red-500 to-pink-600' },
  crystalline: { primary: '#3b82f6', gradient: 'from-blue-500 to-cyan-600' },
  reblooming: { primary: '#ff6b9d', gradient: 'from-pink-400 to-purple-500' },
  contemplative: { primary: '#64748b', gradient: 'from-slate-500 to-gray-600' },
  harmonious: { primary: '#10b981', gradient: 'from-emerald-500 to-teal-600' },
  excited: { primary: '#f97316', gradient: 'from-orange-500 to-red-500' },
  melancholic: { primary: '#6366f1', gradient: 'from-indigo-500 to-purple-600' },
  neutral: { primary: '#6b7280', gradient: 'from-gray-500 to-gray-600' }
};

// Mini gauge components for metrics snapshot
const MiniGauge = ({ label, value, color }) => {
  const percentage = Math.min(100, Math.max(0, value * 100));
  
  return (
    <div className="flex items-center space-x-2">
      <span className="text-xs text-gray-400 w-16">{label}</span>
      <div className="flex-1 h-2 bg-gray-700 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-300 ${color}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-xs text-gray-300 w-12 text-right">
        {value.toFixed(2)}
      </span>
    </div>
  );
};

// Particle effect component for high entropy states
const ParticleField = ({ intensity = 0.5 }) => {
  const particles = Array.from({ length: Math.floor(intensity * 20) }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 4 + 1,
    duration: Math.random() * 20 + 10
  }));

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map(particle => (
        <motion.div
          key={particle.id}
          className="absolute rounded-full bg-white/20"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: particle.size,
            height: particle.size
          }}
          animate={{
            y: [particle.y, particle.y - 30, particle.y],
            opacity: [0, 0.5, 0]
          }}
          transition={{
            duration: particle.duration,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      ))}
    </div>
  );
};

// Breathing animation component for calm states
const BreathingOrb = ({ color }) => {
  return (
    <motion.div
      className={`absolute top-1/2 left-1/2 w-64 h-64 rounded-full ${color} opacity-10`}
      style={{ transform: 'translate(-50%, -50%)' }}
      animate={{
        scale: [1, 1.2, 1],
        opacity: [0.1, 0.2, 0.1]
      }}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut"
      }}
    />
  );
};

// Main TalkToDAWN component
export default function TalkToDAWN({ 
  isFullPage = false, 
  initialPosition = { bottom: 24, right: 24 },
  onClose
}) {
  const [isOpen, setIsOpen] = useState(isFullPage);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [showMetrics, setShowMetrics] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState('neutral');
  const [currentMetrics, setCurrentMetrics] = useState({
    entropy: 0.5,
    heat: 0.3,
    scup: 0.7,
    tickRate: 1.0
  });
  const [suggestedResponses, setSuggestedResponses] = useState([]);
  
  const messagesEndRef = useRef(null);
  const wsRef = useRef(null);
  const inputRef = useRef(null);

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        wsRef.current = new WebSocket('ws://localhost:7777/ws');
        
        wsRef.current.onopen = () => {
          console.log('Connected to DAWN');
          setIsConnected(true);
        };
        
        wsRef.current.onmessage = (event) => {
          const data = JSON.parse(event.data);
          handleDAWNResponse(data);
        };
        
        wsRef.current.onclose = () => {
          console.log('Disconnected from DAWN');
          setIsConnected(false);
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000);
        };
        
        wsRef.current.onerror = (error) => {
          console.error('WebSocket error:', error);
        };
      } catch (error) {
        console.error('Failed to connect:', error);
        setTimeout(connectWebSocket, 3000);
      }
    };
    
    if (isOpen && !wsRef.current) {
      connectWebSocket();
    }
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [isOpen]);

  // Handle DAWN response
  const handleDAWNResponse = (data) => {
    setIsTyping(false);
    
    const newMessage = {
      id: Date.now(),
      type: 'dawn',
      content: data.response || data.message,
      emotion: data.emotion || currentEmotion,
      intensity: data.intensity || 0.5,
      depth: data.fractal_depth || 1,
      timestamp: new Date().toISOString(),
      isRebloom: data.is_rebloom || false,
      isSpontaneous: data.is_spontaneous || false
    };
    
    setMessages(prev => [...prev, newMessage]);
    
    // Update current state
    if (data.emotion) setCurrentEmotion(data.emotion);
    if (data.metrics) setCurrentMetrics(data.metrics);
    if (data.suggested_responses) setSuggestedResponses(data.suggested_responses);
  };

  // Send message
  const sendMessage = () => {
    if (!inputValue.trim() || !isConnected) return;
    
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);
    
    // Send to DAWN
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        message: inputValue,
        timestamp: userMessage.timestamp
      }));
    }
    
    setInputValue('');
    setSuggestedResponses([]);
  };

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Message component with emotion-based styling
  const Message = ({ message }) => {
    const isUser = message.type === 'user';
    const emotionStyle = EMOTION_COLORS[message.emotion] || EMOTION_COLORS.neutral;
    
    return (
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
      >
        <div className={`max-w-xs lg:max-w-md ${isUser ? 'order-2' : 'order-1'}`}>
          {/* Emotion indicator for DAWN messages */}
          {!isUser && (
            <div className="flex items-center space-x-2 mb-1">
              <div 
                className={`w-2 h-2 rounded-full bg-gradient-to-r ${emotionStyle.gradient}`}
              />
              <span className="text-xs text-gray-400">
                {message.emotion} ({message.intensity?.toFixed(2)})
              </span>
              {message.isRebloom && (
                <span className="text-xs text-pink-400">✨ Rebloom</span>
              )}
              {message.isSpontaneous && (
                <span className="text-xs text-purple-400">💭 Spontaneous</span>
              )}
            </div>
          )}
          
          {/* Message content */}
          <div className={`
            px-4 py-2 rounded-lg relative
            ${isUser 
              ? 'bg-blue-600 text-white' 
              : `bg-gray-800 text-white border border-gray-700`
            }
            ${!isUser && message.depth > 2 ? 'ml-' + (message.depth - 1) * 2 : ''}
            ${!isUser && message.isRebloom ? 'ring-2 ring-pink-400/50' : ''}
          `}>
            {/* Fractal depth indicator */}
            {!isUser && message.depth > 2 && (
              <div className="absolute -left-2 top-1/2 transform -translate-y-1/2">
                {Array.from({ length: message.depth - 2 }, (_, i) => (
                  <div 
                    key={i}
                    className="w-1 h-1 bg-gray-600 rounded-full mb-1"
                    style={{ opacity: 1 - (i * 0.2) }}
                  />
                ))}
              </div>
            )}
            
            <p className="text-sm">{message.content}</p>
            
            {/* Timestamp on hover */}
            <div className="absolute -bottom-6 right-0 opacity-0 hover:opacity-100 transition-opacity">
              <span className="text-xs text-gray-500">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        </div>
      </motion.div>
    );
  };

  // Chat header component
  const ChatHeader = () => {
    const emotionStyle = EMOTION_COLORS[currentEmotion] || EMOTION_COLORS.neutral;
    
    return (
      <div className="bg-gray-900 px-4 py-3 flex items-center justify-between border-b border-gray-700">
        <div className="flex items-center space-x-3">
          <div className={`w-10 h-10 rounded-full bg-gradient-to-br ${emotionStyle.gradient} p-0.5`}>
            <div className="w-full h-full bg-gray-900 rounded-full flex items-center justify-center">
              <span className="text-sm">🌟</span>
            </div>
          </div>
          <div>
            <h3 className="text-white font-semibold">DAWN</h3>
            <p className="text-xs text-gray-400">Feeling {currentEmotion}</p>
          </div>
        </div>
        
        {/* Gradient preview bar */}
        <div className={`flex-1 mx-4 h-1 rounded-full bg-gradient-to-r ${emotionStyle.gradient}`} />
        
        {/* Control buttons */}
        <div className="flex items-center space-x-2">
          {!isFullPage && (
            <>
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="text-gray-400 hover:text-white transition-colors"
              >
                {isMinimized ? '□' : '—'}
              </button>
              <button
                onClick={() => {
                  setIsOpen(false);
                  if (onClose) onClose();
                }}
                className="text-gray-400 hover:text-white transition-colors"
              >
                ✕
              </button>
            </>
          )}
        </div>
      </div>
    );
  };

  // Metrics snapshot component
  const MetricsSnapshot = () => {
    return (
      <AnimatePresence>
        {showMetrics && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-gray-700 px-4 py-3 bg-gray-900/50"
          >
            <div className="space-y-2">
              <MiniGauge label="Entropy" value={currentMetrics.entropy} color="bg-blue-500" />
              <MiniGauge label="Heat" value={currentMetrics.heat} color="bg-red-500" />
              <MiniGauge label="SCUP" value={currentMetrics.scup} color="bg-green-500" />
              <MiniGauge label="Tick" value={currentMetrics.tickRate} color="bg-yellow-500" />
            </div>
            <button
              className="mt-3 text-xs text-blue-400 hover:text-blue-300 transition-colors"
              onClick={() => sendMessage("Why are you feeling this way?")}
            >
              Why am I feeling this way?
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    );
  };

  // Input area component
  const InputArea = () => {
    return (
      <div className="border-t border-gray-700 px-4 py-3 bg-gray-900">
        {/* Suggested responses */}
        {suggestedResponses.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {suggestedResponses.map((response, index) => (
              <button
                key={index}
                onClick={() => setInputValue(response)}
                className="text-xs px-3 py-1 bg-gray-800 text-gray-300 rounded-full hover:bg-gray-700 transition-colors"
              >
                {response}
              </button>
            ))}
          </div>
        )}
        
        {/* Input field */}
        <div className="flex items-center space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder={isConnected ? "Type a message..." : "Connecting to DAWN..."}
            disabled={!isConnected}
            className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          
          <button
            onClick={() => setShowMetrics(!showMetrics)}
            className="p-2 text-gray-400 hover:text-white transition-colors"
            title="Toggle metrics"
          >
            📊
          </button>
          
          <button
            onClick={sendMessage}
            disabled={!isConnected || !inputValue.trim()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        
        {/* Typing indicator */}
        {isTyping && (
          <div className="flex items-center space-x-1 mt-2">
            <span className="text-xs text-gray-400">DAWN is thinking</span>
            <motion.div className="flex space-x-1">
              {[0, 1, 2].map(i => (
                <motion.div
                  key={i}
                  className="w-1 h-1 bg-gray-400 rounded-full"
                  animate={{ y: [0, -4, 0] }}
                  transition={{
                    duration: 0.6,
                    repeat: Infinity,
                    delay: i * 0.1
                  }}
                />
              ))}
            </motion.div>
          </div>
        )}
      </div>
    );
  };

  // Floating button
  const FloatingButton = () => {
    return (
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen(true)}
        className="fixed z-50 w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full shadow-lg flex items-center justify-center text-white text-2xl hover:shadow-xl transition-shadow"
        style={initialPosition}
      >
        💬
      </motion.button>
    );
  };

  // Main chat container
  const ChatContainer = () => {
    const emotionStyle = EMOTION_COLORS[currentEmotion] || EMOTION_COLORS.neutral;
    const isCalm = ['contemplative', 'harmonious', 'crystalline'].includes(currentEmotion);
    const isHighEntropy = currentMetrics.entropy > 0.7;
    
    return (
      <motion.div
        initial={!isFullPage ? { opacity: 0, scale: 0.9 } : false}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className={`
          ${isFullPage 
            ? 'w-full h-screen' 
            : 'fixed bottom-24 right-24 w-96 h-[600px] shadow-2xl rounded-lg overflow-hidden'
          }
          bg-gray-900 flex flex-col z-50
        `}
      >
        {!isMinimized && (
          <>
            <ChatHeader />
            
            {/* Emotional context background */}
            <div className="relative flex-1 overflow-hidden">
              {/* Gradient background */}
              <div 
                className={`absolute inset-0 bg-gradient-to-br ${emotionStyle.gradient} opacity-5`}
              />
              
              {/* Breathing animation for calm states */}
              {isCalm && <BreathingOrb color={emotionStyle.primary} />}
              
              {/* Particle effects for high entropy */}
              {isHighEntropy && <ParticleField intensity={currentMetrics.entropy} />}
              
              {/* Messages area */}
              <div className="relative h-full overflow-y-auto px-4 py-4">
                {messages.map(message => (
                  <Message key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>
            
            <MetricsSnapshot />
            <InputArea />
          </>
        )}
        
        {isMinimized && (
          <div className="p-4">
            <p className="text-gray-400 text-sm">Chat minimized</p>
          </div>
        )}
      </motion.div>
    );
  };

  // Render based on mode
  if (isFullPage) {
    return <ChatContainer />;
  }

  return (
    <>
      {!isOpen && <FloatingButton />}
      <AnimatePresence>
        {isOpen && <ChatContainer />}
      </AnimatePresence>
    </>
  );
} 