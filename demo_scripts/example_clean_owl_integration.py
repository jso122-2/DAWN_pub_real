#!/usr/bin/env python3
"""
Clean Owl Tracer Integration Example
Shows how to integrate the professional OwlTracer into existing DAWN systems
"""

from reflection.owl.owl_tracer import OwlTracer
from utils.clean_logger import CleanLogger, clean_section_header

def main():
    """Demonstrate clean owl tracer integration"""
    
    clean_section_header("Clean Owl Tracer Integration Example")
    
    # Initialize components
    logger = CleanLogger("EXAMPLE")
    owl = OwlTracer("COGNITIVE-ANALYZER")
    
    logger.info("Initializing tick processing with clean owl commentary")
    
    # Simulate tick processing loop
    tick_log = {}
    current_tick_data = {
        "heat": 0.65,
        "entropy": 0.72,
        "scup": 0.58,
        "zone": "surge"
    }
    
    logger.info("Processing current tick", current_tick_data)
    
    # CLEAN VERSION: Use professional OwlTracer without emojis
    owl_comment = owl.comment_on_tick(current_tick_data)
    tick_log["comment"] = owl_comment
    tick_log["timestamp"] = "2025-07-09T20:30:15"
    tick_log["tick_data"] = current_tick_data
    
    # Display results
    logger.success("Tick processing complete", {
        "comment": tick_log["comment"],
        "timestamp": tick_log["timestamp"]
    })
    
    # Show the before/after comparison
    print("\nBEFORE/AFTER COMPARISON")
    print("=" * 60)
    
    print("\nOLD EMOJI VERSION:")
    print("🦉 Bloom entropy rising — rebloom likely.")
    print("🦉 Surge state detected. Cognitive pressure high.")
    print("🦉 Drift detected. Coherence weakening.")
    
    print("\nNEW CLEAN VERSION:")
    print("BLOOM ENTROPY RISING: Rebloom sequence likely imminent")
    print("SURGE STATE ACTIVE: Cognitive pressure elevated")
    print("DRIFT DETECTED: Coherence weakening below threshold")
    
    # Advanced usage examples
    print("\nADVANCED USAGE PATTERNS")
    print("=" * 60)
    
    # Batch analysis
    recent_ticks = [
        {"heat": 0.4, "entropy": 0.5, "scup": 0.7, "zone": "calm"},
        {"heat": 0.6, "entropy": 0.6, "scup": 0.6, "zone": "active"},
        {"heat": 0.8, "entropy": 0.7, "scup": 0.5, "zone": "surge"}
    ]
    
    logger.info("Performing batch analysis on recent ticks")
    trend_analysis = owl.analyze_trend(recent_ticks)
    
    logger.info("Trend analysis complete", {
        "trend": trend_analysis["trend"],
        "recommendation": trend_analysis["recommendation"]
    })
    
    # Report generation
    logger.info("Generating comprehensive analysis report")
    report = owl.generate_report()
    
    print("\nGENERATED REPORT:")
    print("-" * 40)
    print(report)
    
    logger.success("Clean owl tracer integration demonstration complete")


if __name__ == "__main__":
    main() 