import { useEffect, useState, useCallback } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import './ResetPipelinePanel.css'

interface ResetState {
  activeOperation: string | null
  lastOperation: string | null
  confirmationVisible: boolean
  pendingOperation: (() => Promise<void>) | null
}

interface ResetButton {
  id: string
  label: string
  command: string
  hotkey: string
  description: string
  dangerous?: boolean
}

/**
 * DAWN Reset Pipeline Panel - Runtime Reflex Controls
 * 
 * Provides manual override controls for DAWN's internal pressure systems
 * with hotkey support and confirmation dialogs for dangerous operations
 */
export function ResetPipelinePanel() {
  const [resetState, setResetState] = useState<ResetState>({
    activeOperation: null,
    lastOperation: null,
    confirmationVisible: false,
    pendingOperation: null
  })

  // Reset button configurations
  const resetButtons: ResetButton[] = [
    {
      id: 'heat',
      label: 'Reset Heat',
      command: 'reset_heat',
      hotkey: 'Shift+H',
      description: 'Clear thermal pressure accumulation'
    },
    {
      id: 'sigils',
      label: 'Clear Sigils',
      command: 'clear_sigils',
      hotkey: 'Shift+S',
      description: 'Deactivate all active sigil processes'
    },
    {
      id: 'entropy',
      label: 'Zero Entropy',
      command: 'zero_entropy',
      hotkey: 'Shift+E',
      description: 'Reset entropy accumulator to baseline'
    },
    {
      id: 'restart',
      label: 'Soft System Restart',
      command: 'soft_restart',
      hotkey: 'Shift+R',
      description: 'Reinitialize cognitive subsystems',
      dangerous: true
    }
  ]

  // Execute reset operation
  const executeReset = useCallback(async (button: ResetButton) => {
    if (resetState.activeOperation) {
      console.log('⚠️ [RESET] Operation already in progress')
      return
    }

    console.log(`🔄 [RESET] Executing ${button.label} (${button.command})`)
    
    setResetState(prev => ({ 
      ...prev, 
      activeOperation: button.id,
      lastOperation: null
    }))

    try {
      // Call Tauri backend command
      const result = await invoke(button.command, {
        timestamp: new Date().toISOString(),
        triggered_by: 'manual_panel'
      })
      
      console.log(`✅ [RESET] ${button.label} completed:`, result)
      
      setResetState(prev => ({
        ...prev,
        activeOperation: null,
        lastOperation: `${button.label} completed`
      }))
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setResetState(prev => ({ ...prev, lastOperation: null }))
      }, 3000)
      
    } catch (error) {
      console.error(`❌ [RESET] ${button.label} failed:`, error)
      
      setResetState(prev => ({
        ...prev,
        activeOperation: null,
        lastOperation: `${button.label} failed`
      }))
      
      // Clear error message after 5 seconds
      setTimeout(() => {
        setResetState(prev => ({ ...prev, lastOperation: null }))
      }, 5000)
    }
  }, [resetState.activeOperation])

  // Handle button click with confirmation for dangerous operations
  const handleButtonClick = useCallback((button: ResetButton) => {
    if (button.dangerous) {
      setResetState(prev => ({
        ...prev,
        confirmationVisible: true,
        pendingOperation: () => executeReset(button)
      }))
    } else {
      executeReset(button)
    }
  }, [executeReset])

  // Confirm dangerous operation
  const confirmOperation = useCallback(() => {
    if (resetState.pendingOperation) {
      resetState.pendingOperation()
    }
    setResetState(prev => ({
      ...prev,
      confirmationVisible: false,
      pendingOperation: null
    }))
  }, [resetState.pendingOperation])

  // Cancel dangerous operation
  const cancelOperation = useCallback(() => {
    setResetState(prev => ({
      ...prev,
      confirmationVisible: false,
      pendingOperation: null
    }))
  }, [])

  // Hotkey handler
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!event.shiftKey) return
      
      const button = resetButtons.find(btn => {
        const [modifier, key] = btn.hotkey.split('+')
        return modifier === 'Shift' && event.key.toLowerCase() === key.toLowerCase()
      })
      
      if (button && !resetState.activeOperation && !resetState.confirmationVisible) {
        event.preventDefault()
        handleButtonClick(button)
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [handleButtonClick, resetState.activeOperation, resetState.confirmationVisible])

  return (
    <div className="reset-pipeline-panel">
      <div className="reset-header">
        <span className="reset-title">🔄 RUNTIME REFLEX CONTROLS</span>
        <div className="reset-indicators">
          <span className={`activity-indicator ${resetState.activeOperation ? 'active' : 'idle'}`}>
            {resetState.activeOperation ? '⚡' : '⚙️'}
          </span>
        </div>
      </div>

      <div className="reset-controls">
        {resetButtons.map((button) => (
          <div key={button.id} className="control-group">
            <button
              className={`reset-button ${button.dangerous ? 'dangerous' : ''} ${
                resetState.activeOperation === button.id ? 'loading' : ''
              }`}
              onClick={() => handleButtonClick(button)}
              disabled={!!resetState.activeOperation}
              title={`${button.description} (${button.hotkey})`}
            >
              {resetState.activeOperation === button.id ? (
                <>
                  <span className="loading-dots"></span>
                  Processing...
                </>
              ) : (
                button.label
              )}
            </button>
            <div className="control-info">
              <span className="control-description">{button.description}</span>
              <span className="control-hotkey">{button.hotkey}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Confirmation Dialog */}
      {resetState.confirmationVisible && (
        <div className="confirmation-overlay">
          <div className="confirmation-dialog">
            <div className="confirmation-header">
              <span className="warning-icon">⚠️</span>
              <span className="confirmation-title">Confirm System Operation</span>
            </div>
            <div className="confirmation-message">
              This operation will perform a soft restart of DAWN's cognitive subsystems.
              Active processes and temporary state will be lost.
            </div>
            <div className="confirmation-buttons">
              <button 
                className="confirm-button cancel"
                onClick={cancelOperation}
              >
                Cancel
              </button>
              <button 
                className="confirm-button proceed"
                onClick={confirmOperation}
              >
                Proceed
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="reset-footer">
        {resetState.lastOperation && (
          <div className={`status-banner ${
            resetState.lastOperation.includes('failed') ? 'error' : 'success'
          }`}>
            {resetState.lastOperation.includes('failed') ? '❌' : '✅'} {resetState.lastOperation}
          </div>
        )}
        {!resetState.lastOperation && (
          <div className="hotkey-hint">
            Use Shift + H/S/E/R for quick access
          </div>
        )}
      </div>
    </div>
  )
}

export default ResetPipelinePanel 