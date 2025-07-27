from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .utils import MockTask, MockResponse

@dataclass
class TestScenario:
    """Represents a complete test scenario with tasks and expected outcomes"""
    name: str
    description: str
    tasks: List[MockTask]
    expected_rebloom_rate: float
    expected_modes: Dict[str, float]  # mode -> expected percentage
    expected_flags: List[str]
    metadata: Dict[str, Any]

class ScenarioFactory:
    """Factory for creating complex test scenarios"""
    
    @staticmethod
    def create_volatile_chain(
        chain_length: int = 5,
        volatility_increase: float = 0.1
    ) -> TestScenario:
        """Create a chain of tasks with increasing volatility"""
        tasks = []
        for i in range(chain_length):
            volatility = 0.3 + (i * volatility_increase)
            tasks.append(MockTask(
                task_id=f"volatile_chain_{i:03d}",
                priority=True,
                score=0.8 - (i * 0.05),
                matrix_entry={
                    "memory_excerpts": [f"Memory {i} with volatility {volatility}"],
                    "sigil": f"volatile/chain_{i}",
                    "volatility": volatility
                }
            ))
        
        return TestScenario(
            name="Volatile Chain",
            description="Tests system response to increasing volatility",
            tasks=tasks,
            expected_rebloom_rate=0.8,
            expected_modes={
                "rephrase": 0.4,
                "regenerate": 0.4,
                "clarify": 0.2
            },
            expected_flags=["drift", "entropy", "volatility"],
            metadata={"chain_length": chain_length}
        )
    
    @staticmethod
    def create_sigil_edge_cases() -> TestScenario:
        """Create tasks with edge case sigils"""
        tasks = [
            MockTask(
                task_id="edge_case_001",
                priority=True,
                score=0.9,
                matrix_entry={
                    "memory_excerpts": ["Memory with complex sigil"],
                    "sigil": "complex/nested/sigil/with/many/levels"
                }
            ),
            MockTask(
                task_id="edge_case_002",
                priority=True,
                score=0.9,
                matrix_entry={
                    "memory_excerpts": ["Memory with minimal sigil"],
                    "sigil": "min"
                }
            ),
            MockTask(
                task_id="edge_case_003",
                priority=True,
                score=0.9,
                matrix_entry={
                    "memory_excerpts": ["Memory with special characters"],
                    "sigil": "special/chars/!@#$%^&*()"
                }
            )
        ]
        
        return TestScenario(
            name="Sigil Edge Cases",
            description="Tests system handling of unusual sigil patterns",
            tasks=tasks,
            expected_rebloom_rate=0.3,
            expected_modes={
                "clarify": 0.7,
                "rephrase": 0.3
            },
            expected_flags=["sigil_complexity", "format_validation"],
            metadata={"edge_case_types": ["nested", "minimal", "special_chars"]}
        )
    
    @staticmethod
    def create_mood_transition_chain(
        moods: List[str] = ["calm", "focused", "tense", "overloaded"]
    ) -> TestScenario:
        """Create a chain of tasks with mood transitions"""
        tasks = []
        for i, mood in enumerate(moods):
            tasks.append(MockTask(
                task_id=f"mood_transition_{i:03d}",
                priority=True,
                score=0.8,
                matrix_entry={
                    "memory_excerpts": [f"Memory in {mood} state"],
                    "sigil": f"mood/{mood}",
                    "mood": mood
                }
            ))
        
        return TestScenario(
            name="Mood Transition Chain",
            description="Tests system response to mood transitions",
            tasks=tasks,
            expected_rebloom_rate=0.5,
            expected_modes={
                "rephrase": 0.3,
                "clarify": 0.4,
                "regenerate": 0.3
            },
            expected_flags=["mood_shift", "emotional_overload"],
            metadata={"mood_sequence": moods}
        )
    
    @staticmethod
    def create_drift_recovery_chain(
        initial_drift: float = 0.8,
        recovery_steps: int = 3
    ) -> TestScenario:
        """Create a chain of tasks simulating drift recovery"""
        tasks = []
        for i in range(recovery_steps):
            drift = initial_drift * (1 - (i / recovery_steps))
            tasks.append(MockTask(
                task_id=f"drift_recovery_{i:03d}",
                priority=True,
                score=0.7 + (i * 0.1),
                matrix_entry={
                    "memory_excerpts": [f"Memory with drift {drift:.2f}"],
                    "sigil": f"drift/recovery_{i}",
                    "drift": drift
                }
            ))
        
        return TestScenario(
            name="Drift Recovery Chain",
            description="Tests system recovery from high drift",
            tasks=tasks,
            expected_rebloom_rate=0.7,
            expected_modes={
                "regenerate": 0.4,
                "rephrase": 0.4,
                "clarify": 0.2
            },
            expected_flags=["drift", "recovery", "stability"],
            metadata={
                "initial_drift": initial_drift,
                "recovery_steps": recovery_steps
            }
        )

def run_scenario_test(
    scenario: TestScenario,
    test_runner: Any
) -> Dict[str, Any]:
    """Run a complete scenario test and return results"""
    results = []
    for task in scenario.tasks:
        result = test_runner.run_single_test(task)
        results.append(result)
    
    # Calculate actual metrics
    rebloom_count = sum(1 for r in results if r["should_rebloom"])
    rebloom_rate = rebloom_count / len(results)
    
    modes = {}
    for result in results:
        if result["should_rebloom"]:
            mode = result["mode"]
            modes[mode] = modes.get(mode, 0) + 1
    
    mode_distribution = {
        mode: count / rebloom_count
        for mode, count in modes.items()
    }
    
    # Collect all flags
    all_flags = []
    for result in results:
        all_flags.extend(result["flags"])
    
    return {
        "scenario_name": scenario.name,
        "expected_rebloom_rate": scenario.expected_rebloom_rate,
        "actual_rebloom_rate": rebloom_rate,
        "expected_modes": scenario.expected_modes,
        "actual_modes": mode_distribution,
        "expected_flags": scenario.expected_flags,
        "actual_flags": list(set(all_flags)),
        "results": results
    } 