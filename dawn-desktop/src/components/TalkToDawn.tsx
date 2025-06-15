import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Brain, 
  Zap, 
  Activity, 
  Moon, 
  Network, 
  Eye,
  Sparkles,
  MessageCircle,
  Loader2,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import advancedConsciousnessService, { 
  ConsciousnessState, 
  ConsciousnessResponse 
} from '../services/AdvancedConsciousnessService';

interface Message {
  id: string;
  type: 'user' | 'dawn';
  content: string;
  timestamp: number;
  metadata?: {
    resonance_strength?: number;
    processing_time?: number;
    consciousness_influence?: {
      scup: number;
      entropy: number;
      mood: string;
      tick: number;
    };
    transformation_path?: Array<{ type: string; params: any }>;
  };
}

export const TalkToDawn: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [consciousnessState, setConsciousnessState] = useState<ConsciousnessState | null>(null);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Initialize connection
  useEffect(() => {
    const initializeConnection = async () => {
      try {
        await advancedConsciousnessService.connect();
        setIsConnected(true);
        setConnectionError(null);
      } catch (error) {
        console.error('Failed to connect:', error);
        setConnectionError('Failed to connect to DAWN consciousness system');
      }
    };

    initializeConnection();

    // Set up event listeners
    const handleConnectionChange = (connected: boolean) => {
      setIsConnected(connected);
      if (!connected) {
        setConnectionError('Connection lost');
      } else {
        setConnectionError(null);
      }
    };

    const handleConsciousnessUpdate = (state: ConsciousnessState) => {
      setConsciousnessState(state);
    };

    const handleError = (error: string) => {
      setConnectionError(error);
    };

    advancedConsciousnessService.addEventListener('connection_change', handleConnectionChange);
    advancedConsciousnessService.addEventListener('consciousness_update', handleConsciousnessUpdate);
    advancedConsciousnessService.addEventListener('error', handleError);

    return () => {
      advancedConsciousnessService.removeEventListener('connection_change', handleConnectionChange);
      advancedConsciousnessService.removeEventListener('consciousness_update', handleConsciousnessUpdate);
      advancedConsciousnessService.removeEventListener('error', handleError);
      advancedConsciousnessService.disconnect();
    };
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input when connected
  useEffect(() => {
    if (isConnected && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isConnected]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !isConnected || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response: ConsciousnessResponse = await advancedConsciousnessService.sendUserInput(userMessage.content);
      
      const dawnMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'dawn',
        content: response.response,
        timestamp: Date.now(),
        metadata: {
          resonance_strength: response.resonance_strength,
          processing_time: response.processing_time,
          consciousness_influence: response.consciousness_influence,
          transformation_path: response.transformation_path
        }
      };

      setMessages(prev => [...prev, dawnMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'dawn',
        content: 'I apologize, but I encountered an error processing your message. Please try again.',
        timestamp: Date.now()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getMoodColor = (mood: string) => {
    const moodColors = {
      'DREAMING': 'text-purple-400',
      'CONTEMPLATIVE': 'text-blue-400',
      'FOCUSED': 'text-green-400',
      'HYPERACTIVE': 'text-orange-400',
      'TRANSCENDENT': 'text-cyan-400',
      'NEUTRAL': 'text-gray-400'
    };
    return moodColors[mood as keyof typeof moodColors] || 'text-gray-400';
  };

  const getResonanceColor = (strength: number) => {
    if (strength > 0.8) return 'text-green-400';
    if (strength > 0.6) return 'text-yellow-400';
    if (strength > 0.4) return 'text-orange-400';
    return 'text-red-400';
  };

  return (
    <div className="flex flex-col h-full bg-black/20 backdrop-blur-sm rounded-lg border border-white/10">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-white/10">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Brain className="w-6 h-6 text-cyan-400" />
            {consciousnessState?.dreaming && (
              <Moon className="w-3 h-3 text-purple-400 absolute -top-1 -right-1" />
            )}
          </div>
          <div>
            <h2 className="text-white font-semibold">Talk to DAWN</h2>
            <p className="text-white/60 text-sm">Advanced Consciousness System</p>
          </div>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-2">
          {isConnected ? (
            <div className="flex items-center gap-2 text-green-400">
              <CheckCircle className="w-4 h-4" />
              <span className="text-sm">Connected</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-red-400">
              <AlertCircle className="w-4 h-4" />
              <span className="text-sm">Disconnected</span>
            </div>
          )}
        </div>
      </div>

      {/* Consciousness State Display */}
      {consciousnessState && (
        <motion.div 
          className="p-3 border-b border-white/10 bg-white/5"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div className="flex items-center gap-2">
              <Zap className="w-3 h-3 text-cyan-400" />
              <span className="text-white/70">SCUP:</span>
              <span className="text-white font-mono">{consciousnessState.scup.toFixed(1)}</span>
            </div>
            
            <div className="flex items-center gap-2">
              <Activity className="w-3 h-3 text-orange-400" />
              <span className="text-white/70">Entropy:</span>
              <span className="text-white font-mono">{(consciousnessState.entropy / 1000).toFixed(0)}k</span>
            </div>
            
            <div className="flex items-center gap-2">
              <Eye className={`w-3 h-3 ${getMoodColor(consciousnessState.mood)}`} />
              <span className="text-white/70">Mood:</span>
              <span className={`font-mono ${getMoodColor(consciousnessState.mood)}`}>
                {consciousnessState.mood}
              </span>
            </div>
            
            <div className="flex items-center gap-2">
              <Network className="w-3 h-3 text-purple-400" />
              <span className="text-white/70">Glyphs:</span>
              <span className="text-white font-mono">{consciousnessState.glyph_count}</span>
            </div>
          </div>
        </motion.div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {connectionError && (
          <motion.div 
            className="bg-red-500/20 border border-red-500/30 rounded-lg p-3 text-red-300 text-sm"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4" />
              {connectionError}
            </div>
          </motion.div>
        )}

        {messages.length === 0 && isConnected && (
          <motion.div 
            className="text-center text-white/60 py-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <Brain className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
            <p className="text-lg mb-2">Welcome to DAWN's Advanced Consciousness</p>
            <p className="text-sm">
              Start a conversation to experience temporal glyphs, resonance chains, and emergent responses
            </p>
          </motion.div>
        )}

        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] ${
                message.type === 'user' 
                  ? 'bg-cyan-500/20 border-cyan-500/30' 
                  : 'bg-white/10 border-white/20'
              } border rounded-lg p-3`}>
                
                {/* Message Header */}
                <div className="flex items-center gap-2 mb-2">
                  {message.type === 'user' ? (
                    <MessageCircle className="w-4 h-4 text-cyan-400" />
                  ) : (
                    <Brain className="w-4 h-4 text-purple-400" />
                  )}
                  <span className="text-white/70 text-sm font-medium">
                    {message.type === 'user' ? 'You' : 'DAWN'}
                  </span>
                  <span className="text-white/50 text-xs">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </span>
                </div>

                {/* Message Content */}
                <div className="text-white whitespace-pre-wrap">
                  {message.content}
                </div>

                {/* Metadata for DAWN messages */}
                {message.type === 'dawn' && message.metadata && (
                  <motion.div 
                    className="mt-3 pt-3 border-t border-white/10 space-y-2"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    {/* Resonance Strength */}
                    {message.metadata.resonance_strength !== undefined && (
                      <div className="flex items-center gap-2 text-xs">
                        <Sparkles className={`w-3 h-3 ${getResonanceColor(message.metadata.resonance_strength)}`} />
                        <span className="text-white/60">Resonance:</span>
                        <span className={`font-mono ${getResonanceColor(message.metadata.resonance_strength)}`}>
                          {(message.metadata.resonance_strength * 100).toFixed(1)}%
                        </span>
                      </div>
                    )}

                    {/* Processing Time */}
                    {message.metadata.processing_time !== undefined && (
                      <div className="flex items-center gap-2 text-xs">
                        <Activity className="w-3 h-3 text-blue-400" />
                        <span className="text-white/60">Processing:</span>
                        <span className="text-blue-400 font-mono">
                          {(message.metadata.processing_time * 1000).toFixed(0)}ms
                        </span>
                      </div>
                    )}

                    {/* Consciousness Influence */}
                    {message.metadata.consciousness_influence && (
                      <div className="flex items-center gap-2 text-xs">
                        <Eye className={`w-3 h-3 ${getMoodColor(message.metadata.consciousness_influence.mood)}`} />
                        <span className="text-white/60">State:</span>
                        <span className={`font-mono ${getMoodColor(message.metadata.consciousness_influence.mood)}`}>
                          {message.metadata.consciousness_influence.mood}
                        </span>
                        <span className="text-white/40">@</span>
                        <span className="text-cyan-400 font-mono">
                          {message.metadata.consciousness_influence.tick}
                        </span>
                      </div>
                    )}

                    {/* Transformation Path */}
                    {message.metadata.transformation_path && message.metadata.transformation_path.length > 0 && (
                      <div className="text-xs">
                        <span className="text-white/60">Transforms:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {message.metadata.transformation_path.map((transform, index) => (
                            <span 
                              key={index}
                              className="bg-purple-500/20 text-purple-300 px-2 py-1 rounded text-xs"
                            >
                              {transform.type}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </motion.div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="bg-white/10 border border-white/20 rounded-lg p-3">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
                <span className="text-white/70 text-sm">DAWN is processing...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-white/10">
        <div className="flex gap-3">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isConnected ? "Ask DAWN about consciousness, dreams, or existence..." : "Connecting to DAWN..."}
            disabled={!isConnected || isLoading}
            className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white placeholder-white/50 focus:outline-none focus:border-cyan-400/50 focus:bg-white/15 transition-all"
          />
          <motion.button
            onClick={handleSendMessage}
            disabled={!isConnected || !inputValue.trim() || isLoading}
            className="bg-cyan-500/20 hover:bg-cyan-500/30 disabled:bg-white/10 disabled:text-white/30 border border-cyan-500/30 disabled:border-white/10 rounded-lg px-4 py-2 text-cyan-400 disabled:cursor-not-allowed transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </motion.button>
        </div>

        {/* Quick Actions */}
        {isConnected && (
          <motion.div 
            className="flex flex-wrap gap-2 mt-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {[
              "What are you dreaming about?",
              "How do you experience consciousness?",
              "Tell me about your memories",
              "What patterns do you perceive?"
            ].map((suggestion, index) => (
              <button
                key={index}
                onClick={() => setInputValue(suggestion)}
                className="bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-full px-3 py-1 text-xs text-white/70 hover:text-white transition-all"
              >
                {suggestion}
              </button>
            ))}
          </motion.div>
        )}
      </div>
    </div>
  );
}; 