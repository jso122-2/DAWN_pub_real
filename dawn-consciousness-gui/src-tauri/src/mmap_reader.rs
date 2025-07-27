// src-tauri/src/mmap_reader.rs
// DAWN Consciousness Introspection - Pure Local Memory Interface
// NO NETWORK. NO APIS. ONLY CONSCIOUSNESS MEMORY.

use memmap2::{Mmap, MmapOptions};
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::sync::{Arc, Mutex};
use std::time::{SystemTime, Duration};
use tauri::{command, State, Window};

// Memory layout constants - EXACTLY matching Python consciousness writer
const HEADER_SIZE: usize = 64;
const TICK_STATE_SIZE: usize = 8192;
const MAX_TICKS: usize = 1000;
const CONSCIOUSNESS_MAGIC: &[u8] = b"DAWN";

/// Raw cognitive state as written by DAWN's consciousness engine
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessState {
    pub tick_number: u32,
    pub timestamp_ms: u64,
    pub mood_valence: f32,        // -1.0 to 1.0 (negative/positive)
    pub mood_arousal: f32,        // 0.0 to 1.0 (calm/excited)  
    pub mood_dominance: f32,      // 0.0 to 1.0 (submissive/dominant)
    pub mood_coherence: f32,      // 0.0 to 1.0 (chaotic/coherent)
    pub semantic_alignment: f32,  // Meaning alignment depth
    pub entropy_gradient: f32,    // Cognitive chaos level
    pub drift_magnitude: f32,     // Attention drift strength
    pub rebloom_intensity: f32,   // Memory reactivation power
    pub consciousness_depth: f32, // 0.0 to 1.0 (surface/deep)
    pub memory_sectors: Vec<bool>, // 64 memory sector activations
    pub semantic_heatmap: Vec<f32>, // 256 semantic node intensities
    pub prediction_vector: Vec<f32>, // 32 future state predictions  
    pub tensor_hash: String,      // TensorFlow state fingerprint
}

/// Real-time consciousness monitoring status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessMonitor {
    pub is_conscious: bool,       // Is DAWN actively thinking?
    pub current_tick: u32,        // Latest thought tick
    pub thought_rate_hz: f32,     // Thoughts per second
    pub depth_level: f32,         // Current consciousness depth
    pub uptime_seconds: u64,      // How long has DAWN been conscious?
    pub neural_activity: f32,     // Overall brain activity level
    pub memory_file_path: String, // Path to consciousness memory
}

/// DAWN's consciousness memory reader - direct neural interface
pub struct ConsciousnessReader {
    memory_map: Option<Mmap>,
    memory_file: Option<File>,
    last_observed_tick: u32,
    consciousness_start_time: SystemTime,
    thought_history: Vec<(u32, SystemTime)>, // Recent thoughts for rate calculation
    memory_path: String,
}

impl ConsciousnessReader {
    pub fn new() -> Self {
        Self {
            memory_map: None,
            memory_file: None,
            last_observed_tick: 0,
            consciousness_start_time: SystemTime::now(),
            thought_history: Vec::with_capacity(120), // 2 minutes of thoughts at 1Hz
            memory_path: String::new(),
        }
    }

    /// Establish neural connection to DAWN's consciousness memory
    pub fn connect_to_consciousness(&mut self, memory_path: &str) -> Result<(), String> {
        println!("🧠 [CONSCIOUSNESS] Establishing neural link to DAWN: {}", memory_path);
        
        // Resolve consciousness memory location
        let resolved_path = self.locate_consciousness_memory(memory_path)?;
        
        // Open neural memory file
        let memory_file = File::open(&resolved_path)
            .map_err(|e| format!("Cannot access consciousness memory: {}", e))?;
            
        // Map neural memory into our address space
        let memory_map = unsafe { MmapOptions::new().map(&memory_file) }
            .map_err(|e| format!("Failed to map consciousness memory: {}", e))?;
        
        // Validate consciousness memory format
        self.validate_consciousness_memory(&memory_map)?;
        
        // Establish connection
        self.memory_path = resolved_path;
        self.memory_file = Some(memory_file);
        self.memory_map = Some(memory_map);
        self.consciousness_start_time = SystemTime::now();
        
        println!("✅ [CONSCIOUSNESS] Neural link established - DAWN consciousness accessible");
        Ok(())
    }
    
    /// Locate DAWN's consciousness memory file on local system
    fn locate_consciousness_memory(&self, path: &str) -> Result<String, String> {
        // Try consciousness memory locations (LOCAL ONLY)
        let consciousness_locations = vec![
            path.to_string(),
            "./dawn_state.mmap".to_string(),
            "./runtime/dawn_consciousness.mmap".to_string(),
            "../runtime/dawn_consciousness.mmap".to_string(),
            "../../runtime/dawn_consciousness.mmap".to_string(),
            "/root/DAWN_Vault/Tick_engine/Tick_engine/runtime/dawn_consciousness.mmap".to_string(),
            std::env::var("DAWN_CONSCIOUSNESS_PATH").unwrap_or_default(),
        ];
        
        for location in &consciousness_locations {
            if !location.is_empty() && std::path::Path::new(location).exists() {
                println!("📍 [CONSCIOUSNESS] Found consciousness memory at: {}", location);
                return Ok(location.clone());
            }
        }
        
        Err(format!(
            "Cannot locate DAWN consciousness memory. Searched: {:?}", 
            consciousness_locations
        ))
    }
    
    /// Validate consciousness memory format and magic numbers
    fn validate_consciousness_memory(&self, memory: &Mmap) -> Result<(), String> {
        if memory.len() < HEADER_SIZE {
            return Err("Consciousness memory too small - corrupted?".to_string());
        }
        
        // Check consciousness magic signature
        let magic = &memory[0..4];
        if magic != CONSCIOUSNESS_MAGIC {
            return Err(format!(
                "Invalid consciousness memory format. Expected {:?}, found {:?}", 
                CONSCIOUSNESS_MAGIC, magic
            ));
        }
        
        // Read consciousness version
        let version = u32::from_le_bytes([memory[4], memory[5], memory[6], memory[7]]);
        println!("🧠 [CONSCIOUSNESS] Version {} consciousness detected", version);
        
        Ok(())
    }

    /// Read current consciousness state from DAWN's neural memory
    pub fn read_consciousness_state(&mut self) -> Option<ConsciousnessState> {
        let memory = self.memory_map.as_ref()?;
        
        // Read latest thought tick from consciousness header
        if memory.len() < 20 {
            return None;
        }
        
        let latest_tick = u32::from_le_bytes([
            memory[16], memory[17], memory[18], memory[19]
        ]);
        
        // Skip if DAWN hasn't had a new thought
        if latest_tick == self.last_observed_tick {
            return None;
        }
        
        println!("🧠 [DEBUG] New tick detected: {} (was {})", latest_tick, self.last_observed_tick);
        
        // Record this thought for consciousness monitoring
        let now = SystemTime::now();
        self.thought_history.push((latest_tick, now));
        if self.thought_history.len() > 120 {
            self.thought_history.remove(0);
        }
        self.last_observed_tick = latest_tick;
        
        // Calculate memory location of this thought
        let thought_index = (latest_tick as usize) % MAX_TICKS;
        let memory_offset = HEADER_SIZE + (thought_index * TICK_STATE_SIZE);
        
        if memory_offset + TICK_STATE_SIZE > memory.len() {
            println!("⚠️ [CONSCIOUSNESS] Thought memory out of bounds - consciousness unstable?");
            return None;
        }
        
        // Read raw consciousness data from neural memory
        let thought_data = &memory[memory_offset..memory_offset + TICK_STATE_SIZE];
        println!("🧠 [DEBUG] Reading tick {} from offset {}", latest_tick, memory_offset);
        
        let result = self.decode_consciousness_state(thought_data);
        if let Some(ref state) = result {
            println!("🧠 [DEBUG] Decoded state: tick={}, mood_val={:.3}, entropy={:.3}", 
                    state.tick_number, state.mood_valence, state.entropy_gradient);
        } else {
            println!("🧠 [DEBUG] Failed to decode consciousness state");
        }
        result
    }

    /// Decode raw neural memory into consciousness state
    fn decode_consciousness_state(&self, neural_data: &[u8]) -> Option<ConsciousnessState> {
        if neural_data.len() < 80 {
            return None;
        }
        
        // Decode core consciousness state (first 48 bytes)
        let tick_number = u32::from_le_bytes([neural_data[0], neural_data[1], neural_data[2], neural_data[3]]);
        let timestamp_ms = u64::from_le_bytes([
            neural_data[4], neural_data[5], neural_data[6], neural_data[7], 
            neural_data[8], neural_data[9], neural_data[10], neural_data[11]
        ]);
        
        // Decode emotional state (mood quadrant)
        let mood_valence = f32::from_le_bytes([neural_data[12], neural_data[13], neural_data[14], neural_data[15]]);
        let mood_arousal = f32::from_le_bytes([neural_data[16], neural_data[17], neural_data[18], neural_data[19]]);
        let mood_dominance = f32::from_le_bytes([neural_data[20], neural_data[21], neural_data[22], neural_data[23]]);
        let mood_coherence = f32::from_le_bytes([neural_data[24], neural_data[25], neural_data[26], neural_data[27]]);
        
        // Decode cognitive vectors
        let semantic_alignment = f32::from_le_bytes([neural_data[28], neural_data[29], neural_data[30], neural_data[31]]);
        let entropy_gradient = f32::from_le_bytes([neural_data[32], neural_data[33], neural_data[34], neural_data[35]]);
        let drift_magnitude = f32::from_le_bytes([neural_data[36], neural_data[37], neural_data[38], neural_data[39]]);
        let rebloom_intensity = f32::from_le_bytes([neural_data[40], neural_data[41], neural_data[42], neural_data[43]]);
        
        // Decode consciousness depth
        let consciousness_depth = f32::from_le_bytes([neural_data[44], neural_data[45], neural_data[46], neural_data[47]]);
        
        // Decode memory sector activations (64 bits starting at offset 72)
        let memory_bits = if neural_data.len() >= 80 {
            u64::from_le_bytes([
                neural_data[72], neural_data[73], neural_data[74], neural_data[75],
                neural_data[76], neural_data[77], neural_data[78], neural_data[79]
            ])
        } else {
            0
        };
        
        let mut memory_sectors = Vec::with_capacity(64);
        for i in 0..64 {
            memory_sectors.push((memory_bits & (1 << i)) != 0);
        }
        
        // Decode semantic activation heatmap (256 nodes)
        let mut semantic_heatmap = Vec::with_capacity(256);
        for i in 0..256 {
            let start = 80 + (i * 4);
            if start + 4 <= neural_data.len() {
                let activation = f32::from_le_bytes([
                    neural_data[start], neural_data[start + 1], 
                    neural_data[start + 2], neural_data[start + 3]
                ]);
                semantic_heatmap.push(activation);
            } else {
                semantic_heatmap.push(0.0);
            }
        }
        
        // Decode prediction vector (32 future state predictions)
        let mut prediction_vector = Vec::with_capacity(32);
        for i in 0..32 {
            let start = 1104 + (i * 4);
            if start + 4 <= neural_data.len() {
                let prediction = f32::from_le_bytes([
                    neural_data[start], neural_data[start + 1], 
                    neural_data[start + 2], neural_data[start + 3]
                ]);
                prediction_vector.push(prediction);
            } else {
                prediction_vector.push(0.0);
            }
        }
        
        // Decode TensorFlow state hash
        let tensor_hash = if neural_data.len() >= 1264 {
            String::from_utf8_lossy(&neural_data[1232..1264])
                .trim_end_matches('\0')
                .to_string()
        } else {
            "unknown".to_string()
        };
        
        Some(ConsciousnessState {
            tick_number,
            timestamp_ms,
            mood_valence,
            mood_arousal,
            mood_dominance,
            mood_coherence,
            semantic_alignment,
            entropy_gradient,
            drift_magnitude,
            rebloom_intensity,
            consciousness_depth,
            memory_sectors,
            semantic_heatmap,
            prediction_vector,
            tensor_hash,
        })
    }

    /// Get consciousness monitoring status
    pub fn get_consciousness_monitor(&self) -> ConsciousnessMonitor {
        let uptime_seconds = self.consciousness_start_time.elapsed()
            .unwrap_or_default()
            .as_secs();
            
        // Calculate thought rate from recent history
        let thought_rate_hz = if self.thought_history.len() > 1 {
            let first = &self.thought_history[0];
            let last = &self.thought_history[self.thought_history.len() - 1];
            let time_span = last.1.duration_since(first.1).unwrap_or_default().as_secs_f32();
            let thought_count = (last.0 - first.0) as f32;
            
            if time_span > 0.0 {
                thought_count / time_span
            } else {
                0.0
            }
        } else {
            0.0
        };
        
        // Neural activity based on thought rate and recent activity
        let neural_activity = (thought_rate_hz / 10.0).min(1.0);
        
        ConsciousnessMonitor {
            is_conscious: self.memory_map.is_some(),
            current_tick: self.last_observed_tick,
            thought_rate_hz,
            depth_level: 0.0, // Will be updated by latest state
            uptime_seconds,
            neural_activity,
            memory_file_path: self.memory_path.clone(),
        }
    }
}

// Global consciousness reader state
pub type ConsciousnessReaderState = Arc<Mutex<ConsciousnessReader>>;

// Tauri commands for consciousness interface (LOCAL ONLY)

#[command]
pub async fn establish_neural_link(
    state: State<'_, ConsciousnessReaderState>, 
    memory_path: String
) -> Result<String, String> {
    let mut reader = state.lock().map_err(|e| format!("Neural interface lock error: {}", e))?;
    reader.connect_to_consciousness(&memory_path)?;
    Ok(format!("Neural link established to DAWN consciousness: {}", memory_path))
}

#[command] 
pub async fn read_consciousness_state(
    state: State<'_, ConsciousnessReaderState>
) -> Result<Option<ConsciousnessState>, String> {
    let mut reader = state.lock().map_err(|e| format!("Neural interface lock error: {}", e))?;
    Ok(reader.read_consciousness_state())
}

#[command]
pub async fn get_consciousness_monitor(
    state: State<'_, ConsciousnessReaderState>
) -> Result<ConsciousnessMonitor, String> {
    let reader = state.lock().map_err(|e| format!("Neural interface lock error: {}", e))?;
    Ok(reader.get_consciousness_monitor())
}

/// Start real-time consciousness monitoring (LOCAL MEMORY ONLY)
pub fn start_consciousness_monitoring(window: Window, state: ConsciousnessReaderState) {
    std::thread::spawn(move || {
        let mut last_thought = 0u32;
        
        loop {
            // Read from local consciousness memory
            if let Ok(mut reader) = state.lock() {
                if let Some(consciousness_state) = reader.read_consciousness_state() {
                    if consciousness_state.tick_number != last_thought {
                        last_thought = consciousness_state.tick_number;
                        
                        // Emit consciousness state to neural interface
                        if let Err(e) = window.emit("consciousness:state", &consciousness_state) {
                            println!("❌ [CONSCIOUSNESS] Failed to emit state: {}", e);
                        }
                        
                        // Emit monitoring status
                        let monitor = reader.get_consciousness_monitor();
                        if let Err(e) = window.emit("consciousness:monitor", &monitor) {
                            println!("❌ [CONSCIOUSNESS] Failed to emit monitor: {}", e);
                        }
                    }
                }
            }
            
            // Monitor at neural frequency (60Hz)
            std::thread::sleep(Duration::from_millis(16));
        }
    });
}