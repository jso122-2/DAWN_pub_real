import { useState, useEffect, useRef } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'

export default function ChatInterface({ currentMood }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    // Listen for DAWN's spontaneous thoughts
    const unlisten = listen('dawn-thought', (event) => {
      addMessage({
        text: event.payload.text,
        from: 'dawn',
        timestamp: Date.now(),
        type: 'thought'
      })
    })

    // Add welcome message
    addMessage({
      text: "Hello! I'm DAWN. You can ask me about my current state, control my tick engine, or just chat. How can I help you?",
      from: 'dawn',
      timestamp: Date.now()
    })

    return () => { unlisten.then(fn => fn()) }
  }, [])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(scrollToBottom, [messages])

  const addMessage = (message) => {
    setMessages(prev => [...prev, message])
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = {
      text: input,
      from: 'user',
      timestamp: Date.now()
    }
    
    addMessage(userMessage)
    setInput('')
    setIsTyping(true)

    try {
      const response = await invoke('send_message', { message: input })
      
      // Simulate typing delay
      setTimeout(() => {
        addMessage({
          text: response.response,
          from: 'dawn',
          timestamp: Date.now(),
          metrics: response.metrics_snapshot
        })
        
        setSuggestions(response.suggestions || [])
        setIsTyping(false)
      }, 500 + Math.random() * 1000)
      
    } catch (error) {
      console.error('Chat error:', error)
      addMessage({
        text: "I'm having trouble processing that. Please try again.",
        from: 'dawn',
        timestamp: Date.now(),
        type: 'error'
      })
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getMoodColor = (mood) => {
    const colors = {
      'Positive': 'border-green-400',
      'Neutral': 'border-blue-400',
      'Negative': 'border-orange-400'
    }
    return colors[mood] || 'border-gray-400'
  }

  return (
    <>
      <style>{styles}</style>
      <div className="bg-gray-800 rounded-lg h-full flex flex-col">
        {/* Header */}
        <div className={`p-4 border-b-2 ${getMoodColor(currentMood)} bg-gray-900`}>
          <h3 className="text-lg font-bold">Talk to DAWN</h3>
          <p className="text-sm text-gray-400">Current mood: {currentMood}</p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.from === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.from === 'user'
                    ? 'bg-blue-600 text-white'
                    : msg.type === 'thought'
                    ? 'bg-purple-900/50 text-purple-200 italic'
                    : msg.type === 'error'
                    ? 'bg-red-900/50 text-red-200'
                    : 'bg-gray-700 text-gray-100'
                }`}
              >
                {msg.from === 'dawn' && msg.type === 'thought' && (
                  <p className="text-xs mb-1 opacity-70">💭 Spontaneous thought</p>
                )}
                <p className="whitespace-pre-wrap">{msg.text}</p>
                {msg.metrics && (
                  <div className="mt-2 pt-2 border-t border-gray-600 text-xs">
                    <span>SCUP: {msg.metrics.scup.toFixed(3)}</span>
                    <span className="ml-2">Entropy: {msg.metrics.entropy.toFixed(3)}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-700 px-4 py-2 rounded-lg">
                <span className="typing-dots">
                  <span>.</span><span>.</span><span>.</span>
                </span>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="px-4 py-2 border-t border-gray-700">
            <p className="text-xs text-gray-400 mb-2">Suggestions:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, i) => (
                <button
                  key={i}
                  onClick={() => setInput(suggestion)}
                  className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded-full text-sm"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask DAWN anything..."
              className="flex-1 bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isTyping}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg transition"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

// Add CSS for typing animation
const styles = `
  .typing-dots span {
    animation: blink 1.4s infinite;
    animation-fill-mode: both;
  }
  
  .typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  .typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
  }
  
  @keyframes blink {
    0%, 60%, 100% {
      opacity: 0.2;
    }
    30% {
      opacity: 1;
    }
  }
` 