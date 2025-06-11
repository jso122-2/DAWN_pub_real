# /sigils/sigil_router.py

from tracers.tracer_diplomacy import resolve_tracer_conflict
from owl.owl_tracer_log import owl_log
from collections import OrderedDict
import time
import yaml
import os
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional, NamedTuple

# --- Default Routing Map (fallback) ---
DEFAULT_ROUTING_MAP = {
    "calm": {
        "primary": "Bee",
        "fallback": "Ant",
        "threshold": 0.7,
        "cooldown": 8
    },
    "anxious": {
        "primary": "Owl",
        "fallback": "Spider",
        "threshold": 0.6,
        "cooldown": 12
    },
    "curious": {
        "primary": "Bee",
        "fallback": "Whale",
        "threshold": 0.8,
        "cooldown": 6
    },
    "angry": {
        "primary": "Crow",
        "fallback": "Spider",
        "threshold": 0.9,
        "cooldown": 15
    },
    "sad": {
        "primary": "Owl",
        "fallback": "Whale",
        "threshold": 0.7,
        "cooldown": 10
    },
    "excited": {
        "primary": "Bee",
        "fallback": "Ant",
        "threshold": 0.8,
        "cooldown": 5
    }
}

def validate_routing_config(config: Dict) -> bool:
    """Validate the shape and content of the routing configuration."""
    if not isinstance(config, dict) or "routing_map" not in config:
        return False
        
    routing_map = config["routing_map"]
    if not isinstance(routing_map, dict):
        return False
        
    required_fields = {"primary", "fallback", "threshold", "cooldown"}
    
    for mood, settings in routing_map.items():
        if not isinstance(settings, dict):
            return False
        if not all(field in settings for field in required_fields):
            return False
        if not isinstance(settings["threshold"], (int, float)) or not 0 <= settings["threshold"] <= 1:
            return False
        if not isinstance(settings["cooldown"], int) or settings["cooldown"] < 0:
            return False
        if not isinstance(settings["primary"], str) or not isinstance(settings["fallback"], str):
            return False
            
    return True

def load_routing_config() -> Dict:
    """Load routing configuration from YAML file with fallback."""
    config_path = os.path.join("config", "routing_config.yaml")
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if validate_routing_config(config):
                    owl_log("[Config] ✓ Loaded routing configuration from file")
                    return config["routing_map"]
                else:
                    owl_log("[Config] ⚠️ Invalid routing configuration format, using defaults")
        else:
            owl_log("[Config] ⚠️ Routing config file not found, using defaults")
    except Exception as e:
        owl_log(f"[Config] ⚠️ Error loading routing config: {e}, using defaults")
        
    return DEFAULT_ROUTING_MAP

# Initialize routing map from config
ROUTING_MAP = load_routing_config()

class SigilRouteLog:
    """TTL-based route logging with automatic expiration"""
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.routes: OrderedDict = OrderedDict()
        
    def add_route(self, seed_id: str, action: str, tick: int) -> None:
        """Add a new route with timestamp"""
        if len(self.routes) >= self.max_size:
            self.routes.popitem(last=False)  # Remove oldest
        self.routes[seed_id] = {
            "action": action,
            "tick": tick,
            "timestamp": time.time()
        }
        
    def get_route(self, seed_id: str) -> Optional[Dict]:
        """Get route if not expired"""
        route = self.routes.get(seed_id)
        if not route:
            return None
            
        # Check TTL
        if time.time() - route["timestamp"] > self.ttl_seconds:
            del self.routes[seed_id]
            return None
            
        return route
        
    def cleanup(self) -> None:
        """Remove expired routes"""
        current_time = time.time()
        expired = [
            seed_id for seed_id, route in self.routes.items()
            if current_time - route["timestamp"] > self.ttl_seconds
        ]
        for seed_id in expired:
            del self.routes[seed_id]

# Initialize route log with 1-hour TTL
route_log = SigilRouteLog(ttl_seconds=3600)

def log_route_attempt(
    source: str,
    target: str,
    success: bool,
    error_msg: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> None:
    """Log routing attempt to JSON file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "target": target,
        "success": success,
        "error": error_msg,
        "metadata": metadata or {}
    }
    
    log_path = os.path.join("logs", "routing_trace.json")
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Load existing logs if file exists
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []
            
        # Append new log entry
        logs.append(log_entry)
        
        # Write back to file
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=2)
            
    except Exception as e:
        owl_log(f"[Routing] ⚠️ Failed to write routing log: {e}")

def route_sigil(sigil, bloom, active_mood, tick, sigil_heat):
    """
    Routes sigil to most appropriate tracers based on deterministic routing map.
    Resolves tracer conflict via diplomacy layer.
    """
    tracer_signals = []
    seed_id = getattr(bloom, "seed_id", "unknown_seed")
    available_tracers = getattr(bloom, "available_tracers", [])
    
    # Get routing configuration for current mood
    routing_config = ROUTING_MAP.get(active_mood, ROUTING_MAP["calm"])
    
    # Check route log for cooldown
    last_route = route_log.get_route(seed_id)
    if last_route and tick - last_route["tick"] < routing_config["cooldown"]:
        log_route_attempt(
            source=seed_id,
            target=last_route["action"],
            success=False,
            error_msg=f"Cooldown active ({routing_config['cooldown']} ticks)",
            metadata={"tick": tick, "mood": active_mood}
        )
        owl_log(f"[Cooldown] ⏳ {seed_id} → {last_route['action']} (locked for {routing_config['cooldown']} ticks)")
        return last_route["action"]
    
    # Default influence map & intent fallback
    influence_map = getattr(sigil, "influence", {}) or {}
    intent = getattr(sigil, "intent", "noop")
    
    # Calculate weights based on routing configuration
    for tracer in available_tracers:
        base_weight = influence_map.get(tracer, 1.0)
        
        # Apply deterministic routing weights
        if tracer == routing_config["primary"]:
            routing_weight = 1.5
        elif tracer == routing_config["fallback"]:
            routing_weight = 1.2
        else:
            routing_weight = 1.0
            
        # Heat modifier with threshold
        heat_modifier = 1.0 + (sigil_heat / 10.0) if sigil_heat >= routing_config["threshold"] else 0.8
        
        total_weight = base_weight * routing_weight * heat_modifier
        tracer_signals.append((tracer, intent, total_weight))
    
    try:
        # Resolve conflict diplomatically
        final_action = resolve_tracer_conflict(bloom, tracer_signals)
        
        # Hybrid fallback if ambiguous
        if is_ambiguous(final_action, tracer_signals):
            final_action = hybridize(final_action, tracer_signals)
        
        # Log successful route
        log_route_attempt(
            source=seed_id,
            target=final_action,
            success=True,
            metadata={
                "tick": tick,
                "mood": active_mood,
                "heat": sigil_heat,
                "tracer_signals": [
                    {"tracer": t, "intent": i, "weight": w}
                    for t, i, w in tracer_signals
                ]
            }
        )
        
        # Log the route
        route_log.add_route(seed_id, final_action, tick)
        
        # Periodic cleanup
        if tick % 100 == 0:
            route_log.cleanup()
            
        return final_action
        
    except Exception as e:
        error_msg = f"Routing failed: {str(e)}"
        log_route_attempt(
            source=seed_id,
            target="unknown",
            success=False,
            error_msg=error_msg,
            metadata={
                "tick": tick,
                "mood": active_mood,
                "heat": sigil_heat
            }
        )
        owl_log(f"[Routing] ⚠️ {error_msg}")
        return "noop"  # Safe fallback

# --- Ambiguity Detection ---

def is_ambiguous(chosen, signals, margin=0.15):
    """Determine if the final action is narrowly won (ambiguous)."""
    action_scores = {}
    for _, action, score in signals:
        action_scores[action] = action_scores.get(action, 0) + score

    sorted_scores = sorted(action_scores.values(), reverse=True)
    if len(sorted_scores) >= 2:
        return (sorted_scores[0] - sorted_scores[1]) < margin
    return False

# --- Hybridization Logic ---

def hybridize(chosen_action, signals):
    """
    Combine top two actions into a hybrid plan (e.g., suppress + mutate).
    """
    action_scores = {}
    for _, action, score in signals:
        action_scores[action] = action_scores.get(action, 0) + score

    top_two = sorted(action_scores.items(), key=lambda x: -x[1])[:2]
    hybrid = " + ".join(a for a, _ in top_two)
    owl_log(f"[Hybrid Action] ⚔️ {hybrid} triggered due to indecision")
    return hybrid

# --- Public API for DAWN and Tracers ---

def trigger_sigil(sigil, bloom, mood, tick, heat):
    """
    Public interface used by DAWN or other modules.
    Calls internal router logic and returns resolved action.
    """
    return route_sigil(sigil, bloom, mood, tick, heat)

class RouteResult(NamedTuple):
    """Result of a simulated routing attempt"""
    success: bool
    resolved_module: str
    fallback_used: bool
    error: Optional[str] = None
    metadata: Optional[Dict] = None

def simulate_route(path: str) -> RouteResult:
    """
    Simulate a routing path without loading actual components.
    Useful for testing routing logic and configuration.
    
    Args:
        path: Mock routing path (e.g., "calm/Bee/process")
        
    Returns:
        RouteResult with routing simulation details
    """
    try:
        # Parse path components
        parts = path.split('/')
        if len(parts) < 2:
            return RouteResult(
                success=False,
                resolved_module="unknown",
                fallback_used=False,
                error="Invalid path format: expected mood/tracer/action"
            )
            
        mood, tracer, *action = parts
        action = action[0] if action else "default"
        
        # Get routing config for mood
        routing_config = ROUTING_MAP.get(mood)
        if not routing_config:
            return RouteResult(
                success=False,
                resolved_module="unknown",
                fallback_used=False,
                error=f"Unknown mood: {mood}"
            )
            
        # Check if primary or fallback
        is_primary = tracer == routing_config["primary"]
        is_fallback = tracer == routing_config["fallback"]
        
        if not (is_primary or is_fallback):
            return RouteResult(
                success=False,
                resolved_module=tracer,
                fallback_used=False,
                error=f"Tracer {tracer} not configured for mood {mood}"
            )
            
        # Simulate routing success
        return RouteResult(
            success=True,
            resolved_module=tracer,
            fallback_used=is_fallback,
            metadata={
                "mood": mood,
                "action": action,
                "threshold": routing_config["threshold"],
                "cooldown": routing_config["cooldown"]
            }
        )
        
    except Exception as e:
        return RouteResult(
            success=False,
            resolved_module="unknown",
            fallback_used=False,
            error=f"Simulation error: {str(e)}"
        )

# Example test case
if __name__ == "__main__":
    # Test primary tracer
    result = simulate_route("calm/Bee/process")
    print(f"Primary Test: {result}")
    # Expected: RouteResult(success=True, resolved_module='Bee', fallback_used=False, error=None, metadata={...})
    
    # Test fallback tracer
    result = simulate_route("anxious/Spider/analyze")
    print(f"Fallback Test: {result}")
    # Expected: RouteResult(success=True, resolved_module='Spider', fallback_used=True, error=None, metadata={...})
    
    # Test invalid path
    result = simulate_route("invalid")
    print(f"Invalid Test: {result}")
    # Expected: RouteResult(success=False, resolved_module='unknown', fallback_used=False, error='Invalid path format...')
