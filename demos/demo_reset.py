#!/usr/bin/env python3
"""
DAWN Demo Reset - Clean State Reset Without Wiping Config
========================================================

Utility that clears DAWN's memory, logs, and state artifacts while preserving
runtime config, UUIDs, and GUI structure. Perfect for starting fresh demos
without losing system configuration.

Usage:
    python demo_reset.py                    # Interactive confirmation
    python demo_reset.py --silent           # Auto-confirm
    python demo_reset.py --preserve-reflections  # Keep reflection.log
    python demo_reset.py --dry-run          # Show what would be deleted
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import List, Set

def print_banner():
    """Print the demo reset banner"""
    print("🧠" + "=" * 60 + "🧠")
    print("   DAWN Demo Reset - Clean Consciousness Baseline")
    print("🧠" + "=" * 60 + "🧠")
    print()

def get_files_to_remove(preserve_reflections: bool = False) -> List[Path]:
    """Get list of files to be removed"""
    base_path = Path(".")
    files_to_remove = []
    
    # Runtime logs to clear
    runtime_logs = base_path / "runtime" / "logs"
    if runtime_logs.exists():
        log_patterns = [
            "*.log",
            "event_stream.log",
            "tracer_alerts.log", 
            "root_trace.log",
            "spoken_trace.log",
            "sigil_trace.log"
        ]
        
        for pattern in log_patterns:
            for log_file in runtime_logs.glob(pattern):
                # Preserve reflections if requested
                if preserve_reflections and log_file.name == "reflection.log":
                    continue
                files_to_remove.append(log_file)
    
    # Memory files to clear
    runtime_memory = base_path / "runtime" / "memory"
    if runtime_memory.exists():
        memory_patterns = [
            "rebloom_log.jsonl",
            "mycelium_graph.json",
            "lineage_log.jsonl",
            "memory_cache.pkl"
        ]
        
        for pattern in memory_patterns:
            for memory_file in runtime_memory.glob(pattern):
                files_to_remove.append(memory_file)
    
    # State directories to clear
    state_dirs = [
        base_path / "runtime" / "state",
        base_path / "state", 
        base_path / "pulse",
        base_path / "memories"
    ]
    
    for state_dir in state_dirs:
        if state_dir.exists():
            for item in state_dir.rglob("*"):
                if item.is_file() and item.suffix in ['.pkl', '.json', '.log', '.tmp']:
                    files_to_remove.append(item)
    
    # Backend logs and temp files
    backend_logs = base_path / "backend" / "logs"
    if backend_logs.exists():
        for log_file in backend_logs.glob("*.log"):
            files_to_remove.append(log_file)
    
    # Snapshots (except config snapshots)
    snapshots_dir = base_path / "runtime" / "snapshots"
    if snapshots_dir.exists():
        for snapshot in snapshots_dir.glob("semantic_trace_*.json"):
            files_to_remove.append(snapshot)
    
    return files_to_remove

def get_files_to_preserve() -> Set[str]:
    """Get set of files that should be preserved"""
    return {
        "tick_config.json",
        "gui_config.json", 
        "settings.env",
        "version.txt",
        "config.yaml",
        "cursor_guard.yaml",
        ".env",
        "requirements.txt",
        "README.md",
        "INTEGRATION_COMPLETE.md",
        "COMPLETE_SYMBOLIC_INTEGRATION_SUCCESS.md"
    }

def show_reset_plan(files_to_remove: List[Path], preserve_reflections: bool = False):
    """Show what files will be removed"""
    print("📋 Reset Plan:")
    print("-" * 40)
    
    if not files_to_remove:
        print("✅ No files to remove - state already clean")
        return
    
    # Group by directory
    by_directory = {}
    for file_path in files_to_remove:
        dir_name = str(file_path.parent)
        if dir_name not in by_directory:
            by_directory[dir_name] = []
        by_directory[dir_name].append(file_path.name)
    
    for directory, files in by_directory.items():
        print(f"📁 {directory}:")
        for file_name in sorted(files):
            print(f"   🗑️  {file_name}")
    
    print(f"\n📊 Summary:")
    print(f"   Files to remove: {len(files_to_remove)}")
    print(f"   Preserve reflections: {'Yes' if preserve_reflections else 'No'}")
    
    # Show what will be preserved
    preserved = get_files_to_preserve()
    if preserve_reflections:
        preserved.add("reflection.log")
    
    print(f"\n✅ Files Preserved:")
    for preserved_file in sorted(preserved):
        if Path(preserved_file).exists():
            print(f"   🛡️  {preserved_file}")

def confirm_reset(silent: bool = False) -> bool:
    """Confirm the reset operation with user"""
    if silent:
        return True
    
    print("\n⚠️  WARNING: This will delete DAWN's memory, logs, and state data!")
    print("   Configuration files will be preserved.")
    
    while True:
        response = input("\n🤔 Are you sure you want to reset DAWN state? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def perform_reset(files_to_remove: List[Path], dry_run: bool = False) -> tuple:
    """Perform the actual reset operation"""
    removed_count = 0
    error_count = 0
    
    print(f"\n🧹 {'[DRY RUN] ' if dry_run else ''}Starting reset...")
    
    for file_path in files_to_remove:
        try:
            if file_path.exists():
                if not dry_run:
                    file_path.unlink()
                print(f"   ✅ {'[DRY] ' if dry_run else ''}Removed: {file_path}")
                removed_count += 1
            else:
                print(f"   ⚠️  Already gone: {file_path}")
        except Exception as e:
            print(f"   ❌ Error removing {file_path}: {e}")
            error_count += 1
    
    # Clean empty directories
    empty_dirs = []
    for check_dir in [Path("runtime/logs"), Path("runtime/memory"), Path("runtime/state")]:
        if check_dir.exists() and not any(check_dir.iterdir()):
            empty_dirs.append(check_dir)
    
    if empty_dirs and not dry_run:
        print(f"\n🗂️  Cleaning empty directories...")
        for empty_dir in empty_dirs:
            try:
                empty_dir.rmdir()
                print(f"   ✅ Removed empty: {empty_dir}")
            except Exception as e:
                print(f"   ⚠️  Could not remove {empty_dir}: {e}")
    
    return removed_count, error_count

def create_fresh_directories():
    """Create fresh directory structure"""
    directories = [
        Path("runtime/logs"),
        Path("runtime/memory"), 
        Path("runtime/state"),
        Path("runtime/snapshots")
    ]
    
    print(f"\n📁 Creating fresh directory structure...")
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}")

def show_reset_summary(removed_count: int, error_count: int, dry_run: bool = False):
    """Show the reset operation summary"""
    print(f"\n{'🔍 DRY RUN SUMMARY' if dry_run else '🎉 RESET COMPLETE'}")
    print("=" * 40)
    print(f"   Files {'would be ' if dry_run else ''}removed: {removed_count}")
    
    if error_count > 0:
        print(f"   Errors encountered: {error_count}")
    else:
        print(f"   No errors")
    
    if not dry_run:
        print(f"\n🧠 DAWN consciousness baseline reset successfully!")
        print(f"   Configuration and structure preserved")
        print(f"   Ready for fresh symbolic regulation")
        print(f"   Run your cognition systems to begin new traces")

def main():
    """Main demo reset function"""
    parser = argparse.ArgumentParser(description="Reset DAWN's cognitive state while preserving configuration")
    parser.add_argument("--silent", action="store_true", help="Auto-confirm without user prompt")
    parser.add_argument("--preserve-reflections", action="store_true", help="Keep reflection.log intact")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without actually deleting")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Get files to remove
    files_to_remove = get_files_to_remove(args.preserve_reflections)
    
    # Show reset plan
    show_reset_plan(files_to_remove, args.preserve_reflections)
    
    if not files_to_remove:
        print("\n✅ DAWN state is already clean - no reset needed!")
        return
    
    # Confirm operation (unless dry run)
    if not args.dry_run:
        if not confirm_reset(args.silent):
            print("\n🚫 Reset cancelled by user")
            return
    
    # Perform reset
    removed_count, error_count = perform_reset(files_to_remove, args.dry_run)
    
    # Create fresh directories (unless dry run)
    if not args.dry_run:
        create_fresh_directories()
    
    # Show summary
    show_reset_summary(removed_count, error_count, args.dry_run)
    
    # Show next steps
    if not args.dry_run:
        print(f"\n🚀 Next Steps:")
        print(f"   1. Run: python cognition_runtime.py")
        print(f"   2. Start: python voice_symbolic_integration.py")
        print(f"   3. Launch: python complete_integration_demo.py")
        print(f"   4. Monitor: python voice_loop.py --start")

if __name__ == "__main__":
    main() 