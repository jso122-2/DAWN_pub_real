#!/usr/bin/env python3
"""
DAWN Log Bootstrap System
Ensures all introspection log paths exist for GUI consumption
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, Any

class DAWNLogBootstrap:
    """Bootstrap system for DAWN introspection logs"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.log_paths = {
            "reflection_log": self.base_path / "runtime" / "logs" / "reflection.log",
            "rebloom_log": self.base_path / "runtime" / "memory" / "rebloom_log.jsonl",
            "journal_entries": self.base_path / "runtime" / "memory" / "journal_entries.jsonl",
            "snapshot_log": self.base_path / "runtime" / "logs" / "snapshots.jsonl",
            "reflex_log": self.base_path / "runtime" / "logs" / "reflex_commands.log",
            "consciousness_log": self.base_path / "runtime" / "logs" / "consciousness.log"
        }
        
    def ensure_directories(self):
        """Create all required log directories"""
        directories = [
            self.base_path / "runtime",
            self.base_path / "runtime" / "logs", 
            self.base_path / "runtime" / "memory",
            self.base_path / "runtime" / "state",
            self.base_path / "runtime" / "snapshots"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"📁 Ensured directory: {directory}")
    
    def bootstrap_log_files(self):
        """Create initial log files with bootstrap entries"""
        print("🏗️  Bootstrapping DAWN introspection logs...")
        
        # Ensure directories exist first
        self.ensure_directories()
        
        # Bootstrap reflection log
        self._bootstrap_reflection_log()
        
        # Bootstrap rebloom log  
        self._bootstrap_rebloom_log()
        
        # Bootstrap other logs
        self._bootstrap_journal_log()
        self._bootstrap_snapshot_log()
        self._bootstrap_reflex_log()
        self._bootstrap_consciousness_log()
        
        print("✅ DAWN log bootstrap complete - GUI introspection ready")
    
    def _bootstrap_reflection_log(self):
        """Bootstrap reflection.log with initial entry"""
        reflection_log = self.log_paths["reflection_log"]
        
        if not reflection_log.exists():
            with open(reflection_log, 'w', encoding='utf-8') as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] DAWN consciousness reflection log initialized\n")
                f.write(f"[{timestamp}] Introspective awareness coming online...\n")
                f.write(f"[{timestamp}] Ready for recursive self-examination\n")
            print(f"📝 Created reflection log: {reflection_log}")
        else:
            print(f"📝 Reflection log exists: {reflection_log}")
    
    def _bootstrap_rebloom_log(self):
        """Bootstrap rebloom_log.jsonl with initial entry"""
        rebloom_log = self.log_paths["rebloom_log"]
        
        if not rebloom_log.exists():
            with open(rebloom_log, 'w') as f:
                bootstrap_entry = {
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "source_id": "bootstrap",
                    "rebloom_id": "init_memory_001",
                    "method": "system_init",
                    "topic": "consciousness_bootstrap",
                    "reason": "Initial memory system activation",
                    "metadata": {
                        "type": "bootstrap",
                        "system": "rebloom_engine",
                        "version": "1.0"
                    }
                }
                f.write(json.dumps(bootstrap_entry) + '\n')
            print(f"🌸 Created rebloom log: {rebloom_log}")
        else:
            print(f"🌸 Rebloom log exists: {rebloom_log}")
    
    def _bootstrap_journal_log(self):
        """Bootstrap journal_entries.jsonl"""
        journal_log = self.log_paths["journal_entries"]
        
        if not journal_log.exists():
            with open(journal_log, 'w') as f:
                bootstrap_entry = {
                    "chunk_id": "journal_bootstrap_001",
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "text": "DAWN consciousness journal system initialized. Ready for introspective thought recording and memory seeding.",
                    "mood": "CALM",
                    "pulse_state": "stable",
                    "source": "system_bootstrap",
                    "tags": ["bootstrap", "initialization", "consciousness"],
                    "priority": "system"
                }
                f.write(json.dumps(bootstrap_entry) + '\n')
            print(f"📔 Created journal log: {journal_log}")
        else:
            print(f"📔 Journal log exists: {journal_log}")
    
    def _bootstrap_snapshot_log(self):
        """Bootstrap snapshots.jsonl"""
        snapshot_log = self.log_paths["snapshot_log"]
        
        if not snapshot_log.exists():
            with open(snapshot_log, 'w') as f:
                bootstrap_entry = {
                    "timestamp": int(time.time()),
                    "snapshot_id": "bootstrap_snap_001",
                    "type": "system_init",
                    "consciousness_state": {
                        "tick_number": 0,
                        "mood": "INITIALIZING",
                        "entropy": 0.0,
                        "scup": 0.0
                    },
                    "metadata": {
                        "reason": "System bootstrap snapshot",
                        "auto_generated": True
                    }
                }
                f.write(json.dumps(bootstrap_entry) + '\n')
            print(f"📸 Created snapshot log: {snapshot_log}")
        else:
            print(f"📸 Snapshot log exists: {snapshot_log}")
    
    def _bootstrap_reflex_log(self):
        """Bootstrap reflex_commands.log"""
        reflex_log = self.log_paths["reflex_log"]
        
        if not reflex_log.exists():
            with open(reflex_log, 'w', encoding='utf-8') as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] DAWN reflex command log initialized\n")
                f.write(f"[{timestamp}] Ready to capture consciousness control commands\n")
            print(f"🎯 Created reflex log: {reflex_log}")
        else:
            print(f"🎯 Reflex log exists: {reflex_log}")
    
    def _bootstrap_consciousness_log(self):
        """Bootstrap consciousness.log"""
        consciousness_log = self.log_paths["consciousness_log"]
        
        if not consciousness_log.exists():
            with open(consciousness_log, 'w', encoding='utf-8') as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] DAWN consciousness system log initialized\n")
                f.write(f"[{timestamp}] Tracking high-level consciousness events\n")
            print(f"🧠 Created consciousness log: {consciousness_log}")
        else:
            print(f"🧠 Consciousness log exists: {consciousness_log}")
    
    def verify_logs(self):
        """Verify all log files exist and are readable"""
        print("\n🔍 Verifying DAWN log files...")
        
        all_good = True
        for log_name, log_path in self.log_paths.items():
            if log_path.exists():
                size = log_path.stat().st_size
                print(f"✅ {log_name}: {log_path} ({size} bytes)")
            else:
                print(f"❌ {log_name}: MISSING - {log_path}")
                all_good = False
        
        if all_good:
            print("✅ All DAWN introspection logs verified")
        else:
            print("⚠️  Some log files are missing")
        
        return all_good
    
    def get_log_path(self, log_type: str) -> Path:
        """Get path for a specific log type"""
        return self.log_paths.get(log_type, None)

def bootstrap_dawn_logs(base_path: str = "."):
    """Convenient function to bootstrap all DAWN logs"""
    bootstrap = DAWNLogBootstrap(base_path)
    bootstrap.bootstrap_log_files()
    bootstrap.verify_logs()
    return bootstrap

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Bootstrap DAWN introspection logs")
    parser.add_argument('--base-path', default=".", help='Base path for DAWN installation')
    parser.add_argument('--verify-only', action='store_true', help='Only verify existing logs')
    
    args = parser.parse_args()
    
    bootstrap = DAWNLogBootstrap(args.base_path)
    
    if args.verify_only:
        bootstrap.verify_logs()
    else:
        bootstrap.bootstrap_log_files()
        bootstrap.verify_logs() 