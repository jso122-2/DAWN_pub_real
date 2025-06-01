# direct_bloom_test.py
import os
import json
from datetime import datetime

# Create directories
os.makedirs("juliet_flowers/bloom_metadata", exist_ok=True)

# Create a test bloom
bloom = {
    "seed_id": "test_bloom_001",
    "mood": "curious",
    "bloom_factor": 1.0,
    "entropy_score": 0.5,
    "generated_at": datetime.now().isoformat(),
    "fractal_memory": {
        "raw": "aPS~5|TH@|S^",
        "note": "ASCII fractal string"
    }
}

# Save it
filename = f"test_bloom_{datetime.now().strftime('%H%M%S')}.json"
filepath = os.path.join("juliet_flowers/bloom_metadata", filename)

with open(filepath, "w") as f:
    json.dump(bloom, f, indent=2)

print(f"Bloom saved to: {filepath}")
print("Success!")