"""
DAWN Visual Utilities - Diagnostic and schema-aware visual tools
"""

import sys
from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime

# Import visual consciousness manager
try:
    from visual.visual_consciousness_manager import (
        VisualConsciousnessManager,
        VisualPriority,
        VisualMode,
        enable_visual_process,
        disable_visual_process
    )
    visual_manager = VisualConsciousnessManager()
except ImportError:
    print("⚠️ Visual consciousness manager not found")
    visual_manager = None

def print_visual_status():
    """
    Print comprehensive visual system status with schema context.
    Shows active processes, system load, and schema metrics.
    """
    try:
        if not visual_manager:
            print("❌ Visual system not initialized")
            return
        
        status = visual_manager.get_visual_status()
        
        print("\n🎬 Visual Consciousness Status")
        print("="*50)
        print(f"System Running: {status['is_running']}")
        print(f"Active Processes: {status['active_processes']}/{status['max_processes']}")
        print(f"System Load: {status['system_load']:.2f}")
        print()
        
        # Group processes by priority
        by_priority = defaultdict(list)
        for name, info in status['processes'].items():
            by_priority[info['priority']].append((name, info))
        
        # Print status for each priority level
        for priority in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'POETIC']:
            if priority in by_priority:
                print(f"📊 {priority} Priority:")
                for name, info in by_priority[priority]:
                    status_icon = "🟢" if info['running'] else "🔴" if info['enabled'] else "⚫"
                    fps_info = f"@{info['target_fps']:.1f}fps" if info['running'] else ""
                    error_info = f" (errors: {info['error_count']})" if info['error_count'] > 0 else ""
                    print(f"   {status_icon} {name} ({info['mode']}) {fps_info}{error_info}")
                print()
        
    except Exception as e:
        print(f"❌ Error getting visual status: {e}")

def enable_poetic_visuals():
    """
    Enable poetic/aesthetic visual processes.
    Activates mythological and artistic visualizations.
    """
    try:
        if not visual_manager:
            print("❌ Visual system not initialized")
            return
        
        poetic_processes = [
            'persephone_decay_map',
            'crow_stall_heatmap',
            'recursive_bloom_tree',
            'semantic_timeline_animator'
        ]
        
        for process_name in poetic_processes:
            enable_visual_process(process_name)
        
        print("🌸 Poetic visual processes enabled:")
        print("   → Persephone decay mapping")
        print("   → Crow stall heatmap")
        print("   → Recursive bloom visualization")
        print("   → Semantic timeline animation")
        
    except Exception as e:
        print(f"❌ Error enabling poetic visuals: {e}")

def emergency_visual_mode():
    """
    Switch to emergency diagnostic visual mode.
    Disables non-critical processes and focuses on system health monitoring.
    """
    try:
        if not visual_manager:
            print("❌ Visual system not initialized")
            return
        
        # Define critical processes
        critical_processes = [
            'pulse_map_renderer',
            'cognition_pressure_map',
            'entropy_cluster_plot',
            'thermal_zone_monitor'
        ]
        
        # Disable non-critical processes
        for name, process in visual_manager.processes.items():
            if name not in critical_processes and process.enabled:
                disable_visual_process(name)
        
        # Ensure critical processes are enabled
        for process_name in critical_processes:
            enable_visual_process(process_name)
        
        print("🚨 Emergency visual mode activated:")
        print("   → Critical diagnostics enabled")
        print("   → Non-essential visuals disabled")
        print("   → System health monitoring active")
        
    except Exception as e:
        print(f"❌ Error switching to emergency mode: {e}")

def restore_normal_visuals():
    """
    Restore normal visual operation.
    Re-enables standard visual processes and resets priorities.
    """
    try:
        if not visual_manager:
            print("❌ Visual system not initialized")
            return
        
        # Standard visual processes
        standard_processes = [
            'pulse_map_renderer',
            'mood_heatmap',
            'entropy_arc_animator',
            'cognition_pressure_map',
            'thermal_zone_monitor'
        ]
        
        # Enable standard processes
        for process_name in standard_processes:
            enable_visual_process(process_name)
        
        # Reset process priorities
        for process in visual_manager.processes.values():
            if process.priority == VisualPriority.POETIC:
                process.enabled = False
        
        print("✅ Normal visual operation restored:")
        print("   → Standard processes enabled")
        print("   → Priority levels reset")
        print("   → System monitoring active")
        
    except Exception as e:
        print(f"❌ Error restoring normal visuals: {e}")

if __name__ == "__main__":
    # Test visual utilities
    print_visual_status()
    enable_poetic_visuals()
    print("\nWaiting 2 seconds...")
    import time
    time.sleep(2)
    emergency_visual_mode()
    print("\nWaiting 2 seconds...")
    time.sleep(2)
    restore_normal_visuals() 