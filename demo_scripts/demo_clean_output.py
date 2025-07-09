#!/usr/bin/env python3
"""
DAWN Clean Output Demonstration
Shows the structured, professional output system without emojis
"""

import sys
import time
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.clean_logger import (
    CleanLogger, clean_section_header, clean_section_footer,
    log_fractal_render, log_tick_update, log_sigil_event, log_system_event
)

def demo_clean_logging():
    """Demonstrate clean logging system"""
    
    # Initialize different component loggers
    system_logger = CleanLogger("SYSTEM")
    fractal_logger = CleanLogger("FRACTAL")
    tick_logger = CleanLogger("TICK") 
    sigil_logger = CleanLogger("SIGIL")
    
    clean_section_header("DAWN Clean Output System Demo")
    
    # System initialization
    system_logger.info("DAWN consciousness system initializing")
    time.sleep(0.5)
    
    system_logger.parameter_block("System Configuration", {
        "consciousness_mode": "enhanced",
        "fractal_rendering": "julia_set",
        "sigil_processing": "safe_mode",
        "tick_interval": "0.5s",
        "debug_level": "structured"
    })
    
    system_logger.success("Core systems initialized")
    
    # Demonstrate status reporting
    system_logger.status_list({
        "Consciousness Engine": True,
        "Fractal Renderer": True,
        "Sigil Processor": True,
        "Tick Engine": True,
        "Memory Systems": True,
        "Dream Conductor": False
    }, "Component Status")
    
    # Simulate fractal rendering process
    fractal_logger.subsection("Fractal Bloom Rendering")
    
    fractal_params = {
        "julia_constant": "-0.7269 + 0.1889i",
        "max_iterations": 100,
        "zoom_level": 250.0,
        "color_palette": "lineage_based",
        "bloom_depth": 7
    }
    
    fractal_logger.parameter_block("Fractal Parameters", fractal_params)
    
    # Simulate rendering steps
    rendering_steps = [
        "Parameter validation and sanitization",
        "Julia set constant calculation", 
        "Color palette generation",
        "Pixel iteration and mapping",
        "Visual indicators and overlays"
    ]
    
    for i, step in enumerate(rendering_steps):
        fractal_logger.progress_update("Rendering", i+1, len(rendering_steps), step)
        time.sleep(0.3)
    
    fractal_logger.success("Fractal bloom rendered successfully", {
        "render_time": "0.876s",
        "pixel_count": 22500,
        "palette_colors": 3
    })
    
    # Simulate tick engine updates
    tick_logger.subsection("Tick Engine Processing")
    
    for tick in range(3):
        tick_data = {
            "tick_id": f"tick_{tick + 1}",
            "scup_score": round(random.uniform(0.3, 0.8), 3),
            "pulse_heat": round(random.uniform(0.2, 0.9), 3),
            "entropy": round(random.uniform(0.4, 0.7), 3),
            "complexity": round(random.uniform(0.5, 0.8), 3)
        }
        
        tick_logger.tick("Processing cognitive tick", tick_data)
        time.sleep(0.4)
    
    tick_logger.success("Tick processing cycle complete")
    
    # Simulate sigil system
    sigil_logger.subsection("Sigil System Processing")
    
    sigil_houses = ["Perception", "Memory", "Logic", "Intuition", "Expression"]
    generated_sigils = []
    
    for i, house in enumerate(sigil_houses):
        sigil_data = {
            "symbol": f"/\\{i}\\",
            "house": house,
            "heat": round(random.uniform(0.1, 0.9), 2),
            "decay_rate": round(random.uniform(0.01, 0.05), 3),
            "position": f"({random.randint(50, 250)}, {random.randint(50, 250)})"
        }
        generated_sigils.append(sigil_data)
        
        sigil_logger.sigil("Generated sigil", sigil_data)
        time.sleep(0.2)
    
    sigil_logger.success("Sigil generation complete", {
        "total_sigils": len(generated_sigils),
        "active_houses": len(sigil_houses),
        "processing_mode": "safe"
    })
    
    # Demonstrate error handling
    system_logger.subsection("Error Handling Examples")
    
    system_logger.warning("Low memory detected in consciousness buffer")
    system_logger.error("Temporary fractal rendering anomaly", {
        "error_type": "mathematical_overflow",
        "affected_component": "julia_iteration",
        "recovery_action": "fallback_to_placeholder"
    })
    system_logger.info("Automatic recovery successful")
    
    # Final status
    system_logger.subsection("Final System State")
    
    final_stats = {
        "total_ticks": 3,
        "fractals_rendered": 1, 
        "sigils_generated": len(generated_sigils),
        "errors_handled": 1,
        "uptime": "demo_mode"
    }
    
    system_logger.parameter_block("Session Statistics", final_stats)
    
    # Cleanup
    system_logger.info("Demo complete - shutting down systems")
    system_logger.success("All systems cleanly terminated")
    
    clean_section_footer("DAWN Clean Output Demo")

def compare_output_styles():
    """Show comparison between old emoji style and new clean style"""
    
    print("\n" + "="*80)
    print("OUTPUT STYLE COMPARISON")
    print("="*80)
    
    print("\nOLD EMOJI STYLE:")
    print("-" * 20)
    print("🚀 DAWN GUI System Launcher")
    print("🔧 Initializing queue-based communication...")
    print("✅ Tick engine initialized")
    print("🎯 All systems ready!")
    print("🌸 Starting consciousness simulation...")
    
    print("\nNEW CLEAN STYLE:")
    print("-" * 20)
    logger = CleanLogger("DEMO")
    logger.info("DAWN GUI System Launcher")
    logger.info("Initializing queue-based communication")
    logger.success("Tick engine initialized")
    logger.info("All systems ready")
    logger.info("Starting consciousness simulation")
    
    print("\nBENEFITS OF CLEAN STYLE:")
    print("-" * 30)
    benefits = [
        "Professional appearance",
        "Better readability", 
        "Structured information display",
        "Consistent formatting",
        "Easy to parse programmatically",
        "Works in all terminal environments",
        "No character encoding issues",
        "Cleaner logs for debugging"
    ]
    
    for benefit in benefits:
        print(f"  • {benefit}")

if __name__ == "__main__":
    print("DAWN Clean Output System Demonstration")
    print("=" * 50)
    
    try:
        demo_clean_logging()
        print("\n" + "="*50)
        compare_output_styles()
        
        print(f"\n{'='*80}")
        print("DEMONSTRATION COMPLETE")
        print("Clean, structured output provides:")
        print("  • Professional appearance without emoji distractions")
        print("  • Better information organization") 
        print("  • Consistent formatting across all DAWN components")
        print("  • Improved readability for debugging and monitoring")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nDemo error: {e}")
        import traceback
        traceback.print_exc() 