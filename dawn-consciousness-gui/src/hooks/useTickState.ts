// Check if we're running in Tauri environment
const isTauri = typeof window !== 'undefined' && (window as any).__TAURI__;

// Tauri API import
const getTauriListen = async () => {
  if (!isTauri) return null;
  
  try {
    const { listen } = await import('@tauri-apps/api/event');
    return listen;
  } catch (e) {
    console.warn('Tauri listen API not available, using fallback mode');
    return null;
  }
};

// DAWN cognitive state type
export type DawnState = {
  tick_number: number
  mood: string
  entropy: number
  scup: number
  heat?: number
  zone?: string
  sigils?: number
}

// Subscriber function type
type SubscriberFn = (state: DawnState) => void
type UnsubscribeFn = () => void

// Internal state - not React state to avoid re-renders
let currentState: DawnState | null = null
let subscribers: SubscriberFn[] = []
let isInitialized = false
let tauriUnlisten: (() => void) | null = null

/**
 * Get the most recent DAWN cognitive state
 * @returns Current DawnState or null if no data received yet
 */
export function get(): DawnState | null {
  if (currentState) {
    console.log('📊 [GET] Returning current state:', currentState)
  } else {
    console.log('📊 [GET] No current state available')
  }
  return currentState
}

/**
 * Subscribe to DAWN state updates
 * @param fn Callback function called on each tick update
 * @returns Function to unsubscribe
 */
export function subscribe(fn: SubscriberFn): UnsubscribeFn {
  // Add subscriber to list
  subscribers.push(fn)
  console.log(`📝 [SUBSCRIBE] New subscriber added. Total subscribers: ${subscribers.length}`)
  
  // Return unsubscribe function
  return () => {
    const index = subscribers.indexOf(fn)
    if (index > -1) {
      subscribers.splice(index, 1)
      console.log(`📝 [UNSUBSCRIBE] Subscriber removed. Total subscribers: ${subscribers.length}`)
    }
  }
}

/**
 * Initialize the tick state listener
 * Should only be called once in main.tsx or root layout
 */
export async function init(): Promise<void> {
  if (isInitialized) {
    console.warn('useTickState already initialized')
    return
  }

  try {
    console.log('🔄 Initializing DAWN tick state listener...')
    
    const listen = await getTauriListen();
    
    if (!listen) {
      console.log('⚠️ [INIT] Tauri not available, starting debug mode immediately...')
      startDebugMode()
      isInitialized = true
      return
    }
    
    // Listen for tick_update events from Tauri backend (v1.x syntax)
    tauriUnlisten = await listen<DawnState>('tick_update', (event: any) => {
      console.log('🎯 [TICK UPDATE] Raw event received:', event)
      console.log('📦 [TICK UPDATE] Event payload:', event.payload)
      
      const newState = event.payload
      
      // Validate payload structure
      if (!newState || typeof newState !== 'object') {
        console.error('❌ [TICK UPDATE] Invalid payload structure:', newState)
        return
      }
      
      // Log individual fields for debugging
      console.log('🧠 [TICK UPDATE] Parsed state:', {
        tick_number: newState.tick_number,
        mood: newState.mood,
        entropy: newState.entropy,
        scup: newState.scup,
        heat: newState.heat,
        zone: newState.zone,
        sigils: newState.sigils
      })
      
      // Update current state
      currentState = newState
      
      // Notify all subscribers
      console.log(`📢 [TICK UPDATE] Notifying ${subscribers.length} subscribers`)
      subscribers.forEach((subscriber, index) => {
        try {
          subscriber(newState)
        } catch (error) {
          console.error(`❌ Error in tick state subscriber ${index}:`, error)
        }
      })
    })
    
    isInitialized = true
    console.log('✅ DAWN tick state listener initialized successfully')
    console.log('👂 Listening for "tick_update" events from Tauri backend')
    
    // Start debug mode after 5 seconds if no real data received
    setTimeout(() => {
      if (!currentState) {
        console.log('⚠️ [DEBUG] No real data received after 5s, starting debug mode...')
        startDebugMode()
      }
    }, 5000)
    
  } catch (error) {
    console.error('❌ Failed to initialize tick state listener:', error)
    
    // Fallback to debug mode if Tauri setup fails
    console.log('🔄 [DEBUG] Starting debug mode as fallback...')
    startDebugMode()
    isInitialized = true
  }
}

/**
 * Cleanup the tick state listener
 * Called on app shutdown or hot reload
 */
export function cleanup(): void {
  if (tauriUnlisten) {
    tauriUnlisten()
    tauriUnlisten = null
  }
  
  // Clean up debug interval if running
  if ((window as any).debugInterval) {
    clearInterval((window as any).debugInterval)
    ;(window as any).debugInterval = null
    console.log('🧹 Debug mode stopped')
  }
  
  subscribers.length = 0
  currentState = null
  isInitialized = false
  
  console.log('🧹 DAWN tick state cleaned up')
}

/**
 * Stop debug mode
 */
export function stopDebugMode(): void {
  if ((window as any).debugInterval) {
    clearInterval((window as any).debugInterval)
    ;(window as any).debugInterval = null
    console.log('🛑 [DEBUG] Debug mode stopped manually')
  } else {
    console.log('ℹ️ [DEBUG] Debug mode is not running')
  }
}

/**
 * Get current subscriber count (for debugging)
 */
export function getSubscriberCount(): number {
  return subscribers.length
}

/**
 * Get initialization status (for debugging)
 */
export function getInitStatus(): boolean {
  return isInitialized
}

/**
 * Start debug mode with simulated data
 */
function startDebugMode(): void {
  console.log('🔥 [DEBUG MODE] Starting simulated DAWN data stream...')
  
  let debugTick = 1000000
  
  const debugInterval = setInterval(() => {
    debugTick++
    
    const testState: DawnState = {
      tick_number: debugTick,
      mood: ['CALM', 'EXCITED', 'FOCUSED', 'DEEP'][Math.floor(Math.random() * 4)],
      entropy: Math.random() * 0.8 + 0.1, // Random 0.1-0.9
      scup: Math.random() * 80 + 10,       // Random 10-90
      heat: Math.random() * 0.6 + 0.2,     // Random 0.2-0.8
      zone: ['GREEN', 'YELLOW', 'ORANGE'][Math.floor(Math.random() * 3)],
      sigils: Math.floor(Math.random() * 5)
    }
    
    // Update current state
    currentState = testState
    
    // Notify subscribers
    subscribers.forEach((subscriber) => {
      try {
        subscriber(testState)
      } catch (error) {
        console.error('❌ [DEBUG] Error in subscriber:', error)
      }
    })
  }, 200) // 5Hz update rate
  
  // Store interval ID for cleanup
  ;(window as any).debugInterval = debugInterval
}

/**
 * Test function to manually inject data for debugging
 * Call this from browser console: window.testDawnData()
 */
export function injectTestData(): void {
  console.log('🧪 [TEST] Injecting test data...')
  
  const testState: DawnState = {
    tick_number: Math.floor(Date.now() / 1000),
    mood: 'TESTING',
    entropy: Math.random() * 0.8 + 0.1, // Random 0.1-0.9
    scup: Math.random() * 80 + 10,       // Random 10-90
    heat: Math.random() * 0.6 + 0.2,     // Random 0.2-0.8
    zone: 'YELLOW',
    sigils: Math.floor(Math.random() * 5)
  }
  
  console.log('🧪 [TEST] Test state:', testState)
  
  // Update current state
  currentState = testState
  
  // Notify subscribers
  console.log(`🧪 [TEST] Notifying ${subscribers.length} subscribers`)
  subscribers.forEach((subscriber, index) => {
    try {
      subscriber(testState)
    } catch (error) {
      console.error(`❌ [TEST] Error in subscriber ${index}:`, error)
    }
  })
}

// Make test function available globally for debugging
if (typeof window !== 'undefined') {
  ;(window as any).testDawnData = injectTestData
  ;(window as any).startDebugMode = startDebugMode
  ;(window as any).stopDebugMode = stopDebugMode
  ;(window as any).dawnDebug = {
    get,
    getSubscriberCount,
    getInitStatus,
    injectTestData,
    startDebugMode,
    stopDebugMode
  }
}

// Export default object with all functions
export default {
  get,
  subscribe,
  init,
  cleanup,
  getSubscriberCount,
  getInitStatus,
  injectTestData,
  stopDebugMode
} 