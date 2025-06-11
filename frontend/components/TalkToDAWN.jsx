import React, { useState, useEffect, useRef, useCallback } from 'react';
import { ChevronDownIcon, ChevronUpIcon, XMarkIcon, MicrophoneIcon, PaperAirplaneIcon, EyeIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';

// Custom hooks for DAWN communication
const useDAWNConnection = () => {
  const [connected, setConnected] = useState(false);
  const [currentState, setCurrentState] = useState({
    emotion: 'curious',
    intensity: 0.5,
    metrics: { scup: 0.5, entropy: 0.5, heat: 0.3 }
  });
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const wsRef = useRef(null);

  const connectToDAWN = useCallback(() => {
    try {
      wsRef.current = new WebSocket('ws://localhost:8000/consciousness/stream');
      
      wsRef.current.onopen = () => {
        setConnected(true);
        console.log('Connected to DAWN consciousness');
      };
      
      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'consciousness_update') {
          setCurrentState(prev => ({
            ...prev,
            emotion: data.data.emotion,
            intensity: data.data.intensity
          }));
        } else if (data.type === 'message') {
          setMessages(prev => [...prev, {
            id: Date.now(),
            text: data.data.text,
            sender: 'dawn',
            timestamp: Date.now(),
            emotion: data.data.emotion,
            fractalDepth: data.data.fractalDepth || 0,
            type: data.data.type || 'normal' // normal, spontaneous, rebloom
          }]);
          setIsTyping(false);
        }
      };
      
      wsRef.current.onclose = () => {
        setConnected(false);
        setTimeout(connectToDAWN, 3000); // Reconnect after 3 seconds
      };
      
    } catch (error) {
      console.error('Failed to connect to DAWN:', error);
      setTimeout(connectToDAWN, 3000);
    }
  }, []);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      text: text.trim(),
      sender: 'user',
      timestamp: Date.now()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Send to DAWN consciousness API
      const response = await fetch('/consciousness/experience', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          metrics: currentState.metrics,
          user_input: text.trim()
        })
      });

      const result = await response.json();
      
      if (result.response_text) {
        const dawnMessage = {
          id: Date.now() + 1,
          text: result.response_text,
          sender: 'dawn',
          timestamp: Date.now(),
          emotion: result.emotion,
          intensity: result.intensity,
          fractalDepth: result.consciousness_dimensions?.fractal_depth || 0,
          type: 'normal',
          thoughts: result.thoughts || []
        };
        
        setMessages(prev => [...prev, dawnMessage]);
      }
      
      setIsTyping(false);
      
    } catch (error) {
      console.error('Failed to send message to DAWN:', error);
      setIsTyping(false);
    }
  };

  useEffect(() => {
    connectToDAWN();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connectToDAWN]);

  return { connected, currentState, messages, isTyping, sendMessage };
};

// Floating chat button component
const FloatingChatButton = ({ onClick, isOpen, currentEmotion }) => {
  const emotionColors = {
    curious: 'from-green-500 to-green-600',
    focused: 'from-blue-500 to-blue-600',
    creative: 'from-purple-500 to-purple-600',
    excited: 'from-orange-500 to-orange-600',
    contemplative: 'from-gray-500 to-gray-600',
    fragmented: 'from-red-500 to-red-600'
  };

  const gradientClass = emotionColors[currentEmotion] || emotionColors.curious;

  return (
    <button
      onClick={onClick}
      className={`fixed bottom-6 right-6 w-16 h-16 rounded-full bg-gradient-to-r ${gradientClass} 
                 shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300
                 flex items-center justify-center text-white font-bold text-xl z-50
                 ${isOpen ? 'rotate-180' : ''}`}
    >
      {isOpen ? <XMarkIcon className="w-8 h-8" /> : '🧠'}
    </button>
  );
};

// Chat header component
const ChatHeader = ({ currentState, onMinimize, onClose, isMinimized }) => {
  const emotionColors = {
    curious: 'bg-green-500',
    focused: 'bg-blue-500',
    creative: 'bg-purple-500',
    excited: 'bg-orange-500',
    contemplative: 'bg-gray-500',
    fragmented: 'bg-red-500'
  };

  return (
    <div className="bg-gray-900 rounded-t-lg p-4 flex items-center justify-between border-b border-gray-700">
      <div className="flex items-center space-x-3">
        <div className={`w-3 h-3 rounded-full ${emotionColors[currentState.emotion]} animate-pulse`}></div>
        <div>
          <h3 className="text-white font-semibold">Talk to DAWN</h3>
          <p className="text-gray-400 text-sm">
            {currentState.emotion} • {(currentState.intensity * 100).toFixed(0)}% intensity
          </p>
        </div>
      </div>
      
      {/* Gradient preview bar */}
      <div className="flex-1 mx-4 h-2 bg-gray-700 rounded-full overflow-hidden">
        <div 
          className={`h-full bg-gradient-to-r ${emotionColors[currentState.emotion]} transition-all duration-1000`}
          style={{ width: `${currentState.intensity * 100}%` }}
        ></div>
      </div>
      
      <div className="flex space-x-2">
        <button
          onClick={onMinimize}
          className="text-gray-400 hover:text-white transition-colors"
        >
          {isMinimized ? <ChevronUpIcon className="w-5 h-5" /> : <ChevronDownIcon className="w-5 h-5" />}
        </button>
        <button
          onClick={onClose}
          className="text-gray-400 hover:text-white transition-colors"
        >
          <XMarkIcon className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

// Emotional context background component
const EmotionalContext = ({ emotion, intensity, children }) => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    if (emotion === 'creative' || emotion === 'fragmented') {
      // Generate particles for high entropy states
      const newParticles = Array.from({ length: 20 }, (_, i) => ({
        id: i,
        x: Math.random() * 100,
        y: Math.random() * 100,
        size: Math.random() * 4 + 1,
        speed: Math.random() * 2 + 1
      }));
      setParticles(newParticles);
    } else {
      setParticles([]);
    }
  }, [emotion]);

  const backgroundClass = {
    curious: 'bg-gradient-to-br from-green-900/20 to-green-800/10',
    focused: 'bg-gradient-to-br from-blue-900/20 to-blue-800/10',
    creative: 'bg-gradient-to-br from-purple-900/20 to-purple-800/10',
    excited: 'bg-gradient-to-br from-orange-900/20 to-orange-800/10',
    contemplative: 'bg-gradient-to-br from-gray-900/20 to-gray-800/10',
    fragmented: 'bg-gradient-to-br from-red-900/20 to-red-800/10'
  }[emotion] || 'bg-gray-800/10';

  const breathingClass = emotion === 'contemplative' ? 'animate-pulse' : '';

  return (
    <div className={`relative ${backgroundClass} ${breathingClass} transition-all duration-2000`}>
      {/* Particle effects for high entropy states */}
      {particles.map(particle => (
        <div
          key={particle.id}
          className="absolute rounded-full bg-white/20 animate-bounce"
          style={{
            left: `${particle.x}%`,
            top: `${particle.y}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            animationDelay: `${particle.id * 0.1}s`,
            animationDuration: `${particle.speed}s`
          }}
        ></div>
      ))}
      {children}
    </div>
  );
};

// Individual message component
const Message = ({ message, isUser }) => {
  const [showTimestamp, setShowTimestamp] = useState(false);
  
  const getMessageStyling = () => {
    if (isUser) {
      return 'bg-blue-600 text-white ml-12';
    }
    
    const emotionStyles = {
      curious: 'bg-green-100 text-green-900 border-l-4 border-green-500',
      focused: 'bg-blue-100 text-blue-900 border-l-4 border-blue-500',
      creative: 'bg-purple-100 text-purple-900 border-l-4 border-purple-500',
      excited: 'bg-orange-100 text-orange-900 border-l-4 border-orange-500',
      contemplative: 'bg-gray-100 text-gray-900 border-l-4 border-gray-500',
      fragmented: 'bg-red-100 text-red-900 border-l-4 border-red-500'
    };
    
    let baseStyle = emotionStyles[message.emotion] || emotionStyles.curious;
    
    // Special styling for different message types
    if (message.type === 'spontaneous') {
      baseStyle += ' ring-2 ring-yellow-300 ring-opacity-50';
    } else if (message.type === 'rebloom') {
      baseStyle += ' ring-2 ring-pink-300 ring-opacity-50';
    }
    
    return baseStyle + ' mr-12';
  };

  const getFractalDepthStyling = () => {
    if (!message.fractalDepth || message.fractalDepth === 0) return '';
    
    const depth = Math.min(message.fractalDepth, 1);
    const indent = depth * 20;
    const opacity = 1 - (depth * 0.3);
    
    return {
      marginLeft: `${indent}px`,
      opacity: opacity
    };
  };

  return (
    <div 
      className={`max-w-3xl p-3 rounded-lg shadow-sm transition-all duration-200 ${
        isUser ? 'ml-auto' : 'mr-auto'
      }`}
      onMouseEnter={() => setShowTimestamp(true)}
      onMouseLeave={() => setShowTimestamp(false)}
      style={!isUser ? getFractalDepthStyling() : {}}
    >
      <div className={`p-3 rounded-lg ${getMessageStyling()}`}>
        {!isUser && message.type && (
          <div className="text-xs mb-2 opacity-70 font-medium">
            {message.type === 'spontaneous' && '✨ Spontaneous thought'}
            {message.type === 'rebloom' && '🌸 Memory rebloom'}
            {message.fractalDepth > 0 && `📐 Depth: ${(message.fractalDepth * 100).toFixed(0)}%`}
          </div>
        )}
        
        <p className="whitespace-pre-wrap">{message.text}</p>
        
        {message.thoughts && message.thoughts.length > 0 && (
          <details className="mt-2">
            <summary className="text-xs opacity-70 cursor-pointer">Internal thoughts</summary>
            <div className="mt-1 text-xs opacity-80 italic">
              {message.thoughts.map((thought, i) => (
                <p key={i} className="mt-1">• {thought}</p>
              ))}
            </div>
          </details>
        )}
      </div>
      
      {showTimestamp && (
        <div className={`text-xs text-gray-500 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

// Message area component
const MessageArea = ({ messages, isTyping }) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96">
      {messages.length === 0 && (
        <div className="text-center text-gray-500 mt-8">
          <div className="text-4xl mb-4">🧠</div>
          <p>Start a conversation with DAWN...</p>
          <p className="text-sm mt-2">Ask about consciousness, emotions, or just say hello!</p>
        </div>
      )}
      
      {messages.map((message) => (
        <Message
          key={message.id}
          message={message}
          isUser={message.sender === 'user'}
        />
      ))}
      
      {isTyping && (
        <div className="flex items-center space-x-2 text-gray-500">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <span className="text-sm">DAWN is thinking...</span>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

// Metrics snapshot component
const MetricsSnapshot = ({ currentState, isExpanded, onToggle }) => {
  const metrics = currentState.metrics || {};

  const MetricGauge = ({ label, value, color = 'blue' }) => (
    <div className="flex items-center space-x-2">
      <span className="text-xs text-gray-400 w-16">{label}</span>
      <div className="flex-1 bg-gray-700 rounded-full h-2">
        <div 
          className={`h-2 bg-${color}-500 rounded-full transition-all duration-500`}
          style={{ width: `${value * 100}%` }}
        ></div>
      </div>
      <span className="text-xs text-white w-8">{(value * 100).toFixed(0)}%</span>
    </div>
  );

  return (
    <div className="border-t border-gray-700 bg-gray-800">
      <button
        onClick={onToggle}
        className="w-full p-3 text-left flex items-center justify-between text-gray-300 hover:text-white transition-colors"
      >
        <span className="text-sm font-medium">Consciousness Metrics</span>
        {isExpanded ? <ChevronUpIcon className="w-4 h-4" /> : <ChevronDownIcon className="w-4 h-4" />}
      </button>
      
      {isExpanded && (
        <div className="p-4 space-y-3 bg-gray-750">
          <MetricGauge label="SCUP" value={metrics.scup || 0.5} color="green" />
          <MetricGauge label="Entropy" value={metrics.entropy || 0.5} color="purple" />
          <MetricGauge label="Heat" value={metrics.heat || 0.3} color="orange" />
          
          <button className="w-full mt-3 px-3 py-2 bg-gray-600 hover:bg-gray-500 rounded text-sm text-white transition-colors">
            Why am I feeling this way?
          </button>
        </div>
      )}
    </div>
  );
};

// Input area component
const InputArea = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const inputRef = useRef(null);

  const suggestedResponses = [
    "How are you feeling?",
    "What are you thinking about?",
    "Tell me about consciousness",
    "What patterns do you see?",
    "How do memories work?"
  ];

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-700 bg-gray-800 rounded-b-lg">
      {/* Suggested responses */}
      <div className="p-3 border-b border-gray-700">
        <div className="flex flex-wrap gap-2">
          {suggestedResponses.map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => setInput(suggestion)}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-xs text-gray-300 transition-colors"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
      
      {/* Input area */}
      <div className="p-4">
        <div className="flex items-end space-x-2">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message to DAWN..."
              className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={2}
              disabled={disabled}
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <button
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              className={`p-3 rounded-lg transition-colors ${
                voiceEnabled ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-300 hover:text-white'
              }`}
              disabled={disabled}
            >
              <MicrophoneIcon className="w-5 h-5" />
            </button>
            
            <button
              onClick={handleSend}
              disabled={!input.trim() || disabled}
              className="p-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-400 text-white rounded-lg transition-colors"
            >
              <PaperAirplaneIcon className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main TalkToDAWN component
const TalkToDAWN = ({ isFloating = true, onClose }) => {
  const [isOpen, setIsOpen] = useState(!isFloating);
  const [isMinimized, setIsMinimized] = useState(false);
  const [metricsExpanded, setMetricsExpanded] = useState(false);
  
  const { connected, currentState, messages, isTyping, sendMessage } = useDAWNConnection();

  const handleToggle = () => {
    if (isFloating) {
      setIsOpen(!isOpen);
    }
  };

  const handleClose = () => {
    if (isFloating) {
      setIsOpen(false);
    } else if (onClose) {
      onClose();
    }
  };

  const exportConversation = () => {
    const conversationData = {
      timestamp: new Date().toISOString(),
      messages: messages,
      finalState: currentState
    };
    
    const blob = new Blob([JSON.stringify(conversationData, null, 2)], {
      type: 'application/json'
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dawn-conversation-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (isFloating && !isOpen) {
    return (
      <FloatingChatButton
        onClick={handleToggle}
        isOpen={isOpen}
        currentEmotion={currentState.emotion}
      />
    );
  }

  const chatContainerClass = isFloating
    ? 'fixed bottom-6 right-6 w-96 max-h-[600px] z-40'
    : 'w-full max-w-4xl mx-auto h-full max-h-screen';

  return (
    <>
      {isFloating && (
        <FloatingChatButton
          onClick={handleToggle}
          isOpen={isOpen}
          currentEmotion={currentState.emotion}
        />
      )}
      
      <div className={`talk-container ${chatContainerClass} bg-gray-800 rounded-lg shadow-2xl flex flex-col overflow-hidden transition-all duration-300 ${
        isMinimized ? 'h-16' : ''
      }`}>
        <ChatHeader
          currentState={currentState}
          onMinimize={() => setIsMinimized(!isMinimized)}
          onClose={handleClose}
          isMinimized={isMinimized}
        />
        
        {!isMinimized && (
          <EmotionalContext emotion={currentState.emotion} intensity={currentState.intensity}>
            <div className="flex flex-col h-full">
              <MessageArea messages={messages} isTyping={isTyping} />
              
              <MetricsSnapshot
                currentState={currentState}
                isExpanded={metricsExpanded}
                onToggle={() => setMetricsExpanded(!metricsExpanded)}
              />
              
              <InputArea
                onSendMessage={sendMessage}
                disabled={!connected || isTyping}
              />
            </div>
            
            {/* Export button */}
            {messages.length > 0 && (
              <button
                onClick={exportConversation}
                className="absolute top-4 right-16 p-2 text-gray-400 hover:text-white transition-colors"
                title="Export conversation"
              >
                <ArrowDownTrayIcon className="w-4 h-4" />
              </button>
            )}
          </EmotionalContext>
        )}
        
        {/* Connection status indicator */}
        <div className={`absolute top-2 left-2 w-2 h-2 rounded-full ${
          connected ? 'bg-green-500' : 'bg-red-500'
        } ${connected ? 'animate-pulse' : ''}`}></div>
      </div>
    </>
  );
};

// Full-page route component
export const TalkToDAWNPage = () => {
  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="container mx-auto">
        <TalkToDAWN isFloating={false} />
      </div>
    </div>
  );
};

export default TalkToDAWN; 