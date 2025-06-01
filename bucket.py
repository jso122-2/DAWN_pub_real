import os
import shutil

# Root DAWN path — modify if different
ROOT_DIR = "C:/Users/Admin/OneDrive/Desktop/DAWN/Tick_engine"

# Buckets: folder name -> list of file names or patterns
BUCKETS = {
    "core": [
        "tick_engine.py", "tick_loop.py", "tick_emitter.py", "tick_listener.py",
        "system_state.py", "pulse_heat.py", "pulse_thresholds.py", "main.py", "main_loop.py", "event_bus.py"
    ],
    "bloom": [
        "bloom_engine.py", "bloom_event.py", "bloom_writer.py", "bloom_registry.json",
        "juliet_flower.py", "juliet_cluster.py", "juliet_utils.py", "juliet_inspector.py",
        "juliet_field_summary.py", "clean_blooms.py", "repair_misplaced_moods.py",
        "memory_utils.py", "memory_blooms"
    ],
    "fractal": [
        "generate_julia_set.py", "fractal_generator.py", "fractal_propagation_animator.py",
        "fractal_field_map.py", "drift_entropy_field.py", "drift_vector_field.py",
        "bloom_visualizer.py", "field_drift_visualizer.py", "field_map_visualizer.py",
        "field_report.py", "nutrient_heat_field.py"
    ],
    "owl": [
        "owl.py", "owl_auditor.py", "owl_entropy_audit.py", "trust_model.py",
        "rebloom_depth_stats.py", "rebloom_lineage.py", "lineage_tools.py",
        "lineage_tracker.py", "lineage_tree_visualizer.py", "owl_log.json"
    ],
    "mycelium": [
        "mycelium_layer.py", "mycelium_nutrient_map.py", "mycelium_animation.py",
        "run_root_animation.py", "compute_mood_drift.py", "mood_drift.py"
    ],
    "scripts": [
        "test_2.py", "test_log_parse.py", "seed_coord_backfill.py", "folder_normalizer.py",
        "bucket_ctrl_f.py", "bucket_ctrl_f_results.txt"
    ],
    "router": [
        "router.py", "tracer_core.py", "tracer_listener.py", "cluster_graph.py", "cluster_linker.py"
    ]
}

def move_files():
    for folder, files in BUCKETS.items():
        target_dir = os.path.join(ROOT_DIR, folder)
        os.makedirs(target_dir, exist_ok=True)

        for f in files:
            src = os.path.join(ROOT_DIR, f)
            dst = os.path.join(target_dir, os.path.basename(f))
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"✅ Moved {f} → {folder}/")
            else:
                print(f"⚠️  Not found: {f}")

if __name__ == "__main__":
    move_files()
