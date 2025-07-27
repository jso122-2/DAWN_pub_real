//! DAWN Tick Handler
//! Handles real-time consciousness tick monitoring and processing

use std::sync::{Arc, Mutex, RwLock, OnceLock};
use std::thread;
use std::time::{Duration, Instant};
use serde::{Deserialize, Serialize};
use tauri::Window;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TickData {
    pub tick_id: u64,
    pub timestamp: u64,
    pub entropy: f64,
    pub scup: f64,
    pub heat: f64,
    pub active_sigils: Vec<String>,
    pub processing_status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TickMonitorState {
    pub current_tick: Option<TickData>,
    pub total_ticks: u64,
    pub monitoring_active: bool,
    pub last_update: u64,
    pub connection_status: String,
}

impl Default for TickMonitorState {
    fn default() -> Self {
        Self {
            current_tick: None,
            total_ticks: 0,
            monitoring_active: false,
            last_update: 0,
            connection_status: "Disconnected".to_string(),
        }
    }
}

pub struct TickMonitor {
    state: Arc<RwLock<TickMonitorState>>,
    monitoring_thread: Option<thread::JoinHandle<()>>,
    should_stop: Arc<Mutex<bool>>,
    connected: bool,
}

impl TickMonitor {
    pub fn new() -> Self {
        Self {
            state: Arc::new(RwLock::new(TickMonitorState::default())),
            monitoring_thread: None,
            should_stop: Arc::new(Mutex::new(false)),
            connected: false,
        }
    }

    pub fn get_state(&self) -> TickMonitorState {
        self.state.read().unwrap().clone()
    }

    pub fn connect(&mut self, memory_path: &str) -> Result<(), String> {
        println!("🔮 [TICK] Connecting to memory path: {}", memory_path);
        // In a real implementation, this would connect to the memory-mapped file
        self.connected = true;
        
        // Update connection status
        {
            let mut state = self.state.write().unwrap();
            state.connection_status = "Connected".to_string();
        }
        
        println!("🔮 [TICK] Connection established");
        Ok(())
    }

    pub fn start_monitoring(&mut self, window: Window) -> Result<(), String> {
        if !self.connected {
            return Err("Not connected to tick system".to_string());
        }

        let state_clone = Arc::clone(&self.state);
        let should_stop_clone = Arc::clone(&self.should_stop);

        // Reset stop flag
        *self.should_stop.lock().unwrap() = false;

        let handle = thread::spawn(move || {
            println!("🔮 [TICK] Starting tick monitoring thread...");
            
            let mut tick_counter = 0u64;
            let start_time = Instant::now();
            
            loop {
                // Check if we should stop
                if *should_stop_clone.lock().unwrap() {
                    println!("🔮 [TICK] Monitoring thread stopping...");
                    break;
                }

                // Simulate tick data (in a real implementation, this would read from DAWN's tick system)
                tick_counter += 1;
                let current_time = start_time.elapsed().as_secs();
                
                let tick_data = TickData {
                    tick_id: tick_counter,
                    timestamp: current_time,
                    entropy: 0.3 + (tick_counter as f64 * 0.01) % 0.4, // Simulated entropy
                    scup: 45.0 + (tick_counter as f64 * 0.5) % 20.0,  // Simulated SCUP
                    heat: 0.2 + (tick_counter as f64 * 0.01) % 0.3,   // Simulated heat
                    active_sigils: vec![], // Would be populated from sigil engine
                    processing_status: "Active".to_string(),
                };

                // Update state
                {
                    let mut state = state_clone.write().unwrap();
                    state.current_tick = Some(tick_data.clone());
                    state.total_ticks = tick_counter;
                    state.monitoring_active = true;
                    state.last_update = current_time;
                    state.connection_status = "Connected".to_string();
                }

                // Emit tick data to frontend
                if let Err(e) = window.emit("tick-update", &tick_data) {
                    println!("🔮 [TICK] Failed to emit tick update: {}", e);
                }

                // Sleep for tick interval (100ms for 10 TPS)
                thread::sleep(Duration::from_millis(100));
            }
        });

        self.monitoring_thread = Some(handle);
        println!("🔮 [TICK] Tick monitoring started");
        Ok(())
    }

    pub fn stop_monitoring(&mut self) {
        *self.should_stop.lock().unwrap() = true;
        
        if let Some(handle) = self.monitoring_thread.take() {
            let _ = handle.join();
        }

        // Update state to reflect stopped monitoring
        {
            let mut state = self.state.write().unwrap();
            state.monitoring_active = false;
            state.connection_status = if self.connected { "Connected" } else { "Disconnected" }.to_string();
        }

        println!("🔮 [TICK] Tick monitoring stopped");
    }
}

impl Drop for TickMonitor {
    fn drop(&mut self) {
        self.stop_monitoring();
    }
}

// Type alias for Tauri state management
pub type TickMonitorStateManager = Arc<Mutex<TickMonitor>>;

// Global tick monitor instance using lazy initialization
static TICK_MONITOR: OnceLock<TickMonitorStateManager> = OnceLock::new();

fn get_global_tick_monitor() -> TickMonitorStateManager {
    TICK_MONITOR.get_or_init(|| {
        Arc::new(Mutex::new(TickMonitor::new()))
    }).clone()
}

/// Tauri command: Connect to the tick monitoring system
#[tauri::command]
pub fn connect_tick_monitor() -> Result<(), String> {
    println!("🔮 [TICK] Connecting to DAWN tick monitor...");
    
    let monitor = get_global_tick_monitor();
    let mut monitor_guard = monitor.lock().unwrap();
    
    // Initialize connection (in real implementation, this would connect to DAWN's tick system)
    monitor_guard.connect("/tmp/dawn_tick_system")?;
    println!("🔮 [TICK] Tick monitor connection established");
    Ok(())
}

/// Tauri command: Get the current tick data
#[tauri::command]
pub fn get_current_tick() -> Option<TickData> {
    let monitor = get_global_tick_monitor();
    let monitor_guard = monitor.lock().unwrap();
    let state = monitor_guard.get_state();
    state.current_tick
}

/// Start tick monitoring with window for events
pub fn start_tick_monitoring(window: Window, tick_state: TickMonitorStateManager) {
    println!("🔮 [TICK] Starting tick monitoring...");
    
    // Use the provided state manager instead of global
    if let Ok(mut monitor_guard) = tick_state.lock() {
        if let Err(e) = monitor_guard.start_monitoring(window) {
            println!("🔮 [TICK] Failed to start monitoring: {}", e);
        }
    }
}

/// Get tick monitor state
pub fn get_tick_monitor_state() -> TickMonitorState {
    let monitor = get_global_tick_monitor();
    let monitor_guard = monitor.lock().unwrap();
    monitor_guard.get_state()
}

/// Stop tick monitoring
pub fn stop_tick_monitoring() {
    let monitor = get_global_tick_monitor();
    let mut monitor_guard = monitor.lock().unwrap();
    monitor_guard.stop_monitoring();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tick_monitor_creation() {
        let monitor = TickMonitor::new();
        let state = monitor.get_state();
        assert!(!state.monitoring_active);
        assert_eq!(state.total_ticks, 0);
    }

    #[test]
    fn test_connect_tick_monitor() {
        let result = connect_tick_monitor();
        assert!(result.is_ok());
    }
} 