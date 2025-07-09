#!/usr/bin/env python3
"""
DAWN Clean Owl Tracer Demo
Demonstrates professional cognitive analysis without emoji clutter
"""

import sys
import os

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'reflection/owl'))
from owl_tracer import OwlTracer
from utils.clean_logger import CleanLogger, clean_section_header, clean_section_footer


def main():
    """Demonstrate clean owl tracer functionality"""
    
    # Initialize clean logger for demo
    demo_logger = CleanLogger("DEMO")
    
    clean_section_header("DAWN Clean Owl Tracer Demonstration")
    
    demo_logger.info("Initializing professional cognitive analysis system")
    
    # Create owl tracer instance
    owl = OwlTracer("OWL-ANALYSIS")
    
    # Simulate real-time tick analysis
    demo_logger.info("Beginning tick analysis simulation")
    
    # Example tick sequences representing different system states
    tick_sequences = [
        {
            "sequence_name": "System Startup",
            "ticks": [
                {"heat": 0.2, "entropy": 0.3, "scup": 0.9, "zone": "calm"},
                {"heat": 0.3, "entropy": 0.4, "scup": 0.85, "zone": "calm"},
                {"heat": 0.4, "entropy": 0.5, "scup": 0.8, "zone": "active"}
            ]
        },
        {
            "sequence_name": "Cognitive Surge Event",
            "ticks": [
                {"heat": 0.6, "entropy": 0.6, "scup": 0.7, "zone": "active"},
                {"heat": 0.8, "entropy": 0.7, "scup": 0.6, "zone": "surge"},
                {"heat": 0.9, "entropy": 0.8, "scup": 0.5, "zone": "surge"}
            ]
        },
        {
            "sequence_name": "System Stabilization",
            "ticks": [
                {"heat": 0.7, "entropy": 0.6, "scup": 0.6, "zone": "active"},
                {"heat": 0.5, "entropy": 0.4, "scup": 0.7, "zone": "calm"},
                {"heat": 0.3, "entropy": 0.2, "scup": 0.85, "zone": "calm"}
            ]
        },
        {
            "sequence_name": "Coherence Drift",
            "ticks": [
                {"heat": 0.4, "entropy": 0.5, "scup": 0.6, "zone": "active"},
                {"heat": 0.3, "entropy": 0.4, "scup": 0.4, "zone": "calm"},
                {"heat": 0.2, "entropy": 0.3, "scup": 0.3, "zone": "calm"}
            ]
        }
    ]
    
    all_ticks = []
    
    # Process each sequence
    for sequence in tick_sequences:
        print(f"\nPROCESSING SEQUENCE: {sequence['sequence_name']}")
        print("-" * 60)
        
        for i, tick in enumerate(sequence['ticks'], 1):
            print(f"\nTick {i}:")
            demo_logger.parameter_block("Tick Data", tick)
            
            # Get owl analysis
            comment = owl.comment_on_tick(tick)
            print(f"Owl Analysis: {comment}")
            
            all_ticks.append(tick)
    
    # Generate comprehensive trend analysis
    print("\nCOMPREHENSIVE TREND ANALYSIS")
    print("=" * 60)
    
    trend_analysis = owl.analyze_trend(all_ticks)
    demo_logger.parameter_block("Trend Analysis Results", trend_analysis)
    
    # Generate final report
    print("\nGENERATING ANALYSIS REPORT")
    print("=" * 60)
    
    report = owl.generate_report()
    print(report)
    
    # Demonstrate additional functionality
    print("\nADDITIONAL ANALYSIS FEATURES")
    print("=" * 60)
    
    demo_logger.info("Demonstrating recent trend analysis")
    recent_trend = owl.analyze_trend(all_ticks[-5:])  # Last 5 ticks
    
    demo_logger.info("Analysis history management")
    demo_logger.info(f"Total analyses stored: {len(owl.analysis_history)}")
    
    # Show usage examples
    print("\nUSAGE EXAMPLES")
    print("=" * 60)
    
    example_code = '''
# Basic usage:
owl = OwlTracer("MY-SYSTEM")
comment = owl.comment_on_tick(tick_data)
tick_log["comment"] = comment

# Trend analysis:
trend = owl.analyze_trend(recent_ticks)
system_status["trend_analysis"] = trend

# Generate reports:
report = owl.generate_report()
print(report)
'''
    
    print("Code Example:")
    print(example_code)
    
    demo_logger.success("Clean owl tracer demonstration complete")
    clean_section_footer("Demonstration")


if __name__ == "__main__":
    main() 