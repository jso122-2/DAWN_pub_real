
from bloom.seed_matrix_synthesis import seed_matrix_synthesis
from visual.drift_lattice_generator import generate_lattice
from bloom.fuse_all_corners import fuse_all_corners
from visual.recursive_fieldmap import render_fieldmap
from visual.entropy_arc_animator import animate_entropy
from visual.recursive_bloom_tree import animate_bloom_tree

def run_full_drift_fusion():
    print("🔁 Running full drift + fusion loop...")
    seed_matrix_synthesis()
    generate_lattice()
    fuse_all_corners()
    render_fieldmap()
    animate_entropy()
    animate_bloom_tree()
    print("✅ Drift + fusion loop complete.")

if __name__ == "__main__":
    run_full_drift_fusion()
