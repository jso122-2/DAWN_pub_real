#!/bin/bash

echo "🌅 WAKING DAWN..."

# 1. Launch Tick Engine Core
echo "🧠 Starting Tick Engine..."
python main_with_weight_charge.py &

# 2. Owl Binding for Rebloom + Sigil Logic
echo "🦉 Binding Owl Tracer..."
python codex/owl_bound_boot.py &

# 3. Load Mood → Heat Mappings
echo "🌈 Loading mood → heat logic..."
python semantic/mood_map_loader.py &

# 4. Render Julia-set Fractal Blooms
echo "🌸 Generating fractal bloom signatures..."
python fractal_generator.py &

# 5. Animate Mycelium Nutrient Growth
echo "🕸️ Animating mycelium root density..."
python mycelium_animation.py &

# 6. Animate Drift + Entropy Overlay
echo "🌪️ Rendering drift-entropy hybrid field..."
python semantic/animate_drift_entropy.py &

# 7. Animate Rebloom Trails
echo "🧬 Visualizing rebloom trail maps..."
python semantic/rebloom_trail_animation.py &

# 8. Activate Semantic Trigger Rules
echo "⚡ Activating trigger rule engine..."
python semantic_trigger_rules.py &

# 9. Optional Console Report (Schema Health)
echo "📊 Printing pulse report to console..."
python debug/console_report.py

echo "✅ DAWN is awake and running."
