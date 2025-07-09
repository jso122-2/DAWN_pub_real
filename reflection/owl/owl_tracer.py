"""
DAWN Owl Tracer - Clean cognitive analysis and tick commentary
Provides structured analysis of system states without emoji clutter
"""
from typing import Dict, Any, Optional
import sys
import os

# Add utils to path for clean logger access
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from utils.clean_logger import CleanLogger


class OwlTracer:
    """
    Professional cognitive state analyzer for DAWN tick system
    Provides structured commentary on system behavior patterns
    """
    
    def __init__(self, component_name: str = "OWL-TRACER"):
        self.logger = CleanLogger(component_name)
        self.analysis_history = []
        
    def comment_on_tick(self, tick: Dict[str, Any]) -> str:
        """
        Generate clean, structured commentary on tick state
        
        Args:
            tick: Dictionary containing tick data (heat, entropy, scup, zone)
            
        Returns:
            str: Professional analysis comment without emojis
        """
        heat = tick.get("heat", 0)
        entropy = tick.get("entropy", 0)
        scup = tick.get("scup", 1)
        zone = tick.get("zone", "calm")
        
        # Generate analysis based on state
        if scup < 0.5:
            comment = "DRIFT DETECTED: Coherence weakening below threshold"
            severity = "WARNING"
        elif entropy > 0.7:
            comment = "BLOOM ENTROPY RISING: Rebloom sequence likely imminent"
            severity = "INFO"
        elif zone == "surge":
            comment = "SURGE STATE ACTIVE: Cognitive pressure elevated"
            severity = "WARNING"
        elif heat > 0.8:
            comment = "HIGH HEAT DETECTED: System approaching critical zone"
            severity = "WARNING"
        elif entropy < 0.2:
            comment = "LOW ENTROPY STATE: System in stable configuration"
            severity = "SUCCESS"
        else:
            comment = "NOMINAL OPERATION: System within stable parameters"
            severity = "INFO"
            
        # Store analysis
        analysis = {
            "comment": comment,
            "severity": severity,
            "tick_data": tick,
            "timestamp": self.logger._format_timestamp()
        }
        self.analysis_history.append(analysis)
        
        # Log the analysis
        self.logger.log(severity, comment, {
            "heat": heat,
            "entropy": entropy,
            "scup": scup,
            "zone": zone
        })
        
        return comment
    
    def analyze_trend(self, recent_ticks: list) -> Dict[str, Any]:
        """
        Analyze trends across multiple ticks
        
        Args:
            recent_ticks: List of recent tick data
            
        Returns:
            Dict containing trend analysis
        """
        if not recent_ticks:
            return {"trend": "NO_DATA", "recommendation": "Insufficient data for analysis"}
        
        # Calculate averages
        avg_heat = sum(t.get("heat", 0) for t in recent_ticks) / len(recent_ticks)
        avg_entropy = sum(t.get("entropy", 0) for t in recent_ticks) / len(recent_ticks)
        avg_scup = sum(t.get("scup", 1) for t in recent_ticks) / len(recent_ticks)
        
        # Determine trend
        if avg_entropy > 0.7 and avg_heat > 0.6:
            trend = "CRITICAL_ASCENT"
            recommendation = "Monitor for imminent state transition"
        elif avg_scup < 0.6:
            trend = "COHERENCE_DRIFT"
            recommendation = "Stabilization protocols recommended"
        elif avg_heat < 0.3 and avg_entropy < 0.4:
            trend = "STABLE_DESCENT"
            recommendation = "System achieving equilibrium"
        else:
            trend = "NOMINAL_FLUCTUATION"
            recommendation = "Continue normal monitoring"
        
        analysis = {
            "trend": trend,
            "recommendation": recommendation,
            "averages": {
                "heat": round(avg_heat, 3),
                "entropy": round(avg_entropy, 3),
                "scup": round(avg_scup, 3)
            },
            "sample_size": len(recent_ticks)
        }
        
        self.logger.info(f"Trend Analysis: {trend}", analysis)
        
        return analysis
    
    def generate_report(self) -> str:
        """
        Generate comprehensive analysis report
        
        Returns:
            str: Formatted report string
        """
        if not self.analysis_history:
            return "No analysis data available"
        
        recent_analyses = self.analysis_history[-10:]  # Last 10 analyses
        
        # Count severity levels
        severity_counts = {}
        for analysis in recent_analyses:
            severity = analysis["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        report_lines = [
            "OWL TRACER ANALYSIS REPORT",
            "=" * 50,
            f"Total Analyses: {len(self.analysis_history)}",
            f"Recent Sample: {len(recent_analyses)} entries",
            "",
            "SEVERITY DISTRIBUTION:",
        ]
        
        for severity, count in severity_counts.items():
            percentage = (count / len(recent_analyses)) * 100
            report_lines.append(f"  {severity}: {count} ({percentage:.1f}%)")
        
        if recent_analyses:
            latest = recent_analyses[-1]
            report_lines.extend([
                "",
                "LATEST ANALYSIS:",
                f"  Comment: {latest['comment']}",
                f"  Severity: {latest['severity']}",
                f"  Timestamp: {latest['timestamp']}"
            ])
        
        return "\n".join(report_lines)
    
    def clear_history(self):
        """Clear analysis history"""
        self.analysis_history = []
        self.logger.info("Analysis history cleared")


# Example usage function
def demonstrate_clean_owl_tracer():
    """Demonstrate the clean owl tracer functionality"""
    
    print("\nDEMONSTRATING CLEAN OWL TRACER")
    print("=" * 50)
    
    # Create tracer instance
    owl = OwlTracer()
    
    # Example tick data scenarios
    test_scenarios = [
        {
            "name": "Normal Operation",
            "tick": {"heat": 0.5, "entropy": 0.4, "scup": 0.8, "zone": "calm"}
        },
        {
            "name": "Drift Condition", 
            "tick": {"heat": 0.3, "entropy": 0.3, "scup": 0.4, "zone": "calm"}
        },
        {
            "name": "High Entropy",
            "tick": {"heat": 0.6, "entropy": 0.8, "scup": 0.7, "zone": "active"}
        },
        {
            "name": "Surge State",
            "tick": {"heat": 0.9, "entropy": 0.6, "scup": 0.6, "zone": "surge"}
        }
    ]
    
    # Process each scenario
    tick_history = []
    for scenario in test_scenarios:
        print(f"\nTesting: {scenario['name']}")
        print("-" * 30)
        
        comment = owl.comment_on_tick(scenario['tick'])
        tick_history.append(scenario['tick'])
        
        print(f"Result: {comment}")
    
    # Generate trend analysis
    print("\nTREND ANALYSIS")
    print("-" * 30)
    trend_analysis = owl.analyze_trend(tick_history)
    
    # Generate report
    print("\nFINAL REPORT")
    print("-" * 30)
    print(owl.generate_report())


if __name__ == "__main__":
    # Run demonstration
    demonstrate_clean_owl_tracer() 