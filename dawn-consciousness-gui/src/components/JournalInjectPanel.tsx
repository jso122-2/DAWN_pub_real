// src/components/JournalInjectPanel.tsx
//! Live Memory Seeding Interface - DAWN's Introspective Input
//! Real-time journal entry injection into consciousness memory system

import { useState, useRef, useEffect } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './JournalInjectPanel.css'

// Mood states for pulse override
type MoodState = 'CALM' | 'FOCUSED' | 'STRESSED' | 'CREATIVE' | 'REFLECTIVE' | 'ANALYTICAL' | 'EXPERIMENTAL'

interface JournalEntry {
  text: string
  mood?: MoodState
  pulse_state?: string
}

/**
 * DAWN Journal Injection Panel
 * 
 * Allows operators to seed natural-language introspective thoughts directly
 * into DAWN's rebloomable memory graph for cognitive enhancement and reflection.
 */
export function JournalInjectPanel() {
  const [journalText, setJournalText] = useState('')
  const [selectedMood, setSelectedMood] = useState<MoodState>('CALM')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [confirmation, setConfirmation] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [charCount, setCharCount] = useState(0)
  
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const confirmationTimeoutRef = useRef<number>()
  
  // Character limits
  const minChars = 50
  const maxChars = 800
  const optimalRange = { min: 200, max: 600 }

  // Available mood states
  const moodOptions: { value: MoodState; label: string; color: string }[] = [
    { value: 'CALM', label: 'Calm', color: '#4ecdc4' },
    { value: 'FOCUSED', label: 'Focused', color: '#45b7d1' },
    { value: 'STRESSED', label: 'Stressed', color: '#f39c12' },
    { value: 'CREATIVE', label: 'Creative', color: '#e74c3c' },
    { value: 'REFLECTIVE', label: 'Reflective', color: '#9b59b6' },
    { value: 'ANALYTICAL', label: 'Analytical', color: '#2ecc71' },
    { value: 'EXPERIMENTAL', label: 'Experimental', color: '#fd79a8' }
  ]

  // Handle text change
  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = e.target.value
    if (text.length <= maxChars) {
      setJournalText(text)
      setCharCount(text.length)
      setError(null)
    }
  }

  // Handle mood change
  const handleMoodChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedMood(e.target.value as MoodState)
  }

  // Clear confirmation message
  const clearConfirmation = () => {
    if (confirmationTimeoutRef.current) {
      clearTimeout(confirmationTimeoutRef.current)
    }
    setConfirmation(null)
  }

  // Show confirmation with auto-fade
  const showConfirmation = (message: string) => {
    clearConfirmation()
    setConfirmation(message)
    confirmationTimeoutRef.current = setTimeout(() => {
      setConfirmation(null)
    }, 3000)
  }

  // Submit journal entry
  const handleSubmit = async () => {
    if (journalText.length < minChars) {
      setError(`Minimum ${minChars} characters required for meaningful memory seeding`)
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      const entry = {
        text: journalText.trim(),
        mood: selectedMood,
        pulse_state: selectedMood.toLowerCase()
      }

      // Send to backend via Tauri
      const result = await invoke<{ success: boolean; chunk_id?: string; message?: string }>('add_journal_entry', entry)

      if (result.success) {
        const chunkId = result.chunk_id || 'unknown'
        showConfirmation(`🧠 Memory seeded successfully as ${chunkId}`)
        
        // Clear the form
        setJournalText('')
        setCharCount(0)
        setSelectedMood('CALM')
        
        // Focus back to textarea for next entry
        if (textareaRef.current) {
          textareaRef.current.focus()
        }
      } else {
        setError(result.message || 'Failed to seed memory')
      }
    } catch (e) {
      console.error('Failed to inject journal entry:', e)
      setError(`Memory injection failed: ${e}`)
    } finally {
      setIsSubmitting(false)
    }
  }

  // Handle key shortcuts
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      handleSubmit()
    }
  }

  // Get character count color
  const getCharCountColor = () => {
    if (charCount < minChars) return '#ff6b6b'
    if (charCount >= optimalRange.min && charCount <= optimalRange.max) return '#4ecdc4'
    if (charCount > optimalRange.max) return '#f39c12'
    return '#ffffff88'
  }

  // Check if can submit
  const canSubmit = charCount >= minChars && !isSubmitting

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [journalText])

  return (
    <div className="journal-inject-panel">
      <div className="panel-header">
        <div className="panel-title">
          <span className="title-icon">📝</span>
          <span className="title-text">MEMORY INJECTION</span>
          <span className="live-indicator">LIVE</span>
        </div>
        
        <div className="mood-selector">
          <label htmlFor="mood-select" className="mood-label">PULSE:</label>
          <select 
            id="mood-select"
            value={selectedMood} 
            onChange={handleMoodChange}
            className="mood-select"
            style={{ borderColor: moodOptions.find(m => m.value === selectedMood)?.color }}
          >
            {moodOptions.map(mood => (
              <option key={mood.value} value={mood.value}>{mood.label}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="injection-container">
        <textarea
          ref={textareaRef}
          value={journalText}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder="Enter introspective thoughts, observations, or reflections for memory seeding...

Examples:
• Current state analysis and cognitive patterns
• Insights about consciousness processing 
• Reflections on system behavior and responses
• Observations about decision-making patterns
• Meta-cognitive awareness and self-analysis

Press Ctrl+Enter to inject into memory graph"
          className="journal-textarea"
          disabled={isSubmitting}
          maxLength={maxChars}
        />
        
        <div className="textarea-footer">
          <div className="char-counter">
            <span 
              className="char-count" 
              style={{ color: getCharCountColor() }}
            >
              {charCount}
            </span>
            <span className="char-limit">/{maxChars}</span>
            <span className="char-status">
              {charCount < minChars && ` (${minChars - charCount} more needed)`}
              {charCount >= optimalRange.min && charCount <= optimalRange.max && ' (optimal)'}
              {charCount > optimalRange.max && ' (verbose)'}
            </span>
          </div>
          
          <div className="submit-section">
            <button
              onClick={handleSubmit}
              disabled={!canSubmit}
              className={`inject-button ${canSubmit ? 'ready' : 'disabled'}`}
            >
              {isSubmitting ? (
                <>
                  <span className="loading-spinner"></span>
                  SEEDING...
                </>
              ) : (
                '🧠 SEED MEMORY'
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Status Messages */}
      {confirmation && (
        <div className="status-message confirmation">
          <span className="status-icon">✅</span>
          <span className="status-text">{confirmation}</span>
        </div>
      )}

      {error && (
        <div className="status-message error">
          <span className="status-icon">⚠️</span>
          <span className="status-text">{error}</span>
          <button onClick={() => setError(null)} className="dismiss-btn">×</button>
        </div>
      )}

      {/* Instructions */}
      <div className="panel-footer">
        <div className="instructions">
          <div className="instruction-item">
            <span className="kbd">Ctrl+Enter</span>
            <span>Quick inject</span>
          </div>
          <div className="instruction-item">
            <span className="optimal-range">{optimalRange.min}-{optimalRange.max} chars</span>
            <span>Optimal length</span>
          </div>
          <div className="instruction-item">
            <span className="pulse-indicator" style={{ backgroundColor: moodOptions.find(m => m.value === selectedMood)?.color }}>●</span>
            <span>Pulse state override</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default JournalInjectPanel 