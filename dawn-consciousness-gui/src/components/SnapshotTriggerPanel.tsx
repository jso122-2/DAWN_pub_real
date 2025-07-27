import { useEffect, useRef, useState } from 'react'
import { invoke } from '@tauri-apps/api/tauri'
import { get, subscribe, DawnState } from '../hooks/useTickState'
import './SnapshotTriggerPanel.css'

interface SnapshotState {
  lastSnapshot: Date | null
  stateHash: string | null
  isCreating: boolean
  lastResult: 'success' | 'error' | null
  autoSaveEnabled: boolean
  autoSaveCountdown: number
}

/**
 * DAWN Snapshot Trigger Panel - Cognitive State Preservation
 * 
 * Provides manual and automatic snapshot capabilities for DAWN's complete
 * mindstate including memory, sigils, and consciousness metrics
 */
export function SnapshotTriggerPanel() {
  const [snapshot, setSnapshot] = useState<SnapshotState>({
    lastSnapshot: null,
    stateHash: null,
    isCreating: false,
    lastResult: null,
    autoSaveEnabled: false,
    autoSaveCountdown: 300 // 5 minutes in seconds
  })
  
  const autoSaveIntervalRef = useRef<number>()
  const unsubscribeRef = useRef<(() => void) | null>(null)
  const lastEntropyCheckRef = useRef<number>(0)
  
  // Auto-save countdown and triggers
  useEffect(() => {
    if (!snapshot.autoSaveEnabled) {
      if (autoSaveIntervalRef.current) {
        clearInterval(autoSaveIntervalRef.current)
      }
      return
    }
    
    // Start countdown timer
    autoSaveIntervalRef.current = setInterval(() => {
      setSnapshot(prev => {
        const newCountdown = prev.autoSaveCountdown - 1
        
        // Trigger auto-save when countdown reaches 0
        if (newCountdown <= 0) {
          createSnapshot(true)
          return { ...prev, autoSaveCountdown: 300 } // Reset to 5 minutes
        }
        
        return { ...prev, autoSaveCountdown: newCountdown }
      })
    }, 1000)
    
    return () => {
      if (autoSaveIntervalRef.current) {
        clearInterval(autoSaveIntervalRef.current)
      }
    }
  }, [snapshot.autoSaveEnabled])
  
  // Monitor entropy for emergency snapshots
  useEffect(() => {
    if (!snapshot.autoSaveEnabled) return
    
    unsubscribeRef.current = subscribe((state: DawnState) => {
      const now = Date.now()
      
      // Check entropy every 10 seconds to avoid spam
      if (now - lastEntropyCheckRef.current < 10000) return
      lastEntropyCheckRef.current = now
      
      // Emergency snapshot on high entropy
      if (state.entropy > 0.9) {
        console.log('🚨 [SNAPSHOT] Emergency snapshot triggered - high entropy:', state.entropy)
        createSnapshot(true, 'emergency')
      }
    })
    
    return () => {
      if (unsubscribeRef.current) {
        unsubscribeRef.current()
      }
    }
  }, [snapshot.autoSaveEnabled])
  
  // Create snapshot via Tauri backend
  const createSnapshot = async (isAuto: boolean = false, trigger: string = 'manual') => {
    if (snapshot.isCreating) {
      console.log('⚠️ [SNAPSHOT] Snapshot already in progress')
      return
    }
    
    console.log(`📸 [SNAPSHOT] Creating ${isAuto ? 'automatic' : 'manual'} snapshot (trigger: ${trigger})`)
    
    setSnapshot(prev => ({ 
      ...prev, 
      isCreating: true, 
      lastResult: null 
    }))
    
    try {
      // Call Tauri backend command
      const result = await invoke('create_snapshot', {
        trigger,
        timestamp: new Date().toISOString(),
        auto: isAuto
      })
      
      console.log('✅ [SNAPSHOT] Snapshot created successfully:', result)
      
      // Generate simple state hash from current data
      const currentState = get()
      const stateHash = currentState 
        ? `${currentState.tick_number}-${currentState.entropy.toFixed(3)}-${currentState.scup.toFixed(1)}`
        : null
      
      setSnapshot(prev => ({
        ...prev,
        lastSnapshot: new Date(),
        stateHash,
        isCreating: false,
        lastResult: 'success',
        autoSaveCountdown: prev.autoSaveEnabled ? 300 : prev.autoSaveCountdown // Reset countdown on successful save
      }))
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSnapshot(prev => ({ ...prev, lastResult: null }))
      }, 3000)
      
    } catch (error) {
      console.error('❌ [SNAPSHOT] Failed to create snapshot:', error)
      
      setSnapshot(prev => ({
        ...prev,
        isCreating: false,
        lastResult: 'error'
      }))
      
      // Clear error message after 5 seconds
      setTimeout(() => {
        setSnapshot(prev => ({ ...prev, lastResult: null }))
      }, 5000)
    }
  }
  
  // Toggle auto-save
  const toggleAutoSave = () => {
    setSnapshot(prev => ({
      ...prev,
      autoSaveEnabled: !prev.autoSaveEnabled,
      autoSaveCountdown: 300 // Reset countdown when toggling
    }))
  }
  
  // Format countdown time
  const formatCountdown = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }
  
  // Format timestamp
  const formatTimestamp = (date: Date | null): string => {
    if (!date) return 'Never'
    return date.toISOString().replace('T', ' ').replace('Z', ' UTC')
  }
  
  return (
    <div className="snapshot-trigger-panel">
      <div className="snapshot-header">
        <span className="snapshot-title">📦 COGNITIVE STATE SNAPSHOTS</span>
        <div className="snapshot-indicators">
          <span className={`status-indicator ${snapshot.lastResult || 'idle'}`}>
            {snapshot.lastResult === 'success' && '✅'}
            {snapshot.lastResult === 'error' && '❌'}
            {!snapshot.lastResult && '💾'}
          </span>
        </div>
      </div>
      
      <div className="snapshot-info">
        <div className="info-row">
          <span className="info-label">Last Snapshot:</span>
          <span className="info-value timestamp">
            {formatTimestamp(snapshot.lastSnapshot)}
          </span>
        </div>
        
        {snapshot.stateHash && (
          <div className="info-row">
            <span className="info-label">State Hash:</span>
            <span className="info-value hash">
              {snapshot.stateHash}
            </span>
          </div>
        )}
        
        <div className="info-row">
          <span className="info-label">Status:</span>
          <span className={`info-value status ${snapshot.isCreating ? 'creating' : 'ready'}`}>
            {snapshot.isCreating ? 'CREATING...' : 'READY'}
          </span>
        </div>
      </div>
      
      <div className="snapshot-controls">
        <button 
          className={`snapshot-button ${snapshot.isCreating ? 'loading' : ''}`}
          onClick={() => createSnapshot(false)}
          disabled={snapshot.isCreating}
        >
          {snapshot.isCreating ? (
            <>
              <span className="loading-spinner"></span>
              Creating...
            </>
          ) : (
            '📸 Save Snapshot'
          )}
        </button>
        
        <div className="auto-save-controls">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={snapshot.autoSaveEnabled}
              onChange={toggleAutoSave}
              className="auto-save-checkbox"
            />
            <span className="checkbox-custom"></span>
            Auto-Save (5min / high entropy)
          </label>
          
          {snapshot.autoSaveEnabled && (
            <div className="countdown-display">
              <span className="countdown-label">Next auto-save:</span>
              <span className="countdown-value">
                {formatCountdown(snapshot.autoSaveCountdown)}
              </span>
            </div>
          )}
        </div>
      </div>
      
      <div className="snapshot-footer">
        {snapshot.lastResult === 'success' && (
          <span className="result-message success">
            ✅ Mindstate captured successfully
          </span>
        )}
        {snapshot.lastResult === 'error' && (
          <span className="result-message error">
            ❌ Snapshot failed - check backend connection
          </span>
        )}
        {!snapshot.lastResult && (
          <span className="result-message idle">
            Ready to preserve cognitive state
          </span>
        )}
      </div>
    </div>
  )
}

export default SnapshotTriggerPanel 