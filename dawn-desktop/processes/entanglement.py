#!/usr/bin/env python3
import json
import time
import random
import math

def main():
    """Dummy subprocess for Entanglement Monitor"""
    metrics = {
        "entanglement_level": {
                "value": 98.7,
                "unit": "%"
        },
        "coherence_time": {
                "value": 2.4,
                "unit": "ms"
        },
        "qbit_fidelity": {
                "value": 99.2,
                "unit": "%"
        }
}
    
    t = 0
    while True:
        # Update metrics with some variation
        current_metrics = {}
        
        for metric_name, metric_info in metrics.items():
            base_value = metric_info["value"]
            unit = metric_info["unit"]
            
            if unit == "%":
                # Oscillate between bounds
                variation = math.sin(t * 0.1) * 10 + random.uniform(-2, 2)
                value = max(0, min(100, base_value + variation))
            else:
                # Random walk
                variation = random.uniform(-0.1, 0.1) * base_value
                value = max(0, base_value + variation)
            
            current_metrics[metric_name] = value
        
        # Output metrics as JSON
        print(json.dumps({
            "type": "metrics",
            "subprocess_id": "entanglement",
            "metrics": current_metrics,
            "timestamp": time.time()
        }))
        
        time.sleep(0.5)  # Update every 500ms
        t += 0.5

if __name__ == "__main__":
    main()
