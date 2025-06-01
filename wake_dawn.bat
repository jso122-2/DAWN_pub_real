@echo off
echo 🌅 WAKING DAWN...

:: Tick Engine Entry
echo 🧠 Starting Tick Engine...
start /B python semantic\main_with_weight_charge.py

:: Owl Binding (main trigger)
echo 🦉 Binding Owl Tracer...
start /B python owl\main_with_owl_trigger.py

:: Mood to Heat Mapping (if relevant script exists)
echo 🌈 Loading mood → heat logic...
REM No exact script found — skipping unless provided

:: Julia-set Fractal Generation
echo 🌸 Generating fractal bloom signatures...
start /B python fractal\fractal_generator.py

:: Mycelium Nutrient Growth Animation
echo 🕸️ Animating mycelium root density...
start /B python mycelium\mycelium_animation.py

:: Drift-Entropy Field Overlay
echo 🌪️ Rendering drift-entropy hybrid field...
start /B python animate_field_map.py

:: Rebloom Trail Animation
echo 🧬 Visualizing rebloom trail maps...
start /B python rebloom_trail_animation.py

:: Trigger Rule Engine (Semantic Logic)
echo ⚡ Activating trigger rule engine...
start /B python semantic\semantic_trigger_rules.py

:: Pulse Status Console Report
echo 📊 Printing pulse report...
REM No console_report.py found — skipping unless provided

echo ✅ DAWN is awake and running.
pause
