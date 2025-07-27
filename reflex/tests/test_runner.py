import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from ..reflex_system import ReflexSystem
from .utils import MockTask, MockClaude, MockCAIRNMatrix, generate_test_tasks
from .scenarios import TestScenario, ScenarioFactory, run_scenario_test

class ReflexTestRunner:
    """Test runner for the reflex system"""
    
    def __init__(self, log_dir: str = "logs/reflex_tests"):
        self.reflex = ReflexSystem(log_dir=log_dir)
        self.cairn_matrix = MockCAIRNMatrix()
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def run_single_test(self, task: MockTask) -> Dict[str, Any]:
        """Run a single test case"""
        # Generate mock response
        claude_output = MockClaude.generate_response(task.task_id)
        
        # Create initial state
        state = self.reflex.create_initial_state(
            mood=claude_output["metadata"]["mood"],
            drift_score=0.5,  # Initial drift score
            heat=claude_output["metadata"]["heat"],
            entropy=claude_output["metadata"]["entropy"],
            sigil=task.matrix_entry["sigil"],
            task_id=task.task_id,
            task_router=self.cairn_matrix,
            metadata={
                "response_summary": claude_output["summary"],
                "response_tokens": claude_output["tokens"],
                "response_embedding": claude_output["embedding"]
            }
        )
        
        # Process through reflex system
        processed_state = self.reflex.process_state(state)
        decision = processed_state.metadata["decision"]
        
        # Format test result
        return {
            "task_id": task.task_id,
            "timestamp": datetime.utcnow().isoformat(),
            "should_rebloom": decision.should_rebloom,
            "mode": decision.mode.value,
            "drift_score": decision.drift_score,
            "faltering": decision.faltering,
            "flags": decision.flags,
            "metadata": {
                "mood": state.mood,
                "heat": state.heat,
                "entropy": state.entropy,
                "sigil": state.sigil
            }
        }
    
    def run_batch_tests(self, num_tasks: int = 5) -> List[Dict[str, Any]]:
        """Run a batch of test cases"""
        tasks = generate_test_tasks(num_tasks)
        results = []
        
        for task in tasks:
            result = self.run_single_test(task)
            results.append(result)
            
            # Print test summary
            print("\n=== REFLEX TEST RESULT ===")
            print(f"Task ID: {result['task_id']}")
            print(f"Should Rebloom: {result['should_rebloom']}")
            print(f"Mode: {result['mode']}")
            print(f"Drift Score: {result['drift_score']:.2f}")
            print(f"Faltering: {result['faltering']}")
            print(f"Flags: {', '.join(result['flags'])}")
            print("=" * 30)
        
        # Save results to log file
        self._save_results(results)
        return results
    
    def run_scenario(self, scenario: TestScenario) -> Dict[str, Any]:
        """Run a complete scenario test"""
        print(f"\n=== Running Scenario: {scenario.name} ===")
        print(f"Description: {scenario.description}")
        print(f"Number of tasks: {len(scenario.tasks)}")
        print("=" * 50)
        
        # Run scenario test
        results = run_scenario_test(scenario, self)
        
        # Print scenario summary
        print("\n=== SCENARIO RESULTS ===")
        print(f"Expected Rebloom Rate: {scenario.expected_rebloom_rate:.1%}")
        print(f"Actual Rebloom Rate: {results['actual_rebloom_rate']:.1%}")
        print("\nMode Distribution:")
        for mode, expected in scenario.expected_modes.items():
            actual = results['actual_modes'].get(mode, 0)
            print(f"  {mode}: Expected {expected:.1%}, Actual {actual:.1%}")
        print("\nFlags:")
        print(f"  Expected: {', '.join(scenario.expected_flags)}")
        print(f"  Actual: {', '.join(results['actual_flags'])}")
        print("=" * 50)
        
        # Save results
        self._save_results(results['results'], prefix=f"scenario_{scenario.name.lower().replace(' ', '_')}")
        return results
    
    def run_all_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Run all predefined scenarios"""
        scenarios = [
            ScenarioFactory.create_volatile_chain(),
            ScenarioFactory.create_sigil_edge_cases(),
            ScenarioFactory.create_mood_transition_chain(),
            ScenarioFactory.create_drift_recovery_chain()
        ]
        
        results = {}
        for scenario in scenarios:
            results[scenario.name] = self.run_scenario(scenario)
        
        return results
    
    def _save_results(self, results: List[Dict[str, Any]], prefix: str = "reflex_test") -> None:
        """Save test results to log file"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"{prefix}_{timestamp}.jsonl"
        
        with open(log_file, "w") as f:
            for result in results:
                f.write(json.dumps(result) + "\n")
        
        print(f"\nTest results saved to: {log_file}")

def main():
    """Main entry point for test runner"""
    runner = ReflexTestRunner()
    
    # Run single test
    print("\nRunning single test...")
    task = MockTask(
        task_id="test_001_drift",
        priority=True,
        score=0.92,
        matrix_entry={
            "memory_excerpts": ["Claude has shown increased loop behavior recently."],
            "sigil": "loop/feedback"
        }
    )
    runner.run_single_test(task)
    
    # Run batch tests
    print("\nRunning batch tests...")
    runner.run_batch_tests(num_tasks=5)
    
    # Run all scenarios
    print("\nRunning all scenarios...")
    runner.run_all_scenarios()

if __name__ == "__main__":
    main() 