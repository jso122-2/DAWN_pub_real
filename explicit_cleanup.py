import os
import shutil

# Explicit directory mapping
directories = {
    'bloom': ['spawn_bloom.py', 'bloom_emitter_handler.py', 'automated_health_checks.py', 
              'semantic_integration.py', 'expanded_semantic_integration.py', 'ci_tests.py'],
    'fractal': ['fractal_generator.py', 'generate_julia_set.py', 'fractal_animation_visualization.py', 
                'drift_vector_field.py', 'drift_entropy_field.py', 'nutrient_heat_field.py'],
    'mycelium': ['enhanced_nutrient_mapping.py', 'nutrient_logger.py', 'mycelium_nutrient_map.py'],
    'mood': ['mood_stability_tuning.py', 'mood_entropy_index.py'],
    'pulse': ['pulse_heat.py', 'pulse_thresholds.py'],
    'core': ['tick_engine.py', 'event_bus.py', 'tick_listener.py', 'tick_loop.py'],
    'semantic': ['semantic_reasoning_field.py', 'expanded_semantic_integration.py'],
    'owl': ['entropy_logger.py', 'lineage_tracker.py', 'owl.py'],
    'tracers': ['tracer_logic.py', 'tracer_scheduler.py'],
    'visual': ['drift_animation.py', 'drift_entropy_overlay.py'],
    'router': ['cluster_graph.py', 'router.py'],
    'codex': ['sigil_registry.py', 'audit.py'],
    'diagnostics': ['mr_wolf.py'],
    'scripts': ['bucket_ctrl_f.py', 'folder_normalizer.py'],
    'tests': ['emit_test_blooms.py'],
    'logs/juliet_flowers': [],
    'logs/mycelium_logs': [],
    'docs': [],
    'maintenance': ['sync_structure.py']
}

base_dir = 'C:\\Users\\Admin\\OneDrive\\Desktop\\DAWN\\Tick_engine'

# Explicit move operation
for dir_name, files in directories.items():
    dir_path = os.path.join(base_dir, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    for file in files:
        src_file = os.path.join(base_dir, file)
        if os.path.isfile(src_file):
            shutil.move(src_file, dir_path)
            print(f"✅ Moved {file} explicitly to {dir_path}")
        else:
            print(f"⚠️ {file} not found explicitly in base directory")

print("📑 Directory structure explicitly updated and cleaned.")
