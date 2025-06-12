import { useState, useEffect, useRef } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { listen } from '@tauri-apps/api/event'

export default function MinimalDawnChat({ currentMetrics }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [dawnState, setDawnState] = useState('stable')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    // Check for thoughts every 30 seconds
    const thoughtInterval = setInterval(async () => {
      try {
        const thought = await invoke('get_dawn_thought')
        if (thought.thought) {
          addMessage({
            text: thought.thought,
            from: 'dawn',
            type: 'thought'
          })
        }
      } catch (err) {
        console.error('Thought check failed:', err)
      }
    }, 30000)

    // Listen for state changes
    const unlisten = listen('dawn-state-change', (event) => {
      setDawnState(event.payload.to)
      addMessage({
        text: `[${event.payload.description}]`,
        from: 'system',
        type: 'state'
      })
    })

    // Auto-scroll to bottom
    const scrollToBottom = () => {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }
    scrollToBottom()

    return () => {
      clearInterval(thoughtInterval)
      unlisten.then(fn => fn())
    }
  }, [messages])

  const addMessage = (msg) => {
    setMessages(prev => [...prev, { ...msg, timestamp: Date.now() }])
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    addMessage({ text: input, from: 'user' })
    setInput('')

    try {
      const response = await invoke('send_message', { message: input })
      addMessage({ 
        text: response.text, 
        from: 'dawn',
        state: response.state 
      })
    } catch (err) {
      addMessage({ 
        text: 'Connection error', 
        from: 'system', 
        type: 'error' 
      })
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      sendMessage()
    }
  }

  const stateColors = {
    'stable': 'border-green-500',
    'chaotic': 'border-orange-500', 
    'fragmented': 'border-red-500',
    'reflective': 'border-blue-500'
  }

  const getStateIndicator = (state) => {
    const indicators = {
      'stable': '🟢',
      'chaotic': '🟠',
      'fragmented': '🔴',
      'reflective': '🔵'
    }
    return indicators[state] || '⚪'
  }

  return (
    <div className={`glass border-0 shadow-glow-sm ${stateColors[dawnState]} transition-colors duration-300 h-full flex flex-col hover:shadow-glow-md transition-all duration-300`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-700 flex justify-between items-center flex-shrink-0">
        <h3 className="font-bold text-white">DAWN Interface</h3>
        <div className="flex items-center space-x-2">
          <span className="text-lg">{getStateIndicator(dawnState)}</span>
          <span className="text-sm text-gray-400 capitalize">{dawnState}</span>
        </div>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 text-sm italic">
            DAWN ready. Ask about state, metrics, or control.
          </div>
        )}
        
        {messages.map((msg, i) => (
          <div key={i} className={`
            ${msg.from === 'user' ? 'text-right' : 'text-left'}
            ${msg.type === 'thought' ? 'italic text-gray-400 text-sm' : ''}
            ${msg.type === 'state' ? 'text-center text-sm text-gray-500' : ''}
            ${msg.type === 'error' ? 'text-center text-sm text-red-400' : ''}
          `}>
            {msg.type === 'thought' && (
              <div className="text-xs text-gray-500 mb-1">💭 spontaneous</div>
            )}
            
            <span className={`
              inline-block px-3 py-2 rounded-lg max-w-xs break-words
              ${msg.from === 'user' ? 'bg-blue-600 text-white' : 
                msg.from === 'dawn' ? 'bg-gray-700 text-gray-100' : 
                'bg-transparent text-gray-400'}
              ${msg.type === 'thought' ? 'bg-purple-900/30 text-purple-200' : ''}
              ${msg.type === 'error' ? 'bg-red-900/30 text-red-300' : ''}
            `}>
              {msg.text}
            </span>
            
            {msg.state && msg.state !== dawnState && (
              <div className="text-xs text-gray-500 mt-1">
                → {msg.state}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <div className="p-4 border-t border-gray-700 flex-shrink-0">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Message DAWN..."
            className="flex-1 bg-dawn-surface/50 focus:shadow-glow-sm focus:border-dawn-glow-teal text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg transition-colors"
          >
            Send
          </button>
        </div>
        
        {/* Quick actions */}
        <div className="flex space-x-2 mt-2">
          {['Show metrics', 'Current state', 'Help'].map(action => (
            <button
              key={action}
              onClick={() => setInput(action)}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 text-gray-300 text-xs rounded transition-colors"
            >
              {action}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
} 