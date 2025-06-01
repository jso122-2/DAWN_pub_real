"""
DAWN Command Watcher - Make DAWN respond to external commands
Run this to make DAWN listen for command files
"""

import json
import time
import os
from pathlib import Path
import threading

class DawnCommandWatcher:
    """Watches for command files and executes them"""
    
    def __init__(self, command_dir="dawn_commands"):
        self.command_dir = Path(command_dir)
        self.command_dir.mkdir(exist_ok=True)
        self.running = False
        self.processed_files = set()
        
        # Mock DAWN functions for testing
        self.dawn_functions = {
            'stimulate_curiosity': self.stimulate_curiosity,
            'stimulate_emotion': self.stimulate_emotion,
            'add_manual_heat': self.add_manual_heat,
            'enable_poetic_visuals': self.enable_poetic_visuals,
            'print_visual_status': self.print_visual_status,
            'print_schema_status': self.print_schema_status,
            'force_test_bloom': self.force_test_bloom,
            'debug_bloom_system': self.debug_bloom_system
        }
    
    def stimulate_curiosity(self):
        print("🔍 DAWN: Curiosity stimulated! Starting to explore...")
        print("    → Opening new pathways of thought")
        print("    → Increasing exploration drive")
        print("    → Seeking novel patterns")
        return "Curiosity activated"
    
    def stimulate_emotion(self):
        print("💝 DAWN: Emotional systems activated!")
        print("    → Valence increasing")
        print("    → Arousal heightened")
        print("    → Emotional depth engaging")
        return "Emotions stirring"
    
    def add_manual_heat(self, amount, reason="external_command"):
        print(f"🔥 DAWN: Adding {amount} units of thermal energy")
        print(f"    → Reason: {reason}")
        print(f"    → Energy systems warming up")
        print(f"    → Pulse rate increasing")
        return f"Heat added: {amount}"
    
    def enable_poetic_visuals(self):
        print("🎨 DAWN: Poetic visual systems ONLINE!")
        print("    → Aesthetic processors activated")
        print("    → Beauty recognition heightened")
        print("    → Creative visualization enabled")
        return "Poetic visuals enabled"
    
    def print_visual_status(self):
        print("📊 DAWN Visual System Status:")
        print("    → Mood Heatmap: ACTIVE")
        print("    → Bloom Visualization: READY")
        print("    → SCUP Display: MONITORING")
        print("    → Aesthetic Processing: ENABLED")
        return "Visual status printed"
    
    def print_schema_status(self):
        print("🧮 DAWN Schema Status:")
        print("    → SCUP: 0.750 (GOOD)")
        print("    → Mood: Curious and Engaged")
        print("    → Energy Level: Rising")
        print("    → Bloom Activity: Increasing")
        return "Schema status printed"
    
    def force_test_bloom(self):
        print("🌸 DAWN: Creating test bloom...")
        print("    → Seeding new memory structure")
        print("    → BLOOM_TEST_001 initiated")
        print("    → Lineage depth: 1")
        print("    → Growth potential: HIGH")
        return "Test bloom created"
    
    def debug_bloom_system(self):
        print("🔧 DAWN: Bloom system diagnostics:")
        print("    → Active blooms: 3")
        print("    → Pending synthesis: 2")
        print("    → Memory coherence: 0.85")
        print("    → Growth rate: OPTIMAL")
        return "Bloom debug complete"
    
    def process_command_file(self, filepath):
        """Process a single command file"""
        try:
            with open(filepath, 'r') as f:
                command_data = json.load(f)
            
            command = command_data.get('command')
            args = command_data.get('args', [])
            
            print(f"\n🎯 Executing command: {command}")
            
            if command in self.dawn_functions:
                if args:
                    result = self.dawn_functions[command](*args)
                else:
                    result = self.dawn_functions[command]()
                print(f"✅ Command completed: {result}")
            else:
                print(f"❓ Unknown command: {command}")
            
            # Move processed file to archive
            archive_dir = self.command_dir / "processed"
            archive_dir.mkdir(exist_ok=True)
            archive_path = archive_dir / filepath.name
            filepath.rename(archive_path)
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
    
    def watch_for_commands(self):
        """Watch for new command files"""
        print("👁️ DAWN Command Watcher ACTIVE")
        print(f"📁 Watching directory: {self.command_dir}")
        print("🎯 Ready to receive commands...\n")
        
        self.running = True
        
        while self.running:
            try:
                # Look for new command files
                command_files = list(self.command_dir.glob("cmd_*.json"))
                
                for filepath in command_files:
                    if filepath.name not in self.processed_files:
                        self.process_command_file(filepath)
                        self.processed_files.add(filepath.name)
                
                time.sleep(0.5)  # Check every 500ms
                
            except KeyboardInterrupt:
                print("\n🛑 Command watcher stopped")
                self.running = False
                break
            except Exception as e:
                print(f"⚠️ Watcher error: {e}")
                time.sleep(1)
    
    def start_watching(self):
        """Start watching in a background thread"""
        if not self.running:
            self.watcher_thread = threading.Thread(target=self.watch_for_commands)
            self.watcher_thread.daemon = True
            self.watcher_thread.start()
            return "Command watcher started"
        return "Already watching"
    
    def stop_watching(self):
        """Stop watching for commands"""
        self.running = False
        return "Command watcher stopped"

def main():
    """Main function to start the command watcher"""
    print("🌅 DAWN Command Watcher")
    print("=" * 40)
    
    watcher = DawnCommandWatcher()
    
    # Process any existing commands first
    existing_commands = list(watcher.command_dir.glob("cmd_*.json"))
    if existing_commands:
        print(f"📋 Found {len(existing_commands)} pending commands")
        for cmd_file in existing_commands:
            watcher.process_command_file(cmd_file)
        print()
    
    # Start watching for new commands
    try:
        watcher.watch_for_commands()
    except KeyboardInterrupt:
        print("\n👋 DAWN command watcher shutting down")

if __name__ == "__main__":
    main()