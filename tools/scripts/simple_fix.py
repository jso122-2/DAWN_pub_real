# save as simple_fix.py
import os
import json
from pathlib import Path

base = Path.cwd()

# Create directories
for d in ["visual_output", "logs", "juliet_flowers/bloom_metadata", 
          "juliet_flowers/cluster_report", "codex"]:
    (base / d).mkdir(parents=True, exist_ok=True)

# Create tick log without emojis
with open(base / "logs/tick_log.csv", 'w') as f:
    f.write("tick,zone,pulse,entropy,scup\n")
    for i in range(100):
        zone = ["calm", "active", "surge"][i % 3]
        f.write(f"{1000+i},{zone},{0.5},{0.3},{0.7}\n")

# Create other files
with open(base / "juliet_flowers/cluster_report/interval_log.csv", 'w') as f:
    for i in range(100):
        f.write(f"{1.0 + i*0.01}\n")

print("✅ Created basic files")
print("\nNow try:")
print("cd visual")
print("python bloom_lineage_radar.py")