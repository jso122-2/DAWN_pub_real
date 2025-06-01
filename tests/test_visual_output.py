# Save as test_visual_output.py
import matplotlib.pyplot as plt
from pathlib import Path

output_dir = Path("visual_output/test")
output_dir.mkdir(parents=True, exist_ok=True)

# Create simple plot
plt.figure(figsize=(8, 6))
plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.title("DAWN Test Visual")

# Save it
output_path = output_dir / "test_output.png"
plt.savefig(output_path)
print(f"✅ Saved to: {output_path}")

# Also show it
plt.show()