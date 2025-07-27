import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()

class ReflexDashboard:
    """CLI dashboard for visualizing reflex test results"""
    
    def __init__(self, log_dir: str = "logs/reflex_tests"):
        self.log_dir = Path(log_dir)
    
    def load_results(self, log_file: str) -> List[Dict[str, Any]]:
        """Load results from a log file"""
        results = []
        with open(self.log_dir / log_file, "r") as f:
            for line in f:
                results.append(json.loads(line))
        return results
    
    def get_latest_log(self) -> str:
        """Get the latest log file (any .jsonl in the log dir)"""
        log_files = list(self.log_dir.glob("*.jsonl"))
        if not log_files:
            raise FileNotFoundError(
                f"No test logs found in {self.log_dir}.\n"
                f"Run the test runner first to generate logs."
            )
        return max(log_files, key=lambda x: x.stat().st_mtime).name
    
    def show_summary(self, results: List[Dict[str, Any]]) -> None:
        """Show summary statistics"""
        # Calculate statistics
        total_tests = len(results)
        rebloom_count = sum(1 for r in results if r["should_rebloom"])
        faltering_count = sum(1 for r in results if r["faltering"])
        avg_drift = np.mean([r["drift_score"] for r in results])
        
        # Create summary panel
        console.print(Panel.fit(
            f"[bold]Test Summary[/bold]\n"
            f"Total Tests: {total_tests}\n"
            f"Rebloom Rate: {rebloom_count/total_tests:.1%}\n"
            f"Faltering Rate: {faltering_count/total_tests:.1%}\n"
            f"Average Drift: {avg_drift:.2f}",
            title="Reflex System Statistics"
        ))
    
    def show_mode_distribution(self, results: List[Dict[str, Any]]) -> None:
        """Show distribution of rebloom modes"""
        modes = {}
        for result in results:
            if result["should_rebloom"]:
                mode = result["mode"]
                modes[mode] = modes.get(mode, 0) + 1
        
        # Create mode table
        table = Table(title="Rebloom Mode Distribution")
        table.add_column("Mode", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        
        total_reblooms = sum(modes.values())
        for mode, count in modes.items():
            percentage = count / total_reblooms if total_reblooms > 0 else 0
            table.add_row(
                mode,
                str(count),
                f"{percentage:.1%}"
            )
        
        console.print(table)
    
    def show_drift_analysis(self, results: List[Dict[str, Any]]) -> None:
        """Show drift score analysis"""
        drift_scores = [r["drift_score"] for r in results]
        
        # Create drift table
        table = Table(title="Drift Score Analysis")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="green")
        
        table.add_row("Mean", f"{np.mean(drift_scores):.3f}")
        table.add_row("Median", f"{np.median(drift_scores):.3f}")
        table.add_row("Std Dev", f"{np.std(drift_scores):.3f}")
        table.add_row("Min", f"{min(drift_scores):.3f}")
        table.add_row("Max", f"{max(drift_scores):.3f}")
        
        console.print(table)
    
    def show_flag_analysis(self, results: List[Dict[str, Any]]) -> None:
        """Show analysis of decision flags"""
        flags = {}
        for result in results:
            for flag in result["flags"]:
                flag_type = flag.split("=")[0]
                flags[flag_type] = flags.get(flag_type, 0) + 1
        
        # Create flag table
        table = Table(title="Flag Analysis")
        table.add_column("Flag Type", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        
        total_flags = sum(flags.values())
        for flag_type, count in sorted(flags.items(), key=lambda x: x[1], reverse=True):
            percentage = count / total_flags if total_flags > 0 else 0
            table.add_row(
                flag_type,
                str(count),
                f"{percentage:.1%}"
            )
        
        console.print(table)
    
    def show_detailed_results(self, results: List[Dict[str, Any]]) -> None:
        """Show detailed results for each test"""
        table = Table(title="Detailed Test Results")
        table.add_column("Task ID", style="cyan")
        table.add_column("Rebloom", justify="center", style="green")
        table.add_column("Mode", style="yellow")
        table.add_column("Drift", justify="right", style="magenta")
        table.add_column("Faltering", justify="center", style="red")
        table.add_column("Flags", style="blue")
        
        for result in results:
            table.add_row(
                result["task_id"],
                "✓" if result["should_rebloom"] else "✗",
                result["mode"],
                f"{result['drift_score']:.2f}",
                "✓" if result["faltering"] else "✗",
                ", ".join(result["flags"])
            )
        
        console.print(table)
    
    def run_dashboard(self, log_file: str = None) -> None:
        """Run the full dashboard"""
        if log_file is None:
            log_file = self.get_latest_log()
        
        console.print(f"\n[bold]Loading results from: {log_file}[/bold]")
        results = self.load_results(log_file)
        
        # Show all dashboard sections
        self.show_summary(results)
        console.print("\n")
        
        self.show_mode_distribution(results)
        console.print("\n")
        
        self.show_drift_analysis(results)
        console.print("\n")
        
        self.show_flag_analysis(results)
        console.print("\n")
        
        self.show_detailed_results(results)

def main():
    """Main entry point for dashboard"""
    dashboard = ReflexDashboard()
    dashboard.run_dashboard()

if __name__ == "__main__":
    main() 