"""
Agreement Matrix Loader and Manager
Handles loading, updating, and managing the agreement matrix for tracers.
The agreement matrix tracks route reliability scores based on successful/failed transfers.
"""

import json
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np
from collections import defaultdict

class AgreementMatrix:
    """Manages the agreement matrix for tracer routes."""
    
    def __init__(self, matrix_path: str = "agreement_matrix.json"):
        self.matrix_path = matrix_path
        self.matrix: Dict[str, float] = {}
        self.history: List[Dict] = []
        self.decay_rate = 0.95  # Score decay per update
        self.min_score = 0.1    # Minimum score before route is considered unreliable
        self.max_score = 0.95   # Maximum score cap
        self.last_use: Dict[str, int] = {}  # Track last use tick for each route
        self.current_tick = 0
        self.load_matrix()
        
    def load_matrix(self) -> None:
        """Load agreement matrix from file."""
        try:
            if os.path.exists(self.matrix_path):
                with open(self.matrix_path, 'r') as f:
                    data = json.load(f)
                    self.matrix = data.get('matrix', {})
                    self.history = data.get('history', [])
                    print(f"[AgreementMatrix] Loaded {len(self.matrix)} route scores")
            else:
                print("[AgreementMatrix] No existing matrix found, starting fresh")
                self.matrix = {}
                self.history = []
        except Exception as e:
            print(f"[AgreementMatrix] Error loading matrix: {e}")
            self.matrix = {}
            self.history = []
            
    def save_matrix(self) -> None:
        """Save agreement matrix to file."""
        try:
            data = {
                'matrix': self.matrix,
                'history': self.history,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.matrix_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[AgreementMatrix] Saved {len(self.matrix)} route scores")
        except Exception as e:
            print(f"[AgreementMatrix] Error saving matrix: {e}")
            
    def get_route_score(self, route: str) -> float:
        """
        Get reliability score for a route.
        
        Args:
            route: Route identifier (format: "source→target")
            
        Returns:
            float: Reliability score [0-1]
        """
        return self.matrix.get(route, 0.5)  # Default to neutral score
        
    def update_route_score(self, route: str, success: bool, 
                          pressure: float = 1.0) -> None:
        """
        Update reliability score for a route.
        
        Args:
            route: Route identifier
            success: Whether the transfer was successful
            pressure: Current system pressure [0-1]
        """
        current_score = self.matrix.get(route, 0.5)
        
        # Calculate score adjustment
        if success:
            # Success increases score more under high pressure
            adjustment = 0.1 * pressure
        else:
            # Failure decreases score more under high pressure
            adjustment = -0.15 * pressure
            
        # Apply decay to current score
        decayed_score = current_score * self.decay_rate
        
        # Calculate new score
        new_score = decayed_score + adjustment
        
        # Clamp score to valid range
        new_score = max(self.min_score, min(self.max_score, new_score))
        
        # Update matrix
        self.matrix[route] = new_score
        
        # Record in history
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'route': route,
            'old_score': current_score,
            'new_score': new_score,
            'success': success,
            'pressure': pressure
        })
        
        # Trim history if too long
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
            
    def get_route_trend(self, route: str, window: int = 10) -> float:
        """
        Calculate trend in route reliability.
        
        Args:
            route: Route identifier
            window: Number of recent updates to consider
            
        Returns:
            float: Trend value [-1 to 1]
        """
        route_history = [h for h in self.history if h['route'] == route]
        if not route_history:
            return 0.0
            
        recent = route_history[-window:]
        if len(recent) < 2:
            return 0.0
            
        scores = [h['new_score'] for h in recent]
        return np.polyfit(range(len(scores)), scores, 1)[0]
        
    def get_recommended_routes(self, source: str, 
                             targets: List[str],
                             min_score: float = 0.6) -> List[Tuple[str, float]]:
        """
        Get recommended routes from source to targets.
        
        Args:
            source: Source component
            targets: List of target components
            min_score: Minimum reliability score
            
        Returns:
            List of (route, score) tuples, sorted by score
        """
        routes = []
        for target in targets:
            route = f"{source}→{target}"
            score = self.get_route_score(route)
            if score >= min_score:
                routes.append((route, score))
                
        return sorted(routes, key=lambda x: x[1], reverse=True)
        
    def get_unreliable_routes(self, threshold: float = 0.3) -> List[str]:
        """
        Get list of unreliable routes.
        
        Args:
            threshold: Score threshold for unreliability
            
        Returns:
            List of route identifiers
        """
        return [route for route, score in self.matrix.items() 
                if score < threshold]
        
    def get_route_stats(self, route: str) -> Dict:
        """
        Get detailed statistics for a route.
        
        Args:
            route: Route identifier
            
        Returns:
            Dict containing route statistics
        """
        route_history = [h for h in self.history if h['route'] == route]
        if not route_history:
            return {
                'total_transfers': 0,
                'success_rate': 0.0,
                'current_score': self.get_route_score(route),
                'trend': 0.0,
                'last_updated': None
            }
            
        successes = sum(1 for h in route_history if h['success'])
        total = len(route_history)
        
        return {
            'total_transfers': total,
            'success_rate': successes / total if total > 0 else 0.0,
            'current_score': self.get_route_score(route),
            'trend': self.get_route_trend(route),
            'last_updated': route_history[-1]['timestamp']
        }
        
    def decay_all_scores(self) -> None:
        """Apply decay to all route scores."""
        for route in self.matrix:
            current_score = self.matrix[route]
            decayed_score = current_score * self.decay_rate
            self.matrix[route] = max(self.min_score, decayed_score)
            
    def reset_route(self, route: str) -> None:
        """Reset score for a specific route to neutral."""
        self.matrix[route] = 0.5
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'route': route,
            'old_score': self.matrix.get(route, 0.5),
            'new_score': 0.5,
            'success': None,
            'pressure': 0.0,
            'reset': True
        })
        
    def reset_all(self) -> None:
        """Reset all route scores to neutral."""
        self.matrix = {}
        self.history = []
        print("[AgreementMatrix] Reset all route scores")
        
    def reinforce_route_success(self, source: str, target: str) -> None:
        """
        Reinforce a successful route with a small positive boost.
        
        Args:
            source: Source component
            target: Target component
        """
        route = f"{source}→{target}"
        current_score = self.matrix.get(route, 0.5)
        
        # Add small positive reinforcement
        new_score = min(self.max_score, current_score + 0.02)
        
        # Update matrix
        self.matrix[route] = new_score
        
        # Update last use tick
        self.last_use[route] = self.current_tick
        
        # Record in history
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'route': route,
            'old_score': current_score,
            'new_score': new_score,
            'type': 'reinforcement',
            'tick': self.current_tick
        })
        
        print(f"[AgreementMatrix] Reinforced route {route}: {current_score:.3f} -> {new_score:.3f}")
        
    def decay_unused_routes(self, ticks_since_use: int) -> None:
        """
        Apply decay to routes that haven't been used recently.
        
        Args:
            ticks_since_use: Number of ticks to consider for decay
        """
        current_time = self.current_tick
        decayed_routes = []
        
        for route, last_used in self.last_use.items():
            idle_ticks = current_time - last_used
            
            if idle_ticks >= ticks_since_use:
                current_score = self.matrix.get(route, 0.5)
                
                # Calculate decay based on idle time
                decay_units = idle_ticks // 10  # One decay unit per 10 ticks
                decay_amount = min(0.01 * decay_units, current_score - self.min_score)
                
                if decay_amount > 0:
                    new_score = current_score - decay_amount
                    self.matrix[route] = new_score
                    
                    # Record in history
                    self.history.append({
                        'timestamp': datetime.now().isoformat(),
                        'route': route,
                        'old_score': current_score,
                        'new_score': new_score,
                        'type': 'decay',
                        'idle_ticks': idle_ticks,
                        'tick': current_time
                    })
                    
                    decayed_routes.append((route, current_score, new_score))
        
        if decayed_routes:
            print(f"[AgreementMatrix] Decayed {len(decayed_routes)} unused routes:")
            for route, old_score, new_score in decayed_routes:
                print(f"  {route}: {old_score:.3f} -> {new_score:.3f}")
                
    def update_tick(self, tick: int) -> None:
        """
        Update the current tick counter.
        
        Args:
            tick: Current system tick
        """
        self.current_tick = tick
        
    def get_route_last_use(self, route: str) -> Optional[int]:
        """
        Get the last use tick for a route.
        
        Args:
            route: Route identifier
            
        Returns:
            Last use tick or None if never used
        """
        return self.last_use.get(route)

    def get_top_routes(self, n: int = 5) -> List[Dict[str, any]]:
        """
        Get the top N highest scoring routes.
        
        Args:
            n: Number of top routes to return
            
        Returns:
            List of route dictionaries with scores and metadata
        """
        # Sort routes by score
        sorted_routes = sorted(
            [(route, score) for route, score in self.matrix.items()],
            key=lambda x: x[1],
            reverse=True
        )
        
        # Get top N routes with metadata
        top_routes = []
        for route, score in sorted_routes[:n]:
            source, target = route.split("→")
            top_routes.append({
                "route": route,
                "source": source,
                "target": target,
                "score": score,
                "last_use": self.last_use.get(route, 0),
                "ticks_since_use": self.current_tick - self.last_use.get(route, 0)
            })
            
        return top_routes
        
    def get_risky_routes(self, threshold: float = 0.3) -> List[Dict[str, any]]:
        """
        Get routes with low success rates.
        
        Args:
            threshold: Score threshold below which routes are considered risky
            
        Returns:
            List of risky route dictionaries with scores and metadata
        """
        risky_routes = []
        
        for route, score in self.matrix.items():
            if score < threshold:
                source, target = route.split("→")
                risky_routes.append({
                    "route": route,
                    "source": source,
                    "target": target,
                    "score": score,
                    "last_use": self.last_use.get(route, 0),
                    "ticks_since_use": self.current_tick - self.last_use.get(route, 0),
                    "risk_level": "high" if score < threshold/2 else "medium"
                })
                
        return risky_routes
        
    def log_meta_snapshot(self) -> None:
        """Log current matrix state and analysis to route_meta_snapshot.json."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "current_tick": self.current_tick,
            "matrix_stats": {
                "total_routes": len(self.matrix),
                "avg_score": sum(self.matrix.values()) / len(self.matrix) if self.matrix else 0,
                "min_score": min(self.matrix.values()) if self.matrix else 0,
                "max_score": max(self.matrix.values()) if self.matrix else 0
            },
            "top_routes": self.get_top_routes(5),
            "risky_routes": self.get_risky_routes(0.3),
            "route_health": {
                "healthy": len([s for s in self.matrix.values() if s > 0.7]),
                "moderate": len([s for s in self.matrix.values() if 0.4 <= s <= 0.7]),
                "risky": len([s for s in self.matrix.values() if s < 0.4])
            },
            "usage_patterns": {
                "recently_used": len([t for t in self.last_use.values() if self.current_tick - t < 10]),
                "stale_routes": len([t for t in self.last_use.values() if self.current_tick - t > 50])
            }
        }
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Write snapshot to file
        with open('logs/route_meta_snapshot.json', 'w') as f:
            json.dump(snapshot, f, indent=2)
            
        print(f"[AgreementMatrix] Logged meta snapshot with {len(snapshot['top_routes'])} top routes "
              f"and {len(snapshot['risky_routes'])} risky routes") 