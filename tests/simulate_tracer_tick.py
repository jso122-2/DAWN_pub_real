import sys
import os
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tracer_router import TracerRouter
from agreement_matrix import AgreementMatrix
from semantic_distance import SemanticDistance

def simulate_tracer_tick():
    # Initialize components
    semantic_distance = SemanticDistance()
    agreement_matrix = AgreementMatrix()
    
    # Initialize router with dependencies
    router = TracerRouter(
        semantic_field=semantic_distance,
        agreement_matrix=agreement_matrix
    )
    
    # Simulate some test routes
    test_routes = [
        ("node_a", "node_b"),
        ("node_b", "node_c"),
        ("node_c", "node_d")
    ]
    
    # Add test routes to agreement matrix
    for source, target in test_routes:
        route = f"{source}→{target}"
        agreement_matrix.update_route_score(route=route, success=True)
    
    # Simulate semantic connections
    for source, target in test_routes:
        semantic_distance.add_semantic_connection(source, target, strength=0.8)
    
    # Simulate a tracer tick
    print("Simulating tracer tick...")
    
    # Test route evaluation
    source = "node_a"
    target = "node_d"
    
    # Get route decision
    route_decision = router.evaluate_route(
        source=source,
        target=target,
        payload_type="data",
        current_pressure=0.7
    )
    
    print(f"\nRoute decision from {source} to {target}:")
    print(f"Route: {route_decision['route']}")
    print(f"Confidence: {route_decision['confidence']:.2f}")
    print(f"Semantic distance: {route_decision['semantic_distance']:.2f}")
    
    # Print agreement matrix stats
    print("\nAgreement Matrix Statistics:")
    for source, target in test_routes:
        route = f"{source}→{target}"
        stats = agreement_matrix.get_route_stats(route)
        print(f"Route {source} -> {target}:")
        print(f"  Score: {stats['current_score']:.2f}")
        print(f"  Success rate: {stats['success_rate']:.2f}")
        print(f"  Trend: {stats['trend']:.2f}")

if __name__ == "__main__":
    simulate_tracer_tick() 